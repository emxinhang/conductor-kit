---
description: Tổng kết phiên làm việc, lưu kiến thức vào Project Memory và chuẩn bị cho phiên tiếp theo. Dùng khi kết thúc một task hoặc cuối ngày.
---

> Reference: `conductor/workflow.md` + `docs/memory/MEMORY.md`

## 1. Review Session (Đánh giá phiên làm việc)

- Nhìn lại các tool đã gọi và task đã hoàn thành trong conversation này.
- Xác định "Kiến thức mới" (New Knowledge) hoặc "Quyết định kỹ thuật" (Tech Decision).
- *Ví dụ*: Một cách fix bug lạ, một thư viện mới, một rule CSS đặc biệt.

## 2. Importance Scoring (Đánh giá mức độ quan trọng)

Trước khi ghi vào memory, đánh giá mỗi kiến thức theo thang:

| Score | Tiêu chí | Hành động |
|-------|----------|-----------|
| **P0 — Critical** | Gây production bug, data loss, hoặc security issue | ✅ GHI NGAY vào memory + đánh dấu `⚠️` |
| **P1 — Important** | Pattern lặp lại ≥2 lần hoặc ảnh hưởng nhiều module | ✅ GHI vào memory |
| **P2 — Useful** | Trick hay nhưng chỉ áp dụng 1 chỗ cụ thể | ⏳ GHI nếu memory file chưa quá dài, else skip |
| **P3 — Trivial** | Kiến thức hiển nhiên, dễ tìm lại trong code | ❌ KHÔNG GHI — tránh bloat memory |

**Rule**: Chỉ ghi P0 + P1 bắt buộc. P2 tùy dung lượng. P3 never.

## 3. Update Fragmented Memory (`docs/memory/`)

Tùy thuộc phạm trù, ghi vào đúng file chuyên biệt:
- 🎨 **Frontend rules/bugs**: `docs/memory/01_frontend_guidelines.md`
- 🗄 **Backend rules/bugs**: `docs/memory/02_backend_guidelines.md`
- 🚀 **DevOps/Config**: `docs/memory/03_devops_infra.md`
- 📚 **Logic/Decisions**: `docs/memory/04_tech_decisions_log.md`
- 📍 **Status Project**: `docs/memory/00_active_context.md`

**Format ghi**: Viết ngắn gọn súc tích bằng tiếng Việt. Mỗi entry có dạng:
```
### [P0/P1/P2] Tên kiến thức (YYYY-MM-DD)
- **Vấn đề**: ...
- **Giải pháp**: ...
- **Áp dụng khi**: ...
```

## 4. Memory Pruning (Định kỳ)

Khi memory file vượt **40KB**:
- Review các entry P2 cũ hơn 30 ngày → xóa nếu không còn relevant
- Merge các entry trùng lặp thành 1
- Giữ nguyên P0 + P1 entries (không bao giờ xóa)

## 5. Update Track Transition Ledger

Nếu track có thay đổi status trong session này, ghi vào `CHANGELOG.md` trong folder track:

```markdown
## Changelog
| Date | From | To | Agent | Note |
|------|------|----|-------|------|
| 2026-03-16 | 📅 Planned | 💻 Dev | CS | Bắt đầu implement backend |
| 2026-03-17 | 💻 Dev | 🧪 QA | CS | Backend + Frontend done, chờ ATu test |
```

Đồng thời update status trong `conductor/tracks.md`.

## 6. Session Save (Lưu trạng thái session)

Ghi file `docs/memory/session_save.md` với format:

```markdown
# Session Save
> Saved: YYYY-MM-DD HH:MM

## Track đang làm
- Track [ID]: [Tên] — [Status hiện tại]

## Đã hoàn thành trong session này
- [Liệt kê ngắn gọn]

## Đang dở dang
- [Task/step cụ thể chưa xong]

## Next Steps
- [Bước tiếp theo cần làm ngay khi resume]

## Context cần nhớ
- [Biến, state, decision quan trọng mà session sau cần biết]
```

**Rule**: File này sẽ bị **overwrite** mỗi lần save. Chỉ giữ state mới nhất.

## 7. Maintain Zero-Loop Skill

- Nếu phát hiện quy trình lặp hoặc lỗi hệ thống mới → update `.agent/skills/zero-loop-dev/SKILL.md`

## 8. Final Report

Báo cáo cho ATu:
- Đã lưu [X] entries (P0: N, P1: N)
- Track [ID] status: [old] → [new]
- Session saved ✓
- Gợi ý: "Lần sau gõ `/new-conversation` để em load lại context"
