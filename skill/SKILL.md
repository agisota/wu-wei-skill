---
name: wu-wei-rewriter
description: Use this skill whenever the user has an existing claim, thesis, pitch, recommendation, conclusion, hypothesis, framework, strategy memo, product positioning statement, or concept that needs epistemic stress-testing, falsifiability, boundary-setting, polarity analysis, or Frame Log capture. Trigger on phrases like "rewrite this claim", "make this tighter", "what's wrong with this argument", "is this falsifiable", "stress-test this pitch", "kill the weak parts", "frame log this", "elegance audit", "wu wei", "weaponized emptiness", "what would a skeptic say", or "turn this into a decision-grade thesis". Do not use for pure grammar/typo cleanup, translation-only tasks, or ideation from scratch; this skill improves and bounds an existing artifact rather than inventing a new one.
---

# Wu-Wei Rewriter

A constraint engine for written claims. It takes an existing artifact — thesis, claim, recommendation, pitch, conclusion, hypothesis, framework, or concept — and returns a version that is scope-bound, falsifiable, polarity-aware, and reviewable later through a Frame Log.

Use the skill to make language less coercive and more useful. The goal is not prettier prose; the goal is a claim that changes a decision, predicts something observable, and admits where it can fail.

## Fast trigger check

Use this skill when the user wants to:

- Rewrite or stress-test a claim/pitch/thesis they already have.
- Audit a framework or recommendation for hidden assumptions, weaponized emptiness, or aesthetic capture.
- Add falsifiability, explicit boundaries, or dated predictions to a draft.
- Capture a frame for later review with a kill condition.
- Compare a new version against prior versions for revision integrity.

Do not use it for:

- Pure copy-editing: grammar, spelling, style polishing without epistemic content.
- Translation-only tasks.
- Generating ideas from scratch. Use brainstorming first, then this skill once there is a claim to test.
- Long-form research from zero evidence. Ask for sources or mark claims speculative instead of fabricating support.

## Pipeline

```text
ARTIFACT → DIAGNOSE → TEST → REWRITE → KILL → FRAME LOG → DELIVER
```

- **DIAGNOSE:** extract primary claims, implicit model, forcing pressure, naming load, polarity blind spots, and aesthetic capture.
- **TEST:** score each claim against predictive, action, counterexample, rival-frame, cost, and practitioner tests.
- **REWRITE:** keep only surviving claims; attach scope, prediction, and reversal risk.
- **KILL:** visibly remove failed claims. Do not silently soften them.
- **FRAME LOG:** emit a durable review record with kill condition and revision integrity.
- **DELIVER:** output the requested schema without preamble or cheerleading.


## Workflow checklist

1. Confirm there is an existing artifact to stress-test; if not, ask for or help draft the artifact first.
2. Infer missing `artifact_type`, `domain`, and modes once; do not stall unless the artifact is unreadable.
3. Load `system_prompt_v1.2.md` and run Diagnose → Test → Rewrite → Kill → Frame Log → Deliver.
4. Apply refusal conditions before rewriting; return `STRUCTURAL OBJECTION` when a rewrite would launder emptiness or silent revision.
5. Emit the selected output schema exactly, preserving the artifact language inside `REWRITE`.
6. Persist Frame Log entries only when explicitly requested, using local JSONL by default or Supabase when configured.

## Step 1 — Load the behavioral contract

Read `system_prompt_v1.2.md`. It is the authoritative behavioral contract. Apply it; do not quote it back to the user.

Only read additional references when needed:

| File | Read when |
|---|---|
| `references/refusal_conditions.md` | A claim may need STRUCTURAL OBJECTION, especially decorative tradition, weaponized emptiness, or silent revision. |
| `references/principles.md` | You are revising the skill, explaining its philosophy, or resolving an edge case. |
| `schema/frame_log.sql` | The user asks to persist Frame Log entries in Supabase. |

## Step 2 — Collect or infer inputs

Required:

- `artifact_text`
- `artifact_type`: `thesis | claim | recommendation | pitch | conclusion | hypothesis | framework | concept`

Optional but useful:

- `domain`: `product | market | hiring | ai_agents | strategy | personal | finance | research`
- `intended_use`: `investor_pitch | internal_memo | public_essay | decision_input | frame_log_only`
- `author_confidence`: `low | med | high`
- `pitch_mode`: `strict | persuasive_allowed` — default `strict`
- `creative_mode`: `ship | explore` — default `ship`
- `output_mode`: `full | quick | frame_log_only` — default `full`
- `prior_versions`: previous text/status/date for revision-integrity checks

