# AI Search Readiness Audit — 25 Checks (AE01-AE25)

Category weight: 20%. Also called AEO (Answer Engine Optimization) or GEO
(Generative Engine Optimization). This is the layer classic SEO audits miss.

## How AI Answers Actually Get Built

Understanding the pipeline tells you what to optimize:

```
User prompt
  → query fan-out (the engine rewrites one prompt into several searches)
  → retrieval (search index + live fetch of candidate pages)
  → chunking (pages split into passages; whole-page context is lost)
  → synthesis (the model writes an answer from the retained chunks)
  → citation (a subset of sources get linked)
```

Three consequences drive every check below:

1. **The chunk is the unit, not the page.** A section that only makes sense in
   the context of the page above it gets dropped.
2. **Retrieval is mostly classic search.** Ranking well still matters — it is a
   necessary condition for most citations, not a separate game.
3. **Third-party pages get cited about your brand more than your own pages do.**
   Off-site presence is not optional here.

## Crawler Access (AE01-AE04)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| AE01 | AI answer crawlers not blocked | Critical | `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `PerplexityBot` allowed |
| AE02 | Content available without JavaScript | Critical | Most answer crawlers do not execute JS — see TE11 |
| AE03 | No aggressive bot protection on content pages | High | WAF/Cloudflare rules not returning 403 to AI user agents |
| AE04 | Training-crawler policy is a deliberate decision | Low | `GPTBot`, `ClaudeBot`, `Google-Extended` allowed or blocked on purpose, documented |

## Chunk-Level Extractability (AE05-AE12)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| AE05 | Answer-first structure | High | A direct 40-60 word answer immediately follows the H1 and each major subhead |
| AE06 | Sections are self-contained | High | No section opens with "it", "this", "they" referring to earlier context |
| AE07 | Subheads are question-shaped or declarative claims | Medium | ≥30% of H2/H3 phrased as the query a user would type |
| AE08 | Semantic HTML | Medium | Real `<h2>`, `<table>`, `<ul>`, `<dl>` — not styled `<div>`s |
| AE09 | Comparisons rendered as tables | Medium | Tables extract far more reliably than comparative prose |
| AE10 | Definitions stated explicitly | Medium | "X is a ..." sentences present for every term the page owns |
| AE11 | Facts are attributable and specific | High | Numbers, dates, named entities — vague claims are not quotable |
| AE12 | Key content not locked in images or PDFs | Medium | Infographic and chart data also present as HTML text |

## Entity & Consistency (AE13-AE18)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| AE13 | Brand name used consistently everywhere | High | Identical spelling on site, social, directories, review sites |
| AE14 | `Organization` schema with `sameAs` links | High | Points to LinkedIn, Crunchbase, GitHub, Wikidata, social profiles |
| AE15 | A canonical "what we are" page exists | High | One page states category, who it is for, pricing model, differentiators plainly |
| AE16 | Wikipedia/Wikidata entry where notability allows | Medium | Strongest single entity-resolution signal; N/A if not notable |
| AE17 | Pricing stated on-site in text | High | "Contact us for pricing" makes you uncitable for every cost query |
| AE18 | Product facts repeated consistently across pages | Medium | No conflicting claims about features, limits, or pricing |

## Off-Site Presence (AE19-AE22)

Usually the biggest gap and the biggest lever.

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| AE19 | Present in third-party "best X" listicles | Critical | Appears in the roundups that rank for your discovery queries |
| AE20 | Review-site profiles claimed and populated | High | G2, Capterra, Trustpilot, or the vertical equivalent, with recent reviews |
| AE21 | Genuine community presence | High | Reddit, Stack Overflow, industry forums — AI answers lean heavily on these |
| AE22 | Recent third-party coverage | Medium | Press, podcasts, or guest content within 12 months |

## Measurement (AE23-AE25)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| AE23 | A fixed prompt set is tested on a schedule | High | `scripts/ai_visibility.py` ledger exists and is run monthly |
| AE24 | AI referral traffic segmented in analytics | Medium | Referrers from `chatgpt.com`, `perplexity.ai`, `claude.ai`, `copilot.microsoft.com` tracked |
| AE25 | `llms.txt` published | Low | Optional and not yet widely consumed — cheap to add, do not overclaim its value |

## Honest Limits

Say these out loud in every report rather than implying more precision than exists:

- **There is no rank API for AI answers.** Visibility is sampled, not measured.
  Answers vary by user, session, region, and model version.
- **Prompt-set results are noisy.** Track direction across months, never read a
  single run as a ranking.
- **`llms.txt` adoption is limited.** Treat it as a low-cost bet, not a fix.
- **AI referral traffic under-reports.** Many answers are read without a click;
  brand-search lift is often the real signal.
