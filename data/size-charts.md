# FitMatch size-chart data (v8)

Every brand's size chart, where each number came from, and how it was stored. Generated from [`size_charts.json`](size_charts.json); every value below matches it exactly.

- **Every stored measurement** with the published value it came from: [`size-chart-measurements.csv`](size-chart-measurements.csv) (414 rows; GitHub shows it as a searchable table).
- **How charts were collected:** each number was transcribed from a screenshot of the brand's own size-guide popup, then stored as a range midpoint (or as published, for single values).

## Summary

| Status | Women's | Men's | Total | Meaning |
|---|---|---|---|---|
| Sourced | 12 | 11 | 23 | From a published size guide (the brand's own, or Levi's via retailer copies of its US chart) |
| Approximate | 1 | 1 | 2 | Converted from one product's garment chart (flat chest × 2 − 12 cm); confidence capped at medium in the app |
| Unverified | 1 | 0 | 1 | From a third-party site that can't be checked against the brand |
| Placeholder | 0 | 1 | 1 | Invented: the average of the real men's charts; labelled in the app |
| **Total** | **14** | **13** | **27** | |

Roadster and HRX were removed in v8 rather than kept as invented numbers.

## Women's brands

| Brand | Status | Sizes | Measurements |
|---|---|---|---|
| Adidas | Sourced | XXS–4XL | bust, waist, hip |
| H&M | Sourced | XXS–4XL | bust, waist, hip |
| Levi's | Sourced | XXS–3XL | bust, waist, hip |
| Lulu & Sky | Sourced | S–XL | bust, waist |
| Marks & Spencer | Sourced | XS–XXL | bust, waist |
| Max | Sourced | XS–4XL | bust, waist |
| Nike | Sourced | XS–XXL | bust, waist, hip |
| Pantaloons | Sourced | XS–XXL | bust, waist, hip |
| Red Tape | Sourced | XS–XL | bust |
| The Souled Store | Sourced | XXS–XXL | bust |
| Uniqlo | Sourced | S–3XL | bust, waist, hip |
| Westside | Sourced | XXS–XXL | bust, waist, hip |
| Zara | Approximate | S–L | bust |
| Zudio | Unverified | XS–XXL | bust, waist, hip |

### Women's bust by size (cm)

Read across to compare brands: a higher number at the same size means the brand runs larger.

| Brand | XXS | XS | S | M | L | XL | XXL | 3XL | 4XL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Adidas | 74.5 | 79.5 | 85.5 | 91.5 | 98 | 105.5 | 114 | 128.5 | 138.5 |
| H&M | 76 | 80 | 86 | 94 | 102.5 | 113 | 125 | 137 | 149 |
| Levi's | 78.7 | 83.8 | 88.9 | 94 | 100.3 | 108 | 115.6 | 130.8 |  |
| Lulu & Sky |  |  | 78.74 | 81.28 | 88.9 | 93.98 |  |  |  |
| Marks & Spencer |  | 78 | 84.5 | 94.5 | 105.25 | 117 | 129 |  |  |
| Max |  | 81.3 | 86.4 | 91.4 | 96.5 | 102 | 107 | 115 | 121 |
| Nike |  | 78.75 | 83.2 | 87 | 92.05 | 98.4 | 104.8 |  |  |
| Pantaloons |  | 83.82 | 88.9 | 93.98 | 99.06 | 105.41 | 113.03 |  |  |
| Red Tape |  | 81.28 | 86.36 | 91.44 | 96.52 | 101.6 |  |  |  |
| The Souled Store | 76 | 81 | 86 | 91 | 97 | 101 | 106 |  |  |
| Uniqlo |  |  | 80 | 84 | 88 | 94 | 100 | 106 |  |
| Westside | 77 | 82 | 87 | 92 | 97 | 102 | 107 |  |  |
| Zara |  |  | 90 | 96 | 102 |  |  |  |  |
| Zudio |  | 81.3 | 86.4 | 91.4 | 96.5 | 101.6 | 106.7 |  |  |

### Women's sources

