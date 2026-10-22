---
name: seo-keywords
description: >
  Keyword and query research mapped to search intent and owner pages. Produces
  a topic cluster architecture and a prioritized query map. Use when user says
  "keyword research", "what keywords should I target", "query mapping",
  "topic clusters", "search intent", "content plan", or "what should I write
  about".
---

# Keyword & Query Research

## Process

1. Read `seo/references/keyword-research.md` for the intent taxonomy and scorecard
2. Collect seeds from reality: sales calls, support tickets, site search logs
3. Mine Search Console for queries already at position 8-20 — cheapest wins
4. Harvest SERP features: People Also Ask, related searches, autocomplete
5. Mine competitor navigation and sitemaps for intents they invested in
6. Cluster by intent, assign one owner page per cluster
7. Score and prioritize, write `QUERY-MAP.md`

## The Output Is a Map, Not a List

A keyword list is useless. The deliverable answers: which questions do buyers
ask, which page owns each one, and what has to change for that page to win.

## Prioritization

Most sites over-invest in informational content and under-invest in comparison
and commercial queries — which are also what AI assistants get asked most.
Build those first.

| Intent | Conversion value | Typical investment | Verdict |
|--------|-----------------|-------------------|---------|
| Comparison ("X vs Y", "best", "alternatives") | Highest ROI | Under-built | **Build first** |
| Commercial ("pricing", "cost", "review") | High | Under-built | Build first |
| Transactional ("buy", "trial", "demo") | Highest | Usually exists | Optimize |
| Informational ("what is", "how to") | Low, high volume | Over-built | Build after |

## Scorecard

Score each candidate 1-5, multiply by weight, rank by total:

| Factor | Weight |
|--------|--------|
| Buyer intent (closeness to purchase) | 3x |
| Winnability | 3x |
| Volume | 1x |
| Existing site relevance | 2x |
| AI-answer exposure | 2x |

Volume carries the lowest weight deliberately. Ten buyers beat a thousand browsers.

## Winnability Without Paid Tools

Search the query and read page one:

| What you see | Reading |
|--------------|---------|
| Forums, Reddit, thin pages | Winnable now |
| Direct competitors your size | Winnable in 3-6 months |
| Wikipedia, major publishers, Amazon | Not winnable — go longer-tail |
| Results that miss the query's intent | Opportunity: nobody built the right page |
| An AI Overview that answers it fully | Low click potential — target citation, not traffic |

## Cluster Architecture

```
PILLAR: [broad topic]        → /topic/
  ├── [subtopic 1]           → /topic/subtopic-1/
  ├── [subtopic 2]           → /topic/subtopic-2/
  ├── [X vs Y]               → /compare/x-vs-y/
  ├── [alternatives to X]    → /alternatives/x/
  ├── [topic pricing]        → /pricing/
  └── [topic for <segment>]  → /solutions/segment/
```

Supporting pages link up to the pillar with descriptive anchors; the pillar
links down to each. That reciprocal linking is what makes it a cluster rather
than a pile of posts.

## AI-Era Additions

- **Conversational long-tail** — people type three words to Google and speak
  full sentences to assistants. Target both phrasings.
- **"Best X for <specific segment>"** — easier to own than "best X", converts better.
- **Questions competitors' docs answer and yours do not** — assistants cite
  whoever documented it.

## Output

### Deliverables
- `QUERY-MAP.md` — one row per cluster: cluster · primary query · intent ·
  owner page · status · priority
- Cluster architecture diagram with URL structure
- Content gap list: intents with no owner page, ranked by the scorecard
- Quick wins: existing pages at position 8-20 with the specific change needed

Never state search volume figures unless a tool or the user provided them.
