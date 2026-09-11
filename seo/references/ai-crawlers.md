# AI & Search Crawler Reference

Verify with `scripts/check_ai_crawlers.py <domain>`. Crawler names change; treat
this table as a starting point and confirm against server logs.

## The Three Purposes

Conflating these is the most common mistake in AI-search advice:

| Purpose | What it does | Blocking it means |
|---------|--------------|-------------------|
| **Search** | Builds a search index | You disappear from that search engine |
| **Answer** | Fetches pages live to ground an AI answer | You disappear from AI citations |
| **Training** | Collects data for model training | You are absent from model weights, but can still be cited live |

Blocking training crawlers while allowing answer crawlers is a coherent
position: you stay citable in live AI answers without contributing training
data. Blocking answer crawlers is what silently removes you from AI results.

## Crawler Table

| User agent | Owner | Purpose | Executes JS |
|------------|-------|---------|-------------|
| `Googlebot` | Google | Search | Yes |
| `Google-Extended` | Google | Training / Gemini grounding control | n/a |
| `Bingbot` | Microsoft | Search (also feeds Copilot) | Partial |
| `DuckDuckBot` | DuckDuckGo | Search | No |
| `Applebot` | Apple | Search (Siri, Spotlight) | Yes |
| `Applebot-Extended` | Apple | Training | n/a |
| `GPTBot` | OpenAI | Training | No |
| `OAI-SearchBot` | OpenAI | Answer (ChatGPT search) | No |
| `ChatGPT-User` | OpenAI | Answer (user-initiated fetch) | No |
| `ClaudeBot` | Anthropic | Training | No |
| `Claude-SearchBot` | Anthropic | Answer | No |
| `Claude-User` | Anthropic | Answer (user-initiated fetch) | No |
| `PerplexityBot` | Perplexity | Answer | No |
| `Perplexity-User` | Perplexity | Answer (user-initiated fetch) | No |
| `Amazonbot` | Amazon | Answer (Alexa) | No |
| `meta-externalagent` | Meta | Training | No |
| `CCBot` | Common Crawl | Training (feeds many models) | No |

**The "Executes JS" column is the one that matters most.** Googlebot renders
JavaScript; nearly nothing else does. A client-rendered site can rank on Google
and be completely invisible to every AI answer engine.

## Recommended robots.txt — Maximum Visibility

The default for most businesses: allow everything, declare the sitemap.

```
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

## Recommended robots.txt — Citable, Not Trainable

For sites that want AI citations without contributing training data:

```
# Search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# AI answer engines — these produce citations
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

# Training crawlers — opted out
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Note the cost: blocking `Google-Extended` may reduce Gemini grounding. It does
not affect Google Search rankings — those are governed by `Googlebot` alone.

## robots.txt Precedence Rules

Crawlers that honor the standard apply these, in order:

1. The **most specific matching user-agent group wins**. A `Googlebot` group
   fully replaces the `*` group for Googlebot — rules are not merged.
2. Within a group, the **longest matching path rule wins**.
3. On an equal-length tie, **Allow beats Disallow**.
4. `Disallow:` with an empty value allows everything.
5. A missing or 404 robots.txt means **everything is allowed**.

A common failure: adding a `User-agent: GPTBot` group and assuming the `*`
group's `Sitemap` and `Allow` rules still apply to it. They do not.

## Common Blocking Mistakes

| Mistake | Effect |
|---------|--------|
| WAF/Cloudflare bot rules returning 403 to AI agents | robots.txt looks fine, crawlers still cannot fetch — check server logs, not just robots.txt |
| Blocking `*` then allowing specific bots after | Order does not matter, but the `*` group never applies to a bot with its own group |
| Rate-limiting by user agent | Partial crawls, stale content in answers |
| `noindex` on paginated or category pages | Removes hub pages that AI crawlers use to discover content |

## llms.txt

A proposed `/llms.txt` markdown file summarizing the site for LLMs. Adoption by
major crawlers remains limited — treat it as cheap and speculative (AE25), and
never present it as a substitute for the checks above.

```markdown
# Example

> One-sentence description of what the company does and for whom.

## Docs
- [Getting started](https://example.com/docs/start): Setup in under 10 minutes
- [Pricing](https://example.com/pricing): Plans and limits

## About
- [Company](https://example.com/about): Team, founding, mission
```
