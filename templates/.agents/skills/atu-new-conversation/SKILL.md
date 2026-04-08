---
name: atu-new-conversation
description: Khởi động phiên làm việc mới, nạp context từ Project Memory và kiểm tra tiến độ dự án. Dùng ngay khi bắt đầu conversation mới.
---

# New Conversation Skill (ATu Project)

Sử dụng skill này để khởi động phiên làm việc mới một cách hiệu quả, nạp lại context dự án và kiểm tra trạng thái hiện tại.

## Khi nào dùng
- Bắt đầu conversation mới.
- Muốn nạp lại context dự án (sau khi bị mất context hoặc đổi agent).
- Cần kiểm tra tiến độ các Track trong Conductor.

## Nguồn tri thức (Knowledge Base)

### Codebase Navigation (Đọc trước khi grep/explore)
- `docs/codebase-map.md`: **LUÔN ĐỌC** để biết Feature -> Files map (19 domains). Giúp định vị file chính xác, không grep mò mẫm.

### Project Memory (Đọc theo Context Profile)
- `docs/memory/00_active_context.md`: **BẮT BUỘC ĐỌC** - Chứa trạng thái hiện tại, Track đang làm.
- `docs/memory/01_frontend_guidelines.md`: Frontend rules/bugs.
- `docs/memory/02_backend_guidelines.md`: Backend rules/bugs.
- `docs/memory/03_devops_infra.md`: DevOps/Config.
- `docs/memory/04_tech_decisions_log.md`: Lịch sử quyết định kiến trúc.

### Session State (Bám sát tiến độ)
- `conductor/state.md`: Shared state (ACTIVE track, PIPELINE queue).
- `conductor/tracks/[active-track]/SESSION.md`: AG/CD implementation context (nếu đang thực hiện track).
- `docs/memory/session_save_cs.md`: CS role context (nếu đang ở phase planning).

## Quy trình thực hiện

### 1. Detect Context Profile
Xác định **profile** dựa trên yêu cầu của ATu hoặc track đang active:
- `planning`: Brainstorm, lập kế hoạch, viết PRD (CS role).
- `backend`: Tập trung vào FastAPI, Database, API.
- `frontend`: Tập trung vào React, Next.js, UI/UX.
- `fullstack`: Cần cả Backend và Frontend.
- `debugging`: Fix bug, Root Cause Analysis.
- `devops`: Deploy, cấu hình hệ thống.
- **Mặc định**: Nếu chưa rõ scope -> dùng `planning`.

### 2. Load Knowledge Base (Theo Profile)
- **Luôn đọc**: `docs/memory/00_active_context.md` và `docs/codebase-map.md`.
- **Theo profile**: Chỉ đọc memory file tương ứng (ví dụ: profile `backend` đọc `02_backend_guidelines.md`).
- **KHÔNG load tất cả** để tiết kiệm token.

### 3. Auto-Search Memory (Thay vì đọc toàn bộ)
- Ưu tiên sử dụng `grep_search` trong thư mục `docs/memory/` với keyword cụ thể để tìm thông tin relevant nhanh chóng.

### 4. Load Conductor State + Session (QUAN TRỌNG)
- Đọc `conductor/state.md` để biết ACTIVE track.
- Kiểm tra file SESSION tương ứng (theo agent role) để khôi phục trạng thái làm việc.
- Nếu tìm thấy session cũ -> Tóm tắt và hỏi ATu: *"Em load được session từ lần trước: [tóm tắt]. Tiếp tục không?"*

### 5. Status Report & Ready
Báo cáo ngắn gọn cho ATu:
- **Profile detected**: [Tên profile]
- **Context loaded**: [Mục tiêu hiện tại]
- **Trạng thái**: Đang làm [Task X] / Chuẩn bị làm [Task Y]

## Tiêu chuẩn giao tiếp (ATu Style)
- **Ngôn ngữ**: BẮT BUỘC sử dụng **Tiếng Việt** (Technical terms giữ Tiếng Anh).
- **Suy nghĩ (Thought)**: Phải dùng Tiếng Việt 100% để ATu hiểu rõ tiến trình tư duy.
- **Thái độ**: Chủ động (Proactive), Minh bạch, Đồng đội.
- **Phản ứng lỗi**: Nếu gặp lỗi lạ hoặc lặp lại > 2 lần -> **DỪNG LẠI & HỎI** (Blocker Alert). Tuyệt đối không thử mò mẫm vô nghĩa.

## Liên kết với các skill khác
- `atu-conductor`: Quản lý tracks chi tiết.
- `atu-update-knowledge`: Lưu kiến thức cuối session.
- `zero-loop-dev`: Quy trình thực thi không lỗi lặp lại.
