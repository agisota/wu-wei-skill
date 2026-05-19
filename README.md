# Wu-Wei Rewriter Skill — v1.3

A multilingual claim-rewriting skill for turning elegant-but-unsafe ideas into bounded, falsifiable, decision-grade language.

Version 1.3 keeps the original philosophy and changes the training signal:

- examples teach mechanism, not style;
- predictions require a metric, source, threshold, and check date;
- Russian output defaults to native Russian, not hybrid English/Russian product jargon;
- compact output is the default for normal use;
- full decision schema is reserved for strategy, research, public claims, and high-stakes memos;
- structural objections include a repair path before refusal.

---

## What this skill does

```text
ARTIFACT → DIAGNOSE → TEST → REWRITE → KILL → LOG OR CHECK
```

The skill takes an existing artifact — thesis, claim, recommendation, pitch, conclusion, hypothesis, framework, or concept — and returns a version that:

1. says what it actually claims;
2. names where it applies and where it fails;
3. removes rhetoric that does more work than the evidence;
4. adds a checkable prediction or marks the claim as speculative;
5. keeps a visible record of killed claims instead of silently softening them.

The goal is not prettier prose. The goal is a claim that changes a decision, predicts something observable, and admits what would prove it wrong.

---

## When to use

Use `wu-wei-rewriter` when you already have a draft and want to make it safer for decisions:

- AI strategy claims;
- founder / investor pitch language;
- product positioning;
- research conclusions;
- architecture recommendations;
- hiring and org-design arguments;
- market theses;
- public essays and memos;
- personal operating principles that should become testable.

Do not use it for:

- grammar-only cleanup;
- translation-only work;
- ideation from zero;
- long-form research without sources;
- slogans that are supposed to remain slogans;
- private therapeutic reflection where falsifiability would distort the purpose.

Fast trigger:

```text
Use this skill when the sentence sounds true before it can be checked.
```

---

## Before / after examples

### 1) English — AI strategy thesis

**Before**

> Multi-agent systems will replace single-LLM workflows in enterprise within 18 months. The economics are inevitable and the technology is here.

**After**

> Multi-agent workflows will take budget first in enterprise processes where failure can be split into steps, reviewed, and retried: support triage, compliance review, internal research, document QA, and back-office checks.
>
> They will not replace single-call LLM workflows where latency, clear ownership, and interface simplicity matter more than delegation.
>
> Prediction: by 2027-11-01, using a fixed list of ten AI workflow vendors selected on 2026-06-01, at least three will publicly report paid enterprise usage or revenue tied specifically to multi-step agent orchestration, not only chat assistants. Confirm through vendor filings, pricing pages, customer case studies, or audited revenue commentary. Weaken this thesis if paid enterprise usage remains concentrated in single-call copilots and embedded assistants.

**What changed**

- Killed: “replace” and “inevitable”.
- Added boundary: decomposable, reviewable, retryable work.
- Added counter-boundary: latency, ownership, UI simplicity.
- Added check: fixed vendor set, source class, threshold, check date.

---

### 2) Русский — продуктовый pitch

**До**

> Наш продукт создаёт новый язык взаимодействия человека и агента. Это не инструмент, а новая операционная система мышления.

**После**

> Мы не продаём «новый язык мышления». Мы продаём более короткий путь от намерения к проверенному действию.
>
> Пользователь описывает цель. Система разбивает её на шаги, выбирает нужные инструменты, выполняет действие и показывает, что было сделано, на каких данных и с каким результатом.
>
> Сильные случаи: исследование, разбор входящих заявок, подготовка документов, контроль повторяемых операций и задачи с несколькими источниками данных.
>
> Слабые случаи: одноразовый вопрос в чат, творческий черновик без проверки, ручное решение, где пользователь обязан подтвердить каждый шаг.
>
> Проверка: за первые 90 дней после регистрации пользователи должны чаще возвращаться к повторным сценариям с сохранённым результатом, чем к одноразовым чатам. Источник: продуктовая аналитика по новым пользователям. Порог: повторный запуск сохранённого сценария у активированных пользователей выше повторного одноразового чата минимум на 20%. Если возврат держится только на демо-эффекте первой сессии, позиционирование надо пересмотреть.

**Что изменилось**

- Убрана метафора «операционная система мышления».
- Механизм стал наблюдаемым: цель → шаги → инструменты → действие → данные → результат.
- Добавлены сильные и слабые случаи.
- Прогноз привязан к метрике, источнику, порогу и сроку.
- Нет гибридного англо-жаргона: `runtime`, `evidence trail`, `workflow-запуски`, `retention`, `novelty`, `frame`.

---

### 3) 中文 — 市场 / 组织判断

