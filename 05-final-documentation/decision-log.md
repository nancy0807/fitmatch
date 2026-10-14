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

---

**Replaced invented size charts with real ones, transcribed from each brand's own size-guide popup (v8).** Search couldn't reach the popups, so each chart came from a screenshot, transcribed and stored as range midpoints, with its source and any quirks in its `_source` note. 23 of 27 charts are now from published size guides. Where two charts from one brand disagreed (Max women's, Lulu & Sky), the main label or the explicitly labelled body chart was chosen and the other logged in `open-questions.md`.

---

**Kept an AI-generated chart out of the data.** With Zudio's site down, a Google AI summary offered a men's chart. It contradicted itself and couldn't be traced to Zudio, so men's Zudio stays a labelled placeholder. A traceable gap beats an untraceable number.

---

**Removed Roadster and HRX** instead of keeping invented numbers for them.

---

**Converted Zara's garment chart to approximate body sizes, rather than leaving it isolated.** Zara publishes only per-product garment measurements, which the engine can't compare with body charts. Considered: leave it isolated (honest, but unreachable), or convert with the engine's own true-fit ease. Chose to convert, with confidence capped at medium and a visible note naming the product. Slim products gave impossible results, so a regular (women's) and relaxed (men's) product were used.

---

**Read Red Tape's "Standard Size" as body chest.** The page doesn't say what the column measures, but it's consistent across products and Indian brands commonly label shirts by the chest they fit. Recorded as an interpretation in the chart's source note.

---

**Normalised scores by the weight actually used.** Charts now differ in how many measurements they publish (chest only, up to chest/waist/hip). Summing weighted differences made one-measurement charts look twice as good; dividing by the weight used makes them comparable. Full charts score exactly as before.

