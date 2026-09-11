---
name: seo-technical
description: >
  Technical SEO audit covering crawlability, indexing, JavaScript rendering,
  Core Web Vitals, mobile experience, and site architecture. Use when user says
  "technical SEO", "crawl issues", "not indexed", "indexing problem",
  "site speed", "Core Web Vitals", "robots.txt", "sitemap", "canonical",
  or "Google can't find my pages".
---

# Technical SEO & Indexing

## Process

1. Run `scripts/seo_crawl.py <url> --crawl 25 --json -o crawl.json`
2. Run `scripts/check_ai_crawlers.py <url>`
3. Read `seo/references/technical-audit.md` for checks TE01-TE30
4. Read `seo/references/benchmarks.md` for Core Web Vitals thresholds
5. Evaluate in gate order — an early failure invalidates later checks
6. Score and write findings with evidence

## Gate Order

Work top-down. Do not report a content-depth finding on a page that is blocked
from indexing.

1. **TE01, TE02, TE26** — reachable and indexable at all?
2. **TE11-TE13** — does content exist without JavaScript?
3. **TE05-TE08** — is there one canonical version of each page?
4. **TE16-TE19** — fast enough to keep?
5. Everything else

## The Rendering Check (TE11-TE15)

The highest-leverage cluster in this skill, and the one most often missed.

Googlebot renders JavaScript. Nearly every AI answer crawler does not. A
client-rendered SPA can rank on Google and be completely invisible to ChatGPT,
Claude, and Perplexity.

**How to test**: `seo_crawl.py` fetches raw HTML with no JS execution. If
`word_count` is under 200 on a page that visibly has substantial copy, the
content is client-rendered.

**Fixes, in order of preference**: SSR or SSG for content routes → static
prerendering for crawlers → dynamic rendering as a last resort.

## Core Web Vitals

Synthetic single-load numbers are a diagnostic, not a score. Google uses field
data at p75 from CrUX. `seo_crawl.py` reports TTFB only; get LCP/INP/CLS from
Search Console or PageSpeed Insights field data, and if you only have lab data,
say so in the finding.

| Metric | Good | Needs improvement | Poor |
|--------|------|-------------------|------|
| LCP | <2.5s | 2.5-4.0s | >4.0s |
| INP | <200ms | 200-500ms | >500ms |
| CLS | <0.1 | 0.1-0.25 | >0.25 |
| TTFB | <800ms | 0.8-1.8s | >1.8s |

## Diagnosing Index Coverage Gaps

When indexed pages fall well short of sitemap pages:

| Search Console status | Usual cause | Fix |
|----------------------|-------------|-----|
| Discovered – not indexed | Crawl budget or perceived low value | Improve internal linking, cut thin pages |
| Crawled – not indexed | Quality or duplication judgment | Expand depth, consolidate near-duplicates |
| Duplicate, submitted URL not canonical | Canonical conflict | Fix TE05/TE06 |
| Excluded by noindex | Intentional or accidental | Verify TE02 |
| Soft 404 | Empty or near-empty page | Fix TE09, add content |

## Output

### Deliverables
- `TECHNICAL-SEO-REPORT.md` — TE01-TE30 results with evidence per finding
- Prioritized fix list with effort estimates
- Specific code or config changes, not general advice

Each finding cites a URL, status code, header, or measured count.
