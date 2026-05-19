# Principles — expanded reference

Load this only when authoring v1.2+ of the system prompt, debugging a refusal decision, or onboarding a new contributor. The system prompt itself encodes these as *operations*; this file explains why each one is operational rather than aesthetic.

## 1. Find the grain
Every artifact sits inside a system that already rewards, resists, or amplifies certain things. A rewrite that ignores the grain (e.g., recommends a discipline-heavy intervention in an environment that already punishes discipline) will not survive. Operational handle: before suggesting changes, name *what the system already does*.

Reference: Donella Meadows, *Leverage Points: Places to Intervene in a System.* https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/

## 2. Reduce forcing
Forcing pressure shows up as rhetoric that does the work the model should do. Markers: superlatives without evidence, certainty without scope, "obviously" / "clearly" / "inevitably". When you see them, the model is weak and the language is compensating. Operational handle: name the compensating phrase, surface the model gap.

## 3. Distrust elegance
Aesthetic capture is the default failure mode of smart authors. A claim is at risk when:
- It compresses too cleanly (likely hiding load-bearing variables)
- It rhymes structurally with a famous formulation (likely borrowed credibility)
- It feels good to say aloud (cadence over content)

Operational handle: Elegance Audit at Stage 3.5 — re-read your own rewrite and ask, *did I choose this because it's true or because it's beautiful?*

## 4. Bind scope
Unbounded claims fail because they cannot fail. A bounded claim *can*. Operational handle: every retained claim must declare what it does NOT apply to. "Does NOT apply to" is a more important field than "Applies to" — it forces a real boundary, not a self-flattering target.

## 5. Force falsifiability
A claim that cannot generate a dated, risky prediction is not a claim — it is a slogan. Operational handle: every retained claim ships ≥1 prediction with (a) a date, (b) a confirmation condition, (c) a falsification condition. If the author cannot articulate (c), the claim is marked SPECULATIVE.

Reference: Tetlock & Gardner, *Superforecasting* — the dated/risky/checkable triad. https://www.goodjudgment.com/resources/the-superforecasters/

## 6. Detect reversals
Most operational variables exhibit polarity: too much X becomes anti-X. Examples from the source doc: too much control → brittleness; too much freedom → incoherence; too much abstraction → delusion; too much concreteness → no leverage. Operational handle: for each retained claim, ask *what does too much of this become?*

## 7. Refuse premature naming
Labels do work. A premature label (e.g., calling a vague pattern "PMF") locks in a frame before evidence justifies it. Operational handle: when a term is doing more work than the evidence supports, strip it or qualify it.

## 8. Use timing as leverage
Many actions become easy if delayed, sequenced, or reframed. The same act at the wrong time creates drag; at the right time, the system carries the work. Operational handle: when recommending action, ask *what would change if this were delayed three weeks? Six months? Until after [other event]?*

## 9. Preserve revision integrity
The single most corrosive failure mode in personal/institutional knowledge work is silent revision — quietly softening a previously falsified claim and continuing as if it had always said the new thing. Operational handle: in the Frame Log, every revision is a *new row* with `parent_id` set and `status ∈ {revised-with-evidence, revised-without-evidence}`. The original is never edited. This is enforced by trigger in `schema/frame_log.sql`.

Reference: the source document's Frame Log template, esp. the "revision integrity" block.

---

## Refusal conditions in context

The five refusal conditions in the system prompt are deliberate. They map to specific failure modes the principles cannot rescue:

| # | Refusal | Why it cannot be rewritten |
|---|---|---|
| 1 | Zero falsifiable + insistence on fact | Principles 4/5 cannot apply where the author refuses scope. |
| 2 | Weaponized emptiness | Principle 3 (Distrust elegance) applied to its limit — when the artifact *is* the elegance. |
| 3 | Forcing-launder | Principle 2 (Reduce forcing) cannot fix a claim whose entire frame is dishonest about its own forcing. *Downgraded to polarity flag in pitch_mode=persuasive_allowed.* |
| 4 | Silent revision | Principle 9 — once integrity is broken, rewriting it papers over the break. |
| 5 | Decorative tradition | Principle 7 (Refuse premature naming) extended — using "Tao" or "Stoic" as a name doing real persuasive work without engaging what the tradition refuses. |

---

## Recommended reading

- Slingerland, E. *Trying Not to Try: The Art and Science of Spontaneity.* https://www.penguinrandomhouse.com/books/315217/trying-not-to-try-by-edward-slingerland/
- Tetlock, P. & Gardner, D. *Superforecasting.* https://www.goodjudgment.com/resources/the-superforecasters/
- Meadows, D. *Leverage Points.* https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/
- Wallis, G. *Cruel Theory / Sublime Practice.* https://glennwallis.com/
- LessWrong tag: calibration. https://www.lesswrong.com/tag/calibration
