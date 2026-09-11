---
name: seo
description: "Comprehensive SEO and AI-search visibility audit for any website. Covers technical SEO and indexing, content quality and E-E-A-T, AI search readiness (AEO/GEO) for ChatGPT, Claude, Perplexity and Google AI Overviews, structured data, backlink authority, keyword and query mapping, competitor gap analysis, and local SEO. 110 weighted checks producing separate Google Search and AI Search scores. Triggers on: SEO, search ranking, rank on Google, organic traffic, AI search, AEO, GEO, answer engine optimization, LLM visibility, ChatGPT visibility, get cited by AI, schema markup, structured data, backlinks, keyword research, Core Web Vitals, crawlability, indexing, robots.txt, sitemap, technical SEO, content audit, SERP, featured snippet."
argument-hint: "audit <url> | technical <url> | content <url> | aeo <url> | schema <url> | authority <url> | keywords <topic> | competitor <url> | local <url>"
license: MIT
---

# SEO — Search Ranking & AI Visibility Audit

Audits a website for classic search ranking and for citation by AI answer
engines. Orchestrates 9 sub-skills and 4 parallel agents over 110 weighted
checks. Companion to the `ads` skill: `ads` covers paid, `seo` covers earned.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo audit <url>` | Full audit with parallel subagent delegation → two scores |
| `/seo technical <url>` | Crawlability, indexing, rendering, Core Web Vitals (TE01-TE30) |
| `/seo content <url>` | Content quality, intent match, E-E-A-T, freshness (CO01-CO25) |
| `/seo aeo <url>` | AI search readiness for ChatGPT/Claude/Perplexity (AE01-AE25) |
| `/seo schema <url>` | Structured data and entity graph (SD01-SD15) |
| `/seo authority <url>` | Backlink profile, brand signals, link gaps (AU01-AU15) |
| `/seo keywords <topic>` | Query mapping by intent → `QUERY-MAP.md` |
| `/seo competitor <url>` | Competitive gap analysis, shared for search and AI |
| `/seo local <url>` | Local SEO, Google Business Profile, NAP consistency |

## Context Intake (Required — Always Do This First)

Without this, benchmarks are generic and priorities will be wrong. Ask in one
message, and skip anything the user already supplied:

1. **Domain** — the site to audit (required)
2. **Business type** — SaaS · E-commerce · Local Service · B2B Enterprise ·
   Info Products · Mobile App · Real Estate · Healthcare · Finance · Agency · Other
3. **Primary goal** — Leads/demos · Sales · Signups · Calls · Brand awareness
4. **Target queries or topics** — what should this site be found for?
5. **Competitors** — 2-3 names or domains
6. **Available data** — Search Console access? Analytics? Any backlink tool?

Proceed with the audit if the user only gives the domain. Everything that needs
missing data goes in the report's "Not Evaluated" table — never guessed.

## Orchestration Logic

For `/seo audit`:

1. **Collect context** (above)
2. **Run the crawl** — `scripts/seo_crawl.py <url> --crawl 25 --json -o crawl.json`
3. **Check crawler access** — `scripts/check_ai_crawlers.py <url> --json`
4. **Spawn agents in parallel** via the Task tool: `audit-seo-technical`,
   `audit-seo-content`, `audit-seo-aeo`, `audit-seo-authority`
5. **Score** with `references/scoring-system.md` — compute both scores separately
6. **Write** `SEO-AUDIT-REPORT.md` per `references/report-template.md`
7. **Offer the baseline**: initialize `ai_visibility.py` so progress is measurable

For single commands, load the sub-skill directly. Still collect context first.

## Core Principle

Google ranking and AI citation share roughly 80% of their inputs — crawlable,
useful, specific content that credible sources cite. The 20% that differs is
chunk-level structure and off-site presence, and it is where most sites fail.

**Always report two scores.** A site with strong links and weak chunk structure
scores well on Google and badly on AI; a new site with excellent answer-first
content scores the reverse. The remediation plans are different. Collapsing
them into one number destroys the finding.

## Quality Gates

Hard rules — never violate these:

- **Never fabricate metrics.** Traffic, rankings, search volume, backlink counts
  and domain authority are stated only from supplied data or tool output. If it
  was not measured, it goes in "Not Evaluated".
- **Never recommend a tactic that risks a manual action** — bought links, PBNs,
  cloaking, doorway pages, marking up invisible content, fabricated reviews.
- **Never promise rankings or timelines faster than `references/benchmarks.md`.**
- **Never claim AI visibility is precisely measurable.** It is sampled via a
  prompt set; report direction over time, not a rank.
- **Never recommend blocking a search crawler** without stating the traffic cost.
- **Never treat `llms.txt` as a fix.** Low cost, speculative payoff — say so.
- **Check rendering before anything else.** If content requires JavaScript, most
  AI crawlers never see it, and every content finding downstream is moot.
- **Evidence per finding.** A URL, status code, count, or quoted line. No
  finding is reported from assumption.

## Business Type Calibration

Detect from the site, and let it reorder priorities:

- **SaaS**: comparison and alternatives pages, pricing transparency (AE17), docs
- **E-commerce**: `Product`/`Offer` schema, faceted navigation control (TE10), feeds
- **Local Service**: Google Business Profile, NAP consistency (AU11), local pages
- **B2B Enterprise**: E-E-A-T, case studies, LinkedIn entity presence
- **Info Products**: topical authority depth, author credibility (CO15)
- **Healthcare / Finance**: YMYL — expert review is Critical, not optional (CO20)
- **Real Estate**: listing schema, geo pages, freshness
- **Agency**: portfolio and results pages, local + national blend

## Reference Files

Load on-demand — do NOT load all at startup.

**Path resolution:** references install to `~/.claude/skills/seo/references/`.
When sub-skills or agents reference `seo/references/*.md`, resolve there.

- `references/scoring-system.md` — Weighted algorithm, both scores, grading
- `references/technical-audit.md` — 30-check technical and indexing checklist
- `references/content-audit.md` — 25-check content quality and E-E-A-T checklist
- `references/aeo-audit.md` — 25-check AI search readiness checklist
- `references/authority-audit.md` — 15-check backlink and brand checklist
- `references/schema-reference.md` — 15-check structured data checklist + patterns
- `references/ai-crawlers.md` — Crawler table, robots.txt precedence, llms.txt
- `references/keyword-research.md` — Intent taxonomy, clustering, scorecard
- `references/benchmarks.md` — CTR, CWV, timelines, AI visibility ranges
- `references/report-template.md` — Output format and writing rules

## Scripts

Installed at `~/.claude/skills/seo/scripts/`. Only `requests` is required; the
visibility tracker is stdlib-only.

```bash
# Crawl and extract on-page SEO + AEO signals
python seo_crawl.py https://example.com --crawl 25 --json -o crawl.json

# Check search and AI crawler access
python check_ai_crawlers.py example.com

# Establish and track an AI visibility baseline
python ai_visibility.py init --brand "Example" --domain example.com \
    --competitors "Alpha,Beta" --topics "topic one,topic two"
python ai_visibility.py record --engine chatgpt --prompt-id P01 --mentioned
python ai_visibility.py report
```

## Scoring

Two scores from the same 110 checks, weighted differently:

```
Google Score    = Technical(30%) + Content(30%) + Authority(25%) + Schema(15%)
AI Search Score = AEO(40%) + Content(25%) + Schema(20%) + Technical(15%)
```

| Grade | Score | Action Required |
|-------|-------|-----------------|
| A | 90-100 | Minor optimizations only |
| B | 75-89 | Some improvement opportunities |
| C | 60-74 | Notable issues need attention |
| D | 40-59 | Significant problems present |
| F | <40 | Urgent intervention required |

## Sub-Skills

1. **seo-audit** — Full audit with parallel delegation
2. **seo-technical** — Crawlability, indexing, rendering, performance
3. **seo-content** — Content quality, intent match, E-E-A-T
4. **seo-aeo** — AI search readiness and citation mechanics
5. **seo-schema** — Structured data and entity graph
6. **seo-authority** — Backlinks, brand signals, link gaps
7. **seo-keywords** — Query research and intent mapping
8. **seo-competitor** — Competitive gap analysis
9. **seo-local** — Local SEO and Google Business Profile

## Subagents

Spawned in parallel during `/seo audit` via the Task tool:

- `audit-seo-technical` — TE01-TE30 crawl, index, render, performance
- `audit-seo-content` — CO01-CO25 quality, intent, E-E-A-T
- `audit-seo-aeo` — AE01-AE25 + SD01-SD15 AI readiness and schema
- `audit-seo-authority` — AU01-AU15 links, brand, off-site presence
