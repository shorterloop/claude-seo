$ErrorActionPreference = "Stop"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python 3 required" }

$SkillDir = Join-Path $HOME ".claude/skills"
if (-not (Test-Path (Join-Path $SkillDir "seo"))) { throw "claude-seo not installed" }

$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$SkillTarget = Join-Path $SkillDir "seo-content-sentinel"
$AgentDir = Join-Path $SkillDir "../agents"

New-Item -ItemType Directory -Path $SkillTarget -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $SkillTarget "scripts") -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $SkillTarget "references") -Force | Out-Null
New-Item -ItemType Directory -Path $AgentDir -Force | Out-Null

Copy-Item (Join-Path $SourceDir "skills/seo-content-sentinel/SKILL.md") (Join-Path $SkillTarget "SKILL.md") -Force
Copy-Item (Join-Path $SourceDir "agents/seo-content-sentinel.md") (Join-Path $AgentDir "seo-content-sentinel.md") -Force
Copy-Item (Join-Path $SourceDir "scripts/audit_content.py") (Join-Path $SkillTarget "scripts/audit_content.py") -Force
Copy-Item (Join-Path $SourceDir "references/*.md") (Join-Path $SkillTarget "references/") -Force

Write-Host "Done."
