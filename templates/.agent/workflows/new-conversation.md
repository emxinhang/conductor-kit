---
description: Khởi động phiên làm việc mới, nạp context từ Project Memory và kiểm tra tiến độ dự án. Dùng ngay khi bắt đầu conversation mới.
---

> Reference: `conductor/workflow.md` + `docs/memory/MEMORY.md`

## 1. Detect Context Profile

Xác định **profile** dựa trên yêu cầu của ATu hoặc track đang active:

| Profile | Khi nào | Memory cần load | Token budget |
|---------|---------|-----------------|--------------|
| `planning` | Bắt đầu track mới, brainstorm, PRD | `00_active_context` + `04_tech_decisions_log` | Nhẹ |
| `backend` | Implement/debug backend | `00_active_context` + `02_backend_guidelines` | Trung bình |
| `frontend` | Implement/debug frontend | `00_active_context` + `01_frontend_guidelines` | Trung bình |
| `fullstack` | Track có cả BE+FE | `00_active_context` + `01` + `02` | Nặng |
| `debugging` | Fix bug, RCA | `00_active_context` + file guidelines liên quan + RCA của track | Trung bình |
| `devops` | Deploy, migration, config | `00_active_context` + `03_devops_infra` | Nhẹ |

**Mặc định**: Nếu chưa rõ scope → dùng `planning` (nhẹ nhất). Hỏi ATu nếu cần.

## 2. Load Knowledge Base (theo Profile)

- **Luôn đọc**: `docs/memory/00_active_context.md` (status hiện tại)
- **Theo profile**: Chỉ đọc file memory tương ứng với profile ở bảng trên
- **KHÔNG load tất cả** — tiết kiệm token, chỉ load đúng thứ cần

## 3. Auto-Search Memory (thay vì đọc toàn bộ)

Nếu ATu đề cập keyword cụ thể (tên module, tên bug, pattern):
- Dùng `Grep` search trong `docs/memory/` với keyword đó
- Chỉ đọc phần relevant thay vì load cả file 49KB
- Ví dụ: ATu nói "fix timezone bug" → grep `timezone` trong `02_backend_guidelines.md` → đọc đúng section đó

## 4. Load Session State

Kiểm tra file `docs/memory/session_save.md`:
- **Nếu tồn tại**: Đọc và báo ATu:
  > "Em load được session save từ lần trước: [tóm tắt]. Anh muốn tiếp tục từ đây không?"
- **Nếu không tồn tại**: Bỏ qua, tiếp tục bình thường

## 5. Load AG Style

- Đọc `.agent/workflows/atu-style.md`
- Tuân thủ quy tắc Ngôn ngữ (Thinking & Planning bằng Tiếng Việt)

## 6. Check Conductor

- Đọc `conductor/tracks.md`
- Xác định Track đang Active (💻 Dev) hoặc Track tiếp theo cần làm (📅 Planned)
- Kiểm tra **Changelog** trong track folder nếu track đang dở (xem transition history)

## 7. Status Report & Ready

Báo cáo cho ATu:
- **Profile detected**: `[profile name]`
- **Context loaded**: [Tóm tắt mục tiêu hiện tại]
- **Trạng thái**: Đang làm dở [Task X] / Chuẩn bị làm [Task Y]
- **Checkpoint**: [Nếu có — tóm tắt session trước]
- Nhắc 1-2 lưu ý quan trọng từ Memory nếu liên quan đến task sắp làm
