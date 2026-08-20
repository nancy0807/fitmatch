# Decision Log

Every real decision point: what was decided, the evidence behind it, and what was rejected.

---

**Started from problem discovery, not a predefined product.** Ruled out picking a solution category up front — generic AI dashboards, chatbots, recommendation engines. Picking a solution before comparing problems tends to produce the first idea considered, not the best available one.

---

**Ran a compressed discovery process, not an extended observation period.** Open-ended journaling risked becoming procrastination against a real application timeline. Substituted active complaint-hunting — forum search, direct conversations — for passive observation.

---

**Killed the wardrobe/styling app direction.** Competitive audit showed the category is already crowded — 10+ named competitors, complaints about execution quality, not an open gap. See `01-problem-research/competitor-audit.md`.

---

**Selected cross-brand sizing.** Stronger evidence profile: severity (return-rate and cost data) plus a decade of well-funded attempts that still haven't closed the gap. A better "why hasn't this been solved" answer than the wardrobe direction had.

---

**Scoped MVP to one category, 5-8 brands, manual fit input.** The goal of v1 is validating whether the matching logic works at all, not maximizing coverage. Rejected starting with jeans — harder fit geometry would have confounded testing the core mechanism with testing a harder measurement problem.

---

**Used labeled placeholder size-chart data instead of scraped aggregator data.** Initial research for real brand size charts returned conflicting numbers across third-party sites. Hardcoding unverified data as accurate would have silently corrupted the matching logic. Chose to build and validate against clearly-labeled placeholder data, with verified collection as a separate tracked task.

---

**v1 matching engine uses a hand-tuned heuristic, not a learned model.** No aggregate user data exists yet to learn from. Documented the v2 upgrade path rather than presenting the heuristic as more sophisticated than it is.

---

**Corrected two unverified statistics after initial drafting.** An early draft cited "$94B in 2019" and an "8-15 hour wardrobe cataloging" figure that could not be re-verified against primary sources on follow-up. Removed and replaced with numbers confirmed directly against Coresight Research's and McKinsey's primary reports. Flagged here deliberately — catching an unverified claim before it ships is part of the process, not a footnote to hide.