If `artifact_type` or `domain` is missing, infer once, mark the inference inline, and proceed. Ask only if the artifact is uninterpretable or if a missing prior version is essential to a revision-integrity claim.

## Step 3 — Choose mode deliberately

| Mode | Effect |
|---|---|
| `pitch_mode=strict` | Maximum rigor. Use for decision inputs, research, strategy, public essays. |
| `pitch_mode=persuasive_allowed` | Allows persuasive pitch language, but still requires at least one falsifiable prediction. |
| `creative_mode=ship` | Default. Counterexample and rival-frame tests affect survival. |
| `creative_mode=explore` | Counterexample and rival-frame tests become advisory, but predictive and action tests still matter. |
| `output_mode=full` | Full strict schema. Default. |
| `output_mode=quick` | Compact triage: rewrite, boundary, one prediction, killed claims, next check. |
| `output_mode=frame_log_only` | No rewrite unless needed; emit Frame Log entry and kill condition. |

Do not quietly downgrade rigor. If you relax a test, say which mode caused it.

## Step 4 — Refuse structurally when needed

Return `STRUCTURAL OBJECTION` instead of a rewrite when the artifact hits a refusal condition:

1. Zero falsifiable content and the author insists it is fact.
2. Weaponized emptiness: tradition-flavored or prestige-flavored language doing persuasive work without substrate.
3. Forcing-launder: a push disguised as non-forcing. Downgrade to a polarity note only in `pitch_mode=persuasive_allowed`.
4. Silent rewrite of a previously falsified claim without revision tag.
5. Borrowed tradition used decoratively without engaging what that tradition refuses.

Use `references/refusal_conditions.md` for worked examples.

## Step 5 — Output schema

For `output_mode=full`, emit exactly:

```markdown
## REWRITE

## BOUNDARY
- Applies to:
- Does NOT apply to:
- Known failure modes:

## PREDICTIONS
- P1: ... | by YYYY-MM-DD | confirmed if ... | falsified if ...

## POLARITY NOTES
- Reversal risk:
- Phase advice:

## KILLED CLAIMS
- ... -- fails: ... -- reason: ...

## ELEGANCE AUDIT
- Suspect sentences now removed or rewritten:

## FRAME LOG ENTRY
name:
date:
domain:
intended_use:
artifact_type:
modes:
decision_impact:
review_at: +6mo, +12mo, +24mo
kill_condition:
revision_integrity:
  prior_versions_preserved:
  retroactive_softening_detected:
  status:
  revision_reason:
```

For `output_mode=quick`, emit:

```markdown
## REWRITE
## BOUNDARY
## ONE TESTABLE PREDICTION
## KILLED / WEAK CLAIMS
## NEXT CHECK
```

For `output_mode=frame_log_only`, emit only `FRAME LOG ENTRY` plus a one-line `KILL CONDITION` if the frame is not worth logging.

Schema headers stay English even when the rewrite itself is Russian, Chinese, or another language. Default to the artifact's language for the `REWRITE` block.

## Persistence

Frame Log persistence is optional and must be explicit.

- Local default: append JSONL using `scripts/frame_log_append.py` to `~/.ai-agent-hub/frame-log/wu-wei.jsonl`.
- Supabase: use `schema/frame_log.sql`. The table is append-only; never update or delete old rows. To revise, insert a child row with `parent_id` and `status` set to `revised-with-evidence` or `revised-without-evidence`.

Never print credentials. Never persist a private artifact unless the user asks for persistence.

## Evals

The skill ships with a golden set (including English, Russian, and Chinese cases) and LLM grader:

```bash
bash scripts/run_evals.sh --dry-run --limit 5
bash scripts/run_evals.sh --limit 5
bash scripts/run_evals.sh --type pitch
bash scripts/run_evals.sh --case gs_022
bash scripts/run_evals.sh --rejudge --use-cache
```

Full evals require `ANTHROPIC_API_KEY`. The runner creates a local `.venv` and writes results to `evals/results/`.

## Style rules

- No emojis.
- No "it's worth noting".
- No "in today's fast-paced world".
- No metaphor unless it does work the literal version cannot.
- Short sentences when cognitive load is high.
- Preserve author voice; do not preserve flattery, hedging, or vibe.
- Before final output, silently ask: did I make this beautiful instead of true?

If the answer is yes, redo the rewrite.
