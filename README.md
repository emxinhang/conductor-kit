# Conductor Kit

Portable workflow pack for installing the same `conductor`, `docs`, `.agent`, `.claude`, and `.codex` conventions into other repositories.

## Origin

This kit was originally inspired by, and partially adapted from, the upstream Conductor project:

- `gemini-cli-extensions/conductor`
- https://github.com/gemini-cli-extensions/conductor

This repo is not a Gemini CLI extension. It is a portable workflow kit adapted for multi-agent local use across `.agent`, `.claude`, and `.codex`.

## Overview

This repo is the reusable distribution layer for the Conductor workflow.

It packages:
- `conductor/workflow.md` as the canonical workflow reference
- `docs/` and `docs/memory/` as the shared documentation and memory roots
- Core workflow wiring for `.agent`, `.claude`, and `.codex`
- A PowerShell installer that copies templates into another repository

This is intentionally a **core pack**, not the full TMS engineering skill library.

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

## Included In v1

- `conductor/workflow.md`
- `conductor/tracks.md`
- `docs/WORKFLOW_STANDARD.md`
- `docs/project_memory.md`
- `docs/memory/*`
- `.agent/workflows/new-conversation.md`
- `.agent/workflows/update-knowleadge.md`
- `.agent/workflows/atu-style.md`
- `.claude/CLAUDE.md`
- `.claude/skills/{conductor,new-conversation,update-knowledge}`
- `.codex/skills/{conductor,new-conversation,update-knowledge}`

## Not Included In v1

- full TMS skill libraries
- project-specific tracks
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

# Conductor Kit

Bộ workflow portable để cài cùng một chuẩn `conductor`, `docs`, `.agent`, `.claude`, và `.codex` sang các repository khác.

## Nguồn Gốc

Bộ kit này ban đầu được lấy cảm hứng và thích nghi một phần từ upstream Conductor:

- `gemini-cli-extensions/conductor`
- https://github.com/gemini-cli-extensions/conductor

Repo này không phải Gemini CLI extension. Nó là bộ workflow portable đã được chỉnh lại để dùng cục bộ cho nhiều agent: `.agent`, `.claude`, và `.codex`.

## Tổng Quan

Repo này là lớp phân phối dùng lại của workflow Conductor.

Nó đóng gói:
- `conductor/workflow.md` làm workflow reference canonical
- `docs/` và `docs/memory/` làm gốc tài liệu và memory dùng chung
- wiring cốt lõi cho `.agent`, `.claude`, và `.codex`
- một installer PowerShell để copy template sang repo khác

Repo này chủ ý chỉ là **core pack**, không phải toàn bộ thư viện skill của TMS.

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

## Phạm Vi Có Trong v1

- `conductor/workflow.md`
- `conductor/tracks.md`
- `docs/WORKFLOW_STANDARD.md`
- `docs/project_memory.md`
- `docs/memory/*`
- `.agent/workflows/new-conversation.md`
- `.agent/workflows/update-knowleadge.md`
- `.agent/workflows/atu-style.md`
- `.claude/CLAUDE.md`
- `.claude/skills/{conductor,new-conversation,update-knowledge}`
- `.codex/skills/{conductor,new-conversation,update-knowledge}`

## Chưa Bao Gồm Trong v1

- full skill libraries của TMS
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
