-- ============================================================================
-- frame_log — append-only persistent Frame Log for Wu-Wei Rewriter
-- ============================================================================
-- Append-only is enforced by triggers (UPDATE/DELETE blocked) AND by the
-- absence of update/delete RLS policies (defense in depth).
--
-- Revisions are NEVER mutations. They are new rows with parent_id set and
-- status in {revised-with-evidence, revised-without-evidence}, plus a
-- revision_reason. Original rows are preserved verbatim — this is what
-- makes retroactive prophecy detectable.
--
-- Run this in Supabase SQL editor or via `psql`. Idempotent where possible.
-- ============================================================================

create extension if not exists "pgcrypto";

-- ----------------------------------------------------------------------------
-- enums
-- ----------------------------------------------------------------------------
do $$ begin
  create type public.revision_status as enum (
    'original',
    'revised-with-evidence',
    'revised-without-evidence'
  );
exception when duplicate_object then null; end $$;

do $$ begin
  create type public.artifact_type as enum (
    'thesis','claim','recommendation','pitch',
    'conclusion','hypothesis','framework','concept'
  );
exception when duplicate_object then null; end $$;

do $$ begin
  create type public.pitch_mode as enum ('strict','persuasive_allowed');
exception when duplicate_object then null; end $$;

do $$ begin
  create type public.creative_mode as enum ('ship','explore');
exception when duplicate_object then null; end $$;

-- ----------------------------------------------------------------------------
-- main table
-- ----------------------------------------------------------------------------
create table if not exists public.frame_log (
  id              uuid primary key default gen_random_uuid(),
  owner           uuid not null references auth.users(id) on delete restrict,

  -- revision chain
  parent_id       uuid references public.frame_log(id) on delete restrict,
  status          public.revision_status not null default 'original',
  revision_reason text,

  -- artifact metadata
  name            text not null,
  artifact_type   public.artifact_type not null,
  domain          text,
  intended_use    text,
  pitch_mode      public.pitch_mode not null default 'strict',
  creative_mode   public.creative_mode not null default 'ship',
  author_confidence text check (author_confidence in ('low','med','high')),

  -- agent output blocks
  original_text   text not null,           -- input as received, verbatim
  rewrite_text    text not null,           -- agent's REWRITE block
  boundary        jsonb not null,          -- {applies_to, does_not_apply_to, failure_modes}
  predictions     jsonb not null,          -- [{p, by_date, confirms_if, falsifies_if}]
  polarity_notes  jsonb,                   -- {reversal_risk, phase_advice, forcing_pressure?}
  killed_claims   jsonb,                   -- [{claim, fails, reason}]
  elegance_audit  jsonb,                   -- [{sentence, diagnosis, action}]

  -- frame log fields
  decision_impact text,
  review_at_6mo   date,
  review_at_12mo  date,
  review_at_24mo  date,
  kill_condition  text not null,

  -- bookkeeping
  created_at      timestamptz not null default now(),

  -- integrity constraints
  constraint frame_log_revision_needs_parent
    check (
      (status = 'original'  and parent_id is null and revision_reason is null) or
      (status <> 'original' and parent_id is not null and revision_reason is not null and length(revision_reason) >= 8)
    ),
  constraint frame_log_predictions_or_speculative
    check (
      jsonb_typeof(predictions) = 'array'
      and (jsonb_array_length(predictions) >= 1 or rewrite_text ilike '%SPECULATIVE%')
    ),
  constraint frame_log_kill_condition_nonempty
    check (length(trim(kill_condition)) >= 8),
  constraint frame_log_boundary_has_required_keys
    check (
      boundary ? 'applies_to'
      and boundary ? 'does_not_apply_to'
      and boundary ? 'failure_modes'
    )
);

comment on table  public.frame_log is 'Append-only Frame Log. Never UPDATE/DELETE — insert child rows with parent_id + revised-* status.';
comment on column public.frame_log.parent_id       is 'Points to the row this one revises. NULL for originals.';
comment on column public.frame_log.status          is 'original | revised-with-evidence | revised-without-evidence.';
comment on column public.frame_log.revision_reason is 'Required for any non-original row. >=8 chars. Forces an honest note.';
comment on column public.frame_log.kill_condition  is 'What observation would make us stop using this frame. Required.';

