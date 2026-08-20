# Ethics

Three concerns, examined honestly — not defensively.

- **Overconfidence from thin data.** A user with 1-2 logged items can still receive a "high confidence" label under v1's current logic. That's worse than no prediction — it invites trust the data doesn't support. Design obligation: confidence must reflect sample size, not just score separation. Tracked as an open fix, not hidden as a footnote.

- **A heuristic tuned by one person's intuition.** The ease-per-fit-rating constants were hand-picked, not learned from diverse fit data across body types. If the tool works better for people who happen to resemble whoever's assumptions shaped it, it's not neutral — it's quietly biased toward a default body type, and the failure is easy to miss because the tool always returns *a* size. Mitigation: the confidence score exists specifically to say "less sure" rather than assert false authority.

- **Fit history is body-adjacent personal data.** Brand/size/fit-rating triples are a proxy for body shape, even though they're not raw measurements. v1 sidesteps most of this risk by design — no accounts, no persistence, nothing stored past a single session. If accounts are added later, consent and a stated retention/deletion policy become a requirement, not a nice-to-have.

**What this section is not:** a claim that FitMatch is ethically solved. It's an honest account of where the design is fragile, written before those fragilities cause a real problem — not after.
