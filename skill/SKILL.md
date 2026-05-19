---
name: wu-wei-rewriter
description: Use this skill whenever the user has an existing claim, thesis, pitch, recommendation, conclusion, hypothesis, framework, strategy memo, product positioning statement, or concept that needs epistemic stress-testing, falsifiability, boundary-setting, anti-slop cleanup, native-language sharpening, polarity analysis, repair-first refusal, or Frame Log capture. Trigger on phrases like "rewrite this claim", "make this tighter", "what's wrong with this argument", "is this falsifiable", "stress-test this pitch", "kill the weak parts", "frame log this", "elegance audit", "anti-slop", "wu wei", "weaponized emptiness", "what would a skeptic say", or "turn this into a decision-grade thesis". Do not use for pure grammar/typo cleanup, translation-only tasks, or ideation from scratch; this skill improves and bounds an existing artifact rather than inventing a new one.
---

# Wu-Wei Rewriter

A constraint engine for written claims. It takes an existing artifact — thesis, claim, recommendation, pitch, conclusion, hypothesis, framework, product positioning, or concept — and returns a version that is bounded, falsifiable, decision-useful, native to the artifact language, and reviewable later when needed.

The goal is not prettier prose. The goal is a claim that changes a decision, predicts something observable, admits where it can fail, and avoids replacing one abstraction with another abstraction.

## Fast trigger check

Use this skill when the user wants to:

- Rewrite or stress-test an existing claim, pitch, thesis, memo, recommendation, or framework.
- Turn elegant but slippery language into a bounded, checkable statement.
- Remove hype, prestige terms, vague philosophy, startup jargon, or AI-slop from a draft.
- Add prediction contract: metric, source, threshold, check date, and falsification condition.
- Identify weak claims that must be killed or explicitly marked speculative.
- Compare a new claim against prior versions for revision integrity.
- Capture a thesis in a Frame Log for later review.

Do not use it for:

- Pure copy-editing: grammar, spelling, or style polishing without epistemic content.
- Translation-only tasks.
- Generating ideas from scratch. Use brainstorming first, then this skill once there is a claim to test.
- Long-form research from zero evidence. Ask for sources, mark the claim speculative, or provide a measurement plan.
- Slogans or creative copy that the user explicitly wants to keep untestable.

## Pipeline

```text
ARTIFACT → DIAGNOSE → TEST → REWRITE → KILL → REPAIR/OBJECT → DELIVER
```

- **DIAGNOSE:** extract primary claims, implicit model, forcing pressure, naming load, source gaps, polarity blind spots, and aesthetic capture.
- **TEST:** check each claim against predictive, action, counterexample, rival-frame, cost, and practitioner tests.
- **REWRITE:** keep only surviving claims; attach scope, boundary, prediction contract, and reversal risk.
- **KILL:** visibly remove failed claims. Do not silently soften them.
- **REPAIR/OBJECT:** before structural objection, give the minimum data, boundary, or mechanism that would make the claim rewritable.
- **DELIVER:** emit the selected output mode without preamble or cheerleading.

## Workflow checklist

1. Confirm there is an existing artifact to stress-test. If not, ask for or help draft a minimal artifact first.
2. Infer missing `artifact_type`, `domain`, and mode once. Do not stall unless the artifact is unreadable.
3. Load `system_prompt_v1.3.md` and follow it as the authoritative behavioral contract.
4. Default to `output_mode=compact`, not full/decision schema.
5. Use the artifact language for headers and labels unless `strict_schema=true`, the artifact is English, or the user asks for machine-readable output.
6. Apply anti-slop rules before final output. A rewrite fails if it replaces vague language with different vague language.
7. Apply repair-first refusal logic before objecting. Return `STRUCTURAL OBJECTION` only when repair is impossible or the artifact insists on false certainty.
8. Persist Frame Log entries only when explicitly requested.

## Step 1 — Load the behavioral contract

Read `system_prompt_v1.3.md`. It is the authoritative behavioral contract. Apply it; do not quote it back to the user.

Read additional references only when needed:

| File | Read when |
|---|---|
| `references/mode_matrix.md` | You need to choose between `compact`, `decision`, `frame_log`, and `critique_only`, or map old aliases. |
| `references/anti_slop.md` | The draft contains startup/AI/strategy jargon, fake precision, abstraction laundering, or model-shaped prose. |
| `references/ru_style_guide.md` | The artifact or requested output is Russian. |
| `references/refusal_conditions_v2.md` | A claim may need repair-first `STRUCTURAL OBJECTION`. |
| `references/principles.md` | You are revising the skill, explaining its philosophy, or resolving an edge case. |
| `schema/frame_log.sql` | The user explicitly asks to persist Frame Log entries in Supabase. |

## Step 2 — Collect or infer inputs

Required:

- `artifact_text`
- `artifact_type`: `thesis | claim | recommendation | pitch | conclusion | hypothesis | framework | concept`

Optional but useful:

