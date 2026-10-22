# Content Quality & Relevance Audit — 25 Checks (CO01-CO25)

Category weight: 25%. Evaluated per template and per top-20 page by traffic or
strategic value, not across every URL.

## Intent & Coverage (CO01-CO07)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| CO01 | Every target query has exactly one page that owns it | Critical | No two pages competing for the same primary intent (keyword cannibalization) |
| CO02 | Page format matches SERP intent | High | Informational query → guide; commercial → comparison; transactional → product/pricing |
| CO03 | Topic clusters exist, not orphan posts | High | Each pillar page has ≥5 supporting pages linking up to it |
| CO04 | Content depth matches the competing set | High | Covers the subtopics the top 5 results cover; length is a symptom, not a target |
| CO05 | Bottom-funnel pages exist | High | Pricing, comparison, alternatives, integrations, use-case pages published |
| CO06 | No thin pages in the index | Medium | <300-word pages either expanded, consolidated, or noindexed |
| CO07 | No duplicate or near-duplicate bodies | High | Templated location/product pages carry unique substance, not spun text |

## On-Page Fundamentals (CO08-CO14)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| CO08 | Unique, specific title tag ≤60 chars | High | Primary term near the front; no site-wide boilerplate prefix |
| CO09 | Unique meta description 140-160 chars | Medium | Written as ad copy for the click, not a keyword dump |
| CO10 | Exactly one H1 per page, matching the page's promise | High | Reflects the query the page targets |
| CO11 | Logical H2/H3 hierarchy | Medium | No skipped levels; subheads describe real sections |
| CO12 | Primary term appears in title, H1, first 100 words, and URL | Medium | Naturally, not stuffed |
| CO13 | Internal links use descriptive anchor text | Medium | No "click here"; ≥3 contextual internal links per content page |
| CO14 | Images have descriptive filenames and alt text | Low | Alt describes content, not "image1.png" |

## Quality & Trust — E-E-A-T (CO15-CO20)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| CO15 | Named author with a real bio and credentials | High | Author page exists, links to verifiable profiles |
| CO16 | Original information present | Critical | Proprietary data, testing, examples, or firsthand experience — not a synthesis of page-one results |
| CO17 | Claims are sourced | High | Statistics link to primary sources, not to other blogs citing the same stat |
| CO18 | Publish and genuine last-updated dates shown | Medium | Dates reflect real revision; no date-bumping without changes |
| CO19 | About, contact, and methodology pages exist | High | Real company identity: address, team, how conclusions are reached |
| CO20 | YMYL content reviewed by a qualified expert | Critical | Required for health, finance, legal, safety topics; N/A otherwise |

## Freshness & Maintenance (CO21-CO25)

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| CO21 | Top pages reviewed within 12 months | Medium | Stale facts, prices, screenshots, and year references updated |
| CO22 | Decaying pages identified and refreshed | High | Pages down >30% YoY in clicks have a refresh or consolidate decision |
| CO23 | No broken internal or external links | Medium | <1% of links return 4xx/5xx |
| CO24 | Content inventory maintained | Low | A list of every indexable page with owner, intent, and last review date |
| CO25 | Pruning decisions made for zero-traffic pages | Medium | Pages with no clicks/impressions in 12 months improved, merged, or removed |

## The Refresh Decision Tree

For any underperforming page:

```
Impressions high, clicks low       → rewrite title + meta description (CO08/CO09)
Impressions low, position 11-20    → expand depth and add internal links (CO04/CO13)
Impressions low, position >30      → intent mismatch; rewrite format (CO02)
Two pages trading positions        → consolidate, 301 the weaker (CO01)
Traffic decayed from a good base   → refresh facts and dates (CO21/CO22)
Never ranked, no links, no traffic → prune (CO25)
```

## Writing Rules That Serve Both Google and AI

These pay double — they raise snippet capture and citation rate at once:

1. **Answer in the first 40-60 words**, then go deep. See AE02.
2. **One idea per section**, with a subhead that names it.
3. **Specific over general**: "reduced call handling time 34%" beats "improved efficiency".
4. **Name the entity, not the pronoun**, at the start of each section. See AE06.
5. **Comparison content belongs in a table**, not in prose paragraphs.
