---
name: update-knowledge
description: Tong ket phien lam viec, luu kien thuc vao Project Memory va chuan bi cho phien tiep theo. Dung khi ket thuc mot task hoac cuoi ngay lam viec.
---

# Update Knowledge Skill

Su dung skill nay de tong ket va luu tru kien thuc sau moi phien lam viec.

## Khi nao dung
- Ket thuc mot task lon
- Cuoi ngay lam viec
- Phat hien kien thuc moi quan trong
- Giai quyet xong mot bug kho

## He thong Memory (Fragmented)

```
Layer 1 — Auto-load (Claude Code tu xu ly):
  .claude/CLAUDE.md              → Repo-wide instructions (KHONG sua o day)
  docs/memory/MEMORY.md          → Quick index

Layer 2 — Lazy-load theo thu muc (Claude Code tu xu ly):
  frontend/CLAUDE.md             → Static frontend patterns (KHONG sua o day)
  backend/CLAUDE.md              → Static backend patterns (KHONG sua o day)

Layer 3 — Fragmented Memory (update-knowledge viet vao day):
  docs/memory/00_active_context.md        → Trang thai hien tai
  docs/memory/01_frontend_guidelines.md   → Frontend rules/bugs
  docs/memory/02_backend_guidelines.md    → Backend rules/bugs
  docs/memory/03_devops_infra.md          → DevOps/Config
  docs/memory/04_tech_decisions_log.md    → Lich su quyet dinh kien truc

Session State (per-agent — khong dung chung):
  docs/memory/session_save_cs.md          → CS planning/orchestration context
  conductor/tracks/[id]/SESSION.md        → AG/CD implementation context
  [DEPRECATED] docs/memory/session_save.md
```

**Quy tac**: `update-knowledge` chi viet vao **Layer 3** (`docs/memory/`). KHONG chinh sua CLAUDE.md files (Layer 1, 2).

## Quy trinh thuc hien

### 1. Review Session (Danh gia phien lam viec)
- Nhin lai cac tool da goi va task da hoan thanh trong conversation nay.
- Xac dinh "Kien thuc moi" nao quan trong (bug fix, pattern, gotcha).
- Bo qua nhung gi da co trong CLAUDE.md files hoac da co trong `docs/memory/`.

### 2. Importance Scoring (Danh gia muc do quan trong)

Truoc khi ghi vao memory, danh gia moi kien thuc:

| Score | Tieu chi | Hanh dong |
|-------|----------|-----------|
| **P0 — Critical** | Gay production bug, data loss, security issue | ✅ GHI NGAY + danh dau `⚠️` |
| **P1 — Important** | Pattern lap lai ≥2 lan hoac anh huong nhieu module | ✅ GHI vao memory |
| **P2 — Useful** | Trick hay nhung chi ap dung 1 cho cu the | ⏳ GHI neu file chua qua dai |
| **P3 — Trivial** | Kien thuc hien nhien, de tim lai trong code | ❌ KHONG GHI — tranh bloat |

**Rule**: Chi ghi P0 + P1 bat buoc. P2 tuy dung luong. P3 never.

### 3. Update Fragmented Memory (`docs/memory/`)

Phan loai va ghi vao file tuong ung:
- 📍 **Status Project**: Cap nhat `docs/memory/00_active_context.md`
- 🎨 **Frontend rules/bugs**: Ghi vao `docs/memory/01_frontend_guidelines.md`
- 🗄 **Backend rules/bugs**: Ghi vao `docs/memory/02_backend_guidelines.md`
- 🚀 **DevOps/Config**: Ghi vao `docs/memory/03_devops_infra.md`
- 📚 **Logic/Decisions**: Ghi vao `docs/memory/04_tech_decisions_log.md`

Doc noi dung cu truoc, roi dung `edit` de chen thong tin moi. Viet ngan gon suc tich bang tieng Viet.

**Format ghi** — dùng cấu trúc L1/L2/L3 để phần quan trọng nhất luôn ở trên:
```
### [P0/P1] Tên kiến thức (YYYY-MM-DD)
**L1 — Critical Facts:** [1-2 câu cốt lõi — phần luôn được đọc khi load context]
**L2 — Context:** [Detail cần thiết khi đào sâu — bỏ qua nếu L1 đã đủ]
**L3 — References:** [File:line hoặc track ID liên quan — bỏ qua nếu không có]
```

**Ví dụ đúng:**
```
### [P1] selectinload bắt buộc cho nested relations (2026-04-07)
**L1 — Critical Facts:** Async SQLAlchemy không hỗ trợ lazy load — dùng selectinload() cho tất cả relations cần trong response, joinedload() cho many-to-one.
**L2 — Context:** Lỗi hay gặp: "MissingGreenlet" khi quên eager load. Pattern đúng: options(selectinload(Model.items).joinedload(Item.owner)).
**L3 — References:** backend/app/services/pdf_service.py:38
```

**Ví dụ sai — không viết như này:**
```
### Ghi nhớ về database
Hôm nay phát hiện rằng khi làm việc với SQLAlchemy trong môi trường async, 
cần phải sử dụng selectinload thay vì lazy loading vì... [đoạn dài]
```

**Word limit:** L1 ≤ 2 câu. L2 ≤ 3 câu. L3 chỉ là reference pointer.

### 4. Memory Pruning (Dinh ky)

Khi memory file vuot **40KB**:
- Review cac entry P2 cu hon 30 ngay → xoa neu khong con relevant
- Merge cac entry trung lap thanh 1
- Giu nguyen P0 + P1 entries (khong bao gio xoa)

