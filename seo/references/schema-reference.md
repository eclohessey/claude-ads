# Structured Data & Entity Audit — 15 Checks (SD01-SD15)

Category weight: 10%. Schema does not directly boost rankings, but it drives
rich results, and it is how machines resolve what your site *is* — which is why
it carries outsized weight in the AI Search Score.

## Checks

| ID | Check | Severity | Pass Criteria |
|----|-------|----------|---------------|
| SD01 | `Organization` (or `LocalBusiness`) schema on the homepage | High | Includes name, url, logo, description, `sameAs` |
| SD02 | `sameAs` links to authoritative profiles | High | LinkedIn, Crunchbase, Wikidata, GitHub, primary social |
| SD03 | JSON-LD format, not microdata or RDFa | Medium | Google's stated preference; also easiest to maintain |
| SD04 | Schema present in server-rendered HTML | High | Not injected client-side — see TE14 |
| SD05 | All JSON-LD parses as valid JSON | Critical | A syntax error voids the whole block silently |
| SD06 | Schema matches visible page content | Critical | No marked-up content absent from the page — this is a manual-action risk |
| SD07 | `WebSite` schema with `SearchAction` where site search exists | Low | Enables sitelinks search box |
| SD08 | `BreadcrumbList` on nested pages | Medium | Improves SERP display and internal-structure signals |
| SD09 | `Article`/`BlogPosting` on editorial pages | Medium | With `headline`, `author`, `datePublished`, `dateModified`, `image` |
| SD10 | `Product` + `Offer` on product pages | High | With price, currency, availability; required for shopping rich results |
| SD11 | `FAQPage` on genuine Q&A sections | Medium | Rich-result eligibility is now limited, but the markup still aids extraction |
| SD12 | `HowTo` on step-by-step content | Low | Where genuinely procedural |
| SD13 | `Person` schema on author pages, linked from articles | Medium | Supports E-E-A-T entity resolution |
| SD14 | `AggregateRating`/`Review` only from real, verifiable reviews | Critical | Self-serving fabricated ratings are a policy violation |
| SD15 | No orphaned or duplicate entity nodes | Medium | Use `@id` to link nodes into one graph rather than repeating them |

## Minimum Viable Graph

Every site should ship at least this on the homepage. The `@id` values are what
join the nodes into a single entity graph (SD15).

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example",
      "url": "https://example.com",
      "logo": "https://example.com/logo.png",
      "description": "One plain sentence naming the category and who it is for.",
      "sameAs": [
        "https://www.linkedin.com/company/example",
        "https://www.crunchbase.com/organization/example",
        "https://github.com/example"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com",
      "name": "Example",
      "publisher": { "@id": "https://example.com/#organization" }
    }
  ]
}
```

## Article Pattern

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Title matching the visible H1",
  "datePublished": "2026-01-15T09:00:00Z",
  "dateModified": "2026-09-02T11:30:00Z",
  "author": {
    "@type": "Person",
    "name": "Jane Doe",
    "url": "https://example.com/authors/jane-doe"
  },
  "publisher": { "@id": "https://example.com/#organization" },
  "mainEntityOfPage": "https://example.com/blog/post-slug"
}
```

## Product Pattern

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "description": "What it does, in one sentence.",
  "brand": { "@id": "https://example.com/#organization" },
  "offers": {
    "@type": "Offer",
    "price": "49.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/pricing"
  }
}
```

## SaaS / Software Pattern

Use `SoftwareApplication` for products, not `Product`, when the offering is software:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Example",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "99.00",
    "priceCurrency": "USD"
  }
}
```

## Validation

Always validate before shipping, and re-validate after any template change:

- **Google Rich Results Test** — eligibility for rich results
- **Schema.org validator** — vocabulary correctness
- **Search Console → Enhancements** — errors at scale across the live index

## Hard Rules

- Never mark up content that is not visible on the page (SD06).
- Never fabricate ratings, review counts, or prices (SD14).
- Never mark up `FAQPage` on content that is not actually a question and answer.
- A JSON syntax error silently discards the entire block — validate, do not assume (SD05).
