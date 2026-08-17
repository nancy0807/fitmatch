# Competitive Analysis

## Direction 1 (Killed): Wardrobe Tracking / Styling App

**Concept:** Catalog what a user owns (photo-based), get AI outfit/styling suggestions.

**Competitors identified:** Whering, Acloset, Stylebook, Indyx, Cladwell, SELION.AI, Aurelle, OpenWardrobe, Clueless, Style DNA — an already-active, reviewed, ranked app category.

**What the complaints actually said:**
- Existing apps struggle with outfit-suggestion quality — recommendations that don't logically go together, or repeatedly restyling the same few items while ignoring the rest of a cataloged wardrobe.
- Cataloging itself is a major friction point — manually photographing and tagging a full wardrobe commonly takes 8-15 hours, and at least one competitor sells an in-person cataloging service ($295+) specifically to solve that friction.
- The market splits into two camps: strong on cataloging/analytics but weak on styling, or the reverse. No reviewed app does both well.

**Why it was killed:** The complaints here are about *execution quality* of an already-attempted idea, not about the *problem being unsolved*. Building "another AI wardrobe app" would compete directly against funded products making the same pitch, with no clear evidence of an open gap. This is a weak position for a case study, since "why hasn't this been solved" has a clear answer: it has, repeatedly, just imperfectly.

## Direction 2 (Selected): Cross-Brand Sizing

**Concept:** Predict a user's size in an unfamiliar brand from their fit history in brands they already own.

**Evidence the problem is real and severe:**
- Fit is cited as the top reason for online apparel returns; return rates for online apparel commonly run 20-40%.
- An estimated $94B cost to the industry from returns in 2019.
- 64% of shoppers cite fit uncertainty as their main return reason; 85% say they'd buy more if fit were more predictable.

**Evidence the problem is genuinely unsolved (not just under-attempted):**
- Industry-wide size standardization efforts have failed historically.
- Fit-prediction attempts (Threadbase, True Fit, Body Labs, and various size-prediction patents dating to 2016) exist, but return rates have not meaningfully improved industry-wide — suggesting the hard part of this problem resists existing approaches.

**Why this beats Direction 1:** The signal here is different in kind, not just degree. In Direction 1, existing solutions work reasonably well and complaints are about polish. In Direction 2, well-funded, decade-old attempts still haven't moved the core metric (return rates). That's a stronger case that the problem itself — not just the execution — is hard.

**Known limitation acknowledged upfront:** Most credible existing attempts rely on brand partnerships or body-scanning data this project cannot access. FitMatch's scope is deliberately narrowed to what's buildable without that access — user-supplied fit history plus public size-chart data — trading some accuracy ceiling for feasibility. This tradeoff is documented, not hidden.
