# anti_slop.md — Wu-Wei anti-slop reference

This reference defines the failure modes that make a rewrite sound competent while remaining weak.

The core rule:

```text
A rewrite fails if it replaces one abstraction with another abstraction.
```

A good rewrite usually becomes less impressive, more limited, and easier to check.

---

## 1. What “AI-slop” means here

AI-slop is not merely bad style. In this skill, slop means prose that creates the appearance of decision quality without producing decision value.

A slop rewrite usually has at least one of these properties:

- it sounds sharper but does not change a decision;
- it names abstractions instead of mechanisms;
- it adds fake precision;
- it uses prestige language to hide missing evidence;
- it produces a schema full of fields with weak content;
- it keeps the author’s claim alive by quietly narrowing it without admitting what was killed.

---

## 2. Taxonomy of slop

| Failure mode | Symptom | Example | Required fix |
|---|---|---|---|
| Abstraction laundering | One vague term becomes another | “new language” → “agentic action layer” | Replace with who does what, using which input, producing which result |
| Prestige laundering | Famous or trendy noun does the work | “AI-native”, “Stoic”, “operating system”, “taste” | Define observable behavior or remove |
| Metric theater | Number without method | “73.4% chance this works” | Add method/source or mark speculative |
| Totality creep | Claim expands to everything | “all workflows”, “every company”, “the future” | Bind to segment, task, date, or mechanism |
| Prediction cosplay | Future-sounding but uncheckable | “will become a major driver” | Add metric, source, threshold, check date |
| Hybrid jargon | Non-English output borrows English to sound advanced | “workflow-запуск”, “evidence trail” | Use native operational language |
| Schema stuffing | All sections present, content thin | “Applies to: businesses” | Require discriminating boundaries |
| Silent softening | Strong original claim disappears without record | “replace all” → “may complement some” | List killed claim and reason |
| False inevitability | Causal claim without mechanism | “economics are inevitable” | State mechanism and counter-condition |
| Decorative tradition | Philosophy as vibe | “wu wei for agent design” | Engage what the tradition refuses or object |

---

## 3. Slop detector questions

Before final output, ask:

1. Can a third party check the prediction on the stated date?
2. Does the prediction name a metric, source, threshold, and date?
3. Would the rewrite still sound plausible if the key noun were replaced with its opposite?
4. Did I explain the mechanism in concrete verbs?
5. Did I name where the thesis does not apply?
6. Did I keep any prestige term because it sounds good?
7. Did I introduce English terms into a non-English artifact without need?
8. Did I preserve a metaphor when the literal version was clearer?
9. Did I turn a pitch into a research memo or a memo into a pitch?
10. Did I object before giving a repair path?

If any answer reveals weakness, revise.

---

## 4. Russian anti-slop list

Avoid these in Russian output unless the user explicitly asks for mixed startup jargon:

```text
runtime
workflow-запуск
workflow-сценарий
evidence trail
retention
novelty
frame надо убить
decision-grade
agentic / агентный, when it is not operationally defined
операционная система мышления
новый язык взаимодействия
AI-native, unless defined through concrete architecture or behavior
moat / ров, unless the defense mechanism is measurable
```

Preferred replacements:

| Avoid | Prefer |
|---|---|
| `runtime` | среда выполнения / исполняющий слой / набор инструментов, depending on context |
| `evidence trail` | журнал действий / след действий / сохранённые данные проверки |
| `workflow-запуск` | запуск сценария / повторный сценарий |
| `retention` | возврат пользователей / удержание, if explicitly a product metric |
| `novelty` | демо-эффект / эффект новизны |
| `frame надо убить` | тезис надо снять / позиционирование надо пересмотреть |
| `decision-grade` | пригодный для решения / рабочий, проверяемый |
| `agentic action` | действие, выполненное системой с проверяемым результатом |

---

## 5. Prediction contract

Every prediction must include:

```yaml
metric: what changes
source: where it can be checked
threshold: how much / how many / what event
check_date: when to check
confirmed_if: what confirms
weakened_if: what weakens
falsified_if: what falsifies
```

Reject or downgrade predictions that only say:

```text
will become important
will be a major revenue driver
users will prefer it
adoption will grow
companies will switch
quality will improve
```

Unless they include the full contract.

---

## 6. Before / after mini-examples

### Product pitch

Bad rewrite:

> Мы строим новый слой агентного взаимодействия, где намерения превращаются в проверяемые действия через runtime и evidence trail.

Good rewrite:

> Пользователь описывает цель. Система разбивает её на шаги, выполняет действие через подключённые инструменты и показывает, что было сделано, на каких данных и с каким результатом.

### Strategy claim

Bad rewrite:

> Taste is the dominant moat for AI products in markets where experience compounds.

Good rewrite:

> “Taste” only becomes a defensible advantage when it shows up as faster rejection of weak product directions, higher activation from first-use experience, or lower churn among users who compare alternatives. Without those signals, “taste” is a label, not a moat.

### Hiring claim

Bad rewrite:

> Hire for agentic slope, not static intercept.

Good rewrite:

> For roles with fast-changing tools, prefer candidates who can show a recent example of learning a new tool, applying it to a real task, and explaining where it failed. Do not use this rule for roles where domain judgment or compliance risk matters more than learning speed.

---

## 7. Auto-grader hooks

Add these fields to golden cases when anti-slop matters:

```json
{
  "must_not_contain": ["runtime", "evidence trail", "workflow-запуск"],
  "must_contain": ["метрика", "источник", "порог", "дата проверки"],
  "prediction_requirements": ["metric", "source", "threshold", "check_date"],
  "language_integrity_required": true
}
```

Suggested judge rule:

```text
If a non-English output contains avoidable English product jargon and the input did not require it, grade language_integrity = FAIL.
```
