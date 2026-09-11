# SEO & AI Search Audit Scoring System

<!-- 110 weighted checks across 5 categories -->

## Weighted Scoring Algorithm

Identical in shape to the ads scoring system, so results are comparable:

```
S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100
```

- `C_pass` = check passed (1), WARNING (0.5), failed (0)
- `W_sev` = severity multiplier of the individual check
- `W_cat` = category weight
- Result: 0-100 Search Health Score

## Severity Multipliers

| Severity | Multiplier | Criteria |
|----------|-----------|----------|
| Critical | 5.0 | Blocks indexing or citation entirely. Traffic is zero or at risk. |
| High | 3.0 | Materially suppresses rankings or AI citations. Fix within 14 days. |
| Medium | 1.5 | Optimization opportunity. Fix within 60 days. |
| Low | 0.5 | Best practice, marginal impact. Backlog. |

## Category Weights

| Category | Weight | Checks | Rationale |
|----------|--------|--------|-----------|
| Technical & Indexing | 25% | TE01-TE30 | A page that cannot be crawled or rendered scores zero everywhere else |
| Content Quality & Relevance | 25% | CO01-CO25 | The largest controllable ranking input; also what gets quoted |
| AI Search Readiness | 20% | AE01-AE25 | Retrieval and citation mechanics; distinct from classic ranking |
| Authority & Off-Site | 20% | AU01-AU15 | Links still dominate Google; third-party mentions dominate AI answers |
| Structured Data & Entity | 10% | SD01-SD15 | How machines resolve what the site is; enables rich results |

## Two Scores, Not One

Report both. They diverge often, and the divergence is the insight.

```
Google Score = Technical(30%) + Content(30%) + Authority(25%) + Schema(15%)
AI Search Score = AEO(40%) + Content(25%) + Schema(20%) + Technical(15%)
```

A site with strong backlinks and weak chunk structure scores well on Google and
badly on AI. A new site with excellent answer-first content scores the reverse.
The remediation plans are different, so never collapse them into one number.

## Grading

| Grade | Score | Action Required |
|-------|-------|-----------------|
| A | 90-100 | Minor optimizations only |
| B | 75-89 | Some improvement opportunities |
| C | 60-74 | Notable issues need attention |
| D | 40-59 | Significant problems present |
| F | <40 | Urgent intervention required |

## Priority Levels

- **Critical**: Indexing/citation blocked, or traffic actively lost (fix immediately)
- **High**: Significant ranking or visibility drag (fix within 14 days)
- **Medium**: Optimization opportunity (fix within 60 days)
- **Low**: Best practice, minor impact (backlog)

## Effort / Impact Ranking

Every finding gets both. Sort the action plan by impact-per-effort, not by score.

| Effort | Meaning |
|--------|---------|
| S | Config change or single-page edit, under 1 hour |
| M | Template change or one content piece, 1-3 days |
| L | Multi-page rewrite, migration, or link campaign, weeks |

Quick Wins = Critical/High severity at S effort. Always lead the report with these.

## Scoring Rules

- A check that cannot be evaluated (no data, no access) is **N/A** and is excluded
  from the denominator. Never score N/A as a pass — say what data is missing.
- Site-wide percentage checks grade on thresholds, not binary: ≥90% of pages
  compliant = PASS, 60-89% = WARNING, <60% = FAIL.
- Never report a score derived from fewer than 5 crawled pages without saying so.
