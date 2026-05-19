# ru_style_guide.md — Russian style guide for Wu-Wei output

This guide exists to prevent Russian Wu-Wei output from becoming translated AI-startup prose.

The target style:

```text
спокойный, проверяемый, деловой русский;
конкретные существительные;
короткие причинные связи;
без гибридного англо-жаргона;
без “магического” продуктового языка.
```

---

## 1. Core rule

Do not make Russian output sound “more advanced” by borrowing English terms.

Use English only when it is:

- a product name;
- a model name;
- an API or code symbol;
- a fixed technical standard;
- a term from the user’s own artifact;
- an explicit user preference.

Otherwise translate the operational meaning.

---

## 2. Forbidden / risky phrases

| Avoid | Why it fails | Prefer |
|---|---|---|
| `runtime` | often hides the actual tool layer | среда выполнения / набор инструментов / исполняющий слой |
| `evidence trail` | sounds precise but vague in Russian | журнал действий / след действий / сохранённые данные проверки |
| `workflow-запуск` | hybrid slop | запуск сценария / повторный сценарий |
| `retention` | okay only as product metric; otherwise lazy | возврат пользователей / удержание пользователей |
| `novelty` | unnecessary borrowing | эффект новизны / демо-эффект |
| `frame надо убить` | theatrical and unnatural | тезис надо снять / позиционирование надо пересмотреть |
| `decision-grade` | slogan-like | пригодный для решения |
| `agentic` / `агентный` | often hides mechanism | самостоятельное выполнение шагов системой, if that is what is meant |
| “новый язык взаимодействия” | decorative unless operationalized | новый способ выполнить X, with concrete mechanism |
| “операционная система мышления” | over-claim | система, которая превращает цель в проверенное действие |
| “ров” as `moat` | acceptable only in strategic context | защитный механизм / устойчивое преимущество |

---

## 3. Preferred sentence shapes

### Mechanism first

```text
Пользователь делает X. Система делает Y. Результат можно проверить через Z.
```

### Boundary first

```text
Тезис работает для A и B. Он слаб для C, потому что там важнее D.
```

### Prediction contract

```text
Проверка: к YYYY-MM-DD метрика M в источнике S должна превысить порог T.
Тезис ослабнет, если ...
Тезис опровергнется, если ...
```

### Killed claim

```text
Убрано: «...». Причина: фраза расширяет область до всех случаев, но доказательства есть только для одного сегмента.
```

---

## 4. Examples

### Product pitch

Weak:

> Продукт снижает стоимость перехода от размытой цели к проверяемому агентному действию через runtime и evidence trail.

Better:

> Продукт сокращает путь от цели к проверенному действию. Пользователь описывает задачу, система разбивает её на шаги, выполняет их через подключённые инструменты и показывает, что было сделано, на каких данных и с каким результатом.

### Market thesis

Weak:

> Рынок структурно движется к консолидации вокруг двух AI-native winners.

Better:

> Рынок может сузиться до двух-трёх крупных поставщиков в сегменте корпоративных внедрений, если покупатели начнут выбирать по безопасности, интеграциям и стоимости сопровождения, а не по качеству демо.

### Hiring

Weak:

> Нанимайте людей с агентным мышлением и высокой slope.

Better:

> Для ролей с быстро меняющимися инструментами оценивайте скорость обучения через недавний рабочий пример: кандидат выбрал новый инструмент, применил его к задаче, объяснил ошибку и изменил подход.

### Personal system

Weak:

> Дефолтный дизайн побеждает дисциплину, если ты живёшь в правильном environment.

Better:

> Поведение легче менять через среду, чем через силу воли. Например: телефон вне спальни, готовый список задач на утро, заблокированные уведомления до первого рабочего блока.

---

## 5. Allowed terms

Some borrowed terms are acceptable when the user is clearly in a technical or product context:

| Term | Allowed when |
|---|---|
| API | actual API, not metaphor |
| LLM | technical discussion of models |
| SaaS | market/category discussion |
| CRM | product category |
| SQL / JSONL / YAML | schema or implementation |
| retention | product metric and the audience expects analytics language |
| workflow | only if discussing named tools that use that word; otherwise translate |

---

## 6. Final Russian self-check

Before emitting Russian output, ask:

1. Would a competent Russian founder say this in a memo?
2. Did I import English because it was necessary or because it sounded modern?
3. Can every abstract noun point to a user action, system action, metric, or source?
4. Did I write “агентный” where I could have said what the system actually does?
5. Did I translate the idea or merely transliterate the jargon?
