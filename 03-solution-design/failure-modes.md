# Failure Modes

Where this breaks, and what limits the damage.

| Failure | Root cause | Mitigation |
|---|---|---|
| Overconfident prediction from thin data | Confidence score currently based only on score gap, not sample size — 1 owned item can still read "high confidence" | Documented gap, fix planned: weight confidence by number of owned items logged |
| Heuristic doesn't generalize across body types | Ease-per-fit-rating values are hand-picked from one set of assumptions, not learned from diverse fit data | Confidence scoring exists precisely to signal uncertainty rather than force a false-authority answer |
| Brand has an unusually cut size range | v1 covers 5 brands with standard sizing; an outlier brand (oversized/boxy label) breaks the ease assumptions | Low-confidence flag surfaces this rather than silently mispredicting |
| Placeholder size-chart data used for real prediction | Early data collection hit unreliable, conflicting aggregator sources | Data explicitly labeled placeholder; verified official data is a tracked, separate task before user testing |

**Design principle carried from Pivot:** the system should always surface something honest — a low-confidence flag, a labeled placeholder warning — rather than a clean-looking answer that's silently wrong.
