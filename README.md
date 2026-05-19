# Wu-Wei Rewriter Skill

A claim-rewriting skill for turning elegant-but-unsafe ideas into bounded, falsifiable, decision-grade language.

## Before / after examples

### 1) English — AI strategy thesis

**Before**

> Multi-agent systems will replace single-LLM workflows in enterprise within 18 months. The economics are inevitable and the technology is here.

**After**

> Multi-agent systems will take budget from single-LLM workflows first in enterprise processes where failure can be decomposed, reviewed, and retried: compliance review, support triage, internal research, and back-office QA. They will not replace single-call workflows where latency, audit ownership, or UI simplicity matters more than delegation.
>
> Prediction: by 2027-11-01, at least three of the top ten AI workflow vendors will report agent-orchestration features as a material enterprise revenue driver; the thesis is weakened if single-call assistants remain the dominant paid usage pattern in regulated enterprises.

**What changed:** the rewrite killed inevitability, narrowed the domain, preserved the useful model, and added a prediction that can be checked later.

### 2) Русский — продуктовый pitch

**До**

> Наш продукт создаёт новый язык взаимодействия человека и агента. Это не инструмент, а новая операционная система мышления.

**После**

> Продукт полезен не потому, что создаёт «новый язык мышления», а потому что снижает стоимость перехода от размытой цели к проверяемому агентному действию. Сильный кейс: пользователь формулирует намерение, система превращает его в план, выбирает runtime, запускает проверку и сохраняет evidence trail. Слабый кейс: обычный чат, где достаточно одного ответа без состояния, инструментов и проверки.
>
> Прогноз: если это позиционирование верно, в течение 90 дней новые пользователи будут чаще возвращаться к workflow-запускам с артефактами, чем к одноразовым чатам; если retention держится только на novelty или демо-эффекте, frame надо убить.

**Что изменилось:** метафора была оставлена только там, где она меняет решение; вместо «операционной системы мышления» появился проверяемый механизм ценности.

### 3) 中文 — 市场 / 组织判断

**改写前**

> AI 会让中层管理消失，因为协调会被模型自动化。

**改写后**

> AI 不会简单地让中层管理消失；它会先压缩那些只负责转发信息、汇总状态、追问进度的管理层。仍然有价值的中层会转向三个更难自动化的任务：定义责任边界、处理冲突、判断什么时候不该优化局部效率。
>
> 可验证预测：到 2027 年底，采用 AI 工作流的公司会减少纯状态汇报型岗位，但不会同比例减少负责跨团队决策、绩效判断和风险承担的岗位。如果两类岗位同时下降，本判断需要修正。

**变化:** 原句把“协调自动化”误写成“管理消失”。改写后保留趋势，但给出边界、反例和可验证条件。

## Why this approach exists

Good language is dangerous when it makes weak models feel inevitable. Founders, researchers, strategists, investors, and agent builders often write sentences that sound complete before they are testable. The result is aesthetic capture: the claim becomes memorable before it becomes true.

Wu-Wei Rewriter uses the opposite pressure. It does not push harder; it removes forcing. It asks what the system already rewards, what the claim predicts, what decision changes, where it fails, and what a competent rival frame would say. This is why the name borrows from *wu wei*: not as decorative mysticism, but as a discipline of reducing coercive language until the remaining claim can stand by itself.

The skill is useful when a draft needs to survive contact with adults: a skeptical operator, investor, reviewer, engineer, regulator, or future version of yourself. It rewrites by subtraction, boundary-setting, falsifiability, polarity awareness, and revision integrity.

## Что это такое по-русски

Wu-Wei Rewriter — это скилл для переписывания тезисов, питчей, гипотез, рекомендаций и фреймворков так, чтобы они перестали быть красивыми пустыми формулами и стали проверяемыми рабочими утверждениями.

Он нужен там, где обычная редактура вредна: она делает текст гладким, но не делает мысль честнее. Этот скилл, наоборот, режет «несущую пустоту», связывает claim с областью применимости, добавляет falsifiable predictions, явно убивает слабые утверждения и оставляет Frame Log entry, чтобы через 6/12/24 месяца можно было проверить, не переписали ли мы историю задним числом.

