#Requires -Version 5.1
<#
.SYNOPSIS
    Claude Ads Installer for Windows
.DESCRIPTION
    Installs the Claude Ads and Claude SEO skills, sub-skills, agents, and
    reference files for Claude Code on Windows systems.
#>

$ErrorActionPreference = "Stop"

function Main {
    $SkillDir = Join-Path $env:USERPROFILE ".claude\skills\ads"
    $SeoSkillDir = Join-Path $env:USERPROFILE ".claude\skills\seo"
    $AgentDir = Join-Path $env:USERPROFILE ".claude\agents"
    $RepoUrl = "https://github.com/AgriciDaniel/claude-ads"

    Write-Host "=================================="
    Write-Host "   Claude Ads - Installer"
    Write-Host "   Paid Ads + SEO / AI Search Skills"
    Write-Host "=================================="
    Write-Host ""

    # Check prerequisites
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "X Git is required but not installed." -ForegroundColor Red
        exit 1
    }
    Write-Host "OK Git detected" -ForegroundColor Green

    # Create directories
    New-Item -ItemType Directory -Path (Join-Path $SkillDir "references") -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $SeoSkillDir "references") -Force | Out-Null
    New-Item -ItemType Directory -Path $AgentDir -Force | Out-Null

    # Clone to temp directory
    $TempDir = Join-Path $env:TEMP "claude-ads-install-$(Get-Random)"
    Write-Host "Downloading Claude Ads..."

    try {
        # Temporarily allow stderr (git writes progress to stderr — treated as error in PS 5.1)
        $ErrorActionPreference = "Continue"
        git clone --depth 1 $RepoUrl "$TempDir\claude-ads" 2>&1 | Out-Null
        $ErrorActionPreference = "Stop"
        if ($LASTEXITCODE -ne 0) { throw "Git clone failed" }

        # Copy main skill + references
        Write-Host "Installing skill files..."
        Copy-Item "$TempDir\claude-ads\ads\SKILL.md" -Destination "$SkillDir\SKILL.md" -Force
        Copy-Item "$TempDir\claude-ads\ads\references\*.md" -Destination "$SkillDir\references\" -Force
        Copy-Item "$TempDir\claude-ads\seo\SKILL.md" -Destination "$SeoSkillDir\SKILL.md" -Force
        Copy-Item "$TempDir\claude-ads\seo\references\*.md" -Destination "$SeoSkillDir\references\" -Force

        # Copy sub-skills
        Write-Host "Installing sub-skills..."
        Get-ChildItem "$TempDir\claude-ads\skills" -Directory | ForEach-Object {
            $TargetDir = Join-Path $env:USERPROFILE ".claude\skills\$($_.Name)"
            New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
            Copy-Item (Join-Path $_.FullName "SKILL.md") -Destination "$TargetDir\SKILL.md" -Force

            # Copy assets (industry templates) if they exist
            $AssetsDir = Join-Path $_.FullName "assets"
            if (Test-Path $AssetsDir) {
                $TargetAssets = Join-Path $TargetDir "assets"
                New-Item -ItemType Directory -Path $TargetAssets -Force | Out-Null
                Copy-Item "$AssetsDir\*.md" -Destination "$TargetAssets\" -Force
            }
        }

        # Copy agents
        Write-Host "Installing subagents..."
        Copy-Item "$TempDir\claude-ads\agents\*.md" -Destination "$AgentDir\" -Force

        # Copy scripts (optional Python tools)
        $ScriptsSource = "$TempDir\claude-ads\scripts"
        if (Test-Path $ScriptsSource) {
            Write-Host "Installing Python scripts..."
            $ScriptsDir = Join-Path $SkillDir "scripts"
            New-Item -ItemType Directory -Path $ScriptsDir -Force | Out-Null
            Copy-Item "$ScriptsSource\*.py" -Destination "$ScriptsDir\" -Force
            Copy-Item "$TempDir\claude-ads\requirements.txt" -Destination "$SkillDir\requirements.txt" -Force

            # SEO scripts resolve under the seo skill directory
            $SeoScriptsDir = Join-Path $SeoSkillDir "scripts"
            New-Item -ItemType Directory -Path $SeoScriptsDir -Force | Out-Null
            foreach ($SeoScript in @("seo_crawl.py", "check_ai_crawlers.py", "ai_visibility.py")) {
                Copy-Item (Join-Path $ScriptsSource $SeoScript) -Destination "$SeoScriptsDir\" -Force
            }
            Copy-Item "$TempDir\claude-ads\requirements.txt" -Destination "$SeoSkillDir\requirements.txt" -Force
        }

        # Install Python dependencies (required for /ads generate, /ads dna screenshots)
        Write-Host ""
        Write-Host "Installing Python dependencies..."
        $ErrorActionPreference = "Continue"
        pip install -q -r "$SkillDir\requirements.txt" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  OK Python dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "  Warning: pip install failed. Run manually: pip install -r $SkillDir\requirements.txt" -ForegroundColor Yellow
        }

        # Install Chromium for brand screenshot capture (/ads dna visual scan)
        Write-Host "Installing Chromium for brand screenshots..."
        python -m playwright install chromium 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  OK Chromium ready (brand screenshots enabled)" -ForegroundColor Green
        } else {
            Write-Host "  Warning: Playwright install failed. Fix: python -m playwright install chromium" -ForegroundColor Yellow
        }
        $ErrorActionPreference = "Stop"

        Write-Host ""
        Write-Host "Claude Ads installed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "  Installed:"
        Write-Host "    - 2 main skills (ads + seo orchestrators)"
        Write-Host "    - 26 sub-skills (17 ads + 9 seo)"
        Write-Host "    - 14 agents (6 ad audit + 4 creative + 4 seo audit)"
        Write-Host "    - 30 reference files"
        Write-Host "    - 11 industry templates"
        Write-Host ""
        Write-Host "Usage:"
        Write-Host "  1. Start Claude Code:  claude"
        Write-Host "  2. Run commands:       /ads audit"
        Write-Host "                         /ads plan saas"
        Write-Host "                         /seo audit example.com"
        Write-Host "                         /seo aeo example.com"
    }
    finally {
        # Cleanup temp directory
        if (Test-Path $TempDir) {
            Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

Main
