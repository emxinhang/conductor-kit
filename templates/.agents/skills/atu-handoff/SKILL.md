---
name: atu-handoff
description: Quy trình AG tiếp quản code từ Codex/Cursor và thực thi Giai đoạn 2 (Execution & Verification)
---

# Skill: Handoff (Tiếp quản dự án)

Dùng skill này khi bắt đầu một dự án mà đã có Boilerplate từ Codex/Cursor cung cấp. Skill này giúp AG (Gemini) thẩm thấu bối cảnh và bắt đầu thực hiện dự án theo Giai đoạn 2 (Thực thi và Xác thực).

## Quy trình Handoff Chuẩn

### 0. Load Skills Bổ Trợ (Mandatory Load)
***BẮT BUỘC:*** Trước khi bắt đầu, AG phải sử dụng `view_file` để nạp kiến thức từ các skill sau tùy theo phạm vi task:
- **Nếu làm Backend**: Load `zero-loop-dev` và `qa-verify-expert`.
- **Nếu làm Frontend**: Load `frontend-standard-v1` và `frontend-qa-gatekeeper`.

### 1. Thẩm thấu bối cảnh (Context Absorption)
- **Bắt đầu**: Đọc file `IMPLEMENTATION_PLAN.md` mới nhất trong track hiện tại để hiểu bức tranh dự án.
- **Tiếp theo**: Đọc nội dung file `CHANGELOG.md` của track (nếu có) để xem lịch sử task.
- Nếu track mới khởi tạo: Đọc file `spec.md` và `plan.md` của track đó.

### 2. Khảo sát tình trạng Code (State Reconnaissance)
- Dùng `qa-verify-expert` chạy thử `python scripts/audit_schemas.py` (nếu liên quan tới DB) để kiểm tra Schema.

### 3. Thực thi theo chuẩn Zero-Loop (Execution)
- AG bắt đầu chọn Task tiếp theo trong `IMPLEMENTATION_PLAN.md` (chưa được đánh dấu `[x]`) để làm.
- **Backend API**: Sau khi code xong, gọi `verify_integrity.py` để check import & schemas.
- **Frontend**: Sau khi code xong, check linter (npm run build) ngay tại module đang làm.
- Quá trình viết code (Backend/Frontend) phải tuân thủ nghiêm ngặt kỹ năng `verification-before-completion`.

### 4. Chốt hạ (Verification-Before-Completion)
***TUYỆT ĐỐI NGHIÊM CẦM AG BÁO CÁO "HOÀN THÀNH" KHI CHƯA CHẠY KIỂM THỬ THỰC TẾ.***
- Nếu code API Backend: Tự động tạo 1 script Python tại `scripts/test_{tên_tính_năng}_handoff.py` (hoặc dùng curl), dùng `run_command` chạy script đó để lấy output 200 OK.
- Nếu code Frontend: AG phải đảm bảo không có linter error nào (dùng `npm run build`), nhắc user check UI nếu có.
- Trả kết quả màu Xanh (Logs/Terminal output) vào khung chat cho ATu xem như "Bằng chứng hoàn thành".
- Đánh dấu `[x]` vào `IMPLEMENTATION_PLAN.md` -> Chuyển hướng hỏi ATu task tiếp theo.

## Nguyên tắc Zero-Loop
Không chuyển task nếu chưa làm bước Verification. Code đến đâu, chạy đến đó.
