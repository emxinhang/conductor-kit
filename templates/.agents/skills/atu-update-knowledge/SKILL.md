---
name: atu-update-knowledge
description: Tổng kết phiên làm việc, lưu kiến thức vào Project Memory và chuẩn bị cho phiên tiếp theo. Dùng khi kết thúc một task hoặc cuối ngày.
---

# Skill: Update Knowledge (ATu Project)

Dùng skill này khi kết thúc một task quan trọng, kết thúc ngày làm việc hoặc khi phát hiện một kiến thức/quy chuẩn mới cần lưu trữ cho tương lai.

## Quy trình thực thi

### 1. Phân tích Phiên làm việc (Session Review)
Xác định lại các task đã hoàn thành và xem xét:
- Những kiến thức mới về lỗi, cách fix hoặc pattern vừa nảy sinh.
- Các quyết định kỹ thuật mới.

### 2. Đánh giá Mức độ quan trọng (Prioritization)
- **P0 — Critical**: Lỗi nghiêm trọng, bảo mật, mất dữ liệu (⚠️). Ghi ngay.
- **P1 — Important**: Pattern lặp lại ≥2 lần, ảnh hưởng nhiều module.
- **P2 — Useful**: Trick hay.
- **P3 — Trivial**: Kiến thức căn bản - KHÔNG ghi.

### 3. Cập nhật Memory (`docs/memory/`)
Ghi vào các file tương ứng (00_active_context, 01_frontend_guidelines, 02_backend_guidelines, 03_devops_infra, 04_tech_decisions_log).

### 4. Quản lý trạng thái Track & Conductor
Nếu có sự thay đổi về trạng thái (status) của bất kỳ track nào:
- **Bắt buộc**: Sử dụng lệnh `python conductor/status.py transition <id> <phase> <agent> "<note>"` để cập nhật đồng bộ **4 nơi**: `tracks.md`, `state.md`, `CHANGELOG.md` và `docs/memory/00_active_context.md`.
- **Tuyệt đối không sửa tay** các trạng thái track trong các file này (đặc biệt là cột Status trong `tracks.md` và label trong `00_active_context.md`) để tránh sai lệch metadata.
- **Cập nhật `conductor/state.md`**: Khi xong plan (thêm vào PIPELINE) hoặc xong implement (chuyển sang QA, dùng `status.py transition` với phase tương ứng).

### 5. Lưu trạng thái Session (Session Save)
Lưu theo agent — KHÔNG dùng `session_save.md` chung nữa:

| Agent Role | File lưu |
|---|---|
| **CS (Planner)** | `docs/memory/session_save_cs.md` |
| **AG/CD (Implementer)** | `conductor/tracks/[track-id]/SESSION.md` |

**Format Session:** Tóm tắt công việc đã làm, việc dở dang, file đang mở và bước tiếp theo cụ thể.

### 6. Báo cáo tổng kết (Final Report)
Báo cáo cho ATu:
- Kiến thức đã lưu.
- Trạng thái Track (Cũ -> Mới).
- Thông báo "Session saved ✓" và gợi ý ATu dùng `/new-conversation` lần tới.

## Nguyên tắc giao tiếp
- Luôn sử dụng Tiếng Việt.
- Overwrite file session: Chỉ giữ trạng thái mới nhất. Xóa `SESSION.md` khi track hoàn thành.