- **Adidas** — adidas size-guide popup (women's tops, standard sizes; screenshot supplied by the user): bust, waist and hip in cm ranges, stored as range midpoints. Standard sizes only (no Tall/Petite/Plus). Size labels 2XS..2XL stored as XXS..XXL. Plus sizes: adidas 'Plus size' table 3X and 4X stored as 3XL and 4XL (1X and 2X not stored: they overlap standard XL/XXL).
- **H&M** — H&M size-guide popup, women's Regular tab (chest / waist / low hip, cm ranges; screenshot supplied by the user). Stored as range midpoints. 'Low hip' stored as hip, which is an approximation. Maternity tab not used. The page advises going down a size for its oversized tee.
- **Levi's** — Levi's US women's tops & outerwear chart as reproduced by retailers (hibbett.com, scheels.com); inches converted to cm. Not taken from levi.com directly. The two retailers disagree on size L waist/hip (scheels shows the M values); hibbett's internally consistent values are used. Not yet checked against Levi's India. Plus: the 3X row stored as 3XL (1X and 2X not stored: they overlap standard XL/XXL). No 4X on this chart.
- **Lulu & Sky** — Lulu & Sky size guide labelled 'Body Measurement (inches)' (screenshot supplied by the user); converted to cm. Two quirks: S to M steps only 1 inch (others 2-3), and its 'length' column (12-13 in) is a garment measurement, probably of a crop top, so it is not used. A second Lulu & Sky chart (M-2XL, with sleeve and hem width) is a per-product garment chart and is not used.
- **Marks & Spencer** — M&S India women's Tops size guide (UK sizes 6-30, body bust and waist in cm; screenshot supplied by the user). Converted to letters with M&S's own dual-size row (XS=6, S=8-10, M=12-14, L=16-18, XL=20-22, XXL=24-26) by averaging each pair. The dual-size row is stated to be for jerseys and knitted dresses. XXXL (28-30) NOT stored: the published bust row lists 132 for both 26 and 28, while every other step (and the waist row) rises by 6, so the top of the bust row looks shifted. No hip on this chart.
- **Max** — Max (maxfashion.in) women's chart from the Metallic printed product, 'Above size chart is for body measurements' (cm; screenshot supplied by the user). 5XL and 6XL are published but not stored (beyond 4XL). The step from XXL to 3XL is uneven (bust +8, waist +14, shoulder actually drops), which looks like a separate plus-size block. A second Max product (URB_N oversized) shows the same numbers shifted one size smaller; the main Max label was chosen. Chest column stored as bust; shoulder not used.
- **Nike** — nike.in size guide, 'body measurements this product fits' (screenshots supplied by the user). Identical on the Sportswear Slim Mod-Cropped tee and the Sportswear regular tee, so treated as Nike's women's chart. Stored as range midpoints; '2XL' stored as XXL. The Jordan oversized tee shows a different, wider chart (Jordan label) and is not used.
- **Pantaloons** — Pantaloons size-chart popups, 'All measurements are body measurements' (cm; screenshots supplied by the user). Identical on the Annabelle top and the SF Jeans oversized tee; the user checked other products and found the same chart. Single values (inch sizes converted), not ranges. Shoulder is published but not used. '2XL' stored as XXL.
- **Red Tape** — Red Tape size-chart popup on a women's tee (screenshot supplied by the user). The 'Standard Size' column (32-40 in) is read as body bust; the page does not say so, but the user confirmed the column is the same across products. Garment columns (chest all round, shoulder, length) not used.
- **The Souled Store** — The Souled Store size charts, 'To fit your bust size' column (cm; screenshots supplied by the user). The column is identical on the women's fitted, oversized and polo charts, so it is treated as the brand's body chart. Single values, not ranges; the page doesn't say whether each is a midpoint or a lower bound. Garment columns not used here.
- **Uniqlo** — Uniqlo India body-size chart for the basic tee line (bust / waist / hip, cm ranges; screenshot supplied by the user). Stored as range midpoints. Uniqlo's body chart differs by product line: the UNIQLO:C long-sleeve line runs about 6 cm larger in bust (S 83-89), so this is one line's chart, not the only one.
- **Westside** — Westside size-guide popup on a women's product page (INDIA row, body measurements in cm; screenshot supplied by the user). Replaces numbers stored earlier from a different Westside page, which were bust +1, waist +3 (XS and up), hip +2 higher and had no XXL. Which page is current is not known; this popup is what a shopper sees at the size selector.
- **Zara** — APPROXIMATE — Zara publishes only garment measurements. Converted from the flat chest of one product (women's regular-fit long-sleeve slogan tee, ref 0085/139/250; zara.com/in Product measurements popup, screenshot supplied by the user) as body bust = flat chest x 2 - 12 cm. The 12 cm is FitMatch's existing true-fit garment chest ease (6 cm flat), not a measurement. Slim products were tried and give impossible body sizes, so a non-slim product is used. Confidence is capped at medium and a note is shown.
- **Zudio** — NOT VERIFIED — from zudioonlinestore.com, a third-party site (not zudio.com). Published in inches as single values; converted to cm. Numbers follow a uniform +2 pattern per size, so treat as indicative only. Replaces the earlier invented garment_flat placeholder.

## Men's brands

| Brand | Status | Sizes | Measurements |
|---|---|---|---|
| Adidas | Sourced | XS–3XL | chest, waist, hip |
| H&M | Sourced | XXS–3XL | chest, waist |
| Levi's | Sourced | XS–3XL | chest, waist, hip |
| Marks & Spencer | Sourced | XS–4XL | chest |
| Max | Sourced | XS–XXL | chest, waist |
| Nike | Sourced | XXS–4XL | chest, waist, hip |
| Pantaloons | Sourced | XS–XL | chest, waist, hip |
| Red Tape | Sourced | S–XXL | chest |
| The Souled Store | Sourced | XXS–3XL | chest |
| Uniqlo | Sourced | S–3XL | chest, waist |
| Westside | Sourced | XS–3XL | chest, waist, hip |
| Zara | Approximate | S–XXL | chest |
| Zudio | Placeholder | XS–3XL | chest, waist, hip |

### Men's chest by size (cm)

Read across to compare brands: a higher number at the same size means the brand runs larger.

| Brand | XXS | XS | S | M | L | XL | XXL | 3XL | 4XL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Adidas |  | 84.5 | 89.5 | 96.5 | 104.5 | 113.5 | 124.5 | 136.5 |  |
| H&M | 76 | 82 | 88 | 96 | 104 | 112 | 120 | 128 |  |
| Levi's |  | 83.8 | 91.4 | 99.1 | 106.7 | 114.3 | 121.9 | 129.5 |  |
| Marks & Spencer |  | 83.5 | 90.5 | 99.5 | 106.5 | 114.5 | 122 | 129 | 134.5 |
| Max |  | 86.4 | 91.4 | 96.5 | 101.6 | 106.7 | 111.8 |  |  |
| Nike | 76 | 84 | 92 | 100 | 108 | 118 | 130 | 142 | 154 |
| Pantaloons |  | 86.36 | 91.44 | 96.52 | 101.6 | 106.68 |  |  |  |
| Red Tape |  |  | 96.52 | 101.6 | 106.68 | 111.76 | 116.84 |  |  |
| The Souled Store | 86 | 91 | 97 | 101 | 107 | 111 | 117 | 122 |  |
| Uniqlo |  |  | 84 | 92 | 100 | 108 | 116 | 124 |  |
| Westside |  | 91 | 96 | 101 | 106 | 111 | 116 | 121 |  |
| Zara |  |  | 90 | 96 | 102 | 108 | 114 |  |  |
| Zudio |  | 85.7 | 92.1 | 99 | 106.1 | 113.5 | 121.6 | 129.7 |  |

### Men's sources

- **Adidas** — adidas size-guide popup (men's shirts & tops, standard sizes; screenshot supplied by the user): chest, waist, hip in cm ranges, stored as range midpoints. Matches the retailer pages checked earlier exactly. Adidas's '2XL' stored as XXL. Standard sizes only (no Tall/Short).
- **H&M** — H&M size-guide popup, men's Regular tab (chest / waist, cm ranges; screenshot supplied by the user). Stored as range midpoints. No hip on this chart. Long tab not used. As published there are gaps between sizes (e.g. S ends at 90, M starts at 94) and XS spans 8 cm where others span 4.
- **Levi's** — Levi's US men's shirt sizing as reproduced by hibbett.com (inches ranges -> cm midpoints). 'Seat' stored as hip. In the published numbers seat equals chest at every size, which looks odd — taken as published. Not read from levi.com; not checked against Levi's India.
- **Marks & Spencer** — M&S India men's T-shirts & Polos size guide (body chest, cm ranges; screenshot supplied by the user, shown on an oversized tee page but the chart is category-wide). Stored as range midpoints; '2XL' stored as XXL. As published there are small gaps between sizes and 3XL/4XL overlap at 132.
- **Max** — Max (maxfashion.in) men's chart, 'Above size chart is for body measurements' (cm; same chart on two products, screenshots supplied by the user). Shoulder not used.
- **Nike** — nike.com men's tops chart (body measurements), cm ranges identical on the fi/my/au/id regional pages. Stored as range midpoints. Regular (not Tall) sizes. Not checked against Nike India.
- **Pantaloons** — Pantaloons size-chart popup, 'All measurements are body measurements' (cm; screenshot of the Peregrine slim polo supplied by the user, who checked other men's products and found the same chart). Column labelled 'Bust' stored as chest. Single values (inch sizes converted). Shoulder not used.
- **Red Tape** — Red Tape size-chart popup on a men's polo (screenshot supplied by the user). The 'Standard Size' column (38-46 in) is read as body chest; the page does not say so, but the user confirmed the column is the same across products. Garment columns not used (their room over standard size is uneven: +6.4, +3.8, +3.8, +2.5, +5.1 cm).
- **The Souled Store** — The Souled Store size charts, 'To fit your chest size' column (cm; screenshots supplied by the user). Identical on the oversized, oversized full-sleeve, boxy and relaxed charts, so treated as the brand's body chart. Single values, not ranges. 'XXXL' stored as 3XL.
- **Uniqlo** — Uniqlo India men's body-size chart (chest / waist, cm ranges; screenshot supplied by the user). Stored as range midpoints. Replaces the archived 2021 US chart, which ran about 8 cm larger at M.
- **Westside** — Westside size-guide popup on a men's product page (INDIA row; chest, waist, hip in cm; screenshot supplied by the user). The popup also lists shoulder and neck, which are not used. Westside's 'XXXL' stored as 3XL.
- **Zara** — APPROXIMATE — Zara publishes only garment measurements. Converted from the flat chest of one product (men's relaxed fit interlock tee, ref 5584/471/250; zara.com/in Product measurements popup, screenshot supplied by the user) as body chest = flat chest x 2 - 12 cm. The 12 cm is FitMatch's existing true-fit garment chest ease (6 cm flat), not a measurement. Slim products were tried and give impossible body sizes, so a non-slim product is used. Confidence is capped at medium and a note is shown.
- **Zudio** — PLACEHOLDER — no men's chart sourced for this brand (Zudio's site was down; a Google AI summary was found but not used, because its numbers can't be traced to Zudio and contradict themselves). Numbers are, per measurement, the average of every real men's chart in this file that publishes it at every size XS-3XL: chest Adidas, H&M, Levi's, Marks & Spencer, Nike, The Souled Store, Westside; waist Adidas, H&M, Levi's, Nike, Westside; hip Adidas, Levi's, Nike, Westside. Replace with the brand's own chart when sourced.

## Charts transcribed but not used

| Gender | Brand | Chart | Why not used |
|---|---|---|---|
| Women | Zara | Slim printed tee, fitted tee (garment) | Slim products convert to impossible body sizes (S bust 61–67 cm). |
| Women | Zara | V-neck batwing top (garment) | Grades 1 cm per size; not a regular cut. |
| Men | Zara | Basic slim fit tee (garment) | Converts to an M chest of 81 cm, below every real men's XS. |
| Men | Zara | Senna long-sleeve (garment) | Not needed once the relaxed interlock tee was chosen. |
| Women | Nike | Jordan oversized tee chart | Jordan label, wider chart than Nike Sportswear (M bust 90.2–96.5 vs 85.1–88.9). |
| Women | Max | URB_N oversized chart | Same numbers shifted a full size from the main Max label; main label used. |
| Women | Max | 5XL and 6XL rows | Beyond 4XL, the largest size the app offers. |
| Women | Marks & Spencer | XXXL (UK 28–30) | Bust row lists 132 for both UK 26 and 28; the top of the row looks shifted. |
| Women | Lulu & Sky | M–2XL chart with sleeve and hem width | Per-product garment chart. |
| Women | Uniqlo | UNIQLO:C long-sleeve line | Different product line, about 6 cm larger in bust; basic-tee line used. |
| Men | Uniqlo | Archived 2021 US chart | Replaced by the Uniqlo India chart (about 8 cm smaller at M). |
| Women | H&M | Maternity tab | Out of scope. |
| Men | H&M | Long tab | Out of scope. |
| Both | The Souled Store | Garment columns (chest, length, shoulder, sleeve) | Per-product; used only as cut evidence in open-questions.md. |
| Both | Red Tape | Garment columns (chest all round, shoulder, length) | Per-product; used only as cut evidence. |
| Men | Zudio | Google AI summary chart | Not traceable to Zudio and contradicts itself (L listed as 40–42 and 42–44 in). |
| Both | Roadster, HRX | Invented placeholders | Removed in v8. |

## How values were stored

| Method | Formula | Used for |
|---|---|---|
| Midpoint of range | (low + high) / 2 | H&M, Uniqlo, Nike (women), M&S (men) |
| Average of two UK sizes | (UK a + UK b) / 2, using M&S's own dual-size row | M&S (women) |
| As published | single value, cm | Pantaloons, The Souled Store, Max, Red Tape |
| Inches to cm | value × 2.54 | Lulu & Sky |
| Approximate | flat chest × 2 − 12 cm (FitMatch's true-fit ease) | Zara |
| Placeholder average | average of real men's charts that publish that measurement at every size XS–3XL | Zudio (men) |
| Recorded earlier | stored in a previous version; raw published values not re-transcribed | Westside, Adidas, Levi's, Nike (men), Zudio (women) |
