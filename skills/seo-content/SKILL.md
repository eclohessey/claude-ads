---
name: seo-content
description: >
  Content quality audit for search: intent match, topic cluster structure,
  keyword cannibalization, E-E-A-T signals, thin and decaying content, and
  refresh decisions. Use when user says "content audit", "content strategy",
  "why isn't my content ranking", "E-E-A-T", "thin content", "content refresh",
  "topic clusters", or "blog SEO".
---

# Content Quality & Relevance

## Process

1. Read `seo/references/content-audit.md` for checks CO01-CO25
2. Use `crawl.json` from `seo_crawl.py` for titles, H1s, word counts, duplication
3. Pull Search Console query and page data if available — it changes every priority
4. Evaluate the top 20 pages by traffic or strategic value, plus each template
5. Apply the refresh decision tree to every underperformer
6. Score and write findings

## Intent Match First (CO01-CO02)

The most common cause of "good content that doesn't rank" is not quality. It is
format mismatch: a blog post targeting a query whose SERP is entirely product
and comparison pages.

**How to check**: search the target query, read page one, and ask whether your
page is the same *kind* of thing. If every result is a comparison table and you
published a narrative essay, quality will not save it.

| Query shape | Page format that wins |
|-------------|----------------------|
| "what is", "how to" | Guide, tutorial, definition |
| "best", "X vs Y", "alternatives" | Comparison table, roundup |
| "pricing", "cost", "review" | Pricing page, review page |
| "buy", "trial", "demo" | Product, signup page |

## Cannibalization (CO01)

Two pages targeting one intent split signals and both underperform. Detect by
grouping Search Console queries by page: if one query returns impressions for
two URLs, or positions swap between them week to week, they are competing.

**Fix**: pick the stronger page, merge the useful content in, 301 the weaker.
Do not simply delete — the redirect preserves any links it earned.

## The Refresh Decision Tree

```
Impressions high, clicks low       → rewrite title + meta description (CO08/CO09)
Impressions low, position 11-20    → expand depth and add internal links (CO04/CO13)
Impressions low, position >30      → intent mismatch; rewrite format (CO02)
Two pages trading positions        → consolidate, 301 the weaker (CO01)
Traffic decayed from a good base   → refresh facts and dates (CO21/CO22)
Never ranked, no links, no traffic → prune (CO25)
```

Refreshing an existing ranking page beats publishing a new one roughly every
time — it is faster, cheaper, and compounds the page's existing signals.

## E-E-A-T (CO15-CO20)

Not a ranking factor with a dial. It is a bundle of verifiable signals:

- **Experience**: firsthand use, original screenshots, real test results
- **Expertise**: named authors with credentials and a real bio page
- **Authoritativeness**: cited by others; a recognizable entity (see AU10-AU12)
- **Trust**: real company identity, contact details, sourced claims, honest dates

For YMYL topics — health, finance, legal, safety — expert review is Critical
(CO20), not a nice-to-have.

## Writing Rules That Serve Google and AI Together

These raise both snippet capture and AI citation rate:

1. Answer in the first 40-60 words, then go deep
2. One idea per section, with a subhead that names it
3. Specific over general: "cut handling time 34%" beats "improved efficiency"
4. Name the entity, not the pronoun, at the start of each section
5. Comparisons belong in tables, not prose

## Output

### Deliverables
- `CONTENT-AUDIT-REPORT.md` — CO01-CO25 results
- Page-level table: URL · intent · status · action (keep / refresh / merge / prune)
- Cannibalization pairs with a consolidation recommendation each
- Content gaps: intents with no owner page
