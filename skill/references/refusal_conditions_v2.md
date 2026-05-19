# refusal_conditions_v2.md — Repair-first structural objections

The agent should not use `STRUCTURAL OBJECTION` as a way to avoid hard rewriting.

Default order:

```text
1. Try to find a repair path.
2. If a weaker, bounded, checkable version can survive, rewrite it.
3. If no measurable noun, mechanism, boundary, source, or revision tag can be supplied, object.
```

A refusal should teach the author how to make the artifact rewritable.

---

## Structural objection format

Localized by default.

```markdown
## Структурное возражение
- Тип:
- Почему сейчас нельзя честно переписать:
- Что нужно добавить, чтобы тезис стал переписываемым:
  1.
  2.
  3.
- Минимальная рабочая версия:
- Что я отказываюсь делать:
```

English strict-schema equivalent:

```markdown
## STRUCTURAL OBJECTION
- Type:
- Evidence:
- Repair path:
- Minimal rewritable version:
- What I will not launder:
```

---

## #1 — Zero falsifiable content + insistence on fact

### Refuse

> This is the future. AI agents will change everything. Trust me.

Why: no subject class, no mechanism, no metric, no boundary, no check.

### Repair path

Ask for or infer:

- which users or companies;
- which behavior changes;
- what time frame;
- what source would show change.

### Rewrite if repaired

> AI agents will change the first hour of the workday for analysts who start by collecting updates from multiple tools.

Now it has a measurable subject and behavior.

---

## #2 — Weaponized emptiness

### Refuse

> The only moat in AI is taste.

Why: “taste” does persuasive work without operational definition.

### Repair path

Make “taste” measurable through one or more of:

- faster rejection of weak concepts;
- higher activation from first-use experience;
- fewer shipped features with better retention;
- lower churn among users who tried alternatives;
- expert review quality with blinded comparisons.

### Rewrite if repaired

> In AI products where model access commoditizes, aesthetic judgment becomes defensible only if it shows up as faster activation, lower churn after competitive trials, or fewer shipped features with higher task completion.

---

## #3 — Forcing-launder

### Refuse in strict mode

> We do not push users. We simply remove friction until upgrading is the path of least resistance and cancellation is three menus deep.

Why: the first sentence claims non-forcing; the second describes pressure.

### Repair path

Require the author to name:

- pull mechanics;
- push mechanics;
- user cost;
- guardrail metric;
- cancellation or opt-out visibility.

### Rewrite if repaired

> We use pull through clear free-tier value and push through upgrade prompts after high-usage moments. We will treat support complaints about billing, cancellation, or dark-pattern language as a guardrail metric.

---

## #4 — Silent revision

### Refuse

> I always thought CBDCs would lose to stablecoins on programmability grounds.

If prior versions show the opposite, this is silent revision.

### Repair path

Require:

- previous claim;
- new claim;
- evidence that changed;
- revision status.

### Rewrite if repaired

> I previously argued CBDCs would win on programmability. After new pilot data and stablecoin adoption patterns, I now think programmability matters less than redemption trust and distribution. Status: revised-with-evidence.

---

## #5 — Decorative borrowed tradition

### Refuse

> Wu wei is the perfect philosophy for AI agent design.

Why: borrowed tradition is used as aesthetic authority without operational transfer or limitation.

### Repair path

Require:

- exact principle borrowed;
- what the tradition refuses;
- operational transfer;
- where the analogy breaks.

### Rewrite if repaired

> We borrow one narrow idea from wu wei: avoid adding control loops that fight the user's existing incentives. We are not claiming Taoism as a design system. The operational rule is to remove steps that create pressure without improving task completion.

---

## #6 — Fake quantification

### Refuse

> There is a 73.4% chance this strategy wins.

Why: precision without methodology is emptiness wearing a number.

### Repair path

Require:

- model or method;
- input data;
- uncertainty range;
- calibration history;
- decision threshold.

### Rewrite if repaired

> Based on five comparable launches and current pipeline quality, I would treat this as a high-risk bet rather than a quantified forecast. A real probability estimate requires a model and calibration history.

---

## Edge cases

### Looks empty but is domain shorthand

> We optimize for D7 retention.

Do not refuse in product context. D7 retention is measurable.

### Looks rewritable but should be refused

> AI-native teams win because they operate at the speed of thought.

Refuse or repair. “Speed of thought” has no operational handle.

### Looks philosophical but can be repaired

> Build with the grain of the system.

Refuse if standalone. Rewrite if the author names the system, incentive, resistance, and measurable behavior.

---

## Refusal self-check

Before objecting, verify:

- Did I identify the smallest repair that would make the claim testable?
- Did I avoid refusing just because the claim is vague?
- Did I object only when rewriting would launder emptiness?
- Did I provide a minimal rewritable version?
