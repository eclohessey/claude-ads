#!/usr/bin/env python3
"""
Check whether a site is reachable by search and AI-answer crawlers.

Parses robots.txt per-user-agent, verifies sitemap and llms.txt discovery, and
reports which named bots are allowed, blocked, or crawl-delayed. Blocking an AI
crawler is the single most common reason a site never appears in AI answers.

Usage:
    python check_ai_crawlers.py https://example.com
    python check_ai_crawlers.py example.com --json
"""

import argparse
import json
import re
import sys
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install -r requirements.txt")
    sys.exit(1)


HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ClaudeSEO/1.0)"}

# purpose: "search" bots feed a search index; "answer" bots ground live AI
# answers and are the ones that drive citations; "training" bots only affect
# model training and are a business decision, not an SEO defect.
CRAWLERS = {
    "Googlebot":        {"owner": "Google",     "purpose": "search"},
    "Bingbot":          {"owner": "Microsoft",  "purpose": "search"},
    "DuckDuckBot":      {"owner": "DuckDuckGo", "purpose": "search"},
    "Google-Extended":  {"owner": "Google",     "purpose": "training"},
    "GPTBot":           {"owner": "OpenAI",     "purpose": "training"},
    "OAI-SearchBot":    {"owner": "OpenAI",     "purpose": "answer"},
    "ChatGPT-User":     {"owner": "OpenAI",     "purpose": "answer"},
    "ClaudeBot":        {"owner": "Anthropic",  "purpose": "training"},
    "Claude-SearchBot": {"owner": "Anthropic",  "purpose": "answer"},
    "Claude-User":      {"owner": "Anthropic",  "purpose": "answer"},
    "PerplexityBot":    {"owner": "Perplexity", "purpose": "answer"},
    "Perplexity-User":  {"owner": "Perplexity", "purpose": "answer"},
    "Applebot":         {"owner": "Apple",      "purpose": "search"},
    "Applebot-Extended": {"owner": "Apple",     "purpose": "training"},
    "meta-externalagent": {"owner": "Meta",     "purpose": "training"},
    "Amazonbot":        {"owner": "Amazon",     "purpose": "answer"},
    "CCBot":            {"owner": "Common Crawl", "purpose": "training"},
}


def parse_robots(text):
    """Group robots.txt rules by user-agent. Returns {ua_lower: {...}} + sitemaps."""
    groups, sitemaps, current = {}, [], []
    last_was_ua = False

    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, _, value = line.partition(":")
        field, value = field.strip().lower(), value.strip()

        if field == "user-agent":
            if not last_was_ua:
                current = []
            current.append(value.lower())
            groups.setdefault(value.lower(), {"allow": [], "disallow": [], "crawl_delay": None})
            last_was_ua = True
            continue

        last_was_ua = False
        if field == "sitemap":
            sitemaps.append(value)
        elif field in ("allow", "disallow") and current:
            for ua in current:
                groups[ua][field].append(value)
        elif field == "crawl-delay" and current:
            for ua in current:
                try:
                    groups[ua]["crawl_delay"] = float(value)
                except ValueError:
                    pass

    return groups, sitemaps


def _match_len(patterns, path):
    """Longest matching robots path prefix, honoring the * wildcard and $ anchor."""
    best = -1
    for pat in patterns:
        if pat == "":
            continue
        regex = "^" + "".join(
            ".*" if c == "*" else ("$" if c == "$" else re.escape(c)) for c in pat
        )
        if re.match(regex, path):
            best = max(best, len(pat))
    return best


def verdict_for(groups, ua, path="/"):
    """Apply robots.txt precedence: specific UA group wins over *, longest rule wins."""
    group = groups.get(ua.lower())
    matched_as = ua
    if group is None:
        group = groups.get("*")
        matched_as = "*" if group else None
    if group is None:
        return {"allowed": True, "rule": "no matching group", "matched_as": None,
                "crawl_delay": None}

    allow_len = _match_len(group["allow"], path)
    disallow_len = _match_len(group["disallow"], path)

    if disallow_len < 0:
        allowed, rule = True, "no disallow match"
    elif allow_len >= disallow_len:
        allowed, rule = True, f"allow rule (len {allow_len}) >= disallow (len {disallow_len})"
    else:
        allowed, rule = False, f"disallowed by rule of length {disallow_len}"

    if "" in group["disallow"] and disallow_len < 0:
        rule = "Disallow: (empty) — allows all"

    return {
        "allowed": allowed,
        "rule": rule,
        "matched_as": matched_as,
        "crawl_delay": group["crawl_delay"],
    }


