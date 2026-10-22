# Keyword & Query Research

The goal is not a keyword list. It is a map of the questions buyers ask, which
page owns each one, and what has to be true for that page to win.

## Intent Taxonomy

| Intent | Query shape | Page format that wins | Conversion value |
|--------|-------------|----------------------|------------------|
| Informational | "what is", "how to", "why does" | Guide, tutorial, definition | Low, high volume |
| Comparison | "X vs Y", "best", "alternatives to" | Comparison table, roundup | **Highest ROI** |
| Commercial | "pricing", "cost", "review" | Pricing page, review page | High |
| Transactional | "buy", "free trial", "demo" | Product, signup page | Highest |
| Navigational | brand names | Homepage, brand pages | Defensive |

**Prioritization rule**: most sites over-invest in informational content and
under-invest in comparison and commercial. Those are also the queries AI answer
engines get asked most often. Build them first.

## Building the Query Map

1. **Seed from reality, not tools.** Sales call recordings, support tickets,
   and the site's own search logs contain the exact phrasing buyers use.
2. **Mine Search Console.** Queries at position 8-20 are the cheapest wins on
   the site — the page already ranks, it just needs depth or a better title.
3. **Harvest SERP features.** "People also ask", related searches, and
   autocomplete give the query fan-out AI engines perform internally.
4. **Mine competitor structure.** Their nav and sitemap show which intents they
   decided were worth a page.
5. **Cluster by intent, not by string.** "voice ai pricing" and "how much does
   voice ai cost" are one page, not two.
6. **Assign one owner page per cluster.** Two pages for one intent is
   cannibalization (CO01).

## Cluster Template

```
PILLAR: [broad topic]        → /topic/
  ├── [subtopic 1]           → /topic/subtopic-1/
  ├── [subtopic 2]           → /topic/subtopic-2/
  ├── [X vs Y]               → /compare/x-vs-y/
  ├── [alternatives to X]    → /alternatives/x/
  ├── [topic pricing]        → /pricing/
  └── [topic for <segment>]  → /solutions/segment/
```

Every supporting page links up to the pillar with descriptive anchor text; the
pillar links down to each. This is what turns a pile of posts into a cluster.

## Difficulty Assessment Without Paid Tools

Search the target query and read page one:

| Signal | Reading |
|--------|---------|
| Top results are forums, Reddit, or thin pages | Winnable now |
| Top results are direct competitors your size | Winnable in 3-6 months |
| Top results are Wikipedia, major publishers, Amazon | Not winnable — target a longer-tail variant |
| Results do not match the query's intent | Opportunity: nobody has built the right page |
| An AI Overview answers it completely | Low click potential — target it for citation, not traffic |

## Query Selection Scorecard

Score each candidate 1-5 and rank by total:

| Factor | Weight |
|--------|--------|
| Buyer intent (how close to purchase) | 3x |
| Winnability (per the table above) | 3x |
| Volume | 1x |
| Existing site relevance (do we already rank anywhere for it) | 2x |
| AI-answer exposure (is it a question an assistant gets asked) | 2x |

Volume is deliberately the lowest weight. Ten buyers beat a thousand browsers.

## AI-Era Additions

Classic keyword research misses these; add them explicitly:

- **Conversational long-tail.** People type three words into Google and speak
  full sentences to an assistant. Target both phrasings.
- **Comparison and alternatives queries.** The single highest-value cluster for
  AI visibility — assistants get asked "best X" constantly.
- **"Best X for <specific segment>".** Easier to own than "best X" and converts
  better.
- **Questions your competitors' docs answer but yours do not.** Assistants cite
  whoever documented it.

## Deliverable Format

`QUERY-MAP.md` with one row per cluster:

| Cluster | Primary query | Intent | Owner page | Status | Priority |
|---------|--------------|--------|-----------|--------|----------|
| Pricing | "ai voice agent pricing" | Commercial | /pricing/ | Exists, thin | P1 |
| Alternatives | "alternatives to X" | Comparison | — | Missing | P1 |
