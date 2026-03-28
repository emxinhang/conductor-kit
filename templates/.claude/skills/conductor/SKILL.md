---
name: conductor
description: Quan ly task theo quy trinh Conductor - theo doi tien do tracks, cap nhat status, va duy tri documentation. Dung khi bat dau/ket thuc task, can kiem tra tien do, hoac cap nhat trang thai tracks.
---

# Conductor Workflow Skill

`conductor/workflow.md` la workflow reference canonical cho toan repo.

## Tai nguyen chia se

- Shared state (doc truoc tien): `conductor/state.md`
- Dashboard: `python conductor/status.py`
- Workflow reference: `conductor/workflow.md`
- Track status master list: `conductor/tracks.md`
- Shared docs root: `docs/`
- Memory index: `docs/memory/MEMORY.md`
- Huong dan day du: `conductor/CONDUCTOR_GUIDE.md`

## Cach su dung

### 1. Kiem tra tien do tong quan
```bash
python conductor/status.py   # Dashboard nhanh
```
Hoac doc `conductor/state.md` de xem ACTIVE / PIPELINE / DONE.

### 2. Bat dau lam viec tren track
1. Doc `conductor/state.md` → xem ACTIVE track va PIPELINE
2. Doc `PRD.md` / `spec.md` / `IMPLEMENTATION_PLAN.md` cua track
3. Cap nhat status theo state machine trong `conductor/workflow.md`
4. Ghi `CHANGELOG.md` neu co status transition
5. Update `state.md` ACTIVE khi bat dau implement

### 3. Trong luc thuc hien
- Giu `conductor/state.md` ACTIVE notes cap nhat
- Khi pause: ghi `conductor/tracks/[id]/SESSION.md`
- Giu `CHANGELOG.md` va `tracks.md` khop nhau

### 4. Ket thuc session hoac ket thuc track
1. Verify code theo workflow hien hanh
2. Cap nhat status va `CHANGELOG.md` neu co doi status
3. `python conductor/status.py close <id> [agent] [note]` → done + remove khoi PIPELINE/UPCOMING + promote PIPELINE[0] len ACTIVE
4. Dung `/update-knowledge` de luu learnings vao `docs/memory/`

### 5. QA Gate checklist (bat buoc truoc khi transition → qa)

Truoc khi chay `python conductor/status.py transition <id> qa`:
- [ ] **Frontend build**: `npm run build` chay khong loi
- [ ] **Backend runtime**: script QA chay duoc trong venv (`python qa_script.py`)
- [ ] **Artifact saved**: file script + log output da luu vao `conductor/tracks/<id>/qa/`
- [ ] **Gitignore safe**: thu muc `qa/` khong bi `.gitignore` chan

Neu thieu bat ky dieu kien nao tren → **KHONG duoc chuyen sang QA phase**.
`status.py transition <id> qa` se warn neu chua co thu muc `qa/`.

## Quy tac quan trong

- Khong coi `.claude/docs/WORKFLOW_STANDARD.md` la source of truth nua; file do chi con la redirect
- Khong ghi persistent memory ben ngoai `docs/memory/`
- Luon follow state machine va DoD trong `conductor/workflow.md`

## Lien ket voi cac skill khac

- `/new-conversation` - load context tu `docs/memory/` va `conductor/tracks.md`
- `/update-knowledge` - luu learnings va session state vao `docs/memory/`
- `/module-workflow` - workflow module moi
- `/refactor-workflow` - workflow refactor
- `/qa-verify-expert` - audit data integrity, API contracts, QA artifacts truoc khi done
