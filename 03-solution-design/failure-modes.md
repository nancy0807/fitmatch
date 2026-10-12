# Failure Modes

Where this breaks, and what limits the damage.

| Failure | Root cause | Mitigation |
|---|---|---|
| Overconfident prediction from thin data | Confidence score currently based only on score gap, not sample size — 1 owned item can still read "high confidence" | Documented gap, fix planned: weight confidence by number of owned items logged |
| Heuristic doesn't generalize across body types | Ease-per-fit-rating values are hand-picked from one set of assumptions, not learned from diverse fit data | Confidence scoring exists precisely to signal uncertainty rather than force a false-authority answer |
| Brand has an unusually cut size range | v1 covers 5 brands with standard sizing; an outlier brand (oversized/boxy label) breaks the ease assumptions | Low-confidence flag surfaces this rather than silently mispredicting |
| Placeholder size-chart data used for real prediction | Early data collection hit unreliable, conflicting aggregator sources | Data explicitly labeled placeholder; verified official data is a tracked, separate task before user testing |

**Design principle carried from Pivot:** the system should always surface something honest — a low-confidence flag, a labeled placeholder warning — rather than a clean-looking answer that's silently wrong.

| Cut varies per product, not per brand | The engine treats a size label as a fixed amount of room per brand and "loose" as a fixed +6 cm. An oversized tee in size XS can fit looser than a regular M, and a stretchy slim tee can measure smaller than the body wearing it. Logging one skews the body estimate and can even raise confidence. Reported in user feedback (an oversized H&M tee). | **Partly mitigated** — owned items marked oversized or slim are set aside, not used. The cut of the product being bought adjusts the result by assumed amounts (+10 cm oversized, -4 cm slim) that are not measured; confidence is capped at medium. Not solved: unmarked items aren't detected, and the amounts need to be replaced with measured values. |
