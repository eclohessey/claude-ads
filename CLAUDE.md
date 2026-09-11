# Claude Ads — Paid Advertising + SEO / AI Search Skills

## Project Overview

This repository contains two Tier 4 Claude Code skills sharing one architecture,
following the Agent Skills open standard and the 3-layer model (directive,
orchestration, execution):

- **`ads`** — paid advertising analysis across Google, Meta, YouTube, LinkedIn,
  TikTok, Microsoft, and Apple Search Ads. 17 sub-skills, 10 subagents,
  11 industry templates, 225+ weighted audit checks.
- **`seo`** — organic search ranking and AI-answer visibility (AEO/GEO) for
  ChatGPT, Claude, Perplexity, and Google AI Overviews. 9 sub-skills,
  4 subagents, 110 weighted checks producing separate Google and AI scores.

`ads` covers earned-by-paying; `seo` covers earned. They are independent — either
can be installed and used without the other.

## Architecture

```
claude-ads/
  CLAUDE.md                          # Project instructions (this file)
  ads/                               # Main orchestrator skill
    SKILL.md                         # Entry point, routing table, core rules
    references/                      # On-demand knowledge files (12 files)
    scripts/                         # Python execution scripts
  skills/                            # 12 specialized sub-skills
    ads-audit/SKILL.md              # Full multi-platform audit
    ads-google/SKILL.md            # Google Ads deep analysis
    ads-meta/SKILL.md              # Meta/Facebook Ads analysis
    ads-youtube/SKILL.md           # YouTube Ads analysis
    ads-linkedin/SKILL.md         # LinkedIn Ads analysis
    ads-tiktok/SKILL.md           # TikTok Ads analysis
    ads-microsoft/SKILL.md        # Microsoft/Bing Ads analysis
    ads-creative/SKILL.md         # Creative quality assessment
    ads-landing/SKILL.md          # Landing page analysis
    ads-budget/SKILL.md           # Budget allocation optimization
    ads-plan/SKILL.md             # Strategic ad planning by industry
    ads-competitor/SKILL.md       # Competitor ad research
  seo/                               # SEO / AI search orchestrator skill
    SKILL.md                        # Entry point, routing table, quality gates
    references/                     # On-demand knowledge files (10 files)
  skills/                            # (continued) 9 SEO sub-skills
    seo-audit/SKILL.md             # Full SEO + AI search audit
    seo-technical/SKILL.md         # Crawl, index, render, Core Web Vitals
    seo-content/SKILL.md           # Content quality, intent, E-E-A-T
    seo-aeo/SKILL.md               # AI search readiness (AEO/GEO)
    seo-schema/SKILL.md            # Structured data and entity graph
    seo-authority/SKILL.md         # Backlinks, brand signals, link gaps
    seo-keywords/SKILL.md          # Query research and intent mapping
    seo-competitor/SKILL.md        # Competitive gap analysis
    seo-local/SKILL.md             # Local SEO and Google Business Profile
  agents/                            # 6 parallel subagents
    audit-google.md                # Google Ads audit agent
    audit-meta.md                  # Meta Ads audit agent
    audit-creative.md              # Creative quality agent
    audit-tracking.md              # Conversion tracking agent
    audit-budget.md                # Budget analysis agent
    audit-compliance.md            # Compliance verification agent
    audit-seo-technical.md         # Technical SEO agent (TE01-TE30)
    audit-seo-content.md           # Content quality agent (CO01-CO25)
    audit-seo-aeo.md               # AI search readiness agent (AE01-AE25, SD01-SD15)
    audit-seo-authority.md         # Off-site authority agent (AU01-AU15)
  install.sh / install.ps1          # Cross-platform installers
  uninstall.sh / uninstall.ps1      # Cross-platform uninstallers
```

## Commands

| Command | Purpose |
|---------|---------|
| `/ads audit` | Full multi-platform audit with 6 parallel agents |
| `/ads google` | Google Ads deep analysis |
| `/ads meta` | Meta/Facebook Ads analysis |
| `/ads youtube` | YouTube Ads analysis |
| `/ads linkedin` | LinkedIn Ads analysis |
| `/ads tiktok` | TikTok Ads analysis |
| `/ads microsoft` | Microsoft/Bing Ads analysis |
| `/ads creative` | Creative quality and fatigue assessment |
| `/ads landing` | Landing page conversion analysis |
| `/ads budget` | Budget allocation optimization |
| `/ads plan <type>` | Strategic ad planning by industry |
| `/ads competitor` | Competitor ad research |
| `/seo audit <url>` | Full SEO + AI search audit → two scores |
| `/seo technical <url>` | Crawl, index, render, Core Web Vitals |
| `/seo content <url>` | Content quality, intent match, E-E-A-T |
| `/seo aeo <url>` | AI search readiness for ChatGPT/Claude/Perplexity |
| `/seo schema <url>` | Structured data and entity graph |
| `/seo authority <url>` | Backlinks, brand signals, link gaps |
| `/seo keywords <topic>` | Query mapping by intent |
| `/seo competitor <url>` | Competitive gap analysis |
| `/seo local <url>` | Local SEO and Google Business Profile |

## Development Rules

- Keep SKILL.md files under 500 lines / 5000 tokens
- Reference files should be focused and under 200 lines
- Scripts must have docstrings, CLI interface, and JSON output
- Follow kebab-case naming for all skill directories
- Agents invoked via Task tool with `context: fork`, never via Bash
- No hardcoded credentials; use MCP servers for external API access

## SEO Skill Rules

- **Never fabricate metrics.** Traffic, rankings, search volume, backlink counts,
  and Domain Authority are reported only from supplied data or tool output.
  Anything unmeasured goes in the report's "Not Evaluated" table.
- **Always report two scores.** Google Search and AI Search are weighted from the
  same checks but diverge — collapsing them destroys the finding.
- **Distinguish training crawlers from answer crawlers.** `GPTBot`, `ClaudeBot`,
  and `Google-Extended` are training; `OAI-SearchBot`, `ChatGPT-User`,
  `Claude-SearchBot`, and `PerplexityBot` ground live answers. Only the latter
  affect citation.
- **Never recommend tactics that risk a manual action** — bought links, PBNs,
  cloaking, marking up invisible content, fabricated reviews.
- **Never promise timelines faster than `seo/references/benchmarks.md`.**
- Every finding cites evidence: a URL, status code, header, or measured count.