-- ----------------------------------------------------------------------------
-- indices
-- ----------------------------------------------------------------------------
create index if not exists frame_log_owner_created_idx
  on public.frame_log(owner, created_at desc);

create index if not exists frame_log_review_6mo_idx
  on public.frame_log(review_at_6mo) where review_at_6mo is not null;

create index if not exists frame_log_review_12mo_idx
  on public.frame_log(review_at_12mo) where review_at_12mo is not null;

create index if not exists frame_log_review_24mo_idx
  on public.frame_log(review_at_24mo) where review_at_24mo is not null;

create index if not exists frame_log_kill_condition_fts_idx
  on public.frame_log using gin (to_tsvector('english', kill_condition));

create index if not exists frame_log_parent_idx
  on public.frame_log(parent_id) where parent_id is not null;

create index if not exists frame_log_domain_type_idx
  on public.frame_log(domain, artifact_type);

-- ----------------------------------------------------------------------------
-- append-only enforcement (defense in depth alongside RLS)
-- ----------------------------------------------------------------------------
create or replace function public.frame_log_block_mutation()
returns trigger language plpgsql as $$
begin
  raise exception
    'frame_log is append-only. To revise, insert a new row with parent_id=<old_id> and status in (revised-with-evidence, revised-without-evidence). Old row stays untouched.'
    using errcode = '0L000';  -- invalid_grantor (closest reasonable SQLSTATE)
end $$;

drop trigger if exists frame_log_no_update on public.frame_log;
create trigger frame_log_no_update
  before update on public.frame_log
  for each row execute function public.frame_log_block_mutation();

drop trigger if exists frame_log_no_delete on public.frame_log;
create trigger frame_log_no_delete
  before delete on public.frame_log
  for each row execute function public.frame_log_block_mutation();

-- ----------------------------------------------------------------------------
-- on-insert: auto-fill review dates if caller left them null
-- ----------------------------------------------------------------------------
create or replace function public.frame_log_autofill_reviews()
returns trigger language plpgsql as $$
begin
  if new.review_at_6mo  is null then new.review_at_6mo  := (new.created_at + interval '6 months')::date;  end if;
  if new.review_at_12mo is null then new.review_at_12mo := (new.created_at + interval '12 months')::date; end if;
  if new.review_at_24mo is null then new.review_at_24mo := (new.created_at + interval '24 months')::date; end if;
  return new;
end $$;

drop trigger if exists frame_log_autofill on public.frame_log;
create trigger frame_log_autofill
  before insert on public.frame_log
  for each row execute function public.frame_log_autofill_reviews();

-- ----------------------------------------------------------------------------
-- view: latest revision in each chain (walks parent_id back to root)
-- ----------------------------------------------------------------------------
create or replace view public.frame_log_current as
with recursive chain as (
  -- roots
  select id as root_id, id, owner, parent_id, status, created_at, 0 as depth
  from public.frame_log
  where parent_id is null

  union all

  -- children
  select c.root_id, f.id, f.owner, f.parent_id, f.status, f.created_at, c.depth + 1
  from public.frame_log f
  join chain c on f.parent_id = c.id
),
latest as (
  select root_id, id, owner, status, created_at,
         row_number() over (partition by root_id order by depth desc, created_at desc) as rn
  from chain
)
select f.*
from public.frame_log f
join latest l on l.id = f.id
where l.rn = 1;

comment on view public.frame_log_current is 'Latest revision per chain. Use this for normal reads; raw table for audit/history.';

-- ----------------------------------------------------------------------------
-- view: frames due for review (drives a cron / digest job)
-- ----------------------------------------------------------------------------
create or replace view public.frame_log_due_for_review as
select id, owner, name, domain, artifact_type, kill_condition,
       case
         when review_at_6mo  <= current_date and review_at_12mo > current_date then '6mo'
         when review_at_12mo <= current_date and review_at_24mo > current_date then '12mo'
         when review_at_24mo <= current_date then '24mo'
       end as horizon,
       created_at
