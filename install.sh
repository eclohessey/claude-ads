#!/usr/bin/env bash
set -euo pipefail

# Claude Ads Installer
# Wraps everything in main() to prevent partial execution on network failure

main() {
    SKILL_DIR="${HOME}/.claude/skills/ads"
    SEO_SKILL_DIR="${HOME}/.claude/skills/seo"
    AGENT_DIR="${HOME}/.claude/agents"
    REPO_URL="https://github.com/AgriciDaniel/claude-ads"

    echo "════════════════════════════════════════"
    echo "║   Claude Ads - Installer             ║"
    echo "║   Paid Ads + SEO / AI Search Skills  ║"
    echo "════════════════════════════════════════"
    echo ""

    # Check prerequisites
    command -v git >/dev/null 2>&1 || { echo "✗ Git is required but not installed."; exit 1; }
    echo "✓ Git detected"

    # Create directories
    mkdir -p "${SKILL_DIR}/references"
    mkdir -p "${SEO_SKILL_DIR}/references"
    mkdir -p "${AGENT_DIR}"

    # Clone or update
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf ${TEMP_DIR}" EXIT

    echo "↓ Downloading Claude Ads..."
    git clone --depth 1 "${REPO_URL}" "${TEMP_DIR}/claude-ads" 2>/dev/null

    # Copy main skill + references
    echo "→ Installing skill files..."
    cp "${TEMP_DIR}/claude-ads/ads/SKILL.md" "${SKILL_DIR}/SKILL.md"
    cp "${TEMP_DIR}/claude-ads/ads/references/"*.md "${SKILL_DIR}/references/"
    cp "${TEMP_DIR}/claude-ads/seo/SKILL.md" "${SEO_SKILL_DIR}/SKILL.md"
    cp "${TEMP_DIR}/claude-ads/seo/references/"*.md "${SEO_SKILL_DIR}/references/"

    # Copy sub-skills
    echo "→ Installing sub-skills..."
    for skill_dir in "${TEMP_DIR}/claude-ads/skills"/*/; do
        skill_name=$(basename "${skill_dir}")
        target="${HOME}/.claude/skills/${skill_name}"
        mkdir -p "${target}"
        cp "${skill_dir}SKILL.md" "${target}/SKILL.md"

        # Copy assets (industry templates) if they exist
        if [ -d "${skill_dir}assets" ]; then
            mkdir -p "${target}/assets"
            cp "${skill_dir}assets/"*.md "${target}/assets/"
        fi
    done

    # Copy agents
    echo "→ Installing subagents..."
    cp "${TEMP_DIR}/claude-ads/agents/"*.md "${AGENT_DIR}/" 2>/dev/null || true

    # Copy scripts (optional Python tools)
    SCRIPTS_DIR="${HOME}/.claude/skills/ads/scripts"
    if [ -d "${TEMP_DIR}/claude-ads/scripts" ]; then
        echo "→ Installing Python scripts..."
        mkdir -p "${SCRIPTS_DIR}"
        cp "${TEMP_DIR}/claude-ads/scripts/"*.py "${SCRIPTS_DIR}/"
        cp "${TEMP_DIR}/claude-ads/requirements.txt" "${SKILL_DIR}/requirements.txt"

        # SEO scripts resolve under the seo skill directory
        SEO_SCRIPTS_DIR="${SEO_SKILL_DIR}/scripts"
        mkdir -p "${SEO_SCRIPTS_DIR}"
        for seo_script in seo_crawl.py check_ai_crawlers.py ai_visibility.py; do
            cp "${TEMP_DIR}/claude-ads/scripts/${seo_script}" "${SEO_SCRIPTS_DIR}/"
        done
        cp "${TEMP_DIR}/claude-ads/requirements.txt" "${SEO_SKILL_DIR}/requirements.txt"
    fi

    # Install Python dependencies (required for /ads generate, /ads dna screenshots)
    echo ""
    echo "→ Installing Python dependencies..."
    if command -v pip3 >/dev/null 2>&1 || command -v pip >/dev/null 2>&1; then
        PIP_CMD="pip3"
        command -v pip3 >/dev/null 2>&1 || PIP_CMD="pip"
        ${PIP_CMD} install --break-system-packages -q -r "${SKILL_DIR}/requirements.txt" 2>/dev/null \
            || ${PIP_CMD} install -q -r "${SKILL_DIR}/requirements.txt" 2>/dev/null \
            && echo "  ✓ Python dependencies installed" \
            || echo "  ⚠ pip install failed — run manually: pip3 install -r ${SKILL_DIR}/requirements.txt"

        # Install Chromium for brand screenshot capture (/ads dna visual scan)
        echo "→ Installing Chromium for brand screenshots..."
        python3 -m playwright install chromium --with-deps 2>/dev/null \
            && echo "  ✓ Chromium ready (brand screenshots enabled)" \
            || echo "  ⚠ Playwright install failed — fix: python3 -m playwright install chromium"
    else
        echo "  ⚠ pip not found — install deps manually: pip3 install -r ${SKILL_DIR}/requirements.txt"
    fi

    echo ""
    echo "✓ Claude Ads installed successfully!"
    echo ""
    echo "  Installed:"
    echo "    • 2 main skills (ads + seo orchestrators)"
    echo "    • 26 sub-skills (17 ads + 9 seo)"
    echo "    • 14 agents (6 ad audit + 4 creative + 4 seo audit)"
    echo "    • 30 reference files"
    echo "    • 11 industry templates"
    echo ""
    echo "Usage:"
    echo "  1. Start Claude Code:  claude"
    echo "  2. Run commands:       /ads audit"
    echo "                         /ads plan saas"
    echo "                         /seo audit example.com"
    echo "                         /seo aeo example.com"
    echo ""
    echo "To uninstall: curl -fsSL ${REPO_URL}/raw/main/uninstall.sh | bash"
}

main "$@"
