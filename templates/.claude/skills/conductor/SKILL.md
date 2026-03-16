---
name: conductor
description: Quan ly task theo quy trinh Conductor - theo doi tien do tracks, cap nhat status, va duy tri documentation. Dung khi bat dau/ket thuc task, can kiem tra tien do, hoac cap nhat trang thai tracks.
---

# Conductor Workflow Skill

`conductor/workflow.md` la workflow reference canonical cho toan repo.

## Tai nguyen chia se

- Workflow reference: `conductor/workflow.md`
- Track status master list: `conductor/tracks.md`
- Shared docs root: `docs/`
- Memory index: `docs/memory/MEMORY.md`

## Cach su dung

### 1. Kiem tra tien do tong quan
- Doc `conductor/workflow.md`
- Doc `conductor/tracks.md`

### 2. Bat dau lam viec tren track
1. Doc `PRD.md` / `spec.md`
2. Tao hoac cap nhat `IMPLEMENTATION_PLAN.md`
3. Cap nhat status theo state machine trong `conductor/workflow.md`
4. Ghi `CHANGELOG.md` neu co status transition

### 3. Trong luc thuc hien
- Theo doi status trong `conductor/tracks.md`
- Giu cho `CHANGELOG.md` va track status khop nhau
- Neu can memory/session state, dung `docs/memory/`

### 4. Ket thuc session hoac ket thuc track
1. Verify code theo workflow hien hanh
2. Cap nhat status va `CHANGELOG.md` neu co doi status
3. Dung `/update-knowledge` de luu learnings va session state vao `docs/memory/`

## Quy tac quan trong

- Khong coi `.claude/docs/WORKFLOW_STANDARD.md` la source of truth nua; file do chi con la redirect
- Khong ghi persistent memory ben ngoai `docs/memory/`
- Luon follow state machine va DoD trong `conductor/workflow.md`

## Lien ket voi cac skill khac

- `/new-conversation` - load context tu `docs/memory/` va `conductor/tracks.md`
- `/update-knowledge` - luu learnings va session state vao `docs/memory/`
- `/module-workflow` - workflow module moi
- `/refactor-workflow` - workflow refactor