from public.frame_log_current
where coalesce(review_at_6mo, current_date + 1) <= current_date
   or coalesce(review_at_12mo, current_date + 1) <= current_date
   or coalesce(review_at_24mo, current_date + 1) <= current_date;

-- ----------------------------------------------------------------------------
-- RLS
-- ----------------------------------------------------------------------------
alter table public.frame_log enable row level security;

drop policy if exists frame_log_owner_select on public.frame_log;
create policy frame_log_owner_select on public.frame_log
  for select using (auth.uid() = owner);

drop policy if exists frame_log_owner_insert on public.frame_log;
create policy frame_log_owner_insert on public.frame_log
  for insert with check (auth.uid() = owner);

-- update/delete policies are intentionally absent. Triggers also block them.

-- ----------------------------------------------------------------------------
-- example: insert a new frame
-- ----------------------------------------------------------------------------
-- insert into public.frame_log (
--   owner, name, artifact_type, domain, intended_use,
--   pitch_mode, creative_mode,
--   original_text, rewrite_text,
--   boundary, predictions, polarity_notes, killed_claims, elegance_audit,
--   decision_impact, kill_condition
-- ) values (
--   auth.uid(),
--   'agent_platform_thesis_2026Q2',
--   'thesis',
--   'ai_agents',
--   'decision_input',
--   'strict',
--   'ship',
--   $original$Agent platforms will replace SaaS by 2027.$original$,
--   $rewrite$Within a narrow band of internal-ops workflows (CRM data hygiene, ticket triage, doc retrieval), agent-orchestrated tools will measurably displace seat-based SaaS spend by Q4 2027.$rewrite$,
--   '{"applies_to":"internal-ops workflows in companies >100 employees","does_not_apply_to":"end-user consumer SaaS, regulated workflows requiring audit trails","failure_modes":["models plateau on long-horizon planning","data residency law tightens"]}'::jsonb,
--   '[{"p":"At least 5 of the top 50 enterprise SaaS vendors will publicly report seat-count compression attributable to agentic substitution","by_date":"2027-12-31","confirms_if":"earnings transcripts cite this dynamic","falsifies_if":"no such language by 2028-06"}]'::jsonb,
--   '{"reversal_risk":"too much agent autonomy -> compliance backlash -> SaaS regains moat","phase_advice":"ship narrow agents into ops-heavy verticals before horizontal platforms"}'::jsonb,
--   '[]'::jsonb,
--   '[{"sentence":"will replace SaaS","diagnosis":"naming load too high; SaaS is multi-category","action":"narrowed scope"}]'::jsonb,
--   'Affects how we size our agent-platform play vs SaaS-integration play in 2026 OKR.',
--   'If by 2027-12-31 no top-50 enterprise SaaS vendor reports agentic seat-displacement in earnings calls, retire this thesis.'
-- );

-- ----------------------------------------------------------------------------
-- example: insert a revision (child row)
-- ----------------------------------------------------------------------------
-- insert into public.frame_log (
--   owner, parent_id, status, revision_reason,
--   name, artifact_type, domain, intended_use,
--   original_text, rewrite_text,
--   boundary, predictions, kill_condition
-- ) values (
--   auth.uid(),
--   '<uuid-of-parent>',
--   'revised-with-evidence',
--   'Q3 2026 earnings season showed no displacement language in any top-50 vendor; narrowing scope to top 200.',
--   'agent_platform_thesis_2026Q4_rev1',
--   'thesis',
--   'ai_agents',
--   'decision_input',
--   $original$Agent platforms will replace SaaS by 2027.$original$,
--   $rewrite$Within ops workflows at companies >500 employees, agent orchestration will displace measurable seat-based SaaS spend by Q2 2028 (timeline extended +6mo).$rewrite$,
--   '{"applies_to":"...","does_not_apply_to":"...","failure_modes":[]}'::jsonb,
--   '[{"p":"...","by_date":"2028-06-30","confirms_if":"...","falsifies_if":"..."}]'::jsonb,
--   'Retire if no displacement language by 2028-12-31.'
-- );
