param(
    [string]$SourceRoot = ".."
)

$ErrorActionPreference = "Stop"

$kitRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $kitRoot $SourceRoot)

$syncMap = @(
    @{ Source = "conductor/workflow.md"; Target = "templates/conductor/workflow.md" },
    @{ Source = "docs/WORKFLOW_STANDARD.md"; Target = "templates/docs/WORKFLOW_STANDARD.md" },
    @{ Source = "docs/project_memory.md"; Target = "templates/docs/project_memory.md" },
    @{ Source = "docs/memory/MEMORY.md"; Target = "templates/docs/memory/MEMORY.md" },
    @{ Source = "memory/MEMORY.md"; Target = "templates/memory/MEMORY.md" },
    @{ Source = ".agent/workflows/new-conversation.md"; Target = "templates/.agent/workflows/new-conversation.md" },
    @{ Source = ".agent/workflows/update-knowleadge.md"; Target = "templates/.agent/workflows/update-knowleadge.md" },
    @{ Source = ".claude/docs/WORKFLOW_STANDARD.md"; Target = "templates/.claude/docs/WORKFLOW_STANDARD.md" },
    @{ Source = ".claude/skills/conductor/SKILL.md"; Target = "templates/.claude/skills/conductor/SKILL.md" },
    @{ Source = ".claude/skills/new-conversation/SKILL.md"; Target = "templates/.claude/skills/new-conversation/SKILL.md" },
    @{ Source = ".claude/skills/update-knowledge/SKILL.md"; Target = "templates/.claude/skills/update-knowledge/SKILL.md" },
    @{ Source = ".codex/skills/conductor/SKILL.md"; Target = "templates/.codex/skills/conductor/SKILL.md" },
    @{ Source = ".codex/skills/new-conversation/SKILL.md"; Target = "templates/.codex/skills/new-conversation/SKILL.md" },
    @{ Source = ".codex/skills/update-knowledge/SKILL.md"; Target = "templates/.codex/skills/update-knowledge/SKILL.md" }
)

foreach ($entry in $syncMap) {
    $sourcePath = Join-Path $repoRoot $entry.Source
    $targetPath = Join-Path $kitRoot $entry.Target
    $targetDir = Split-Path -Parent $targetPath

    if (-not (Test-Path $sourcePath)) {
        throw "Missing canonical source: $sourcePath"
    }

    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    }

    Copy-Item -Force $sourcePath $targetPath
    Write-Host "Synced $($entry.Source) -> $($entry.Target)"
}

Write-Host "Conductor kit templates refreshed from canonical sources." -ForegroundColor Green
