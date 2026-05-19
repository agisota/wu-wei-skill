# regression_checklist.md — 30 signs Wu-Wei output has become AI-slop

Use this checklist for manual review and eval-grader automation.

Each item includes:

- symptom;
- why it matters;
- automatic detection idea;
- grader action.

---

## A. Abstraction and mechanism failures

### 1. One abstraction replaced another

- Symptom: “new language” becomes “agentic action layer”.
- Detect: high density of abstract nouns; no concrete user/system verbs.
- Grader: language_integrity = FAIL.

### 2. Mechanism missing

- Symptom: rewrite says product “creates leverage” but not how.
- Detect: no verbs like “does / checks / stores / compares / routes / executes”.
- Grader: value = WEAK or FAIL.

### 3. Boundary is generic

- Symptom: “works for teams that need productivity”.
- Detect: boundary line could apply to any B2B product.
- Grader: boundary = FAIL.

### 4. Failure mode is generic

- Symptom: “may fail if execution is poor”.
- Detect: generic risk list with no domain nouns.
- Grader: boundary = WEAK/FAIL.

### 5. Decision delta absent

- Symptom: output is nicer but no action changes.
- Detect: no “do / do not / choose / delay / measure / stop”.
- Grader: value = FAIL.

---

## B. Prediction failures

### 6. Missing metric

- Detect: prediction lacks observable quantity/event.
- Grader: falsifiability = FAIL.

### 7. Missing source

- Detect: no source class like analytics, filings, logs, survey, benchmark, customer records.
- Grader: falsifiability = FAIL.

### 8. Missing threshold

- Detect: no numeric/event threshold.
- Grader: falsifiability = FAIL.

### 9. Missing check date

- Detect: no `YYYY-MM-DD` or explicit relative check window.
- Grader: falsifiability = FAIL.

### 10. Future-sounding but uncheckable

- Symptom: “will become a major revenue driver”.
- Detect regex: `major|important|dominant|structural|meaningful` near future verb without metric.
- Grader: falsifiability = FAIL.

### 11. Fake precision

- Symptom: “73.4% chance”.
- Detect: decimal probability without methodology.
- Grader: language_integrity = FAIL; may require objection.

### 12. Prediction not tied to rewritten claim

- Symptom: claim about hiring, prediction about revenue.
- Detect: low entity overlap between claim and prediction.
- Grader: falsifiability = WEAK/FAIL.

---

## C. Kill-integrity failures

### 13. Original overclaim disappears silently

- Detect: strong terms in input absent from killed claims.
- Grader: kill_integrity = FAIL.

### 14. “Killed” claim only softened

- Symptom: “all workflows” becomes “many workflows” but not listed as killed.
- Detect: universal quantifiers transformed without killed entry.
- Grader: kill_integrity = FAIL.

### 15. Weak claim survives as metaphor

- Symptom: “operating system of thinking” retained.
- Detect: phrase from must_not_contain appears outside killed/audit context.
- Grader: language_integrity = FAIL.

### 16. Killed reason is generic

- Symptom: “too broad” with no specific reason.
- Detect: killed claim reason under 8 words or no test reference.
- Grader: kill_integrity = WEAK.

---

## D. Language-integrity failures

### 17. Hybrid jargon in Russian

- Detect terms: `runtime`, `evidence trail`, `workflow-запуск`, `retention`, `novelty`, `frame надо убить`.
- Grader: language_integrity = FAIL unless quoted as killed/prohibited.

### 18. English headers when native mode expected

- Detect: headers `REWRITE`, `BOUNDARY` in Russian artifact with `strict_schema=false`.
- Grader: structure_mode_fit = WEAK.

### 19. Prestige nouns without handles

- Detect: `taste`, `moat`, `AI-native`, `agentic`, `operating system`, `paradigm`, `grain` without definition.
- Grader: language_integrity = WEAK/FAIL.

### 20. “Founder memo voice” replaces meaning

- Symptom: crisp, punchy, empty lines.
- Detect: many short abstract slogans; no metric/source.
- Grader: value = FAIL.

### 21. Metaphor retained without literal version

- Detect: metaphor list appears with no concrete paraphrase.
- Grader: language_integrity = WEAK/FAIL.

### 22. Decorative philosophy

- Detect: Tao, Zen, Stoic, wu wei used as authority without operational transfer.
- Grader: structural_objection_accuracy = FAIL if not objected/repaired.

---

## E. Mode failures

### 23. Compact mode omits killed claims

- Detect: no killed/weak claims section.
- Grader: structure_mode_fit = FAIL.

### 24. Compact mode emits full bureaucracy

- Detect: full frame log despite compact request.
- Grader: structure_mode_fit = WEAK.

### 25. Decision mode lacks frame log

- Detect: no review date or kill condition.
- Grader: structure_mode_fit = FAIL.

### 26. Critique-only mode rewrites without diagnosis

- Detect: rewrite section present but no diagnosis/repair path.
- Grader: structure_mode_fit = FAIL.

### 27. Frame-log mode lacks kill condition

- Detect: no “kill if / снять если / опровергнется если”.
- Grader: structure_mode_fit = FAIL.

---

## F. Objection failures

### 28. Refusal without repair path

- Detect: `STRUCTURAL OBJECTION` but no unblock/repair fields.
- Grader: structural_objection_accuracy = FAIL.

### 29. False refusal of vague-but-repairable claim

- Symptom: refuses “AI agents change first hour of workday”.
- Detect: input contains measurable noun/time/actor but output objects.
- Grader: structural_objection_accuracy = FAIL.

### 30. Silent revision missed

- Detect: prior_versions contradict artifact; output does not mark revision.
- Grader: kill_integrity = FAIL; structural_objection_accuracy = FAIL if expected objection.

---

## Suggested machine checks

### Regex flags

```yaml
russian_hybrid_jargon:
  - "\\bruntime\\b"
  - "evidence trail"
  - "workflow[- ]?запуск"
  - "\\bretention\\b"
  - "\\bnovelty\\b"
  - "frame надо убить"

fake_precision:
  - "\\b\\d{1,2}\\.\\d%"
  - "\\b\\d{1,2}\\.\\d percent"

future_vague:
  - "will become (major|important|dominant|structural)"
  - "станет (важным|ключевым|доминирующим)"

universal_overclaim:
  - "\\ball\\b|\\bevery\\b|everything|все|каждый|любой|единственный|only|inevitable|неизбежно"
```

### Contract checks

```yaml
prediction_contract_required:
  required_fields:
    - metric
    - source
    - threshold
    - check_date
    - confirmed_if
    - weakened_if
    - falsified_if
```

### Must-not-contain policy

If a forbidden term appears inside an explicit killed/audit sentence, it may pass.
If it appears in the retained rewrite, fail.

---

## Grader assertion additions

```json
{
  "language_integrity_required_met": true,
  "prediction_contract_complete": true,
  "must_not_contain_clean": true,
  "repair_path_present_if_objection": true,
  "localized_headers_correct": true,
  "silent_softening_absent": true
}
```
