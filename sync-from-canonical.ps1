param(
    [string]$SourceRoot = ".."
)

$ErrorActionPreference = "Stop"

$kitRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Support both absolute paths and relative paths (relative to kitRoot)
if ([System.IO.Path]::IsPathRooted($SourceRoot)) {
    $repoRoot = Resolve-Path $SourceRoot
} else {
    $repoRoot = Resolve-Path (Join-Path $kitRoot $SourceRoot)
}

$syncMap = @(
    # --- conductor runtime ---
    @{ Source = "conductor/workflow.md";        Target = "templates/conductor/workflow.md" },
    @{ Source = "conductor/CONDUCTOR_GUIDE.md"; Target = "templates/conductor/CONDUCTOR_GUIDE.md" },
    @{ Source = "conductor/status.py";          Target = "templates/conductor/status.py" },
    @{ Source = "conductor/state.md";           Target = "templates/conductor/state.md" },
    @{ Source = "conductor/tracks.md";          Target = "templates/conductor/tracks.md" },
    @{ Source = "conductor/constitution.md";    Target = "templates/conductor/constitution.md" },

    # --- conductor track-templates ---
    @{ Source = "conductor/track-templates/SPEC_TEMPLATE.md";  Target = "templates/conductor/track-templates/SPEC_TEMPLATE.md" },
    @{ Source = "conductor/track-templates/TASKS_TEMPLATE.md"; Target = "templates/conductor/track-templates/TASKS_TEMPLATE.md" },

    # --- docs/memory ---
    @{ Source = "docs/memory/MEMORY.md";               Target = "templates/docs/memory/MEMORY.md" },
    @{ Source = "docs/memory/00_active_context.md";    Target = "templates/docs/memory/00_active_context.md" },
    @{ Source = "docs/memory/01_frontend_guidelines.md"; Target = "templates/docs/memory/01_frontend_guidelines.md" },
    @{ Source = "docs/memory/02_backend_guidelines.md";  Target = "templates/docs/memory/02_backend_guidelines.md" },
    @{ Source = "docs/memory/03_devops_infra.md";      Target = "templates/docs/memory/03_devops_infra.md" },
    @{ Source = "docs/memory/04_tech_decisions_log.md"; Target = "templates/docs/memory/04_tech_decisions_log.md" },
    @{ Source = "docs/memory/session_save_cs.md";      Target = "templates/docs/memory/session_save_cs.md" },

    # --- .agents/workflows (atu-style) ---
    @{ Source = ".agents/workflows/atu-style.md";      Target = "templates/.agents/workflows/atu-style.md" },

    # --- .agents/skills (Gemini AG) ---
    @{ Source = ".agents/skills/atu-conductor/SKILL.md";         Target = "templates/.agents/skills/atu-conductor/SKILL.md" },
    @{ Source = ".agents/skills/atu-new-conversation/SKILL.md";  Target = "templates/.agents/skills/atu-new-conversation/SKILL.md" },
    @{ Source = ".agents/skills/atu-update-knowledge/SKILL.md";  Target = "templates/.agents/skills/atu-update-knowledge/SKILL.md" },
    @{ Source = ".agents/skills/atu-handoff/SKILL.md";           Target = "templates/.agents/skills/atu-handoff/SKILL.md" },

    # --- .claude/skills (Claude CS) ---
    @{ Source = ".claude/skills/conductor/SKILL.md";         Target = "templates/.claude/skills/conductor/SKILL.md" },
    @{ Source = ".claude/skills/new-conversation/SKILL.md";  Target = "templates/.claude/skills/new-conversation/SKILL.md" },
    @{ Source = ".claude/skills/update-knowledge/SKILL.md";  Target = "templates/.claude/skills/update-knowledge/SKILL.md" },
    @{ Source = ".claude/skills/handoff/SKILL.md";           Target = "templates/.claude/skills/handoff/SKILL.md" },

    # --- .codex/skills (Codex CD) ---
    @{ Source = ".codex/skills/conductor/SKILL.md";         Target = "templates/.codex/skills/conductor/SKILL.md" },
    @{ Source = ".codex/skills/new-conversation/SKILL.md";  Target = "templates/.codex/skills/new-conversation/SKILL.md" },
    @{ Source = ".codex/skills/update-knowledge/SKILL.md";  Target = "templates/.codex/skills/update-knowledge/SKILL.md" },
    @{ Source = ".codex/skills/handoff/SKILL.md";           Target = "templates/.codex/skills/handoff/SKILL.md" }
)

$synced = 0
$skipped = 0

foreach ($entry in $syncMap) {
    $sourcePath = Join-Path $repoRoot $entry.Source
    $targetPath = Join-Path $kitRoot $entry.Target
    $targetDir = Split-Path -Parent $targetPath

    if (-not (Test-Path $sourcePath)) {
        Write-Host "SKIP (not found): $($entry.Source)" -ForegroundColor Yellow
        $skipped++
        continue
    }

    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    }

    Copy-Item -Force $sourcePath $targetPath
    Write-Host "Synced  $($entry.Source)" -ForegroundColor Cyan
    $synced++
}

Write-Host ""
Write-Host "Done. Synced: $synced | Skipped: $skipped" -ForegroundColor Green
Write-Host "Source: $repoRoot"
Write-Host "Kit:    $kitRoot"
