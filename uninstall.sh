#!/usr/bin/env bash
set -euo pipefail

main() {
    echo "→ Uninstalling Claude Ads..."

    # Remove main skills (orchestrators + references + scripts)
    rm -rf "${HOME}/.claude/skills/ads"
    rm -rf "${HOME}/.claude/skills/seo"

    # Remove sub-skills
    for skill in ads-audit ads-google ads-meta ads-youtube ads-linkedin ads-tiktok ads-microsoft ads-creative ads-landing ads-budget ads-plan ads-competitor ads-apple ads-dna ads-create ads-generate ads-photoshoot \
                 seo-audit seo-technical seo-content seo-aeo seo-schema seo-authority seo-keywords seo-competitor seo-local; do
        rm -rf "${HOME}/.claude/skills/${skill}"
    done

    # Remove agents
    for agent in audit-google audit-meta audit-creative audit-tracking audit-budget audit-compliance creative-strategist visual-designer copy-writer format-adapter \
                 audit-seo-technical audit-seo-content audit-seo-aeo audit-seo-authority; do
        rm -f "${HOME}/.claude/agents/${agent}.md"
    done

    echo "✓ Claude Ads uninstalled."
}

main "$@"