def check_site(base_url, timeout=15):
    if not urlparse(base_url).scheme:
        base_url = f"https://{base_url}"
    root = f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}"

    result = {
        "site": root,
        "robots_txt": {"url": urljoin(root, "/robots.txt"), "found": False,
                       "status": None, "sitemaps": []},
        "crawlers": {},
        "sitemap": {"found": False, "url": None, "url_count": 0},
        "llms_txt": {"found": False, "url": urljoin(root, "/llms.txt")},
        "blocked_answer_engines": [],
        "blocked_search_engines": [],
        "error": None,
    }

    session = requests.Session()

    # robots.txt
    groups = {}
    try:
        r = session.get(result["robots_txt"]["url"], headers=HEADERS, timeout=timeout)
        result["robots_txt"]["status"] = r.status_code
        if r.status_code == 200 and "html" not in r.headers.get("Content-Type", "").lower():
            result["robots_txt"]["found"] = True
            groups, sitemaps = parse_robots(r.text)
            result["robots_txt"]["sitemaps"] = sitemaps
    except requests.exceptions.RequestException as e:
        result["error"] = f"robots.txt fetch failed: {e}"

    # A missing robots.txt means everything is allowed — that is a pass, not a fail.
    for name, meta in CRAWLERS.items():
        v = verdict_for(groups, name, "/")
        entry = {**meta, **v}
        result["crawlers"][name] = entry
        if not v["allowed"]:
            if meta["purpose"] == "answer":
                result["blocked_answer_engines"].append(name)
            elif meta["purpose"] == "search":
                result["blocked_search_engines"].append(name)

    # sitemap
    candidates = result["robots_txt"]["sitemaps"] or [urljoin(root, "/sitemap.xml")]
    for sm in candidates:
        try:
            r = session.get(sm, headers=HEADERS, timeout=timeout)
            if r.status_code == 200 and "<" in r.text[:200]:
                result["sitemap"] = {
                    "found": True,
                    "url": sm,
                    "url_count": len(re.findall(r"<loc>", r.text)),
                    "is_index": "<sitemapindex" in r.text[:500],
                    "declared_in_robots": bool(result["robots_txt"]["sitemaps"]),
                }
                break
        except requests.exceptions.RequestException:
            continue

    # llms.txt — low-cost, adoption still limited; informational only
    try:
        r = session.get(result["llms_txt"]["url"], headers=HEADERS, timeout=timeout)
        result["llms_txt"]["found"] = (
            r.status_code == 200 and "html" not in r.headers.get("Content-Type", "").lower()
        )
    except requests.exceptions.RequestException:
        pass

    return result


def print_report(res):
    print("Crawler Access Check")
    print("=" * 52)
    print(f"\nSite: {res['site']}")

    rb = res["robots_txt"]
    print(f"\nrobots.txt: {'FOUND' if rb['found'] else 'NOT FOUND'} (HTTP {rb['status']})")
    if not rb["found"]:
        print("  Note: no robots.txt means all crawlers are allowed — not a defect.")

    sm = res["sitemap"]
    print(f"Sitemap:    {'FOUND' if sm['found'] else 'NOT FOUND'}"
          f"{' — ' + str(sm['url_count']) + ' URLs' if sm['found'] else ''}")
    if sm["found"] and not sm.get("declared_in_robots"):
        print("  Warning: sitemap exists but is not declared in robots.txt")
    print(f"llms.txt:   {'FOUND' if res['llms_txt']['found'] else 'not present (optional)'}")

    print("\nCrawler access:")
    for purpose in ("search", "answer", "training"):
        rows = [(n, c) for n, c in res["crawlers"].items() if c["purpose"] == purpose]
        print(f"\n  [{purpose.upper()}]")
        for name, c in rows:
            state = "ALLOW" if c["allowed"] else "BLOCK"
            delay = f"  crawl-delay={c['crawl_delay']}" if c["crawl_delay"] else ""
            print(f"    {state:5}  {name:20} ({c['owner']}){delay}")

    if res["blocked_search_engines"]:
        print(f"\nCRITICAL: search crawlers blocked: {', '.join(res['blocked_search_engines'])}")
    if res["blocked_answer_engines"]:
        print(f"\nHIGH: AI answer crawlers blocked: {', '.join(res['blocked_answer_engines'])}")
        print("  These bots ground live AI answers. Blocking them removes you from AI citations.")
    if not res["blocked_search_engines"] and not res["blocked_answer_engines"]:
        print("\nOK: no search or AI-answer crawler is blocked at the site root.")


def main():
    parser = argparse.ArgumentParser(
        description="Check search and AI crawler access via robots.txt"
    )
    parser.add_argument("url", help="Site URL or domain")
    parser.add_argument("--timeout", "-t", type=int, default=15)
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    res = check_site(args.url, timeout=args.timeout)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print_report(res)

    sys.exit(1 if res["blocked_search_engines"] else 0)


if __name__ == "__main__":
    main()
