# Wu-Wei Rewriter Skill — v1.3

`wu-wei-rewriter` существует для одной конкретной проблемы: сильная формулировка часто начинает убеждать раньше, чем становится проверяемой. В стратегиях, pitch, исследованиях и продуктовых тезисах это опасно: красивый язык скрывает область применимости, цену ошибки, отсутствие источников и отсутствие прогноза. Skill не «улучшает стиль». Он переписывает статус утверждения: из фразы, которая звучит убедительно, в тезис, который можно применить, проверить и пересмотреть.

Подход называется Wu-Wei не как декоративная философская метка, а как редакторский принцип: не давить языком сильнее, чем позволяет реальность. Хорошая версия тезиса должна идти по зерну фактов: меньше принуждения, меньше метафор, больше механизма, границ, источников и условий снятия.

---

## До / после

### 1) English — AI strategy thesis

**Before**

> Multi-agent systems will replace single-LLM workflows in enterprise within 18 months. The economics are inevitable and the technology is here.

**After**

> Multi-agent workflows will take budget first in enterprise processes where failure can be split into steps, reviewed, and retried: support triage, compliance review, internal research, document QA, and back-office checks.
>
> They will not replace single-call LLM workflows where latency, clear ownership, and interface simplicity matter more than delegation.
>
> Prediction: by 2027-11-01, using a fixed list of ten AI workflow vendors selected on 2026-06-01, at least three will publicly report paid enterprise usage or revenue tied specifically to multi-step agent orchestration, not only chat assistants. Confirm through vendor filings, pricing pages, customer case studies, or audited revenue commentary. Weaken this thesis if paid enterprise usage remains concentrated in single-call copilots and embedded assistants.

**Что изменилось:** снята неизбежность, добавлена область применения, названы исключения, прогноз привязан к источникам и порогу.

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

**Что изменилось:** метафора заменена механизмом: цель → шаги → инструменты → действие → данные → результат. Нет гибридного жаргона вроде `runtime`, `evidence trail`, `workflow-запуск`, `retention`, `novelty`.

### 3) 中文 — 组织判断

**改写前**

> AI 会让中层管理消失，因为协调会被模型自动化。

**改写后**

> AI 不会让中层管理作为一个类别消失。它会先压缩那些主要负责转发信息、汇总状态、追问进度的岗位。
>
> 仍然有价值的中层管理会集中在三类工作上：定义责任边界、处理跨团队冲突、为取舍和结果承担责任。
>
> 可验证预测：到 2027-12-31，在已经公开采用 AI 工作流的公司中，职位描述以状态汇总和进度追踪为主的中层岗位减少速度，应高于明确承担跨团队决策、绩效判断或风险责任的岗位。验证来源：公司招聘信息、组织公告、裁员说明、岗位说明变化。如果两类岗位以相近速度下降，本判断需要修正。

**Что изменилось:** общий вывод «менеджмент исчезнет» заменён различением ролей и проверяемым условием.

---

## Когда использовать

Используй skill, когда текст должен выдержать вопрос:

> Что я теперь сделаю иначе, и что через N дней покажет, что я ошибался?

Подходит для:

- AI/product strategy claims;
- founder / investor pitch;
- product positioning;
- research conclusions;
- architecture recommendations;
- hiring and org-design arguments;
- market theses;
- public essays and memos;
- personal operating principles, если их надо сделать проверяемыми.

Не подходит для:

- обычной корректуры;
- перевода;
- генерации идей с нуля;
- лозунгов, которые специально должны остаться лозунгами;
- юридических, медицинских или финансовых решений без профильной экспертизы и источников.

---

## Как работает skill

```text
ARTIFACT → DIAGNOSE → TEST → REWRITE → KILL → REPAIR/OBJECT → DELIVER
```

1. Находит основные утверждения.
2. Достаёт скрытую модель: почему автор думает, что это правда.
3. Убирает слова, которые давят сильнее, чем доказательства.
4. Сужает область применимости.
5. Называет, где тезис не работает.
6. Добавляет проверку во времени: метрика, источник, порог, дата, условия подтверждения/ослабления/опровержения.
7. Видимо фиксирует снятые утверждения.
8. Если тезис пока нельзя честно переписать, сначала даёт repair path, и только потом структурное возражение.

---

## Режимы вывода

По умолчанию используется `compact`, а не тяжёлая полная схема.

| Режим | Когда использовать | Что выдаёт |
|---|---|---|
| `compact` | быстрая правка, pitch, заметка | переписанная версия, граница, один прогноз, снятые claims, следующая проверка |
| `decision` | стратегия, исследование, публичный тезис, hiring/architecture/investment decision | полная схема с прогнозами, рисками обратного эффекта, снятыми утверждениями и Frame Log |
| `frame_log` | нужно сохранить тезис для будущей проверки | запись журнала рамки и kill condition |
| `critique_only` | нужно понять, что не так, без финальной переписи | диагноз, repair path, тесты, что убрать |

Старые aliases поддерживаются:

| Старое | Новое |
|---|---|
| `quick` | `compact` |
| `full` | `decision` |
| `frame_log_only` | `frame_log` |

---

## Контракт прогноза

Каждый не-спекулятивный сохранённый тезис должен иметь:

```yaml
P1:
  claim: "..."
  metric: "что наблюдаем"
  source: "где это проверить"
  threshold: "какой порог должен быть достигнут"
  check_date: "YYYY-MM-DD"
  confirmed_if: "..."
  weakened_if: "..."
  falsified_if: "..."
```

Если метрику или источник нельзя честно назвать, skill не должен выдумывать точность. Он помечает тезис как `SPECULATIVE` и предлагает план измерения.

---

## Установка

```bash
git clone https://github.com/agisota/wu-wei-skill.git
cd wu-wei-skill
bash scripts/install_all_cli.sh
bash scripts/validate.sh
```

Пакет для ручной установки:

```bash
bash scripts/package.sh
# dist/wu-wei-rewriter.skill
```

---

## Важные файлы

- `skill/SKILL.md` — entrypoint skill.
- `skill/system_prompt_v1.3.md` — основной behavioral contract.
- `skill/references/anti_slop.md` — правила против AI-slop.
- `skill/references/ru_style_guide.md` — русская языковая политика.
- `skill/references/refusal_conditions_v2.md` — repair-first objection logic.
- `skill/references/mode_matrix.md` — режимы вывода.
- `skill/evals/golden_set_ru.jsonl` — русские regression cases.
- `skill/evals/grader_prompt_v2.md` — оценщик с language integrity / anti-slop.