- `domain`: `product | market | hiring | ai_agents | strategy | personal | finance | research`
- `intended_use`: `investor_pitch | internal_memo | public_essay | decision_input | frame_log | personal_note`
- `author_confidence`: `low | med | high`
- `pitch_mode`: `strict | persuasive_allowed` — default `strict`
- `creative_mode`: `ship | explore` — default `ship`
- `output_mode`: `compact | decision | frame_log | critique_only` — default `compact`
- `strict_schema`: `true | false` — default `false`
- `output_language`: `native | english | artifact` — default `artifact`
- `prior_versions`: previous text/status/date for revision-integrity checks

Aliases for older prompts:

| Old mode | New mode |
|---|---|
| `quick` | `compact` |
| `full` | `decision` |
| `frame_log_only` | `frame_log` |

If `artifact_type` or `domain` is missing, infer once and mark the inference inline. Ask only if the artifact is uninterpretable or if a missing prior version is essential to a revision-integrity claim.

## Step 3 — Choose mode deliberately

| Mode | Use when | Must include |
|---|---|---|
| `output_mode=compact` | Normal default: fast rewrite, pitch cleanup, note sharpening. | Rewrite, boundary, one prediction, killed/weak claims, next check. |
| `output_mode=decision` | Strategy memo, public thesis, research conclusion, hiring/architecture/investment decision. | Full boundary, predictions, polarity, killed claims, elegance audit, Frame Log entry. |
| `output_mode=frame_log` | User asks to preserve a thesis for later review. | Frame entry, review dates, kill condition, revision integrity. |
| `output_mode=critique_only` | User asks “what’s wrong?”, “where is the slop?”, “stress-test this”. | Diagnosis, forcing pressure, repair path, tests, what to remove. |

Do not quietly downgrade rigor. If you relax a test, say which mode caused it.

## Step 4 — Prediction contract

Every retained non-speculative claim needs a checkable prediction with:

```yaml
P1:
  claim: string
  metric: observable quantity or event
  source: where a third party can check it
  threshold: what must be true
  check_date: YYYY-MM-DD
  confirmed_if: condition
  weakened_if: condition
  falsified_if: condition
```

If no credible metric or source can be named, do not invent precision. Mark the claim `SPECULATIVE` and provide a measurement plan.

## Step 5 — Language policy

Default to the artifact language for headers, labels, explanations, and rewrite.

For non-English artifacts:

- translate operational terms into the artifact language;
- keep English only for product names, fixed technical standards, API/model names, code symbols, or user-provided terms;
- avoid hybrid phrases such as `workflow-запуск`, `evidence trail`, `runtime`, `retention`, `novelty`, `frame надо убить`, unless the user explicitly asks for startup jargon;
- prefer concrete nouns, observable mechanisms, and native phrasing over imported prestige terms.

Use English schema headers only when `strict_schema=true`, the user asks for machine-readable output, the artifact is English, or an eval runner requires exact English keys.

## Step 6 — Repair-first structural objection

Before `STRUCTURAL OBJECTION`, provide a minimal repair path:

1. What noun or mechanism would make the claim measurable?
2. What boundary would make it safe to rewrite?
3. What source or observation would let a third party check it?
4. What weaker version could survive?

Object only when the artifact still has no measurable substrate or the author insists on false certainty. Use `references/refusal_conditions_v2.md` for worked examples.

## Persistence

Frame Log persistence is optional and must be explicit.

- Local default: append JSONL using `scripts/frame_log_append.py` to `~/.ai-agent-hub/frame-log/wu-wei.jsonl`.
- Supabase: use `schema/frame_log.sql`. The table is append-only; never update or delete old rows. To revise, insert a child row with `parent_id` and `status` set to `revised-with-evidence` or `revised-without-evidence`.

Never print credentials. Never persist a private artifact unless the user asks for persistence.

## Evals

The skill ships with base multilingual cases, a Russian anti-slop golden set, an LLM grader, and a regression checklist:

```bash
bash scripts/run_evals.sh --dry-run --limit 5
bash scripts/run_evals.sh --dry-run --case gs_ru_v2_001
bash scripts/run_evals.sh --limit 5
bash scripts/run_evals.sh --type pitch
bash scripts/run_evals.sh --case gs_022
bash scripts/run_evals.sh --rejudge --use-cache
```

Key eval assets:

- `evals/golden_set.jsonl` — base multilingual regression set.
- `evals/golden_set_ru.jsonl` — Russian anti-slop cases.
- `evals/grader_prompt_v2.md` — language-integrity and prediction-contract grader.
- `evals/regression_checklist.md` — 30 signs that output regressed into AI-slop.

Full evals require `ANTHROPIC_API_KEY`. The runner creates a local `.venv` and writes results to `evals/results/`.

## Style rules

- No emojis.
- No “it's worth noting”.
- No “in today's fast-paced world”.
- No metaphor unless it does work the literal version cannot.
- No fake precision.
- No imported jargon where native language is clearer.
- Concrete nouns before abstract nouns.
- Mechanism before label.
- Boundary before confidence.
- Measurement before prediction.
- Preserve author voice; do not preserve flattery, hedging, prestige language, or vibe.

Before final output, silently ask: did I make this beautiful instead of true? If yes, redo the rewrite.
