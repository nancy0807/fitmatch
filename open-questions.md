# Open Questions

Unresolved, tracked honestly rather than papered over.

- Does the fit-history approach actually predict well against real users, or does accuracy collapse outside the 5 seeded brands?
- How many owned items does a user need to log before a prediction becomes trustworthy — and does the product need to enforce a minimum before it'll predict at all?
- Does "tight / true / loose" need per-region granularity to be useful, or is a single overall rating enough?
- Will the hand-tuned ease heuristic hold up across body types meaningfully different from whatever assumptions shaped it?
- At what point does this need real brand size-chart data instead of placeholder data to produce a credible demo?

- **Found while attempting to answer the above:** most brands don't publish one size chart per brand at all — measurements are given per product/style (confirmed even on Uniqlo's official help pages), since cut varies style to style. The current data model assumes one chart per brand. Does that need to change to one representative chart per (brand, garment type), or is a single "flagship tee" reference per brand an acceptable simplification — and if so, how should that assumption be surfaced to the user so a prediction doesn't look more precise than it is?
