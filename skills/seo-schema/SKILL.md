---
name: seo-schema
description: >
  Structured data and entity graph audit. Validates JSON-LD coverage,
  correctness, and entity linking for rich results and AI entity resolution.
  Use when user says "schema markup", "structured data", "JSON-LD",
  "rich results", "rich snippets", "schema.org", "entity SEO", or
  "why don't I get star ratings".
---

# Structured Data & Entity Graph

## Process

1. Read `seo/references/schema-reference.md` for checks SD01-SD15 and patterns
2. Extract existing schema from `crawl.json` (`schema.types`, `invalid_blocks`)
3. Map required schema types to the site's page templates
4. Validate every block: JSON syntax, vocabulary, and content match
5. Write missing markup as ready-to-paste JSON-LD

## What Schema Does and Does Not Do

- **Does not** directly improve rankings. Anyone claiming otherwise is selling something.
- **Does** drive rich results — stars, prices, FAQs, breadcrumbs, sitelinks.
- **Does** help machines resolve what your site *is*, which is why it carries
  double weight in the AI Search Score versus the Google Score.

## Coverage Map by Template

| Template | Required | Recommended |
|----------|----------|-------------|
| Homepage | `Organization` or `LocalBusiness`, `WebSite` | `SearchAction` |
| Product | `Product` + `Offer` | `AggregateRating` (real reviews only) |
| SaaS product | `SoftwareApplication` + `Offer` | `AggregateRating` |
| Blog / article | `BlogPosting` or `Article` | `Person` author, `BreadcrumbList` |
| Author page | `Person` | `sameAs` to verifiable profiles |
| FAQ section | `FAQPage` | — |
| How-to content | `HowTo` | — |
| Local business | `LocalBusiness` + `PostalAddress` + `OpeningHoursSpecification` | `GeoCoordinates` |
| Any nested page | `BreadcrumbList` | — |

## The Entity Graph

The single highest-value item is usually `Organization` with a complete
`sameAs` array. It is how a search engine or model connects your site to your
LinkedIn, Crunchbase, GitHub, and Wikidata records and treats them as one
entity. Use `@id` to join nodes into one graph rather than repeating them —
see the minimum viable graph in `seo/references/schema-reference.md`.

## Validation Workflow

1. **JSON syntax** — `crawl.json`'s `invalid_blocks` count, or `python -m json.tool`.
   A single syntax error silently voids the entire block (SD05).
2. **Vocabulary** — schema.org validator for type and property correctness.
3. **Eligibility** — Google Rich Results Test.
4. **At scale** — Search Console → Enhancements, after deployment.

Re-validate after every template change. Schema breaks silently.

## Hard Rules

- Never mark up content that is not visible on the page (SD06) — manual-action risk
- Never fabricate ratings, review counts, or prices (SD14)
- Never use `FAQPage` on content that is not genuinely a question and answer
- Schema must be server-rendered, not injected client-side (SD04)
- JSON-LD, not microdata or RDFa (SD03)

## Output

### Deliverables
- `SCHEMA-REPORT.md` — SD01-SD15 results, coverage map, validation errors
- Ready-to-paste JSON-LD blocks for every missing type, filled with the site's
  real values — not placeholders
- Priority order: `Organization`+`sameAs` first, then page-type schema, then
  optional enhancements
