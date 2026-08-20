# AI Ethics & Responsible Design

*Written to address the specific risks in FitMatch's actual mechanism — not a generic AI-ethics checklist.*

## Risk 1: Overconfident predictions from thin data

**The risk:** A user who logs only 1-2 owned items still gets a predicted size and a confidence label. If the confidence-scoring logic doesn't account for *how little data* the estimate is based on, a "high confidence" label could be shown when it shouldn't be trusted — actively worse than no prediction, since it invites false trust.

**Current state:** v1's `predict_size()` confidence is based purely on the score gap between the top and second-best size, not on how many owned items informed the estimate. This is a real gap, documented here rather than hidden.

**What should change before this is used for real decisions:** confidence should factor in sample size (e.g. 1 owned item should never produce "high confidence," regardless of how clean the score gap looks) — flagged as a concrete fix for `matching.py`, not just a paragraph in this doc.

## Risk 2: The heuristic encodes assumptions that may not hold for everyone

**The risk:** The `EASE_CM` values (how much "ease" tight/true/loose implies) were hand-picked, not derived from real fit data across diverse body types. A heuristic tuned by one person's intuition risks generalizing poorly — for example, ease preferences may differ systematically by body shape, height, or garment style in ways a single fixed constant per fit-rating can't capture.

**Why this matters ethically, not just technically:** if the tool works well for people who resemble whoever's assumptions shaped the heuristic and poorly for others, it's not neutral — it's quietly biased toward a "default" body type. This is exactly the kind of failure mode that's easy to miss because the tool still *looks* like it's working (it always returns *a* size).

**Mitigation for v1:** confidence scoring exists precisely so the tool can signal "less sure" rather than silently failing — the point of showing the score breakdown (see `design.md`) is transparency over false authority.

## Risk 3: Data the user provides is personal (body-adjacent) information

**The risk:** Fit history is a proxy for body shape and size — sensitive personal information even though it's expressed as "brand/size/fit rating" rather than raw measurements.

**Current state:** v1 has no accounts, no persistence, no data storage beyond a single session — this actually sidesteps most of the risk by design, not as an afterthought. If accounts/persistence are added later (see `architecture.md` roadmap), this becomes a real requirement, not an optional nice-to-have: clear consent, no third-party data sharing, and a stated retention/deletion policy.

## What This Section Is Not

This isn't a claim that FitMatch is "ethically solved" — it's an honest accounting of where the current design is fragile, written before those fragilities cause a real problem rather than after. That ordering is the actual point of doing this at MVP stage instead of skipping it until v2.
