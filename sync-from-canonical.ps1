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
    @{ Source = ".agents/skills/brainstorm-track/SKILL.md";      Target = "templates/.agents/skills/brainstorm-track/SKILL.md" },
    @{ Source = ".agents/skills/planner-track/SKILL.md";         Target = "templates/.agents/skills/planner-track/SKILL.md" },
    @{ Source = ".agents/skills/module-workflow/SKILL.md";       Target = "templates/.agents/skills/module-workflow/SKILL.md" },
    @{ Source = ".agents/skills/refactor-workflow/SKILL.md";     Target = "templates/.agents/skills/refactor-workflow/SKILL.md" },
    @{ Source = ".agents/skills/qa-verify-expert/SKILL.md";      Target = "templates/.agents/skills/qa-verify-expert/SKILL.md" },
    @{ Source = ".agents/skills/frontend-standard-v1/SKILL.md";  Target = "templates/.agents/skills/frontend-standard-v1/SKILL.md" },
    @{ Source = ".agents/skills/zero-loop-dev/SKILL.md";         Target = "templates/.agents/skills/zero-loop-dev/SKILL.md" },
    @{ Source = ".agents/skills/deploy-track/SKILL.md";          Target = "templates/.agents/skills/deploy-track/SKILL.md" },

    # --- .claude/skills (Claude CS) — root files ---
    @{ Source = ".claude/skills/README.md";                      Target = "templates/.claude/skills/README.md" },
    @{ Source = ".claude/skills/SKILLS_CATALOG_VI.md";           Target = "templates/.claude/skills/SKILLS_CATALOG_VI.md" },

    # --- .claude/skills — core workflow ---
    @{ Source = ".claude/skills/conductor/SKILL.md";             Target = "templates/.claude/skills/conductor/SKILL.md" },
    @{ Source = ".claude/skills/new-conversation/SKILL.md";      Target = "templates/.claude/skills/new-conversation/SKILL.md" },
    @{ Source = ".claude/skills/update-knowledge/SKILL.md";      Target = "templates/.claude/skills/update-knowledge/SKILL.md" },
    @{ Source = ".claude/skills/handoff/SKILL.md";               Target = "templates/.claude/skills/handoff/SKILL.md" },
    @{ Source = ".claude/skills/brainstorm-track/SKILL.md";      Target = "templates/.claude/skills/brainstorm-track/SKILL.md" },
    @{ Source = ".claude/skills/planner-track/SKILL.md";         Target = "templates/.claude/skills/planner-track/SKILL.md" },
    @{ Source = ".claude/skills/module-workflow/SKILL.md";       Target = "templates/.claude/skills/module-workflow/SKILL.md" },
    @{ Source = ".claude/skills/refactor-workflow/SKILL.md";     Target = "templates/.claude/skills/refactor-workflow/SKILL.md" },
    @{ Source = ".claude/skills/qa-verify-expert/SKILL.md";      Target = "templates/.claude/skills/qa-verify-expert/SKILL.md" },
    @{ Source = ".claude/skills/frontend-standard-v1/SKILL.md";  Target = "templates/.claude/skills/frontend-standard-v1/SKILL.md" },
    @{ Source = ".claude/skills/zero-loop-dev/SKILL.md";         Target = "templates/.claude/skills/zero-loop-dev/SKILL.md" },
    @{ Source = ".claude/skills/deploy-track/SKILL.md";          Target = "templates/.claude/skills/deploy-track/SKILL.md" },
    @{ Source = ".claude/skills/done-checklist/SKILL.md";        Target = "templates/.claude/skills/done-checklist/SKILL.md" },
    @{ Source = ".claude/skills/review-plan/SKILL.md";           Target = "templates/.claude/skills/review-plan/SKILL.md" },

    # --- .claude/skills — architecture ---
    @{ Source = ".claude/skills/backend-architect/SKILL.md";     Target = "templates/.claude/skills/backend-architect/SKILL.md" },
    @{ Source = ".claude/skills/frontend-architect/SKILL.md";    Target = "templates/.claude/skills/frontend-architect/SKILL.md" },
    @{ Source = ".claude/skills/system-architect/SKILL.md";      Target = "templates/.claude/skills/system-architect/SKILL.md" },
    @{ Source = ".claude/skills/backend-development/SKILL.md";   Target = "templates/.claude/skills/backend-development/SKILL.md" },
    @{ Source = ".claude/skills/frontend-development/SKILL.md";  Target = "templates/.claude/skills/frontend-development/SKILL.md" },
    @{ Source = ".claude/skills/frontend-design/SKILL.md";       Target = "templates/.claude/skills/frontend-design/SKILL.md" },
    @{ Source = ".claude/skills/frontend-qa-gatekeeper/SKILL.md"; Target = "templates/.claude/skills/frontend-qa-gatekeeper/SKILL.md" },
    @{ Source = ".claude/skills/performance-engineer/SKILL.md";  Target = "templates/.claude/skills/performance-engineer/SKILL.md" },
    @{ Source = ".claude/skills/security-engineer/SKILL.md";     Target = "templates/.claude/skills/security-engineer/SKILL.md" },
    @{ Source = ".claude/skills/requirements-analyst/SKILL.md";  Target = "templates/.claude/skills/requirements-analyst/SKILL.md" },
    @{ Source = ".claude/skills/technical-writer/SKILL.md";      Target = "templates/.claude/skills/technical-writer/SKILL.md" },
    @{ Source = ".claude/skills/tech-stack-researcher/SKILL.md"; Target = "templates/.claude/skills/tech-stack-researcher/SKILL.md" },
    @{ Source = ".claude/skills/refactoring-expert/SKILL.md";    Target = "templates/.claude/skills/refactoring-expert/SKILL.md" },
    @{ Source = ".claude/skills/code-review/SKILL.md";           Target = "templates/.claude/skills/code-review/SKILL.md" },
    @{ Source = ".claude/skills/learning-guide/SKILL.md";        Target = "templates/.claude/skills/learning-guide/SKILL.md" },

    # --- .claude/skills — debugging ---
    @{ Source = ".claude/skills/debugging-defense-in-depth/SKILL.md";         Target = "templates/.claude/skills/debugging-defense-in-depth/SKILL.md" },
    @{ Source = ".claude/skills/debugging-root-cause-tracing/SKILL.md";        Target = "templates/.claude/skills/debugging-root-cause-tracing/SKILL.md" },
    @{ Source = ".claude/skills/debugging-systematic-debugging/SKILL.md";      Target = "templates/.claude/skills/debugging-systematic-debugging/SKILL.md" },
    @{ Source = ".claude/skills/debugging-verification-before-completion/SKILL.md"; Target = "templates/.claude/skills/debugging-verification-before-completion/SKILL.md" },
    @{ Source = ".claude/skills/systematic-debugging/SKILL.md";               Target = "templates/.claude/skills/systematic-debugging/SKILL.md" },
    @{ Source = ".claude/skills/verification-before-completion/SKILL.md";      Target = "templates/.claude/skills/verification-before-completion/SKILL.md" },
    @{ Source = ".claude/skills/when-stuck/SKILL.md";                          Target = "templates/.claude/skills/when-stuck/SKILL.md" },

    # --- .claude/skills — thinking frameworks ---
    @{ Source = ".claude/skills/collision-zone-thinking/SKILL.md";   Target = "templates/.claude/skills/collision-zone-thinking/SKILL.md" },
    @{ Source = ".claude/skills/inversion-exercise/SKILL.md";        Target = "templates/.claude/skills/inversion-exercise/SKILL.md" },
    @{ Source = ".claude/skills/meta-pattern-recognition/SKILL.md";  Target = "templates/.claude/skills/meta-pattern-recognition/SKILL.md" },
    @{ Source = ".claude/skills/scale-game/SKILL.md";                Target = "templates/.claude/skills/scale-game/SKILL.md" },
    @{ Source = ".claude/skills/simplification-cascades/SKILL.md";   Target = "templates/.claude/skills/simplification-cascades/SKILL.md" },
    @{ Source = ".claude/skills/red-team-reviewer/SKILL.md";         Target = "templates/.claude/skills/red-team-reviewer/SKILL.md" },

    # --- .claude/skills — tools/infra ---
    @{ Source = ".claude/skills/alembic-workflow/SKILL.md";   Target = "templates/.claude/skills/alembic-workflow/SKILL.md" },
    @{ Source = ".claude/skills/postgresql-psql/SKILL.md";    Target = "templates/.claude/skills/postgresql-psql/SKILL.md" },
    @{ Source = ".claude/skills/cloudflare-r2/SKILL.md";      Target = "templates/.claude/skills/cloudflare-r2/SKILL.md" },
    @{ Source = ".claude/skills/pdf-generation/SKILL.md";     Target = "templates/.claude/skills/pdf-generation/SKILL.md" },
    @{ Source = ".claude/skills/repomix/SKILL.md";            Target = "templates/.claude/skills/repomix/SKILL.md" },
    @{ Source = ".claude/skills/docs-seeker/SKILL.md";        Target = "templates/.claude/skills/docs-seeker/SKILL.md" },
    @{ Source = ".claude/skills/mcp-builder/SKILL.md";        Target = "templates/.claude/skills/mcp-builder/SKILL.md" },
    @{ Source = ".claude/skills/claude-code/SKILL.md";        Target = "templates/.claude/skills/claude-code/SKILL.md" },
    @{ Source = ".claude/skills/skill-creator/SKILL.md";      Target = "templates/.claude/skills/skill-creator/SKILL.md" },

    # --- .claude/skills — UI/styling ---
    @{ Source = ".claude/skills/shadcn-ui/SKILL.md";          Target = "templates/.claude/skills/shadcn-ui/SKILL.md" },
    @{ Source = ".claude/skills/tailwindcss/SKILL.md";        Target = "templates/.claude/skills/tailwindcss/SKILL.md" },

    # --- .claude/skills — atu-specific ---
    @{ Source = ".claude/skills/atu-compact/SKILL.md";        Target = "templates/.claude/skills/atu-compact/SKILL.md" },
    @{ Source = ".claude/skills/atu-hub-components/SKILL.md"; Target = "templates/.claude/skills/atu-hub-components/SKILL.md" },
    @{ Source = ".claude/skills/atu-react-component/SKILL.md"; Target = "templates/.claude/skills/atu-react-component/SKILL.md" },
    @{ Source = ".claude/skills/atu-summary-status/SKILL.md"; Target = "templates/.claude/skills/atu-summary-status/SKILL.md" },
    @{ Source = ".claude/skills/atu-typo-standard/SKILL.md";  Target = "templates/.claude/skills/atu-typo-standard/SKILL.md" },

    # --- .codex/skills (Codex CD) ---
    @{ Source = ".codex/skills/conductor/SKILL.md";              Target = "templates/.codex/skills/conductor/SKILL.md" },
    @{ Source = ".codex/skills/new-conversation/SKILL.md";       Target = "templates/.codex/skills/new-conversation/SKILL.md" },
    @{ Source = ".codex/skills/update-knowledge/SKILL.md";       Target = "templates/.codex/skills/update-knowledge/SKILL.md" },
    @{ Source = ".codex/skills/handoff/SKILL.md";                Target = "templates/.codex/skills/handoff/SKILL.md" },
    @{ Source = ".codex/skills/brainstorm-track/SKILL.md";       Target = "templates/.codex/skills/brainstorm-track/SKILL.md" },
    @{ Source = ".codex/skills/planner-track/SKILL.md";          Target = "templates/.codex/skills/planner-track/SKILL.md" },
    @{ Source = ".codex/skills/module-workflow/SKILL.md";        Target = "templates/.codex/skills/module-workflow/SKILL.md" },
    @{ Source = ".codex/skills/refactor-workflow/SKILL.md";      Target = "templates/.codex/skills/refactor-workflow/SKILL.md" },
    @{ Source = ".codex/skills/zero-loop-dev/SKILL.md";          Target = "templates/.codex/skills/zero-loop-dev/SKILL.md" },
    @{ Source = ".codex/skills/deploy-track/SKILL.md";           Target = "templates/.codex/skills/deploy-track/SKILL.md" }
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
