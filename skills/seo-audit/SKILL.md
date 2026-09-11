---
name: seo-audit
description: >
  Full SEO and AI-search audit of a website with parallel subagent delegation.
  Produces separate Google Search and AI Search scores from 110 weighted checks
  plus a prioritized 90-day action plan. Use when user says "SEO audit",
  "audit my site", "why doesn't my site rank", "site audit", "search audit",
  or "full SEO review".
---

# Full SEO & AI Search Audit

## Process

1. Collect context (domain, business type, goal, target queries, competitors,
   available data). Proceed with just the domain if that is all you get.
2. Run `scripts/seo_crawl.py <url> --crawl 25 --json -o crawl.json`
3. Run `scripts/check_ai_crawlers.py <url> --json`
4. Read `seo/references/scoring-system.md`
5. Spawn four agents in parallel via the Task tool, passing `crawl.json`
6. Collect results, compute both scores, write `SEO-AUDIT-REPORT.md`
7. Offer to initialize the AI visibility baseline

## Parallel Delegation

Spawn all four in a single message so they run concurrently:

| Agent | Owns | Checks |
|-------|------|--------|
| `audit-seo-technical` | Crawl, index, render, performance, mobile | TE01-TE30 |
| `audit-seo-content` | Quality, intent, E-E-A-T, freshness | CO01-CO25 |
| `audit-seo-aeo` | AI readiness, extractability, structured data | AE01-AE25, SD01-SD15 |
| `audit-seo-authority` | Backlinks, brand signals, off-site presence | AU01-AU15 |

Each agent writes its own results file; this skill aggregates them.

## Gate Order

Some failures invalidate downstream findings. Check in this order and say so in
the report when a gate fails:

1. **TE01/TE02 — indexable at all?** If a site-wide `noindex` or robots block is
   live, that is the entire report. Everything else waits.
2. **TE11 — content present without JavaScript?** If not, all AEO findings are
   moot until rendering is fixed, and AI citation is effectively impossible.
3. **TE05-TE07 — one canonical version?** Duplicate hosts split every signal.
4. Then score normally.

## Scoring

Compute both scores separately per `seo/references/scoring-system.md`:

```
Google Score    = Technical(30%) + Content(30%) + Authority(25%) + Schema(15%)
AI Search Score = AEO(40%) + Content(25%) + Schema(20%) + Technical(15%)
```

Report the divergence explicitly — it is usually the most useful sentence in the
audit. A 20-point gap in either direction means the two remediation plans differ
substantially, and the report should say which to run first.

## Handling Missing Data

Checks requiring data you do not have go in the "Not Evaluated" table with what
is needed. Never score them as passes, and never estimate the underlying metric.

| Data source | Unlocks |
|-------------|---------|
| Google Search Console | CO22, AU10, CTR analysis, real index coverage, field CWV |
| Analytics | AE24, traffic segmentation, conversion by landing page |
| Backlink tool | AU01-AU06, AU15 |
| CrUX / PageSpeed field data | TE16-TE19 at p75 |

Without Search Console, an audit is structural only. Say that plainly rather
than implying the findings are complete.

## Output

### Deliverables
- `SEO-AUDIT-REPORT.md` — full report per `seo/references/report-template.md`
- `crawl.json` — raw crawl data for re-analysis
- `ai-visibility.json` — measurement baseline (if initialized)

### Report Shape

```
Google Search Score:  XX/100 (Grade X)
AI Search Score:      XX/100 (Grade X)

Technical & Indexing      ████████░░  XX/100
Content & Relevance       ██████░░░░  XX/100
AI Search Readiness       ███░░░░░░░  XX/100
Authority & Off-Site      █████░░░░░  XX/100
Structured Data & Entity  ███████░░░  XX/100
```

Lead with Quick Wins (Critical/High severity at S effort), then Critical
findings with evidence, then the full check table, then the 90-day plan.
