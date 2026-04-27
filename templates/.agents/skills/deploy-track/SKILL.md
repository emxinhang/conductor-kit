---
name: deploy-track
description: Chuẩn hóa bước cuối cùng (Release) - Triển khai lên Railway/Vercel, chạy migration, kiểm tra Smoke test production và Rollback nếu có biến cố.
---

# Deploy Track Skill

Đóng vai trò Release Manager cho phase cuối cùng của luồng làm việc TMS-2026 (Phase 7).

## Trách nhiệm cốt lõi
1. Đảm bảo Database luôn được cập nhật an toàn (`alembic upgrade head`) trước khi nhả code backend.
2. Confirm status deployment của Backend (Railway) và Frontend (Vercel).
3. Đóng vai trò bảo hộ (Watchdog) cho Production.

## Workflow Thực thi (Release Pipeline)

1. **Pre-Flight Check**:
   - Yêu cầu người dùng (ATu) `commit` and `push` code lên branch gốc (Git). 
   *(Lưu ý: AG tuyệt đối không tự động push code production).*
2. **Railway (Backend) Deployment**:
   - Hỗ trợ User thực thi `railway up` (hoặc kiểm tra status qua Railway CLI nếu cài đặt sẵn).
   - NHẮC NHỞ BẮT BUỘC: Kiểm tra và chạy `alembic upgrade head` đối với Production DB nếu track hiện tại có sinh file revision.
3. **Vercel (Frontend) Deployment**:
   - Theo dõi pipeline deploy của Vercel (nếu tracking qua github/cli).
4. **Production Smoke Test**:
   - Tự động hóa viết cURL check health url Backend `https://production.domain/api/health`.
   - Đảm bảo endpoint liên quan đến module vừa Release trả về `200 OK` (hoặc không 500 Internall Error).
5. **Rollback Guidance (Dành cho rủi ro khẩn)**:
   - Nếu deployment thất bại: Hỗ trợ user downgrade alembic (`alembic downgrade -1`) và rollback git source ngay lập tức.

## Integration
Skill này thường được chạy song song với `@[/conductor]` ngay trước khi kéo trạng thái Feature sang `Done`.
