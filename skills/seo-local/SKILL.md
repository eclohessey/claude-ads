---
name: seo-local
description: >
  Local SEO audit covering Google Business Profile, NAP consistency, local
  pack ranking factors, review velocity, and location page quality. Use when
  user says "local SEO", "Google Business Profile", "Google My Business",
  "map pack", "local pack", "near me", "NAP", "local rankings", or
  "multi-location SEO".
---

# Local SEO

## Applicability Gate

Local SEO applies when the business serves customers at a physical location or
within a defined service area. For a pure-online SaaS or e-commerce business,
skip this skill and say why rather than producing irrelevant findings.

## Process

1. Confirm the business is genuinely local (above)
2. Audit the Google Business Profile
3. Check NAP consistency across the major directories
4. Audit location pages on the site
5. Assess review profile and velocity
6. Check local schema (`LocalBusiness`, `PostalAddress`, `OpeningHoursSpecification`)

## Local Pack Ranking Factors

Roughly ordered by influence:

| Factor | Weight | Notes |
|--------|--------|-------|
| Proximity to searcher | Highest | Not controllable — stop trying |
| Google Business Profile completeness | High | Category, hours, attributes, services, photos |
| Review quantity, velocity, and rating | High | Recency matters as much as count |
| NAP consistency across the web | High | Conflicting data suppresses confidence |
| On-site local relevance | Medium | Location pages, embedded map, local content |
| Local link and citation signals | Medium | Chamber of commerce, local press, sponsorships |
| Behavioral signals | Medium | Clicks to call, direction requests, website clicks |

## Google Business Profile Checklist

- Primary category is the most specific accurate option — this is the single
  highest-leverage GBP field
- Secondary categories added where genuinely applicable
- Complete hours including holiday hours
- Services and products populated with descriptions
- Photos added regularly; geotagged where possible
- Posts published on a cadence
- Q&A section seeded and actively monitored
- Every review responded to, positive and negative
- Messaging enabled if it will be answered promptly

## NAP Consistency

Name, address, and phone must be byte-identical everywhere: GBP, website footer,
Apple Maps, Bing Places, Yelp, Facebook, industry directories, and any
aggregator feeding them. "Suite 200" versus "Ste. 200" counts as a conflict.

This also feeds AE13 — entity consistency is what lets an AI assistant resolve
your business as one entity rather than several.

## Location Pages

For multi-location businesses, each location needs a page with genuinely unique
content — not a templated page with the city name swapped in (CO07).

Include: local address and phone, embedded map, location-specific staff,
location-specific services, local testimonials, and the area served in prose.

## Review Strategy

- Ask consistently, right after a successful interaction
- Never gate reviews (asking only happy customers) — a policy violation
- Never buy reviews
- Respond to everything within 48 hours
- Velocity beats volume: 3 reviews a month beats 40 reviews two years ago

## Output

### Deliverables
- `LOCAL-SEO-REPORT.md` — GBP audit, NAP audit, location page assessment
- NAP inconsistency table: directory · current value · correct value
- GBP optimization checklist with specific field values to set
- `LocalBusiness` JSON-LD ready to paste, with the site's real values
