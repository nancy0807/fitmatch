# Decision Log

Each entry: the decision, the evidence behind it, and what was rejected.

---

**Decision: Started from problem discovery, not a predefined product**
Rejected the default of picking a product category up front (explicitly ruled out generic patterns like AI dashboards/chatbots/recommendation engines as starting points). Reasoning: picking a solution before comparing problems tends to produce the first idea considered, not the best available one.

---

**Decision: Ran a compressed discovery process instead of an extended observation period**
Reasoning: open-ended journaling risked becoming procrastination against a real application timeline. Substituted active complaint-hunting (forum search + direct conversations) for passive observation, on the theory that hunting for evidence beats waiting for it to happen.

---

**Decision: Killed the wardrobe/styling app direction**
Evidence: competitive analysis showed the AI wardrobe app space is already crowded (10+ named competitors), and complaints in that space were about execution quality, not an open gap. See `competitive-analysis.md`.
Rejected alternative: proceeding anyway on the basis that a differentiated angle (purchase-decision support vs. styling) might carve out space — considered, but the stronger opportunity in cross-brand sizing made this not worth pursuing in parallel given the timeline.

---

**Decision: Selected cross-brand sizing as the problem to build against**
Evidence: severity (return rates, cost data) plus a decade of unsolved attempts despite real investment — a stronger "why hasn't this been solved" answer than the wardrobe direction. See `competitive-analysis.md`.

---

**Decision: Scoped MVP to one category (women's tops), 5-8 brands, manual fit input**
Reasoning: the goal of v1 is to validate whether the *matching logic* works at all, not to maximize coverage. Expanding scope before validating the core mechanism multiplies cost without testing the riskiest assumption.
Rejected alternative: starting with jeans (more complex fit geometry, would have confounded testing the core logic with testing a harder measurement problem).

---

**Decision: Used labeled placeholder size-chart data instead of scraped aggregator data**
Evidence: initial web research for real brand size charts (e.g. H&M) returned inconsistent numbers across third-party aggregator sites — conflicting size ranges for the same brand.
Reasoning: hardcoding unverified data as if accurate would silently corrupt the matching logic and produce misleading test results later. Chose to build and validate the logic against clearly-labeled placeholder data, with verified official data collection as an explicit separate task, rather than either stalling on data collection or shipping unverified data unlabeled.

---

**Decision: v1 matching engine uses a hand-tuned heuristic (fixed ease-cm per fit rating), not a learned model**
Reasoning: no aggregate user data exists yet to learn from. Documented the v2 upgrade path (learning ease assumptions from real fit outcomes) rather than presenting the heuristic as more sophisticated than it is.
