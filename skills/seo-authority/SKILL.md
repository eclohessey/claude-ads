---
name: seo-authority
description: >
  Backlink profile, brand signal, and off-site authority audit. Covers
  referring domain health, anchor distribution, broken link reclamation,
  competitor link gaps, and link-earning strategy. Use when user says
  "backlinks", "link building", "domain authority", "link profile",
  "off-page SEO", "link gap", or "how do I get links".
---

# Authority & Off-Site Signals

## Process

1. Read `seo/references/authority-audit.md` for checks AU01-AU15
2. Collect link data — Search Console Links report at minimum; Ahrefs, Semrush,
   or Moz if the user has one
3. Compare referring domains against 2-3 competitors
4. Identify reclamation opportunities and link gaps
5. Recommend a link-earning strategy matched to the business type

## Data Reality Check

Without a backlink tool, AU01-AU06 and AU15 cannot be fully evaluated. Search
Console's Links report shows your own links but not competitors'. Say what you
could and could not assess rather than estimating — do not report a referring
domain count or a Domain Authority figure you did not measure.

Domain Authority, Domain Rating, and Authority Score are third-party estimates,
not Google metrics. Report them as context, never as a target.

## Priority Order

Work the cheapest wins first:

1. **Reclaim broken backlinks (AU07)** — links already pointing at 404s. Free
   authority, one 301 each, effect within weeks.
2. **Convert unlinked mentions (AU09)** — sites already naming you. One email each.
3. **Fix profile and directory consistency (AU11, AU12)** — also feeds AE13/AE20.
4. **Work competitor link gaps (AU15)** — domains linking to ≥2 competitors but
   not you have already shown they link to sites like yours.
5. **Build a link-earning asset (AU13)** — slowest, highest ceiling.

## What Actually Earns Links

Ranked by observed return:

1. **Original data** — a survey, a benchmark, an analysis of your own usage
   data. One good dataset out-earns fifty guest posts, and it doubles as the
   original-information signal in CO16.
2. **Free tools and calculators** — compounding, linked from forums for years
3. **Being quoted as an expert** — podcasts, journalist requests, panels
4. **Definitive reference pages** — the page people link to when explaining a
   concept in your category
5. **Genuine community participation** — slow, and also feeds AE21

## What To Avoid

- Buying links, exchanges, PBNs (AU05) — detection has outpaced the tactic
- Mass guest-post outreach on unrelated sites — relevance gates value (AU03)
- Directory blasts — a few real industry directories help, volume does not
- Over-optimized exact-match anchors (AU04) — keep commercial anchors under 10%

## Brand Signals (AU10-AU12)

Growing branded search volume is the strongest correlate of durable rankings,
and it is what AI-driven awareness shows up as when the answer generated no
click. Baseline it from Search Console's branded queries and track monthly — it
is the best available proxy for AEO progress.

## Output

### Deliverables
- `AUTHORITY-REPORT.md` — AU01-AU15 results with data sources named
- Broken backlink reclamation list with target redirect for each
- Competitor link gap table: domain · links to which competitors · pitch angle
- A link-earning plan with realistic timelines from `seo/references/benchmarks.md`
