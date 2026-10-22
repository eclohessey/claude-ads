#!/usr/bin/env python3
"""
Track brand visibility inside AI answer engines over time.

There is no ranking API for ChatGPT, Claude, Perplexity or Google AI Overviews,
so AI visibility has to be measured by asking a fixed prompt set on a schedule
and recording whether the brand is mentioned and cited. This script maintains
that prompt set and the result ledger, and computes visibility rate, share of
voice, and citation share against competitors.

Stdlib only — no network calls, no API keys. The agent (or a human) runs the
prompts; this script is the measurement system of record.

Usage:
    python ai_visibility.py init --brand "Acme" --domain acme.com \
        --competitors "Beta,Gamma" --topics "ai voice agents,call center automation"
    python ai_visibility.py record --engine chatgpt --prompt-id P01 \
        --mentioned --position 2 --cited-url https://acme.com/guide
    python ai_visibility.py report
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

LEDGER = "ai-visibility.json"

ENGINES = ["chatgpt", "claude", "perplexity", "google-ai-overview", "gemini", "copilot"]

# Prompt templates spanning the funnel. Category drives how a miss is weighted:
# a miss on a "brand" prompt is far more serious than one on "discovery".
TEMPLATES = [
    ("brand",       "What is {brand}?"),
    ("brand",       "Is {brand} any good? What do users say about it?"),
    ("brand",       "How much does {brand} cost?"),
    ("comparison",  "{brand} vs {competitor} — which is better?"),
    ("comparison",  "What are the best alternatives to {competitor}?"),
    ("discovery",   "What is the best tool for {topic}?"),
    ("discovery",   "Recommend software for {topic} for a small business"),
    ("discovery",   "Top 5 {topic} platforms in {year}"),
    ("problem",     "How do I get started with {topic}?"),
    ("problem",     "What should I look for when choosing a {topic} vendor?"),
]


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(path):
    if not os.path.exists(path):
        print(f"Error: {path} not found. Run `ai_visibility.py init` first.", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def cmd_init(args):
    competitors = [c.strip() for c in (args.competitors or "").split(",") if c.strip()]
    topics = [t.strip() for t in (args.topics or "").split(",") if t.strip()]
    if not topics:
        print("Error: --topics is required (comma-separated).", file=sys.stderr)
        sys.exit(1)

    year = datetime.now(timezone.utc).year
    prompts, n = [], 0
    for category, template in TEMPLATES:
        # Fan the template out over whichever variable it references.
        if "{competitor}" in template:
            fills = [{"competitor": c} for c in competitors] or []
        elif "{topic}" in template:
            fills = [{"topic": t} for t in topics]
        else:
            fills = [{}]
        for fill in fills:
            n += 1
            prompts.append({
                "id": f"P{n:02d}",
                "category": category,
                "text": template.format(brand=args.brand, year=year, **fill),
            })

    data = {
        "brand": args.brand,
        "domain": args.domain,
        "competitors": competitors,
        "topics": topics,
        "engines": args.engines.split(",") if args.engines else ENGINES,
        "created_at": _now(),
        "prompts": prompts,
        "runs": [],
    }
    save(args.file, data)

    print(f"Created {args.file} with {len(prompts)} prompts across "
          f"{len(set(p['category'] for p in prompts))} categories.")
    print("\nRun each prompt in each engine, then record the result:\n")
    for p in prompts:
        print(f"  [{p['id']}] ({p['category']}) {p['text']}")
    print(f"\nEngines to test: {', '.join(data['engines'])}")


def cmd_record(args):
    data = load(args.file)
    ids = {p["id"] for p in data["prompts"]}
    if args.prompt_id not in ids:
        print(f"Error: unknown prompt id {args.prompt_id}. Known: {sorted(ids)}",
              file=sys.stderr)
        sys.exit(1)

    data["runs"].append({
        "recorded_at": _now(),
        "engine": args.engine,
        "prompt_id": args.prompt_id,
        "mentioned": bool(args.mentioned),
        "position": args.position,
        "cited_urls": args.cited_url or [],
        "competitors_mentioned": [
            c.strip() for c in (args.competitors_mentioned or "").split(",") if c.strip()
        ],
        "sentiment": args.sentiment,
        "notes": args.notes,
    })
    save(args.file, data)
    state = "MENTIONED" if args.mentioned else "not mentioned"
    print(f"Recorded {args.prompt_id} on {args.engine}: {state}")


def cmd_report(args):
    data = load(args.file)
    runs = data["runs"]
    if not runs:
        print("No runs recorded yet. Use `ai_visibility.py record` after testing prompts.")
        return

    by_id = {p["id"]: p for p in data["prompts"]}
    total = len(runs)
    mentioned = sum(1 for r in runs if r["mentioned"])
    cited = sum(1 for r in runs if r["cited_urls"])

    per_engine = defaultdict(lambda: {"runs": 0, "mentions": 0, "citations": 0})
    per_category = defaultdict(lambda: {"runs": 0, "mentions": 0})
    competitor_counts = Counter()
    cited_pages = Counter()

    for r in runs:
        e = per_engine[r["engine"]]
        e["runs"] += 1
        e["mentions"] += int(r["mentioned"])
        e["citations"] += int(bool(r["cited_urls"]))

        cat = by_id.get(r["prompt_id"], {}).get("category", "unknown")
        per_category[cat]["runs"] += 1
        per_category[cat]["mentions"] += int(r["mentioned"])

        competitor_counts.update(r["competitors_mentioned"])
        cited_pages.update(r["cited_urls"])

    brand_mentions = mentioned
    sov_total = brand_mentions + sum(competitor_counts.values())
    sov = round(100 * brand_mentions / sov_total, 1) if sov_total else 0.0

    if args.json:
        print(json.dumps({
            "brand": data["brand"],
            "total_runs": total,
            "visibility_rate_pct": round(100 * mentioned / total, 1),
            "citation_rate_pct": round(100 * cited / total, 1),
            "share_of_voice_pct": sov,
            "per_engine": dict(per_engine),
            "per_category": dict(per_category),
            "competitor_mentions": dict(competitor_counts.most_common()),
            "most_cited_pages": dict(cited_pages.most_common(10)),
        }, indent=2))
        return

    print(f"AI Visibility Report — {data['brand']}")
    print("=" * 52)
    print(f"\nRuns recorded:     {total}")
    print(f"Visibility rate:   {round(100 * mentioned / total, 1)}%  "
          f"(mentioned in {mentioned}/{total} answers)")
    print(f"Citation rate:     {round(100 * cited / total, 1)}%  "
          f"(linked in {cited}/{total} answers)")
    print(f"Share of voice:    {sov}%  (vs {len(competitor_counts)} competitors)")

    print("\nBy engine:")
    for engine, s in sorted(per_engine.items()):
        rate = round(100 * s["mentions"] / s["runs"], 1) if s["runs"] else 0
        print(f"  {engine:22} {rate:5}%   ({s['mentions']}/{s['runs']} mentions, "
              f"{s['citations']} cited)")

    print("\nBy prompt category:")
    for cat, s in sorted(per_category.items()):
        rate = round(100 * s["mentions"] / s["runs"], 1) if s["runs"] else 0
        flag = "  <-- FIX FIRST" if cat == "brand" and rate < 100 else ""
        print(f"  {cat:22} {rate:5}%   ({s['mentions']}/{s['runs']}){flag}")

    if competitor_counts:
        print("\nCompetitor mentions:")
        for name, count in competitor_counts.most_common():
            print(f"  {name:22} {count}")

    if cited_pages:
        print("\nMost-cited pages:")
        for url, count in cited_pages.most_common(10):
            print(f"  {count:3}x  {url}")

    uncovered = [
        p["id"] for p in data["prompts"]
        if not any(r["prompt_id"] == p["id"] and r["mentioned"] for r in runs)
    ]
    if uncovered:
        print(f"\nZero-visibility prompts ({len(uncovered)}):")
        for pid in uncovered:
            print(f"  [{pid}] {by_id[pid]['text']}")


def main():
    parser = argparse.ArgumentParser(description="Track brand visibility in AI answer engines")
    parser.add_argument("--file", "-f", default=LEDGER, help=f"Ledger path (default {LEDGER})")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Generate the prompt set and create the ledger")
    p_init.add_argument("--brand", required=True)
    p_init.add_argument("--domain", required=True)
    p_init.add_argument("--competitors", help="Comma-separated competitor names")
    p_init.add_argument("--topics", required=True, help="Comma-separated buyer topics")
    p_init.add_argument("--engines", help=f"Comma-separated (default: {','.join(ENGINES)})")
    p_init.set_defaults(func=cmd_init)

    p_rec = sub.add_parser("record", help="Record one prompt/engine result")
    p_rec.add_argument("--engine", required=True, choices=ENGINES)
    p_rec.add_argument("--prompt-id", required=True)
    p_rec.add_argument("--mentioned", action="store_true", help="Brand appeared in the answer")
    p_rec.add_argument("--position", type=int, help="Rank within a list answer, if listed")
    p_rec.add_argument("--cited-url", action="append", help="Repeatable; URLs cited")
    p_rec.add_argument("--competitors-mentioned", help="Comma-separated")
    p_rec.add_argument("--sentiment", choices=["positive", "neutral", "negative"])
    p_rec.add_argument("--notes")
    p_rec.set_defaults(func=cmd_record)

    p_rep = sub.add_parser("report", help="Summarize visibility, citations, share of voice")
    p_rep.add_argument("--json", "-j", action="store_true")
    p_rep.set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
