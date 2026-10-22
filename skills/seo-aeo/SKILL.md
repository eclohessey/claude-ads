---
name: seo-aeo
description: >
  AI search readiness audit (AEO/GEO) — getting cited by ChatGPT, Claude,
  Perplexity, Google AI Overviews, and Copilot. Covers AI crawler access,
  chunk-level extractability, entity consistency, off-site presence, and
  visibility measurement. Use when user says "AI search", "AEO", "GEO",
  "answer engine optimization", "show up in ChatGPT", "get cited by AI",
  "LLM visibility", "AI Overviews", or "generative engine optimization".
---

# AI Search Readiness (AEO / GEO)

## Process

1. Run `scripts/check_ai_crawlers.py <url>` — access is the gate
2. Run `scripts/seo_crawl.py <url> --crawl 25 --json -o crawl.json`
3. Read `seo/references/aeo-audit.md` for checks AE01-AE25
4. Read `seo/references/ai-crawlers.md` for the crawler table and robots rules
5. Assess extractability page by page, then entity and off-site presence
6. Establish a measurement baseline with `ai_visibility.py init`

## How AI Answers Get Built

```
User prompt
  → query fan-out (one prompt becomes several searches)
  → retrieval (search index + live page fetch)
  → chunking (pages split into passages; page context is lost)
  → synthesis (answer written from retained chunks)
  → citation (a subset of sources get linked)
```

Three consequences drive everything:

1. **The chunk is the unit, not the page.** A section that only makes sense in
   the context of what came before it gets dropped.
2. **Retrieval is mostly classic search.** Ranking well is a necessary condition
   for most citations. AEO is a layer on top of SEO, not a replacement for it.
3. **Third parties get cited about you more than you do.** Off-site presence is
   not optional here.

## Gate: Access and Rendering (AE01-AE04)

Check these before anything else. If either fails, no amount of content work
produces a citation.

- **Are answer crawlers blocked?** `OAI-SearchBot`, `ChatGPT-User`,
  `Claude-SearchBot`, `PerplexityBot`. Note that `GPTBot` and `ClaudeBot` are
  *training* crawlers — blocking those is a separate, legitimate decision that
  does not affect live citation.
- **Is content JavaScript-dependent?** Most answer crawlers do not execute JS.
  Check the raw-HTML word count from `seo_crawl.py`.
- **Is a WAF returning 403 to AI user agents?** robots.txt can look perfect
  while the firewall blocks the fetch. Check server logs.

## Chunk-Level Rewrite Pattern (AE05-AE12)

Before:

> ## Our Approach
> When we started building this, we knew the market needed something different.
> It combines several capabilities in a way that makes it easier to deploy than
> the alternatives, and our customers have seen great results.

After:

> ## How does Example reduce deployment time?
> Example cuts voice-agent deployment from three weeks to two days by shipping
> pre-built integrations for Twilio, Salesforce, and HubSpot. Across 40
> customer deployments in 2026, median time-to-first-call was 41 hours.
>
> [then the detail]

What changed: question-shaped heading (AE07), named entity instead of "it"
(AE06), a direct answer in the first sentence (AE05), and specific attributable
numbers instead of "great results" (AE11). The second version stands alone when
lifted out of the page. The first does not.

## Off-Site Presence (AE19-AE22)

Usually the largest gap and the largest lever. Assistants asked "best X" answer
from listicles, review sites, and Reddit far more than from vendor sites.

Priority order:
1. Get into the "best X" roundups that rank for your discovery queries
2. Claim and populate review profiles (G2, Capterra, Trustpilot, or vertical equivalent)
3. Participate genuinely in the communities your buyers use
4. Earn recent third-party coverage

## Measurement (AE23-AE25)

There is no rank API. Build a fixed prompt set and run it on a schedule:

```bash
python ai_visibility.py init --brand "Example" --domain example.com \
    --competitors "Alpha,Beta" --topics "primary topic,secondary topic"
# run each prompt in each engine, then:
python ai_visibility.py record --engine chatgpt --prompt-id P01 --mentioned \
    --cited-url https://example.com/guide --competitors-mentioned "Alpha"
python ai_visibility.py report
```

**Fix brand-prompt visibility first.** If assistants cannot accurately describe
your own product when asked directly, nothing downstream matters.

## Honest Limits

State these in every AEO report:

- AI visibility is **sampled, not measured**. Answers vary by user, session,
  region, and model version.
- Track **direction across months**, never a single run as a ranking.
- **`llms.txt` adoption is limited** — cheap to add, do not overclaim it.
- **AI referral traffic under-reports** badly; many answers are read without a
  click. Watch branded search volume as the better proxy.

## Output

### Deliverables
- `AI-SEARCH-REPORT.md` — AE01-AE25 results with evidence
- Crawler access table with a specific robots.txt recommendation
- Page-level extractability scores and rewrite examples
- Off-site gap list: where competitors appear and you do not
- `ai-visibility.json` — baseline prompt set and ledger