### 5. Constitution Sync Check

Sau khi score P0/P1 entries, hỏi:

> **"Entry nào dưới đây nên vào `conductor/constitution.md` không?"**

Tiêu chí để vào constitution (khác với memory thông thường):

| Tiêu chí | Memory | Constitution |
|----------|--------|-------------|
| Scope | Track/module cụ thể | Ảnh hưởng MỌI track tương lai |
| Loại | Bug fix, workaround | Architectural invariant, non-negotiable rule |
| Ví dụ | "Track 102 dùng selectinload" | "`selectinload` REQUIRED cho ALL nested relations" |

**Nếu có entry đủ điều kiện** → Báo ATu:
```
⚠️ Constitution Update Suggested:
- [Rule]: <mô tả ngắn gọn>
- [Why]: <lý do — incident, bug pattern, hoặc non-negotiable decision>
Anh muốn em cập nhật conductor/constitution.md không?
```

**Nếu ATu đồng ý** → Append vào section phù hợp trong `conductor/constitution.md` + update Changelog table ở cuối file.

**Nếu không có gì đủ điều kiện** → Bỏ qua, không mention.

### 5.5. Contract Registry Sync (track 014+ — nếu track có API/DB changes)

Bỏ qua nếu track không có `contract_delta.md`.

Kiểm tra và cập nhật `docs/contracts/_registry.md`:
- Version đã bump đúng chưa? (PATCH / MINOR / MAJOR theo semver)
- Date đã cập nhật chưa? (ngày hôm nay)
- Breaking changes đã được ghi vào Breaking Change Log chưa?

Nếu chưa → cập nhật ngay trước khi lưu session.

**Không cần** cập nhật `docs/contracts/api/ha_lac.yaml` ở đây — việc đó đã làm trong `planner-track` và `done-checklist`.

### 6. Update Track Transition Ledger

Neu track co thay doi status trong session nay, ghi vao `CHANGELOG.md` trong folder track:

```markdown
## Changelog
| Date | From | To | Agent | Note |
|------|------|----|-------|------|
| 2026-03-16 | 📅 Planned | 💻 Dev | CS | Bat dau implement backend |
| 2026-03-17 | 💻 Dev | 🧪 QA | CS | Backend + Frontend done, cho ATu test |
```

Dong thoi:
- **Bat buoc**: Dung lenh `python conductor/status.py transition <id> <phase> <agent> "<note>"` de cap nhat dong bo 4 noi: `tracks.md`, `state.md`, `CHANGELOG.md`, va `active_context.md`.
- **Khi phase=done**: lenh tren tu dong xoa track khoi PIPELINE/UPCOMING trong `state.md` va them vao DONE — KHONG can sua tay.
- **Khi phase=planned**: track phai duoc them tay vao `## PIPELINE` trong `state.md` (status.py chua tu dong hoa buoc nay).
- Tuyet doi khong sua tay cac file trang thai nay tru truong hop bat kha khang de tranh sai lech metadata.

### 7. Session Save — luu theo agent

**Khong dung `session_save.md` chung nua.** Luu theo PURPOSE:

**CS** → `docs/memory/session_save_cs.md`:
```markdown
# Session Save — CS
> Saved: YYYY-MM-DD

## Track dang lam
- Track [ID]: [Ten] — [Status]

## Hoan thanh trong session nay
- [x] ...

## Do dang
- [ ] ...

## Next Steps / Key Decisions
- ...
```

**AG hoac CD** → `conductor/tracks/[track-id]/SESSION.md`:
```markdown
# SESSION — [track-id]
> Last updated: YYYY-MM-DD | Agent: AG

## Status: In Progress

## Done so far
- [x] ...
- [ ] ...

## Do dang
- Chua xong [component], dang o file: ... ~line ...

## Next step khi resume
1. ...
```

**Rule**: Overwrite moi lan. Xoa `SESSION.md` khi track complete.
Update `conductor/state.md` ACTIVE notes khi pause.

### 8. Maintain Zero-Loop Skill
- Neu phat hien quy trinh lap hoac loi he thong moi → update `.claude/skills/zero-loop-dev/SKILL.md`

### 9. Final Report

Bao cao cho ATu:
- Da luu [X] entries (P0: N, P1: N)
- Track [ID] status: [old] → [new]
- Session saved ✓
- Goi y: "Lan sau go `/new-conversation` de em load lai context"

## Files lien quan (Layer 3 - chi viet vao day)

| File | Muc dich |
|------|----------|
| `docs/memory/00_active_context.md` | Trang thai hien tai |
| `docs/memory/01_frontend_guidelines.md` | Frontend rules/bugs |
| `docs/memory/02_backend_guidelines.md` | Backend rules/bugs |
| `docs/memory/03_devops_infra.md` | DevOps/Config |
| `docs/memory/04_tech_decisions_log.md` | Lich su quyet dinh kien truc |
| `docs/memory/session_save_cs.md` | CS planning session (CS ghi) |
| `conductor/tracks/[id]/SESSION.md` | Track implement session (AG/CD ghi) |
| `conductor/state.md` | Update ACTIVE notes khi pause |
| `conductor/tracks.md` | Tien do tracks |
| `conductor/tracks/<id>/CHANGELOG.md` | Transition ledger per track |

## Lien ket voi cac skill khac
- `/new-conversation` - Nap lai context dau session
- `/conductor` - Quan ly tracks chi tiet
- `/zero-loop-dev` - Scaffold backend entities