## What the skill does

Pipeline:

```text
ARTIFACT → DIAGNOSE → TEST → REWRITE → KILL → FRAME LOG → DELIVER
```

It works on:

- thesis
- claim
- recommendation
- pitch
- conclusion
- hypothesis
- framework
- concept

It is strongest for:

- AI strategy claims
- investor / founder pitch language
- product positioning
- research conclusions
- architecture recommendations
- hiring / org design arguments
- market theses
- public essays and memos
- Obsidian notes that should become testable frames

## Output shape

The default output contains:

1. `REWRITE` — a shippable rewrite.
2. `BOUNDARY` — applies to / does not apply to / failure modes.
3. `PREDICTIONS` — dated falsifiable predictions.
4. `POLARITY NOTES` — reversal risks and phase advice.
5. `KILLED CLAIMS` — weak claims removed visibly, not silently softened.
6. `ELEGANCE AUDIT` — beautiful-but-not-true sentences removed or rewritten.
7. `FRAME LOG ENTRY` — review dates, kill condition, revision integrity.

## Usage

Ask your agent to use the skill when you have an existing artifact to sharpen:

```text
Use wu-wei-rewriter on this thesis:
"Taste is the only moat in AI products."
```

With structured inputs:

```text
artifact_type: pitch
domain: product
intended_use: investor_pitch
pitch_mode: persuasive_allowed
creative_mode: ship
artifact_text: "Our product creates a new language for human-agent collaboration."
```

Russian:

```text
Прогони через wu-wei-rewriter: где тут пустота, какие claims надо убить, что можно проверить через 90 дней?
```

Chinese:

```text
用 wu-wei-rewriter 重写这个判断，让它有边界、反例和可验证预测。
```

## Modes

| Mode | Default | Use when |
|---|---:|---|
| `pitch_mode=strict` | yes | research, strategy, decision inputs, public claims |
| `pitch_mode=persuasive_allowed` | no | founder/investor pitch where persuasive language is allowed but predictions remain required |
| `creative_mode=ship` | yes | final or decision-grade artifact |
| `creative_mode=explore` | no | early-stage exploration where rival/counterexample tests are advisory |
| `output_mode=full` | yes | complete schema |
| `output_mode=quick` | no | fast triage: rewrite, boundary, prediction, killed claims |
| `output_mode=frame_log_only` | no | record the frame without a full rewrite |

## Repository layout

```text
skill/SKILL.md                    skill entrypoint
skill/system_prompt_v1.2.md        authoritative behavior contract
skill/references/                  expanded principles and refusal examples
skill/schema/frame_log.sql          optional Supabase append-only Frame Log
skill/scripts/frame_log_append.py   local JSONL Frame Log helper
skill/evals/golden_set.jsonl        56 golden cases
skill/evals/grader.py               LLM judge runner
scripts/install_all_cli.sh          symlink install into local CLI skill roots
scripts/package.sh                  build dist/wu-wei-rewriter.skill
```

## Install locally

From the repository root:

```bash
bash scripts/install_all_cli.sh
```

Default roots:

- `~/.codex/skills`
- `~/.claude/skills`
- `~/.config/opencode/skills`
- `~/.kimi/skills`
- `~/.gemini/skills`
- `~/.hermes/skills`
- `~/.droid/skills`
- `~/.pi/skills`
- `~/.config/pi/skills`
- `~/.agents/skills.shared-archive`

Add more roots with:

```bash
EXTRA_SKILL_ROOTS="$HOME/.cursor/skills:$HOME/.config/zed/skills" bash scripts/install_all_cli.sh
```

## Validate

```bash
python ~/.ai-agent-hub/skill-quality/validate_skill.py --skill skill
bash skill/scripts/run_evals.sh --dry-run --limit 5
```

Full evals require an Anthropic API key:

```bash
ANTHROPIC_API_KEY=... bash skill/scripts/run_evals.sh --limit 5
```

The eval runner keeps dependencies in `skill/.venv` and writes results under `skill/evals/results/`.

## Packaging

```bash
bash scripts/package.sh
```

Output:

```text
dist/wu-wei-rewriter.skill
```

## License

MIT.
