#!/usr/bin/env python3
"""
Crawl a site and extract on-page SEO + AI-search (AEO) signals.

Dependency-light: uses `requests` for fetching and the stdlib HTML parser for
extraction, so it runs anywhere the other Claude Ads scripts run.

Usage:
    python seo_crawl.py https://example.com
    python seo_crawl.py https://example.com --crawl 25 --json -o crawl.json
    python seo_crawl.py https://example.com/pricing --json
"""

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag, urlparse

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install -r requirements.txt")
    sys.exit(1)


USER_AGENT = (
    "Mozilla/5.0 (compatible; ClaudeSEO/1.0; "
    "+https://github.com/AgriciDaniel/claude-ads)"
)
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Headings phrased as questions extract far better into AI answers.
QUESTION_RE = re.compile(
    r"^\s*(who|what|when|where|why|how|which|can|does|do|is|are|should|will)\b"
    r"|\?\s*$",
    re.IGNORECASE,
)
# Pronouns/deictics that break a chunk when it is lifted out of page context.
DANGLING_RE = re.compile(
    r"^\s*(it|they|this|that|these|those|he|she|we)\b", re.IGNORECASE
)
SKIP_EXT = (
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".avif",
    ".zip", ".mp4", ".mp3", ".css", ".js", ".ico", ".woff", ".woff2",
)
NON_CONTENT_TAGS = {"script", "style", "noscript", "template", "svg"}


