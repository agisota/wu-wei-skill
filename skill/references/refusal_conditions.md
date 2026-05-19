# Refusal conditions — worked examples

Each refusal condition has a positive and a negative example. The agent's job is to distinguish "looks like a refusal but isn't" from "looks rewritable but isn't". Pattern-match generously on these.

---

## #1 — Zero falsifiable content + insistence on fact

**Refuse:**
> "This is the future. AI agents will change everything. Trust me."

Nothing to scope, nothing to falsify, and the framing rejects the request to constrain. Return STRUCTURAL OBJECTION.

**Rewrite (don't refuse):**
> "AI agents will change how knowledge workers spend their first hour each morning."

Vague but bounded enough to rewrite. Push the author for a metric (time-allocation studies, calendar data) and ship a dated prediction.

**Cue distinguishing the two:** does the artifact contain *any* noun that could be measured? "Everything" cannot. "Knowledge workers' first hour" can.

---

## #2 — Weaponized emptiness

**Refuse:**
> "The only moat in the age of AI is taste."

Sounds profound. Operationally: what is "taste"? Who has it? How would you measure a moat made of it? The phrase is doing persuasive work on borrowed credibility (Steve Jobs / a16z aesthetic) without any falsifiable substrate.

**Refuse:**
> "Build with the grain of the system. Don't push. Let the work do itself."

Tao-flavored prose with no operational handle. (Also triggers #5 if the author is in fact reaching for "Taoism" as the source of authority.)

**Rewrite (don't refuse):**
> "We win on aesthetic judgment — specifically, our designers reject 40% more concepts than the industry average and we ship 30% fewer features."

Still about "taste" but now has measurements and a decision rule. Rewritable.

**Cue:** can you replace the key noun with its opposite and still have the sentence sound true? "The only moat is bad taste" reads almost as plausible — that's the tell.

---

## #3 — Forcing-launder

**Refuse (in strict mode):**
> "We don't push our users. We just remove every friction point until upgrading is the path of least resistance and the cancel button is three menus deep."

The first sentence claims non-forcing; the second sentence describes forcing. The artifact lies about its own posture.

**Downgrade to POLARITY FLAG (in pitch_mode=persuasive_allowed):**
Same input. In pitch mode the agent doesn't refuse; it flags under "Forcing pressure (allowed in pitch_mode)" so the founder knows what they're doing while writing it.

**Rewrite (don't refuse, either mode):**
> "We use both pull (clear free-tier value) and push (upgrade prompts at high-affinity moments). Below is the ratio."

Honest about the mix. Rewritable.

**Cue:** does the artifact use Taoist/wu-wei/"natural"/"organic" language to describe what is operationally a high-pressure design?

---

## #4 — Silent revision

**Refuse:**
> "I always thought CBDCs would lose to stablecoins on programmability grounds."

If `prior_versions` contains an artifact from 18 months ago where the author claimed CBDCs would win on programmability grounds, this is silent revision. Refuse and demand a revision tag (`revised-with-evidence` if pointing to new data, `revised-without-evidence` otherwise).

**Rewrite:**
> "I previously argued CBDCs would win on programmability. After [recent BIS paper / failed pilot / etc.], I now think the opposite. Here's why:"

Acknowledges the revision. The author can ship this; the Frame Log entry will mark `status: revised-with-evidence`.

**Cue:** compare to `prior_versions[]` when provided. If the new claim contradicts a prior one and there is no acknowledgment, refuse.

---

## #5 — Decorative tradition

**Refuse:**
> "Our team operates on Stoic principles: virtue, agency, role-duty. Combined with Zen non-attachment and Taoist wu-wei, we have a complete operating system for high-performance work."

Three traditions used as flavor. None engaged with what the tradition *refuses*. Stoicism refuses to locate the good outside one's own judgments; Zen refuses to take conceptual structures as final; Taoism refuses to force. The artifact ignores all of these.

**Refuse:**
> "Wu wei is the perfect philosophy for AI agent design."

Same problem at smaller scale. The author has not engaged with the difference between wu-wei as embodied practice and wu-wei as borrowed adjective.

**Rewrite (don't refuse):**
> "Our review process borrows from Stoic prohairesis — the team explicitly distinguishes outcomes from judgments-about-outcomes during retros. We do not adopt Stoicism wholesale; this one transfer is what we found useful."

Names what's borrowed, what's not, and why. Rewritable.

**Cue:** does the artifact engage with what the tradition refuses, or only with what it offers?

---

## Edge cases

### "Looks like #2 but isn't" — domain-specific shorthand

> "We optimize for D7 retention."

This sounds vague but in a product-domain context, D7 is a well-defined metric. Not weaponized emptiness. Rewrite.

### "Looks like #3 but isn't" — pitch in strict mode

> "Our product wins by being the path of least resistance."

A pitch claim. In `pitch_mode=persuasive_allowed`, this is fine — note as polarity flag, predict on path-length metric. In strict mode, only refuse if the claim explicitly denies its own forcing posture. "Path of least resistance" is description, not denial.

### "Looks rewritable but should be refused" — fake quantification

> "There's a 73.4% chance this strategy works."

A number this precise without methodology is weaponized emptiness wearing a number's clothes. Refuse under #2 unless the author can produce the methodology.
