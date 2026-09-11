# Technical & Indexing Audit — 30 Checks (TE01-TE30)

Category weight: 25%. Run with `scripts/seo_crawl.py` and
`scripts/check_ai_crawlers.py`; Core Web Vitals require field data from Search
Console or CrUX, not a single synthetic load.

## Crawl & Index (TE01-TE10)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| TE01 | robots.txt does not block search crawlers | Critical | Googlebot/Bingbot allowed at `/` and on money pages |
| TE02 | No accidental site-wide `noindex` | Critical | No `noindex` in meta robots or `X-Robots-Tag` on indexable pages |
| TE03 | XML sitemap exists and is declared in robots.txt | High | `Sitemap:` line present; sitemap returns 200 XML |
| TE04 | Sitemap contains only canonical, 200-status, indexable URLs | Medium | No redirects, 404s, or noindexed URLs listed |
| TE05 | Self-referencing canonical on every indexable page | High | `<link rel="canonical">` resolves to the page's own final URL |
| TE06 | No canonical conflicts | High | Canonical does not point to a noindexed, redirected, or 404 URL |
| TE07 | Single hostname resolves | High | http→https and non-www→www (or reverse) both 301 to one origin |
| TE08 | No redirect chains longer than one hop | Medium | Each redirect resolves in 1 step; no loops |
| TE09 | 404s return 404, not 200 | Medium | No soft-404s; custom 404 page returns status 404 |
| TE10 | Pagination and faceted URLs controlled | Medium | Parameter URLs canonicalized or robots-excluded; no infinite crawl space |

## Rendering (TE11-TE15)

The highest-leverage cluster for AI visibility. Googlebot renders JavaScript;
most AI answer crawlers do not.

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| TE11 | Primary content present in the raw HTML response | Critical | Main copy visible with JS disabled (`seo_crawl.py` word count ≥300 on content pages) |
| TE12 | Title, H1, meta description server-rendered | High | Present in initial HTML, not injected client-side |
| TE13 | Internal links are real `<a href>` elements | High | No router-only click handlers; crawlers can follow them |
| TE14 | Structured data server-rendered | Medium | JSON-LD present in raw HTML |
| TE15 | No content hidden behind interaction | Medium | Key copy not gated behind tabs/accordions that load on click only |

## Performance (TE16-TE21)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| TE16 | LCP | High | <2.5s at p75 (field data) |
| TE17 | INP | High | <200ms at p75 |
| TE18 | CLS | Medium | <0.1 at p75 |
| TE19 | TTFB | Medium | <800ms |
| TE20 | Images in modern formats and correctly sized | Medium | WebP/AVIF, explicit width/height, lazy-loaded below fold |
| TE21 | Compression and caching enabled | Low | gzip/brotli on; static assets with long `Cache-Control` |

## Mobile & Accessibility (TE22-TE25)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| TE22 | Responsive viewport meta present | Critical | `<meta name="viewport" content="width=device-width...">` |
| TE23 | No horizontal scroll at 375px | High | Content fits; no fixed-width overflow |
| TE24 | Tap targets ≥48x48px, body text ≥16px | Medium | No pinch-to-zoom needed |
| TE25 | Images have meaningful alt text | Medium | <10% of content images missing alt |

## Security & Architecture (TE26-TE30)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| TE26 | Valid HTTPS on every URL | Critical | No mixed content, no expired or mismatched cert |
| TE27 | Crawl depth ≤3 clicks from home for money pages | High | Important pages not buried |
| TE28 | No orphan pages | Medium | Every indexable page has ≥1 internal link pointing to it |
| TE29 | Descriptive, stable URL slugs | Low | Lowercase, hyphenated, keyword-bearing, no session IDs |
| TE30 | `hreflang` correct where multilingual | Medium | Bidirectional, self-referencing, valid language codes; N/A if single-locale |

## Diagnostic Order

Work top-down — an early failure invalidates later checks:

1. **TE01, TE02, TE26** — is the site reachable and indexable at all?
2. **TE11-TE13** — does content exist without JavaScript?
3. **TE05-TE08** — is there one canonical version of each page?
4. **TE16-TE19** — is it fast enough to keep?
5. Everything else.

## Common Root Causes

| Symptom | Usual cause |
|---------|-------------|
| Indexed page count far below sitemap count | Thin/duplicate content, or crawl budget lost to parameter URLs (TE10) |
| Ranks on Google but never cited by AI | JS-rendered content (TE11) or blocked answer crawlers (TE01) |
| Traffic dropped after a redesign | Lost canonicals, changed slugs without 301s (TE05, TE08) |
| High impressions, low clicks | Not a technical fault — see CO08/CO09 (title and meta description) |
