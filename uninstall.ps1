#Requires -Version 5.1
<#
.SYNOPSIS
    Claude Ads Uninstaller for Windows
.DESCRIPTION
    Removes the Claude Ads skill, sub-skills, agents, and reference files
    from Claude Code on Windows systems.
#>

$ErrorActionPreference = "Stop"

function Main {
    Write-Host "Uninstalling Claude Ads..."

    $ClaudeDir = Join-Path $env:USERPROFILE ".claude"

    # Remove main skills (orchestrators + references + scripts)
    foreach ($Main in @("skills\ads", "skills\seo")) {
        $MainSkill = Join-Path $ClaudeDir $Main
        if (Test-Path $MainSkill) {
            Remove-Item -Path $MainSkill -Recurse -Force
        }
    }

    # Remove sub-skills
    $SubSkills = @(
        "ads-audit", "ads-google", "ads-meta", "ads-youtube",
        "ads-linkedin", "ads-tiktok", "ads-microsoft", "ads-creative",
        "ads-landing", "ads-budget", "ads-plan", "ads-competitor", "ads-apple",
        "ads-dna", "ads-create", "ads-generate", "ads-photoshoot",
        "seo-audit", "seo-technical", "seo-content", "seo-aeo", "seo-schema",
        "seo-authority", "seo-keywords", "seo-competitor", "seo-local"
    )
    foreach ($skill in $SubSkills) {
        $SkillPath = Join-Path $ClaudeDir "skills\$skill"
        if (Test-Path $SkillPath) {
            Remove-Item -Path $SkillPath -Recurse -Force
        }
    }

    # Remove agents
    $Agents = @(
        "audit-google", "audit-meta", "audit-creative",
        "audit-tracking", "audit-budget", "audit-compliance",
        "creative-strategist", "visual-designer", "copy-writer", "format-adapter",
        "audit-seo-technical", "audit-seo-content", "audit-seo-aeo", "audit-seo-authority"
    )
    foreach ($agent in $Agents) {
        $AgentPath = Join-Path $ClaudeDir "agents\$agent.md"
        if (Test-Path $AgentPath) {
            Remove-Item -Path $AgentPath -Force
        }
    }

    Write-Host "[OK] Claude Ads uninstalled." -ForegroundColor Green
}

Main
