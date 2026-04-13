param(
    [string]$TargetDir = ".",
    [string]$ConfigPath = "",
    [switch]$NoBackup
)

$ErrorActionPreference = "Stop"

$kitRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$manifestPath = Join-Path $kitRoot "package-manifest.json"
$exampleConfigPath = Join-Path $kitRoot "project.config.example.json"

if (-not (Test-Path $manifestPath)) {
    throw "Missing package-manifest.json at $manifestPath"
}

if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
}

$targetRoot = Resolve-Path $TargetDir
$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
    $candidates = @(
        (Join-Path $targetRoot ".conductor-kit/project.config.json"),
        (Join-Path $targetRoot "project.config.json"),
        (Join-Path $kitRoot "project.config.json")
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            $ConfigPath = $candidate
            break
        }
    }
}

if ([string]::IsNullOrWhiteSpace($ConfigPath) -or -not (Test-Path $ConfigPath)) {
    Write-Host "Config file not found. Falling back to example config." -ForegroundColor Yellow
    $ConfigPath = $exampleConfigPath
}

$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$today = Get-Date -Format "yyyy-MM-dd"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

$tokens = [ordered]@{
    "{{PROJECT_NAME}}" = [string]$config.project_name
    "{{PROJECT_STACK}}" = [string]$config.project_stack
    "{{FRONTEND_DEPLOY}}" = [string]$config.frontend_deploy
    "{{BACKEND_DEPLOY}}" = [string]$config.backend_deploy
    "{{USER_NAME}}" = [string]$config.user_name
    "{{ASSISTANT_NAME}}" = [string]$config.assistant_name
    "{{DEFAULT_ASSIGNEE}}" = [string]$config.default_assignee
    "{{FULL_STACK_DOC_PATH}}" = [string]$config.full_stack_doc_path
    "{{TODAY}}" = $today
}

function Render-Template {
    param(
        [string]$Content,
        [hashtable]$Map
    )

    $rendered = $Content
    foreach ($key in $Map.Keys) {
        $rendered = $rendered.Replace($key, $Map[$key])
    }
    return $rendered
}

$backupRoot = Join-Path $targetRoot ".conductor-kit/backups/$timestamp"
$installedFiles = @()

foreach ($entry in $manifest.files) {
    $sourcePath = Join-Path $kitRoot $entry.template
    $targetPath = Join-Path $targetRoot $entry.target
    $targetDirPath = Split-Path -Parent $targetPath

    if (-not (Test-Path $sourcePath)) {
        Write-Warning "Missing template: $sourcePath"; continue
    }

    if (-not (Test-Path $targetDirPath)) {
        New-Item -ItemType Directory -Force -Path $targetDirPath | Out-Null
    }

    if ((Test-Path $targetPath) -and (-not $NoBackup)) {
        $backupPath = Join-Path $backupRoot $entry.target
        $backupDir = Split-Path -Parent $backupPath
        if (-not (Test-Path $backupDir)) {
            New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
        }
        Copy-Item -Force $targetPath $backupPath
    }

    $content = Get-Content $sourcePath -Raw
    if ($entry.render) {
        $content = Render-Template -Content $content -Map $tokens
    }

    Set-Content -Path $targetPath -Value $content -Encoding UTF8
    $installedFiles += [string]$entry.target
}

$metadataDir = Join-Path $targetRoot ".conductor-kit"
if (-not (Test-Path $metadataDir)) {
    New-Item -ItemType Directory -Force -Path $metadataDir | Out-Null
}

$metadata = [ordered]@{
    version = $manifest.version
    installed_at = (Get-Date).ToString("s")
    target_dir = [string]$targetRoot
    config_path = [string](Resolve-Path $ConfigPath)
    files = $installedFiles
}

$metadata | ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $metadataDir "installed.json") -Encoding UTF8

Write-Host "Conductor kit installed." -ForegroundColor Green
Write-Host "Version: $($manifest.version)"
Write-Host "Files written: $($installedFiles.Count)"
Write-Host "Target: $targetRoot"
if (-not $NoBackup) {
    Write-Host "Backups: $backupRoot"
}