class PageParser(HTMLParser):
    """Single-pass extraction of the signals the SEO checklists score."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self.meta = {}
        self.canonical = None
        self.hreflang = []
        self.lang = None
        self.headings = []          # (level, text)
        self.jsonld_blocks = []
        self.links = []             # (href, rel, text)
        self.images = []            # (src, alt)
        self.text_parts = []
        self.tag_counts = Counter()
        self.first_paragraph = None
        self.script_chars = 0

        self._stack = []
        self._capture = None        # ("h", level) | ("jsonld",) | ("a",)
        self._buf = []
        self._link_href = None
        self._link_rel = None

    # -- helpers -----------------------------------------------------------
    def _flush(self):
        text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
        self._buf = []
        return text

    def _in_non_content(self):
        return any(t in NON_CONTENT_TAGS for t in self._stack)

    # -- parser hooks ------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._stack.append(tag)
        self.tag_counts[tag] += 1

        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]
        elif tag == "meta":
            key = a.get("name") or a.get("property") or a.get("http-equiv")
            if key and "content" in a:
                self.meta[key.lower()] = a["content"]
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if "canonical" in rel:
                self.canonical = a.get("href")
            if "alternate" in rel and a.get("hreflang"):
                self.hreflang.append({"hreflang": a["hreflang"], "href": a.get("href")})
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._capture = ("jsonld",)
            self._buf = []
        elif tag in ("h1", "h2", "h3", "h4"):
            self._capture = ("h", int(tag[1]))
            self._buf = []
        elif tag == "a" and a.get("href"):
            self._capture = ("a",)
            self._link_href = a["href"]
            self._link_rel = (a.get("rel") or "").lower()
            self._buf = []
        elif tag == "img":
            self.images.append((a.get("src"), a.get("alt")))

    def handle_startendtag(self, tag, attrs):
        # Void elements (<meta/>, <link/>, <img/>) never reach handle_endtag.
        self.handle_starttag(tag, attrs)
        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_endtag(self, tag):
        if self._capture:
            kind = self._capture[0]
            if kind == "h" and tag in ("h1", "h2", "h3", "h4"):
                self.headings.append((self._capture[1], self._flush()))
                self._capture = None
            elif kind == "jsonld" and tag == "script":
                self.jsonld_blocks.append(self._flush())
                self._capture = None
            elif kind == "a" and tag == "a":
                self.links.append((self._link_href, self._link_rel, self._flush()))
                self._capture = None

        if tag == "title":
            self.title = re.sub(r"\s+", " ", "".join(self.text_parts[-1:])).strip() or self.title

        if tag == "p" and self.first_paragraph is None and self.headings:
            tail = re.sub(r"\s+", " ", " ".join(self.text_parts[-40:])).strip()
            if len(tail.split()) >= 12:
                self.first_paragraph = tail

        while tag in self._stack:
            popped = self._stack.pop()
            if popped == tag:
                break

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)
            return
        if "title" in self._stack and self.title is None:
            self.title = re.sub(r"\s+", " ", data).strip()
        if "script" in self._stack:
            self.script_chars += len(data)
        if not self._in_non_content():
            self.text_parts.append(data)


def _abs(base, href):
    try:
        return urldefrag(urljoin(base, href))[0]
    except ValueError:
        return None


def _schema_types(blocks):
    """Collect @type values from JSON-LD, including @graph and nested nodes."""
    types = set()

    def walk(node):
        if isinstance(node, dict):
            t = node.get("@type")
            if isinstance(t, str):
                types.add(t)
            elif isinstance(t, list):
                types.update(x for x in t if isinstance(x, str))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    invalid = 0
    for raw in blocks:
        try:
            walk(json.loads(raw))
        except (ValueError, TypeError):
            invalid += 1
    return sorted(types), invalid


def analyze_html(url, html, status=None, headers=None, elapsed_ms=None, redirects=None):
    """Extract every on-page signal the SEO/AEO checklists score from one page."""
    p = PageParser()
    try:
        p.feed(html)
    except Exception as e:  # malformed markup should degrade, not crash the crawl
        return {"url": url, "error": f"parse failed: {e}"}

    headers = headers or {}
    body_text = re.sub(r"\s+", " ", " ".join(p.text_parts)).strip()
    words = body_text.split()
    h1s = [t for lvl, t in p.headings if lvl == 1]
    subheads = [t for lvl, t in p.headings if lvl in (2, 3)]
    schema_types, invalid_jsonld = _schema_types(p.jsonld_blocks)

    host = urlparse(url).netloc
    internal, external, nofollow = [], [], 0
    for href, rel, _text in p.links:
        target = _abs(url, href)
        if not target or not target.startswith("http"):
            continue
        if "nofollow" in (rel or ""):
            nofollow += 1
        (internal if urlparse(target).netloc == host else external).append(target)

    robots_meta = (p.meta.get("robots") or "").lower()
    desc = p.meta.get("description")
    question_heads = [h for h in subheads if QUESTION_RE.search(h)]
    dangling_heads = [h for h in subheads if DANGLING_RE.match(h)]

    # An SPA that ships an empty shell is invisible to most AI crawlers, which
    # (unlike Googlebot) generally do not execute JavaScript. Word count alone
    # cannot distinguish that from a genuinely thin page, so require the script
    # payload to dwarf the rendered text as well.
    text_chars = len(body_text)
    script_ratio = round(p.script_chars / text_chars, 1) if text_chars else None
    js_dependent = (
        len(words) < 200
        and p.tag_counts.get("script", 0) >= 3
        and text_chars > 0
        and p.script_chars > 5 * text_chars
    )

    return {
        "url": url,
        "status_code": status,
        "redirect_chain": redirects or [],
        "response": {
            "ttfb_ms": elapsed_ms,
            "html_bytes": len(html.encode("utf-8", "ignore")),
            "content_type": headers.get("Content-Type"),
            "x_robots_tag": headers.get("X-Robots-Tag"),
            "compressed": bool(headers.get("Content-Encoding")),
            "cache_control": headers.get("Cache-Control"),
        },
        "content": {
            "title": p.title,
            "title_length": len(p.title) if p.title else 0,
            "meta_description": desc,
            "meta_description_length": len(desc) if desc else 0,
            "lang": p.lang,
            "h1": h1s,
            "h1_count": len(h1s),
            "h2_h3": subheads,
            "heading_count": len(p.headings),
            "word_count": len(words),
            "first_paragraph_words": (
                len(p.first_paragraph.split()) if p.first_paragraph else 0
            ),
        },
        "mobile": {
            # TE22 is a Critical check — a missing viewport meta makes the page
            # non-responsive on mobile, which is most search traffic.
            "viewport_meta": p.meta.get("viewport"),
            "has_viewport": bool(p.meta.get("viewport")),
            "responsive_viewport": "width=device-width" in (p.meta.get("viewport") or ""),
        },
        "indexing": {
            "canonical": p.canonical,
            "canonical_self_referencing": (
                _abs(url, p.canonical) == url if p.canonical else None
            ),
            "meta_robots": robots_meta or None,
            "noindex": "noindex" in robots_meta
            or "noindex" in (headers.get("X-Robots-Tag") or "").lower(),
            "hreflang": p.hreflang,
        },
        "schema": {
            "jsonld_blocks": len(p.jsonld_blocks),
            "types": schema_types,
            "invalid_blocks": invalid_jsonld,
            "has_organization": any(
                t in schema_types for t in ("Organization", "LocalBusiness", "Person")
            ),
            "has_article": any(
                t in schema_types for t in ("Article", "BlogPosting", "NewsArticle")
            ),
            "has_faq": "FAQPage" in schema_types,
            "has_breadcrumb": "BreadcrumbList" in schema_types,
        },
        "aeo": {
            "question_headings": len(question_heads),
            "question_heading_ratio": (
                round(len(question_heads) / len(subheads), 2) if subheads else 0.0
            ),
            "dangling_context_headings": dangling_heads,
            "tables": p.tag_counts.get("table", 0),
            "lists": p.tag_counts.get("ul", 0) + p.tag_counts.get("ol", 0),
            "answer_first": (
                0 < (len(p.first_paragraph.split()) if p.first_paragraph else 0) <= 80
            ),
            "author_meta": p.meta.get("author"),
            "published_time": p.meta.get("article:published_time"),
            "modified_time": p.meta.get("article:modified_time"),
            "js_dependent_content": js_dependent,
            "script_to_text_ratio": script_ratio,
        },
        "links": {
            "internal": len(set(internal)),
            "external": len(set(external)),
            "nofollow": nofollow,
            "internal_urls": sorted(set(internal)),
        },
        "images": {
            "count": len(p.images),
            "missing_alt": sum(1 for _src, alt in p.images if not (alt or "").strip()),
        },
        "social": {
            "og_title": p.meta.get("og:title"),
            "og_image": p.meta.get("og:image"),
            "twitter_card": p.meta.get("twitter:card"),
        },
        "error": None,
    }


def fetch(url, session, timeout=20):
    try:
        r = session.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    except requests.exceptions.RequestException as e:
        return {"url": url, "error": f"{type(e).__name__}: {e}", "status_code": None}

    ctype = r.headers.get("Content-Type", "")
    if "html" not in ctype.lower():
        return {
            "url": r.url,
            "status_code": r.status_code,
            "error": f"not HTML (Content-Type: {ctype})",
        }

    return analyze_html(
        r.url,
        r.text,
        status=r.status_code,
        headers=r.headers,
        elapsed_ms=int(r.elapsed.total_seconds() * 1000),
        redirects=[h.url for h in r.history],
    )


def discover_from_sitemap(base, session, limit, timeout=20):
    """Pull candidate URLs from sitemap.xml, following sitemap index files."""
    found, queue, seen = [], [urljoin(base, "/sitemap.xml")], set()
    while queue and len(found) < limit * 4:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            r = session.get(sm, headers=HEADERS, timeout=timeout)
            if r.status_code != 200:
                continue
            locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
        except requests.exceptions.RequestException:
            continue
        for loc in locs:
            if loc.endswith(".xml") or "sitemap" in loc.rsplit("/", 1)[-1]:
                queue.append(loc)
            elif not loc.lower().endswith(SKIP_EXT):
                found.append(loc)
    return found


def crawl(start_url, limit=10, timeout=20):
    """Breadth-first crawl seeded by sitemap.xml, falling back to internal links."""
    if not urlparse(start_url).scheme:
        start_url = f"https://{start_url}"
    host = urlparse(start_url).netloc
    session = requests.Session()

    queue = [start_url]
    for u in discover_from_sitemap(start_url, session, limit, timeout):
        if u not in queue:
            queue.append(u)

    pages, seen = [], set()
    while queue and len(pages) < limit:
        url = queue.pop(0)
        if url in seen or urlparse(url).netloc != host:
            continue
        seen.add(url)

        page = fetch(url, session, timeout)

        # Dedupe on the FINAL url too: "/x" and "/x/" (or http->https) are one
        # page, and counting both inflates duplicate-title and thin-page counts.
        final = page.get("url", url)
        if final != url:
            if final in seen:
                continue
            seen.add(final)

        pages.append(page)

        for link in page.get("links", {}).get("internal_urls", []):
            if (
                link not in seen
                and link not in queue
                and not link.lower().endswith(SKIP_EXT)
            ):
                queue.append(link)

    return pages


def summarize(pages):
    """Site-level rollup — the numbers the audit report leads with."""
    ok = [p for p in pages if not p.get("error")]
    if not ok:
        return {"pages_crawled": len(pages), "pages_ok": 0}

    titles = [p["content"]["title"] for p in ok if p["content"]["title"]]
    schema_types = Counter()
    for p in ok:
        schema_types.update(p["schema"]["types"])

    def pct(n):
        return round(100 * n / len(ok))

    return {
        "pages_crawled": len(pages),
        "pages_ok": len(ok),
        "pages_errored": len(pages) - len(ok),
        "duplicate_titles": len(titles) - len(set(titles)),
        "missing_title_pct": pct(sum(1 for p in ok if not p["content"]["title"])),
        "missing_meta_desc_pct": pct(
            sum(1 for p in ok if not p["content"]["meta_description"])
        ),
        "bad_h1_pct": pct(sum(1 for p in ok if p["content"]["h1_count"] != 1)),
        "noindex_pages": [p["url"] for p in ok if p["indexing"]["noindex"]],
        "missing_canonical_pct": pct(
            sum(1 for p in ok if not p["indexing"]["canonical"])
        ),
        "missing_viewport_pages": [
            p["url"] for p in ok if not p["mobile"]["responsive_viewport"]
        ],
        "no_schema_pct": pct(sum(1 for p in ok if not p["schema"]["types"])),
        "schema_types": dict(schema_types.most_common()),
        "thin_pages": [
            p["url"] for p in ok if p["content"]["word_count"] < 300
        ],
        "js_dependent_pages": [
            p["url"] for p in ok if p["aeo"]["js_dependent_content"]
        ],
        "answer_first_pct": pct(sum(1 for p in ok if p["aeo"]["answer_first"])),
        "avg_question_heading_ratio": round(
            sum(p["aeo"]["question_heading_ratio"] for p in ok) / len(ok), 2
        ),
        "avg_word_count": round(
            sum(p["content"]["word_count"] for p in ok) / len(ok)
        ),
        "avg_ttfb_ms": round(
            sum(p["response"]["ttfb_ms"] or 0 for p in ok) / len(ok)
        ),
        "images_missing_alt": sum(p["images"]["missing_alt"] for p in ok),
    }


def print_report(pages, summary):
    print("SEO / AEO Crawl Report")
    print("=" * 52)
    print(f"\nPages crawled: {summary.get('pages_ok', 0)}/{summary.get('pages_crawled', 0)}")
    if not summary.get("pages_ok"):
        for p in pages:
            print(f"  [ERROR] {p['url']}: {p.get('error')}")
        return

    print("\nSite-level:")
    print(f"  Avg TTFB:              {summary['avg_ttfb_ms']}ms")
    print(f"  Avg word count:        {summary['avg_word_count']}")
    print(f"  Missing title:         {summary['missing_title_pct']}%")
    print(f"  Missing meta desc:     {summary['missing_meta_desc_pct']}%")
    print(f"  H1 != 1:               {summary['bad_h1_pct']}%")
    print(f"  Missing canonical:     {summary['missing_canonical_pct']}%")
    print(f"  No responsive viewport: {len(summary['missing_viewport_pages'])}")
    print(f"  No structured data:    {summary['no_schema_pct']}%")
    print(f"  Duplicate titles:      {summary['duplicate_titles']}")
    print(f"  Images missing alt:    {summary['images_missing_alt']}")

    print("\nAI-search readiness:")
    print(f"  Answer-first pages:    {summary['answer_first_pct']}%")
    print(f"  Question-heading ratio: {summary['avg_question_heading_ratio']}")
    print(f"  JS-dependent pages:    {len(summary['js_dependent_pages'])}")
    print(f"  Schema types found:    {', '.join(summary['schema_types']) or 'NONE'}")

    if summary["thin_pages"]:
        print(f"\nThin pages (<300 words): {len(summary['thin_pages'])}")
        for u in summary["thin_pages"][:10]:
            print(f"  - {u}")
    if summary["noindex_pages"]:
        print(f"\nNoindex pages: {len(summary['noindex_pages'])}")
        for u in summary["noindex_pages"][:10]:
            print(f"  - {u}")


def main():
    parser = argparse.ArgumentParser(
        description="Crawl a site and extract on-page SEO + AI-search signals"
    )
    parser.add_argument("url", help="Start URL")
    parser.add_argument("--crawl", "-c", type=int, default=1,
                        help="Number of pages to crawl (default 1)")
    parser.add_argument("--timeout", "-t", type=int, default=20,
                        help="Per-request timeout in seconds")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--output", "-o", help="Write JSON to this file")
    args = parser.parse_args()

    pages = crawl(args.url, limit=max(1, args.crawl), timeout=args.timeout)
    summary = summarize(pages)
    payload = {"start_url": args.url, "summary": summary, "pages": pages}

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"Saved to {args.output}", file=sys.stderr)

    if args.json:
        print(json.dumps(payload, indent=2))
    elif not args.output:
        print_report(pages, summary)

    sys.exit(0 if summary.get("pages_ok") else 1)


if __name__ == "__main__":
    main()
