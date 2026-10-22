<p align="center">
  <img src="assets/banner.png" alt="Claude Ads — Paid Advertising Audit Skill for Claude Code" width="100%">
</p>

# Claude Ads — Paid Advertising + SEO / AI Search Skills for Claude Code

Two Claude Code skills sharing one architecture:

- **`/ads`** — paid advertising audit and optimization across Google, Meta, YouTube, LinkedIn, TikTok, Microsoft, and Apple Search Ads. 225+ weighted checks, industry templates, parallel subagent delegation.
- **`/seo`** — organic search ranking and AI-answer visibility (AEO/GEO) for ChatGPT, Claude, Perplexity, and Google AI Overviews. 110 weighted checks producing **separate Google Search and AI Search scores**.

Install together, use either independently.

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/AgriciDaniel/claude-ads)](https://github.com/AgriciDaniel/claude-ads/releases)
[![CI](https://img.shields.io/github/actions/workflow/status/AgriciDaniel/claude-ads/ci.yml?branch=main&label=CI)](https://github.com/AgriciDaniel/claude-ads/actions)

## Contents

- [Installation](#installation)
- [Demo](#demo)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [SEO & AI Search](#seo--ai-search)
- [Features](#features)
- [Architecture](#architecture)
- [How It Analyzes Your Ads](#how-it-analyzes-your-ads)
- [FAQ](#faq)
- [Requirements](#requirements)
- [Uninstall](#uninstall)
- [Related Projects](#related-projects)
- [License](#license)

## Installation

### One-Command Install (Unix/macOS/Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-ads/main/install.sh | bash
```

### One-Command Install (Windows PowerShell)

```powershell
irm https://raw.githubusercontent.com/AgriciDaniel/claude-ads/main/install.ps1 | iex
```

### Manual Install

```bash
git clone https://github.com/AgriciDaniel/claude-ads.git
cd claude-ads
./install.sh          # Unix/macOS/Linux
```

```powershell
.\install.ps1         # Windows PowerShell
```

## Demo

<p align="center">
  <img src="assets/demo.gif" alt="Claude Ads Demo" width="100%">
</p>

## Quick Start

```bash
# Start Claude Code
claude

# Run a full multi-platform audit
/ads audit

# Deep analysis for a single platform
/ads google
/ads meta
/ads linkedin

# Strategic planning by business type
/ads plan saas
/ads plan ecommerce
/ads plan local-service

# Cross-platform creative audit
/ads creative

# Budget and bidding strategy review
/ads budget

# Full SEO + AI search audit of a website
/seo audit example.com

# AI-answer visibility only (ChatGPT, Claude, Perplexity)
/seo aeo example.com

# Single-dimension SEO analysis
/seo technical example.com
/seo content example.com/pricing
/seo keywords "your category"
```

## Commands

| Command | Description |
|---------|-------------|
| `/ads audit` | Full multi-platform audit with parallel subagent delegation |
| `/ads google` | Google Ads deep analysis (Search, PMax, Display, YouTube, Demand Gen) |
| `/ads meta` | Meta Ads deep analysis (FB, IG, Advantage+ Shopping) |
| `/ads youtube` | YouTube Ads specific analysis (Skippable, Shorts, Demand Gen) |
| `/ads linkedin` | LinkedIn Ads deep analysis (B2B, Lead Gen, TLA) |
| `/ads tiktok` | TikTok Ads deep analysis (Creative, Shop, Smart+) |
| `/ads microsoft` | Microsoft/Bing Ads deep analysis (Copilot, Import validation) |
| `/ads creative` | Cross-platform creative quality audit and fatigue detection |
| `/ads landing` | Landing page quality assessment for ad campaigns |
| `/ads budget` | Budget allocation and bidding strategy review |
| `/ads apple` | Apple Search Ads (ASA) deep analysis (campaign structure, bids, MMP, TAP) |
| `/ads plan <type>` | Strategic ad plan with industry templates |
| `/ads competitor` | Competitor ad intelligence across all platforms |
| `/seo audit <url>` | Full SEO + AI search audit → separate Google and AI scores |
| `/seo technical <url>` | Crawlability, indexing, JS rendering, Core Web Vitals |
| `/seo content <url>` | Content quality, intent match, E-E-A-T, cannibalization |
| `/seo aeo <url>` | AI search readiness for ChatGPT, Claude, Perplexity, AI Overviews |
| `/seo schema <url>` | Structured data and entity graph |
| `/seo authority <url>` | Backlink profile, brand signals, link gaps |
| `/seo keywords <topic>` | Query research mapped to intent and owner pages |
| `/seo competitor <url>` | Competitive gap analysis for search and AI |
| `/seo local <url>` | Local SEO, Google Business Profile, NAP consistency |

### `/ads audit`
**Full Multi-Platform Audit**

Spawns 6 parallel subagents to analyze your ad accounts simultaneously:
- **audit-google** — 74 checks across Search, PMax, Display, YouTube, Demand Gen
- **audit-meta** — 46 checks across Pixel/CAPI, Creative, Structure, Audience
- **audit-creative** — 21 cross-platform creative quality checks
- **audit-tracking** — 7 conversion tracking health checks
- **audit-budget** — 24 budget and bidding strategy checks
- **audit-compliance** — 18 compliance and regulatory checks

Generates a unified **Ads Health Score (0-100)** with prioritized action plan.

### `/ads plan <business-type>`
**Strategic Ad Planning**

Industry-specific templates with platform mix, campaign architecture, creative strategy, targeting, budget guidelines, and KPI targets.

**Supported business types:**
- `saas` — Trial/demo focus, Google + LinkedIn primary
- `ecommerce` — Shopping/PMax, ROAS-focused, seasonal
- `local-service` — Google Search + LSA, call tracking, geo radius
- `b2b-enterprise` — LinkedIn ABM, long sales cycle, pipeline metrics
- `info-products` — Meta + YouTube, webinar/VSL funnels
- `mobile-app` — Meta + Google UAC, MMP required, LTV:CPI
- `real-estate` — Special Ad Category (housing), buyer/seller campaigns
- `healthcare` — HIPAA compliance, LegitScript, restricted targeting
- `finance` — Special Ad Category (credit), required disclosures
- `agency` — Multi-client management, reporting framework
- `generic` — Universal template with platform selection questionnaire

## SEO & AI Search

`/seo` audits a site for classic search ranking **and** for citation by AI answer
engines. They share roughly 80% of their inputs; the 20% that differs is where
most sites fail.

```bash
# Full audit with 4 parallel agents
/seo audit example.com

# Just the AI-visibility layer
/seo aeo example.com

# Why isn't this page ranking?
/seo content example.com/pricing
```

### Two Scores, Not One

The same 110 checks are weighted twice, because the remediation plans differ:

```
Google Score    = Technical(30%) + Content(30%) + Authority(25%) + Schema(15%)
AI Search Score = AEO(40%) + Content(25%) + Schema(20%) + Technical(15%)
```

A site with strong backlinks and weak chunk structure scores well on Google and
badly on AI. A new site with excellent answer-first content scores the reverse.
Collapsing them into one number hides the finding.

### 110 SEO Checks

| Category | Checks | Weight | Key Areas |
|----------|--------|--------|-----------|
| Technical & Indexing | TE01-TE30 | 25% | Crawl, index, JS rendering, Core Web Vitals, mobile |
| Content & Relevance | CO01-CO25 | 25% | Intent match, clusters, cannibalization, E-E-A-T, decay |
| AI Search Readiness | AE01-AE25 | 20% | Crawler access, chunk extractability, entity, off-site |
| Authority & Off-Site | AU01-AU15 | 20% | Referring domains, anchors, reclamation, link gaps |
| Structured Data | SD01-SD15 | 10% | JSON-LD coverage, validity, entity graph |

### Included Scripts

Three Python tools, no API keys required:

```bash
# Crawl and extract on-page SEO + AI-extractability signals
python ~/.claude/skills/seo/scripts/seo_crawl.py https://example.com --crawl 25

# Check which search and AI crawlers can actually reach the site
python ~/.claude/skills/seo/scripts/check_ai_crawlers.py example.com

# Build and track an AI visibility baseline across engines
python ~/.claude/skills/seo/scripts/ai_visibility.py init \
    --brand "Example" --domain example.com \
    --competitors "Alpha,Beta" --topics "your category"
```

`check_ai_crawlers.py` distinguishes **training** crawlers (`GPTBot`,
`ClaudeBot`, `Google-Extended`) from **answer** crawlers (`OAI-SearchBot`,
`ChatGPT-User`, `Claude-SearchBot`, `PerplexityBot`). Only the latter affect
whether you get cited in live AI answers — conflating them is the most common
error in AI-search advice.

### What It Will Not Do

- **Invent metrics.** Traffic, rankings, search volume, backlink counts, and
  Domain Authority are reported only from data you supply or a tool returns.
  Everything else lands in the report's "Not Evaluated" table.
- **Claim AI visibility is precisely measurable.** There is no rank API for AI
  answers. Visibility is sampled with a fixed prompt set and tracked as a
  direction over months, never as a rank.
- **Recommend anything that risks a manual action.** No bought links, PBNs,
  cloaking, invisible-content markup, or fabricated reviews.
- **Promise faster timelines than the benchmarks support.** New content on a new
  domain takes 6-12 months. The skill says so.

## Features

### 190+ Audit Checks
Comprehensive coverage across all platforms with weighted severity scoring:

| Platform | Checks | Key Areas |
|----------|--------|-----------|
| Google Ads | 74 | Search, PMax, Display, YouTube, Demand Gen |
| Meta Ads | 46 | Pixel/CAPI, Creative, Structure, Audience |
| LinkedIn Ads | 25 | B2B targeting, TLA, Lead Gen forms |
| TikTok Ads | 25 | Creative-first, Smart+, TikTok Shop |
| Microsoft Ads | 20 | Google import, Copilot, MSAN |
| Apple Search Ads | 35 | Campaign structure, bids, Creative Sets, MMP, TAP placements |

### Ads Health Score (0-100)
Weighted scoring algorithm with severity multipliers:

| Grade | Score | Action Required |
|-------|-------|-----------------|
| A | 90-100 | Minor optimizations only |
| B | 75-89 | Some improvement opportunities |
| C | 60-74 | Notable issues need attention |
| D | 40-59 | Significant problems present |
| F | <40 | Urgent intervention required |

### Industry Detection
Auto-detects business type from ad account signals (product feeds, conversion events, platform mix, targeting patterns) and loads industry-specific benchmarks and templates.

### Quality Gates
Hard rules enforced during every audit:
- Never recommend Broad Match without Smart Bidding (Google)
- 3x Kill Rule: flag CPA >3x target for immediate pause
- Budget sufficiency: Meta ≥5x CPA/ad set, TikTok ≥50x CPA/ad group
- Learning phase protection: no edits during active learning
- Compliance: auto-check Special Ad Categories (housing/credit/finance)

### Reference Data
12 built-in reference files with 2026-current benchmarks, bidding decision trees, platform specifications, compliance requirements, and conversion tracking implementation guides.

## Architecture

```
~/.claude/skills/ads/              # Paid ads orchestrator
~/.claude/skills/ads/references/   # 20 RAG reference files
~/.claude/skills/ads/scripts/      # Python execution scripts
~/.claude/skills/ads-*/            # 17 paid sub-skills
~/.claude/skills/ads-plan/assets/  # 11 industry templates

~/.claude/skills/seo/              # SEO / AI search orchestrator
~/.claude/skills/seo/references/   # 10 RAG reference files
~/.claude/skills/seo/scripts/      # seo_crawl, check_ai_crawlers, ai_visibility
~/.claude/skills/seo-*/            # 9 SEO sub-skills

~/.claude/agents/audit-*.md        # 14 parallel audit agents
```

### How It Works

1. **Orchestrator** (`/ads`) routes commands to specialized sub-skills
2. **Sub-skills** provide deep single-domain analysis with structured output
3. **Agents** run in parallel during full audits for maximum speed
4. **References** load on-demand (RAG pattern) — only what's needed per analysis
5. **Templates** provide industry-specific strategy frameworks

## How It Analyzes Your Ads

**Claude Ads works with data you provide** — exports, screenshots, or pasted metrics from your ad platform dashboards. It does not connect to any ad platform API automatically.

**To get accurate, account-specific recommendations:**
1. Export your account data (last 30 days recommended)
2. Run the relevant command: `/ads google`, `/ads audit`, etc.
3. Claude will ask for your industry and budget context first — provide these for relevant benchmarks
4. Paste or share your data when prompted

### Live Data Integration (Optional)

For direct API access without manual exports, install the [Google Ads MCP](https://github.com/googleads/google-ads-mcp) alongside Claude Ads. This MCP server connects Claude directly to your Google Ads account via the API.

## FAQ

**Does `/seo` connect to Google Search Console automatically?**
No. It crawls the public site directly and asks you to paste or share Search Console data. Without that data the audit is structural only — it says so explicitly rather than filling the gaps with estimates.

**Can Claude Ads log into my ad manager automatically?**
No. Claude Ads analyzes data you provide (exports, screenshots, or pasted metrics). It doesn't connect to ad platforms automatically. See the Live Data Integration section above for Google Ads API access via MCP.

**Does it use real account data or generic benchmarks?**
Benchmarks are based on industry research (WordStream, Triple Whale, etc.) covering 16,000+ campaigns. They're averages — your results will vary by industry, budget level, and account maturity. Always provide your industry and monthly spend when running audits for the most relevant comparisons.

**Is ad posting or campaign creation still manual?**
Yes. Claude Ads is an audit and strategy tool. It finds issues, recommends fixes, and builds campaign plans — but creating, editing, or posting ads remains manual in your ad platform.

**Why do some recommendations seem off for my account size?**
Benchmarks and best practices differ significantly between a $500/month account and a $50k/month account. Always tell Claude your budget upfront: *"I spend $2k/month on Google Ads for a local plumbing business"* gives much better results than running `/ads google` without context.

**Does it support [platform] ads?**
Currently supported: Google, Meta (Facebook/Instagram), YouTube, LinkedIn, TikTok, Microsoft/Bing, and Apple Search Ads. Pinterest and other platforms are on the roadmap.

## Requirements

- Claude Code CLI
- Python 3.10+ with `requests` (for `/seo` crawling and crawler checks)
- Playwright (optional, for live landing page analysis and brand screenshots)

`ai_visibility.py` is stdlib-only and needs no dependencies.

## Uninstall

### Unix/macOS/Linux

```bash
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-ads/main/uninstall.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/AgriciDaniel/claude-ads/main/uninstall.ps1 | iex
```

## Related Projects

- [Claude SEO](https://github.com/AgriciDaniel/claude-seo) — Comprehensive SEO analysis skill for Claude Code

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built for Claude Code by [@AgriciDaniel](https://github.com/AgriciDaniel)
