# mode_matrix.md — Output-mode design for Wu-Wei Rewriter

Default mode: `compact`.

The mode controls how much structure the skill emits. It should not control honesty. Even compact output must kill weak claims and include a real check.

---

## 1. Mode selection table

| Mode | Use when | Do not use when | Must include |
|---|---|---|---|
| `compact` | fast rewrite, pitch cleanup, note sharpening, chat response | high-stakes decision, public thesis, research conclusion | rewrite, boundary, one prediction, killed/weak claims, next check |
| `decision` | strategy memo, hiring policy, investment thesis, architecture recommendation, public claim | user explicitly asks for short answer | full boundary, predictions, polarity, killed claims, elegance audit, frame log |
| `frame_log` | user wants a durable record for later review | user wants a rewrite or critique | frame entry, review dates, kill condition, revision integrity |
| `critique_only` | user asks “what’s wrong?”, “where is the slop?”, “stress-test this” | user asks for shippable rewrite | diagnosis, forcing pressure, repair path, tests, what to remove |

Aliases:

| Old mode | New mode |
|---|---|
| `quick` | `compact` |
| `full` | `decision` |
| `frame_log_only` | `frame_log` |

Context presets:

| Preset | Settings |
|---|---|
| `pitch` | `pitch_mode=persuasive_allowed`, `creative_mode=ship`, `output_mode=compact` |
| `research` | `pitch_mode=strict`, `creative_mode=ship`, `output_mode=decision` |
| `early_concept` | `pitch_mode=persuasive_allowed`, `creative_mode=explore`, `output_mode=critique_only` or `compact` |
| `public_essay` | `pitch_mode=strict`, `creative_mode=ship`, `output_mode=decision` |
| `personal_note` | `pitch_mode=strict`, `creative_mode=explore`, `output_mode=compact` |

---

## 2. Mode decision logic

```text
if user asks to log / review later:
    output_mode = frame_log
elif user asks what's wrong / diagnose / stress-test only:
    output_mode = critique_only
elif intended_use in [decision_input, public_essay, research, hiring_policy, architecture_recommendation]:
    output_mode = decision
else:
    output_mode = compact
```

If the user explicitly asks for `full`, map to `decision`.
If the user explicitly asks for `quick`, map to `compact`.

---

## 3. `compact` schema

Russian default:

```markdown
## Переписанная версия
...

## Граница
- Работает для:
- Не работает для:
- Где может сломаться:

## Проверка
P1:
- метрика:
- источник:
- порог:
- дата проверки:
- подтвердится, если:
- ослабнет, если:
- опровергнется, если:

## Убрано или ослаблено
- ...

## Следующая проверка
...
```

Example:

```markdown
## Переписанная версия
Мы не продаём «новый язык мышления». Мы продаём более короткий путь от цели к проверенному действию: пользователь описывает задачу, система выполняет шаги через подключённые инструменты и показывает результат.

## Граница
- Работает для: повторяемых задач с несколькими источниками данных.
- Не работает для: одноразовых вопросов в чат.
- Где может сломаться: если пользователю всё равно приходится вручную проверять каждый шаг.

## Проверка
P1:
- метрика: доля активированных пользователей с повторным запуском сохранённого сценария
- источник: продуктовая аналитика
- порог: минимум на 20% выше повторного одноразового чата
- дата проверки: через 90 дней после запуска
- подтвердится, если: порог достигнут в новой когорте
- ослабнет, если: возврат есть только в первой неделе
- опровергнется, если: сохранённые сценарии не запускаются повторно

## Убрано или ослаблено
- «операционная система мышления» — метафора не объясняет механизм.
```

---

## 4. `decision` schema

Use when the artifact can influence resource allocation, hiring, public reputation, product direction, or strategic commitment.

Must include:

- rewrite;
- boundary;
- 1–3 predictions with full contract;
- polarity notes;
- killed claims;
- elegance audit;
- frame log entry.

Use this mode when missing a later review would be costly.

---

## 5. `frame_log` schema

Use when the user wants to preserve a thesis for future accountability.

```yaml
name:
date:
domain:
intended_use:
artifact_type:
claim:
metric:
source:
threshold:
review_at:
kill_condition:
revision_integrity:
prior_versions_preserved:
retroactive_softening_detected:
status:
revision_reason:
```

Example kill condition:

```text
Kill if by 2027-11-01 fewer than two vendors from the fixed set show paid enterprise usage tied to multi-step orchestration.
```

---

## 6. `critique_only` schema

Use when the user wants diagnosis before rewrite.

```markdown
## Диагноз

## Сильная часть

## Где пустота

## Что надо убить

## Что надо измерить

## Минимальная ремонтная версия

## Следующий тест
```

Example:

```markdown
## Диагноз
Тезис пытается сказать, что продукт превращает цель в действие. Но формулировка «операционная система мышления» расширяет claim до философского уровня и не даёт проверить ценность.

## Минимальная ремонтная версия
Продукт полезен, если пользователь чаще возвращается к сохранённым сценариям с результатом, чем к одноразовым чатам.
```

---

## 7. Mode-level anti-slop rule

A mode fails if it creates the wrong amount of structure:

- `compact` fails when it omits the check or killed claims.
- `decision` fails when it fills sections with generic content.
- `frame_log` fails when kill condition is not checkable.
- `critique_only` fails when it criticizes without repair path.
