# Report Template

Standard output format for `/seo audit`. Write to `SEO-AUDIT-REPORT.md` in the
working directory.

## Structure

```markdown
# SEO & AI Search Audit — <domain>
Date: <YYYY-MM-DD> · Pages crawled: <n> · Business type: <type>

## Scores

Google Search Score:  XX/100 (Grade X)
AI Search Score:      XX/100 (Grade X)

Technical & Indexing      ████████░░  XX/100
Content & Relevance       ██████░░░░  XX/100
AI Search Readiness       ███░░░░░░░  XX/100
Authority & Off-Site      █████░░░░░  XX/100
Structured Data & Entity  ███████░░░  XX/100

## The One-Paragraph Read

<What is actually wrong, in plain language, and what fixing it is worth.
Lead with the divergence between the two scores if there is one.>

## Quick Wins (Critical/High severity, S effort)

| # | Finding | Check | Impact | Effort | Fix |
|---|---------|-------|--------|--------|-----|

## Critical Findings

### [TE01] <Title>
**Severity**: Critical · **Effort**: S · **Category**: Technical
**Evidence**: <what was observed, with the URL or data point>
**Why it matters**: <mechanism, not a platitude>
**Fix**: <specific, actionable step — code, config, or content>

## Full Check Results

| ID | Check | Result | Severity | Note |
|----|-------|--------|----------|------|

## Not Evaluated

| Check | Why | What is needed |
|-------|-----|----------------|

## 90-Day Action Plan

### Weeks 1-2 — Unblock
### Weeks 3-6 — Build
### Weeks 7-12 — Compound

## Measurement Baseline

| Metric | Today | Source | Re-check |
|--------|-------|--------|----------|
```

## Writing Rules

- **Lead with evidence.** Every finding cites a URL, a status code, a count, or
  a quoted line. No finding is reported from assumption.
- **Say what is unknown.** The "Not Evaluated" table is mandatory. A check that
  needs Search Console access goes there, never silently into the pass column.
- **Never invent metrics.** Do not state traffic, ranking positions, keyword
  volumes, or backlink counts unless the user supplied the data or a tool
  returned it. Estimating these is the fastest way to make the whole report
  untrustworthy.
- **One fix per finding**, specific enough to hand to a developer.
- **Separate the two scores everywhere.** The whole point is that they diverge.
- **Timelines come from `references/benchmarks.md`.** Do not promise faster.

## Tone

Direct and unhedged where the evidence is solid; explicit about uncertainty
where it is not. No growth-marketing register — the reader is deciding where to
spend engineering hours.
