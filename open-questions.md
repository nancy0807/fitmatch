# Open Questions

Unresolved, tracked honestly rather than papered over.

## The product

- Does the fit-history approach actually predict well against real users? First real test: 1 of 1 testers said yes (see `04-ethics-metrics/metrics.md`), but that ran on charts that were all invented placeholders at the time. Every tester from v8 on uses real charts.
- How many owned items does a user need to log before a prediction becomes trustworthy? The engine currently downgrades confidence below 3 same-type items.
- Does "tight / true / loose" need per-region granularity, or is one overall rating enough?
- Will the hand-tuned ease heuristic hold up across body types meaningfully different from the assumptions that shaped it?
- With exactly one owned item, the fit rating cancels out (documented in `03-solution-design/failure-modes.md`, locked in by a test).

## The data (v8)

**Settled:** brand-wide charts are body charts. Every brand-wide chart found publishes body measurements (bust or chest, waist, hip). Garment measurements only appear per product (Zara, Uniqlo "Product size" tabs, The Souled Store, Levi's India), and they vary from product to product within a brand. The data model is one body chart per brand, per gender.

**Still open:**

- **Charts can differ by product line within a brand.** Uniqlo women's basic tees give S bust 77–83; the UNIQLO:C long-sleeve line gives 83–89. The basic-tee line is stored. Max women's shows the same numbers shifted a full size between its main label and URB_N; the main label is stored. Nike's Jordan label uses a wider chart than Nike Sportswear; Sportswear is stored.
- **Single values vs ranges.** The Souled Store, Pantaloons and Red Tape publish one number per size. It's not stated whether that's a midpoint or a lower bound; they're stored as published.
- **Red Tape "Standard Size" is read as body chest/bust.** Indian brands commonly label shirts by the chest they fit, and the column is consistent across products, but the page never says so.
- **Zudio has no verifiable chart.** zudio.com was down. Women's numbers come from a third-party site (flagged "unverified"). A Google AI summary for men's was not used: it contradicts itself (L listed as both 40–42″ and 42–44″, nothing between 44″ and 46″) and can't be traced to Zudio. Men's Zudio is a placeholder averaged from the real men's charts.
- **H&M "low hip"** is stored as hip, an approximation.

**Anomalies in the published charts** (stored as published unless noted):

- M&S women's bust row lists 132 for both UK 26 and 28 while every other step, and the waist row, rises by 6. XXXL (28–30) is not stored.
- Max women's jumps from XXL to 3XL by bust +8 and waist +14 while shoulder drops; it looks like a separate plus-size block.
- H&M men's has gaps between sizes (S ends at 90, M starts at 94) and XS spans 8 cm where others span 4. M&S men's has small gaps and a 3XL/4XL overlap at 132.
- Lulu & Sky steps only 1″ from S to M (others 2–3″), and its "Body Measurement" chart includes a 12″ length that must be a garment measurement.
- The Souled Store men's Relaxed chart lists garment chest equal to body chest for XXS–L (zero room), and its Boxy chart has XL shoulder 69 above XXL's 66. Both look like data-entry errors on the brand's side; only the body column is used.
- The Souled Store men's regular-fit chart appears identical to its oversized full-sleeve chart, which is likely one popup shared across products. It's not usable as cut evidence.

## Zara: approximate by necessity

Zara publishes only "Product measurements" (flat chest, front length, sleeve, back width, arm width, per product). Its own note says chest is measured "from one side to the other at the height of the armhole". Converted as **body chest ≈ flat chest × 2 − 12 cm** (FitMatch's existing true-fit garment ease):

| Product | Flat chest S / M / L / XL / XXL | Converted | Plausible? |
|---|---|---|---|
| Women's regular-fit long-sleeve slogan tee (used) | 51 / 54 / 57 | 90 / 96 / 102 | Yes, 2–5 cm above Pantaloons and Max |
| Women's slim printed tee | 39.5 / 41 / 42.5 | 67 / 70 / 73 | No |
| Women's fitted tee | 36.5 / 37.5 / 38.5 | 61 / 63 / 65 | No |
| Women's V-neck batwing top | 47.5 / 48.5 / 49.5 / 50.5 | — | Grades 1 cm per size; not a regular cut |
| Men's relaxed fit interlock tee (used) | 51 / 54 / 57 / 60 / 63 | 90 / 96 / 102 / 108 / 114 | Yes, almost exactly Max's chart |
| Men's basic slim fit tee | 42.5 / 46.5 / 50.5 / 54.5 / 58.5 | 73 / 81 / 89 / 97 / 105 | No |
| Men's Senna long-sleeve | 51.5 / 54.5 / 57.5 / 60.5 | — | Not used |

**Finding:** slim products don't convert. Subtracting a regular tee's ease from a garment that already sits close to the body double-counts the room. It's a concrete case for why the engine never mixes garment and body charts directly.

**Open:** the relaxed tee may carry more room than a regular one, so men's Zara body sizes may read a few cm high. One consequence worth testing: a women's M wearer gets Zara **S**, because that "regular fit" tee is roomy.

## Calibrating `CUT_ROOM_CM`

The cut adjustment (oversized +10 cm, slim −4 cm) is still an assumption. Evidence so far, as garment girth minus body girth at the same size:

| Source | Cut | Room over body |
|---|---|---|
| The Souled Store women's | fitted | −7 to −8 cm |
| The Souled Store women's | regular polo | +10 to +11 cm (XXL +16) |
| The Souled Store women's | oversized | +20 to +21 cm |
| The Souled Store men's | oversized | +15 to +16 cm |
| The Souled Store men's | boxy | +17 to +19 cm |
| Red Tape women's tee (unlabelled, boxy) | — | +20.3 cm |
| Red Tape men's polo | regular | +2.5 to +6.4 cm, uneven |
| Uniqlo men's | oversized vs regular tee | about +3 cm between them |
| Zara men's (M) | relaxed vs slim | 54 vs 46.5 flat, about +15 cm round |

- **Oversized vs regular:** within The Souled Store women's it's about +10 to +11, matching the current +10. Uniqlo's is about +3. The right value varies by brand, so +10 stays as an assumption.
- **Slim vs regular:** The Souled Store's fitted tee vs its polo suggests about −17, far from −4, but a cropped stretch tee isn't comparable to a polo. Uniqlo's ribbed tee sits 2–5 cm under body size, which supports a small negative number. −4 stays.
- **Men's regular:** still no clean within-brand comparison of men's regular vs oversized.

## Open questions about the product cut options

- FitMatch offers regular, oversized and slim. Brands also sell "boxy" (maps cleanly to oversized) and "relaxed" (ambiguous: between regular and oversized). For now the user picks whichever they think fits.
