# Conductor Kit — v3.4

Portable workflow pack for installing the same `conductor`, `docs`, `.agents`, `.claude`, and `.codex` conventions into other repositories.

Multi-agent support: **Claude** (CS) · **Gemini** (AG) · **Codex** (CD) — run in parallel, share one conductor runtime.

## Overview

This kit packages the Conductor workflow runtime + skills for 3 CLI tools in a single portable git repo.

**Conductor runtime** (shared state, installed into `conductor/`):
- `workflow.md` — canonical workflow reference
- `state.md` — ACTIVE / PIPELINE / DONE state machine
- `tracks.md` — track status master list
- `status.py` — CLI dashboard (`python conductor/status.py`)
- `CONDUCTOR_GUIDE.md` — usage guide
- `constitution.md` — non-negotiable architectural invariants (project-specific, fill in on install)
- `track-templates/SPEC_TEMPLATE.md` — spec template for `/brainstorm-track`
- `track-templates/TASKS_TEMPLATE.md` — task checklist template for `/planner-track`

**Agent skills** (installed into each CLI's folder):
- `.agents/skills/` — Gemini AG: `atu-conductor`, `atu-new-conversation`, `atu-update-knowledge`, `atu-handoff`, `brainstorm-track`, `planner-track`, `module-workflow`, `refactor-workflow`, `qa-verify-expert`, `frontend-standard-v1`, `zero-loop-dev`, `deploy-track`
- `.claude/skills/` — Claude CS: `conductor`, `new-conversation`, `update-knowledge`, `handoff`, `brainstorm-track`, `planner-track`, `module-workflow`, `refactor-workflow`, `qa-verify-expert`, `frontend-standard-v1`, `zero-loop-dev`, `deploy-track`
- `.codex/skills/` — Codex CD: `conductor`, `new-conversation`, `update-knowledge`, `handoff`, `brainstorm-track`, `planner-track`, `module-workflow`, `refactor-workflow`, `zero-loop-dev`, `deploy-track`

**Project memory** (installed into `docs/memory/`):
- `MEMORY.md`, `00_active_context.md`, `01_frontend_guidelines.md`, `02_backend_guidelines.md`
- `03_devops_infra.md`, `04_tech_decisions_log.md`, `session_save_cs.md`

This is intentionally a **core pack**, not the full engineering skill library.

## Recommended Git Model

Use this repo as a standalone Git repository and vendor it into each project with `git subtree`.

Why `git subtree`:
- no submodule friction
- each project keeps a full snapshot
- updates are explicit and easy to review
- local-folder projects can still use the same kit

Example:

```powershell
git subtree add --prefix tooling/conductor-kit <kit-repo-url> main --squash
```

Update:

```powershell
git subtree pull --prefix tooling/conductor-kit <kit-repo-url> main --squash
powershell -ExecutionPolicy Bypass -File tooling/conductor-kit/install.ps1 -TargetDir .
```

## Recommended Consumer Layout

```text
tooling/
  conductor-kit/
conductor/
docs/
.agent/
.claude/
.codex/
.conductor-kit/
```

`tooling/conductor-kit/` holds the reusable pack.

`.conductor-kit/` in the consumer repo holds install metadata, backups, and optional project config.

## Install Into Another Repository

1. Vendor or copy this repo into the target project.
2. Copy `tooling/conductor-kit/project.config.example.json` to `.conductor-kit/project.config.json` in the target repo.
3. Edit the project values.
4. Run:

```powershell
powershell -ExecutionPolicy Bypass -File tooling/conductor-kit/install.ps1 -TargetDir .
```

The installer auto-detects config in this order:
1. `.conductor-kit/project.config.json` in the target repo
2. `project.config.json` in the target repo
3. `project.config.json` inside the kit repo
4. `project.config.example.json` as fallback

You can also pass an explicit config path:

```powershell
powershell -ExecutionPolicy Bypass -File tooling/conductor-kit/install.ps1 -TargetDir . -ConfigPath .conductor-kit/project.config.json
```

## What The Installer Does

- copies files from `templates/` into the target repo
- creates missing directories
- backs up overwritten files to `.conductor-kit/backups/<timestamp>/`
- writes install metadata to `.conductor-kit/installed.json`

Recommended ignore in consumer repos:

```gitignore
.conductor-kit/backups/
```

## Included In v3.4

**conductor/**
- `workflow.md`, `state.md`, `tracks.md`, `status.py`, `CONDUCTOR_GUIDE.md`
- `constitution.md` — non-negotiable architectural invariants template
- `code_styleguides/{general,python,typescript}.md`
- `track-templates/{SPEC_TEMPLATE,TASKS_TEMPLATE}.md`

**docs/memory/**
- `MEMORY.md`, `00_active_context.md`, `01_frontend_guidelines.md`, `02_backend_guidelines.md`
- `03_devops_infra.md`, `04_tech_decisions_log.md`, `session_save_cs.md`

**.agents/**
- `workflows/atu-style.md`
- `skills/{atu-conductor,atu-new-conversation,atu-update-knowledge,atu-handoff}`
- `skills/{brainstorm-track,planner-track,module-workflow,refactor-workflow}`
- `skills/qa-verify-expert`
- `skills/frontend-standard-v1`
- `skills/zero-loop-dev` *(new in v3.4)*
- `skills/deploy-track` *(new in v3.4)*

**.claude/skills/**
- `{conductor,new-conversation,update-knowledge,handoff}`
- `{brainstorm-track,planner-track,module-workflow,refactor-workflow}`
- `qa-verify-expert`, `frontend-standard-v1`
- `zero-loop-dev`, `deploy-track` *(new in v3.4)*

**.codex/skills/**
- `{conductor,new-conversation,update-knowledge,handoff}`
- `{brainstorm-track,planner-track,module-workflow,refactor-workflow}`
- `zero-loop-dev`, `deploy-track` *(new in v3.4)*

## Not Included

- full engineering skill libraries
- project-specific tracks and specs
- project-specific memory content
- project-specific automation scripts

## Maintainer Sync Flow

When the canonical workflow changes in the source project:

1. Update the source-of-truth files there.
2. Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\sync-from-canonical.ps1 -SourceRoot <path-to-source-repo>
```

3. Review the diff in this repo.
4. Commit and tag a new version.
5. Pull that version into downstream projects and rerun the installer.

---

# Conductor Kit — v3.4 (Tiếng Việt)

Bộ workflow portable để cài cùng một chuẩn `conductor`, `docs`, `.agents`, `.claude`, và `.codex` sang các repository khác.

Hỗ trợ 3 CLI song song: **Claude** (CS) · **Gemini AG** · **Codex** (CD) — dùng chung một conductor runtime.

## Tổng Quan

Kit này đóng gói conductor runtime + skills cho 3 CLI tools trong 1 git repo portable.

Repo này chủ ý chỉ là **core pack**, không phải toàn bộ thư viện skill của dự án.

## Mô Hình Git Nên Dùng

Nên để repo này là một Git repo độc lập và nhúng vào từng project bằng `git subtree`.

Lý do dùng `git subtree`:
- không có friction kiểu submodule
- mỗi project giữ được snapshot đầy đủ
- update rõ ràng, dễ review
- các project local folder vẫn dùng chung một bộ kit

Ví dụ:

```powershell
git subtree add --prefix tooling/conductor-kit <kit-repo-url> main --squash
```

Update:

```powershell
git subtree pull --prefix tooling/conductor-kit <kit-repo-url> main --squash
powershell -ExecutionPolicy Bypass -File tooling/conductor-kit/install.ps1 -TargetDir .
```

## Cấu Trúc Nên Có Ở Repo Nhận

```text
tooling/
  conductor-kit/
conductor/
docs/
.agent/
.claude/
.codex/
.conductor-kit/
```

`tooling/conductor-kit/` chứa bộ kit tái sử dụng.

`.conductor-kit/` trong repo nhận dùng để chứa metadata cài đặt, backup, và file config riêng của project.

## Cài Vào Repository Khác

1. Nhúng hoặc copy repo này vào project đích.
2. Copy `tooling/conductor-kit/project.config.example.json` thành `.conductor-kit/project.config.json` trong repo đích.
3. Sửa lại giá trị theo project.
4. Chạy:

```powershell
powershell -ExecutionPolicy Bypass -File tooling/conductor-kit/install.ps1 -TargetDir .
```

Installer sẽ tự dò config theo thứ tự:
1. `.conductor-kit/project.config.json` trong repo đích
2. `project.config.json` trong repo đích
3. `project.config.json` trong chính repo kit
4. `project.config.example.json` làm fallback

Ngoài ra có thể truyền path rõ ràng:

```powershell
powershell -ExecutionPolicy Bypass -File tooling/conductor-kit/install.ps1 -TargetDir . -ConfigPath .conductor-kit/project.config.json
```

## Installer Làm Gì

- copy file từ `templates/` sang repo đích
- tạo thư mục còn thiếu
- backup file bị ghi đè vào `.conductor-kit/backups/<timestamp>/`
- ghi metadata cài đặt vào `.conductor-kit/installed.json`

Nên ignore trong repo đích:

```gitignore
.conductor-kit/backups/
```

## Phạm Vi Có Trong v3.4

**conductor/**
- `workflow.md`, `state.md`, `tracks.md`, `status.py`, `CONDUCTOR_GUIDE.md`
- `constitution.md` — template invariants kiến trúc bắt buộc
- `code_styleguides/{general,python,typescript}.md`
- `track-templates/{SPEC_TEMPLATE,TASKS_TEMPLATE}.md`

**docs/memory/**
- `MEMORY.md`, `00_active_context.md`, `01_frontend_guidelines.md`, `02_backend_guidelines.md`
- `03_devops_infra.md`, `04_tech_decisions_log.md`, `session_save_cs.md`

**.agents/skills/**, **.claude/skills/**
- `{conductor,new-conversation,update-knowledge,handoff}`
- `{brainstorm-track,planner-track,module-workflow,refactor-workflow}`
- `qa-verify-expert`, `frontend-standard-v1`
- `zero-loop-dev`, `deploy-track` *(mới trong v3.4)*

**.codex/skills/**
- `{conductor,new-conversation,update-knowledge,handoff}`
- `{brainstorm-track,planner-track,module-workflow,refactor-workflow}`
- `zero-loop-dev`, `deploy-track` *(mới trong v3.4)*

## Chưa Bao Gồm

- full skill libraries riêng theo project
- các track riêng theo project
- memory content riêng theo project
- automation scripts riêng theo project

## Luồng Sync Cho Người Maintain

Khi workflow canonical thay đổi ở source project:

1. Cập nhật source-of-truth ở repo nguồn.
2. Chạy:

```powershell
powershell -ExecutionPolicy Bypass -File .\sync-from-canonical.ps1 -SourceRoot <path-to-source-repo>
```

3. Review diff trong repo này.
4. Commit và tag version mới.
5. Pull version đó vào các project downstream rồi chạy lại installer.
