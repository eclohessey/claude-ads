---
name: seo-competitor
description: >
  Competitive gap analysis for organic search and AI visibility. Compares
  content coverage, technical setup, structured data, link profiles, and
  AI citation share against named competitors. Use when user says
  "competitor SEO", "competitive analysis", "why do they outrank me",
  "content gap", "link gap", or "competitor research".
---

# Competitor Gap Analysis

## Process

1. Identify 3-5 real competitors — who ranks for your target queries, which is
   often not who you think your business competitors are
2. Crawl each: `scripts/seo_crawl.py <competitor> --crawl 25 --json -o comp-N.json`
3. Compare structurally: content coverage, technical setup, schema, depth
4. Compare off-site: link profiles and AI citation share
5. Produce a gap list ordered by winnability

## Finding the Real Competitors

Search your 5 highest-intent queries and record who appears in the top 5.
Separately, ask ChatGPT, Claude, and Perplexity your discovery prompts and
record who gets named. The two lists often differ — and the second list is who
you are competing with for AI visibility.

## Comparison Dimensions

| Dimension | What to compare | Source |
|-----------|----------------|--------|
| Content coverage | Which intents have an owner page | Sitemap + nav crawl |
| Content depth | Word count, subtopic coverage on shared topics | `crawl.json` |
| Technical | Rendering, CWV, indexable page count | `seo_crawl.py` |
| Schema | Types deployed per template | `crawl.json` schema types |
| Extractability | Answer-first ratio, question headings, tables | `crawl.json` aeo block |
| Authority | Referring domains, link velocity | Backlink tool (if available) |
| AI visibility | Mention and citation share | `ai_visibility.py` |

## Content Gap Method

1. Extract every competitor's URL list from their sitemaps
2. Classify each by intent from the URL and title
3. Diff against your own intent coverage
4. For each gap, score winnability with the `seo-keywords` scorecard

A gap that two or more competitors have filled is a validated intent — they each
independently decided it was worth a page.

## Link Gap Method

Domains linking to ≥2 competitors but not to you have already demonstrated they
link to sites in your category. That is the warmest outreach list available, and
it usually beats cold prospecting by a wide margin. Requires a backlink tool; if
there is none, say so rather than guessing.

## AI Citation Share

Run the same prompt set for each competitor using `ai_visibility.py` with the
`--competitors-mentioned` flag. The report's share-of-voice number tells you
whether the gap is visibility (you are never named) or preference (you are named
but ranked below them) — which are different problems with different fixes.

## Output

### Deliverables
- `COMPETITOR-ANALYSIS.md` — side-by-side comparison table
- Content gap list with winnability scores
- Link gap list with prospect domains and pitch angles
- AI citation share-of-voice comparison
- A "what they do better" section, stated plainly, with what to copy and what to
  deliberately not copy

Report only what was measured. Never estimate a competitor's traffic, revenue,
or spend.