**改写前**

> AI 会让中层管理消失，因为协调会被模型自动化。

**改写后**

> AI 不会让中层管理作为一个类别消失。它会先压缩那些主要负责转发信息、汇总状态、追问进度的岗位。
>
> 仍然有价值的中层管理会集中在三类工作上：定义责任边界、处理跨团队冲突、为取舍和结果承担责任。
>
> 可验证预测：到 2027-12-31，在已经公开采用 AI 工作流的公司中，职位描述以状态汇总和进度追踪为主的中层岗位减少速度，应高于明确承担跨团队决策、绩效判断或风险责任的岗位。验证来源：公司招聘信息、组织公告、裁员说明、岗位说明变化。如果两类岗位以相近速度下降，本判断需要修正。

**变化**

- 原句把“协调自动化”误写成“管理消失”。
- 改写后保留趋势，但限定了岗位类型。
- 预测包含日期、对象、比较关系和可检查来源。

---

## Output modes

Default mode is `compact`, not `full`.

| Mode | Use when | Output |
|---|---|---|
| `compact` | Fast rewrite, pitch cleanup, normal note sharpening | Rewrite, boundary, one prediction, killed claims, next check |
| `decision` | Strategy memo, investment thesis, hiring system, architecture recommendation | Full schema with predictions, polarity notes, killed claims, elegance audit, frame log |
| `frame_log` | You only want to record a thesis for later review | Frame log entry + kill condition |
| `critique_only` | You want diagnosis but no rewrite yet | Failure map, repair path, risky assumptions, suggested tests |

Aliases from v1.x:

| Old | New |
|---|---|
| `quick` | `compact` |
| `full` | `decision` |
| `frame_log_only` | `frame_log` |

---

## Prediction contract

Every non-speculative retained claim needs at least one prediction:

```yaml
P1:
  claim: "..."
  metric: "observable quantity or event"
  source: "where a third party can check it"
  threshold: "what must be true"
  check_date: "YYYY-MM-DD"
  confirmed_if: "..."
  weakened_if: "..."
  falsified_if: "..."
```

If no credible metric or source can be named, do not invent precision. Mark the claim `SPECULATIVE` and provide a measurement plan.

---

## Usage

```text
Use wu-wei-rewriter on this thesis:
"Taste is the only moat in AI products."
```

Structured input:

```yaml
artifact_type: pitch
domain: product
intended_use: investor_pitch
pitch_mode: persuasive_allowed
creative_mode: ship
output_mode: compact
artifact_text: |
  Our product creates a new language for human-agent collaboration.
```

Russian:

```text
Прогони через wu-wei-rewriter: где тут пустота, какие утверждения надо убрать, что можно проверить через 90 дней?
```

Chinese:

```text
用 wu-wei-rewriter 重写这个判断，让它有边界、反例和可验证预测。
```

---

## Installation

```bash
git clone https://github.com/agisota/wu-wei-skill.git
cd wu-wei-skill
bash scripts/install_all_cli.sh
bash scripts/validate.sh
```

Build the portable skill package:

```bash
bash scripts/package.sh
# dist/wu-wei-rewriter.skill
```

The installer symlinks the canonical `skill/` directory into the local CLI skill roots used by Codex, Claude Code, OpenCode, Kimi, Gemini, Hermes, Droid, Pi, and the shared archive when those roots exist.

---

## Repository layout

```text
skill/SKILL.md                         skill entrypoint
skill/system_prompt_v1.3.md             authoritative behavior contract, v1.3
skill/references/anti_slop.md           anti-slop taxonomy and checks
skill/references/ru_style_guide.md      Russian output style guide
skill/references/refusal_conditions_v2.md repair-first structural objections
skill/references/mode_matrix.md         output-mode decision matrix
skill/evals/golden_set.jsonl            existing golden cases
skill/evals/golden_set_ru.jsonl         Russian anti-slop golden cases
skill/evals/grader_prompt_v2.md         LLM judge with language-integrity rubric
skill/evals/regression_checklist.md     30 regression checks
scripts/install_all_cli.sh              symlink install into local CLI skill roots
scripts/package.sh                      build dist/wu-wei-rewriter.skill
```

---

## Validate

```bash
bash skill/scripts/run_evals.sh --dry-run --limit 5
bash skill/scripts/run_evals.sh --type pitch
bash skill/scripts/run_evals.sh --case gs_ru_v2_001
bash skill/scripts/run_evals.sh --rejudge --use-cache
```

Full evals require the configured LLM judge key used by the runner.

---

## Design rule

```text
A rewrite fails if it replaces one abstraction with another abstraction.
```

Good output should feel less impressive and more useful.
