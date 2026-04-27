---
name: planner-track
description: Lập kế hoạch triển khai (Implementation Plan) theo chuẩn technical-writer dựa trên spec.md hoặc PRD đã có. Sử dụng sau khi đã chốt requirements.
---

# Planner Track

Skill này (đóng vai trò như một Technical Lead kết hợp Technical Writer) giúp tự động hóa quy trình phân tích codebase và lập kế hoạch triển khai chi tiết `IMPLEMENTATION_PLAN.md` cho một track đã rõ yêu cầu (có spec.md hoặc PRD.md).

## When to Use (Khi nào dùng)

- Khi track đã có Product Requirements (PRD hoặc spec.md) rõ ràng.
- Khi ATu yêu cầu lên kế hoạch (Implementation Plan) trước khi viết code.
- Khi cần mapping chính xác từ Business Logic sang Technical Files.

## Workflow (3 Phases)

### Phase 1: Codebase Context Grounding (Bắt buộc)

1. **Đọc Spec/PRD**: Đọc hiểu yêu cầu từ `spec.md` hoặc `PRD.md` trong folder track.
2. **Constitution Gate**: Đọc `conductor/constitution.md` — verify plan không vi phạm invariants. Nếu vi phạm → flag cho ATu trước khi tiếp tục.
3. **Contract Delta Check**: Nếu track có `contract_delta.md` trong folder track (track 014+):
   - Đọc `contract_delta.md` để hiểu API/DB changes
   - Xác nhận: breaking changes nào cần migration?
   - Update `docs/contracts/api/ha_lac.yaml` nếu có endpoint mới/sửa (bump version theo semver)
   - Chạy `make sync-types` để generate TypeScript types mới
   - Nếu breaking change: flag cho ATu trước khi tiếp tục
4. **Search Tools**: Bắt buộc sử dụng công cụ tìm kiếm (`grep_search`, `find_by_name`, `view_file`) để quét các file codebase hiện tại.
    - Tìm hiểu System Entity Models hiện tại (database schema/SQL files, Pydantic/SQLAlchemy models).
    - Tìm Frontend Components, API endpoints hoặc Interfaces đã có liên quan.
5. **Verify Dependencies**: Phân tích xem có thư viện nào cần cài thêm, cấu hình nào cần cập nhật không.

*Lưu ý: Tuyệt đối không tự suy diễn kiến trúc. Khớp nối với thực tế codebase.*

### Phase 2: Technical Writer Integration (Viết Plan)

Sử dụng template `templates/IMPLEMENTATION_PLAN_TEMPLATE.md` để tạo file `IMPLEMENTATION_PLAN.md` trong folder track.

**Áp dụng luật của `/technical-writer`**:
- **Scannable**: Trình bày rõ ràng theo Checklist `[ ]` để tiện theo dõi tiến độ.
- **Precision**: Ghi **chính xác đường dẫn** (absolute/relative paths) của các file cần chỉnh sửa hoặc tạo mới.
- **Boundaries**: Bắt buộc phải có mục **Out of Scope** để bảo vệ luồng Zero-Loop (những gì không được đụng vào).
- **Working Examples**: Viết mẫu JSON schema/Interfaces quan trọng nếu có rẽ nhánh logic phức tạp.

### Phase 3: Dependency Check & Cảnh báo

- Review lại plan xem có break rule của các system hiện tại không.
- Thêm warnings về Database Migrations hoặc breaking changes ở frontend/backend.

## Output Location

Output sinh ra sẽ nằm trong folder track hiện tại:
```text
conductor/tracks/<track-id>/
├── IMPLEMENTATION_PLAN.md    # Kế hoạch triển khai chi tiết (narrative)
└── tasks.md                  # Task list có markers [P]/[SEQ]/[US1]/[CHK]
```

> **Contract-First note (track 014+)**: Nếu track có API changes, `docs/contracts/api/ha_lac.yaml` và `frontend/src/types/_generated/` cũng phải được cập nhật trước khi bắt đầu dev phase.

## Templates

### Implementation Plan Template
Đọc và sử dụng: `templates/IMPLEMENTATION_PLAN_TEMPLATE.md`

### Tasks Template
Đọc và sử dụng: `conductor/track-templates/TASKS_TEMPLATE.md`

tasks.md phải có:
- `[P]` đánh dấu task parallel-safe (AG + CD chạy cùng được)
- `[SEQ]` đánh dấu task phụ thuộc vào task trước
- `[US1]`/`[US2]` trace về user story trong spec.md
- `[CHK-N]` checkpoint — ATu verify trước khi tiếp tục
- File path rõ ràng cho mỗi task

## Best Practices

1. **Tập trung vào "How"**: Bỏ qua các câu hỏi "Why" (do `brainstorm-track` đã làm). Focus hoàn toàn vào kỹ thuật.
2. **Liệt kê file cụ thể**: Thay vì "Sửa frontend auth", phải ghi rõ "Cập nhật `frontend/src/features/auth/AuthContext.tsx`".
3. **Giới hạn số bước**: Plan tối ưu trong khoảng 300 dòng và chia phase rõ ràng (Backend, Frontend, QA).
4. **Contract trước code**: Nếu track có `contract_delta.md`, cập nhật OpenAPI spec TRƯỚC khi viết implementation plan chi tiết. Implementation plan phải reference đúng field names từ contract.

## Example Usage

```text
User: /planner-track Hãy lên Plan cho Track 070 (Soft Delete) theo spec sẵn có.

Agent:
1. Đọc spec.md tại tracks/070-soft-delete/spec.md
2. Tìm kiếm codebase các Models liên quan đến User và xóa mềm.
3. Phân vùng kỹ thuật và tạo file IMPLEMENTATION_PLAN.md.
4. Báo cáo hoàn tất.
```

## Enter Routine (Bắt buộc)

Ngay khi bắt đầu viết plan, CS **phải** chạy lệnh sau (track vẫn ở phase brainstorm, chưa có plan):

```bash
python conductor/status.py transition <track-id> brainstorm CS "planning in progress"
```

Lệnh này update `state.md` phase/notes nếu đây là ACTIVE track và ghi log vào `CHANGELOG.md`.

## Exit Routine (Bắt buộc)

Sau khi tạo xong `IMPLEMENTATION_PLAN.md`, CS **phải** chạy lệnh sau để cập nhật Conductor board:

```bash
python conductor/status.py transition <track-id> planned CS "plan vX done"
```

Thay `<track-id>` bằng ID thực tế (e.g., `102n`). Lệnh này tự động:
- Cập nhật badge trong `conductor/tracks.md` → `[📅 Planned]`
- Cập nhật `conductor/state.md` phase nếu đây là ACTIVE track
- Ghi lịch sử vào `conductor/tracks/<id>/CHANGELOG.md`

Khi ATu approve plan và bắt đầu implement (handoff sang AG/CD), chạy tiếp:

```bash
python conductor/status.py transition <track-id> dev AG "start implement"
```