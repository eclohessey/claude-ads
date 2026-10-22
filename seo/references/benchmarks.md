# SEO & AI Search Benchmarks

Use for calibration and expectation-setting. Ranges are directional — always
prefer the site's own Search Console data over any published benchmark, and say
which you used.

## Organic CTR by Position

Desktop, non-branded, approximate. AI Overviews have compressed all of these
meaningfully where they appear.

| Position | CTR range |
|----------|-----------|
| 1 | 25-40% |
| 2 | 12-18% |
| 3 | 8-12% |
| 4-5 | 5-8% |
| 6-10 | 2-5% |
| 11+ | <1% |

Practical reading: moving position 11 → 8 roughly doubles clicks; moving 4 → 2
roughly doubles them again. Anything past page one is effectively zero.

## Core Web Vitals Thresholds

Field data at p75, which is what Google actually uses.

| Metric | Good | Needs improvement | Poor |
|--------|------|-------------------|------|
| LCP | <2.5s | 2.5-4.0s | >4.0s |
| INP | <200ms | 200-500ms | >500ms |
| CLS | <0.1 | 0.1-0.25 | >0.25 |
| TTFB | <800ms | 0.8-1.8s | >1.8s |

## Realistic Timelines

The most common source of disappointment is expecting SEO timelines to look like
paid timelines. State these upfront.

| Change | Time to measurable effect |
|--------|--------------------------|
| Fixing a crawl/index block | Days to 2 weeks |
| Title and meta description rewrite | 2-4 weeks |
| Adding structured data | 2-6 weeks (rich results) |
| Refreshing an existing ranking page | 3-8 weeks |
| New content on an established site | 2-4 months |
| New content on a new domain | 6-12 months |
| Authority/link building shift | 6-12 months |
| Site migration recovery | 4-12 weeks |
| AI citation appearing after fixes | 2-8 weeks (faster than rankings) |

AI citations often move faster than rankings because retrieval re-runs on every
query, while ranking carries inertia.

## Content Benchmarks

| Metric | Healthy range |
|--------|--------------|
| Indexed pages vs sitemap pages | >90% |
| Pages with unique title + meta description | 100% |
| Pages with exactly one H1 | 100% |
| Content pages under 300 words | <10% |
| Internal links per content page | 3-10 contextual |
| Pages updated in last 12 months (top 20) | 100% |
| Crawl depth of money pages | ≤3 clicks |

## AI Visibility Benchmarks

Measured with `scripts/ai_visibility.py`. These are orientation values, not
industry standards — no reliable public dataset exists yet.

| Metric | Weak | Average | Strong |
|--------|------|---------|--------|
| Brand-prompt visibility ("What is X?") | <50% | 50-90% | 100% |
| Discovery-prompt visibility ("best X for Y") | 0% | 5-20% | >30% |
| Citation rate (linked, not just named) | <5% | 5-15% | >25% |
| Share of voice vs named competitors | <10% | 10-30% | >40% |

**Brand-prompt visibility below 100% is the first thing to fix.** If assistants
cannot describe your own product accurately, nothing downstream matters.

## Traffic Mix Expectations

A healthy organic profile, roughly:

| Segment | Share |
|---------|-------|
| Branded queries | 30-50% |
| Non-branded informational | 25-40% |
| Non-branded commercial/comparison | 15-30% |
| AI referral traffic | 1-5% today, rising |

AI referral traffic under-reports badly — many answers are consumed without a
click. Watch branded search volume as the proxy for AI-driven awareness.
