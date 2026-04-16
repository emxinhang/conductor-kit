---
name: brainstorm-track
description: Brainstorm feature mới và tạo PRD theo chuẩn technical-writer. Sử dụng khi cần phân tích yêu cầu, thiết kế giải pháp sơ bộ cho một track mới.
---

# Brainstorm Track

Skill này giúp tự động hóa quy trình brainstorm feature mới, tạo PRD (Product Requirements Document) và file spec.md với mindset của một Product Manager, lưu trực tiếp vào folder track.

## When to Use (Khi nào dùng)

- Khi bắt đầu một track mới và cần phân tích yêu cầu Business logic.
- Khi cần tạo PRD từ ý tưởng/yêu cầu sơ bộ của user.
- Khi muốn clear các "Problem Statement", "Objectives" và "Acceptance Criteria" trước khi chuyển qua bước Implementation Plan.

## Workflow (3 Phases)

### Phase 1: Discovery (Thu thập yêu cầu)

1. **Clarify Requirements**: Hỏi user về mục tiêu, pain points, và expected outcomes
2. **Explore Codebase**: Tìm hiểu patterns hiện có liên quan đến feature
3. **Identify Stakeholders**: Xác định ai sẽ sử dụng feature (Sales, Admin, IT, etc.)

**Output**: Hiểu rõ problem space và constraints

### Phase 2: PRD Writing (Viết PRD)

Sử dụng template `templates/PRD_TEMPLATE.md` để tạo file `PRD.md` trong folder track.

**Sections bắt buộc**:
- Problem Statement (Vấn đề cần giải quyết)
- Objectives (Mục tiêu)
- User Stories (Câu chuyện người dùng)
- Acceptance Criteria (Tiêu chí nghiệm thu)
- Out of Scope (Ngoài phạm vi)

### Phase 3: Technical Design Direction (Hướng thiết kế kỹ thuật)

1. **Data Model**: Xác định concepts chính, tables/collections cần thiết để phục vụ spec
2. **API Design**: Xác định các endpoints chính cần phải có
3. **Dependencies**: Nhận diện các dependencies lớn từ business.

*Lưu ý: Không đi sâu vào technical implementation list (để dành cho skill `planner-track`)*

**Output**: Hướng kiến trúc giải pháp chuẩn bị cho `planner-track`.

### Phase 4: Contract Delta (Track 014+ — Design-First)

> Áp dụng khi track có thay đổi API hoặc DB schema. Bỏ qua nếu track là internal/refactor không có API mới.

Tạo file `contract_delta.md` trong folder track với nội dung:

1. **API Changes**: Liệt kê endpoints mới/sửa/xóa — format: `METHOD /path` + request/response shape sơ bộ
2. **DB Schema Changes**: Liệt kê tables/columns mới nếu có migration
3. **Breaking Changes**: Flag rõ nếu có (field đổi type, path đổi, field bị xóa)
4. **Downstream impact**: Track nào phụ thuộc vào contract này?

Template: `conductor/tracks/<id>/contract_delta.md` (xem ví dụ tại `conductor/tracks/014-ha-lac-data-enrichment/contract_delta.md`)

**Output**: `contract_delta.md` trong folder track.

## Output Location

Tất cả files sẽ được tạo trong folder track hiện tại:
```
conductor/tracks/<track-id>/
├── PRD.md                    # Product Requirements Document
├── spec.md                   # Đặc tả kỹ thuật có cấu trúc (FR-xxx, SC-xxx, Given/When/Then)
└── contract_delta.md         # Contract delta (track 014+ nếu có API/DB changes)
```

## Templates

### PRD Template
Đọc và sử dụng: `templates/PRD_TEMPLATE.md`

### Spec Template
Đọc và sử dụng: `conductor/track-templates/SPEC_TEMPLATE.md`

spec.md phải có cấu trúc:
- **User Stories** (`US1`, `US2` ...) — "As a X, I want Y, so that Z"
- **Functional Requirements** (`FR-001`, `FR-002` ...) — per user story
- **Acceptance Scenarios** (`SC-001` ...) — Given/When/Then
- **Success Criteria** — checklist của SC-xxx
- **Constitution Check** — verify không vi phạm `conductor/constitution.md`

## Best Practices

1. **Luôn hỏi trước khi giả định** - Đặc biệt với business logic. Đứng ở góc nhìn PM, chỉ tập trung làm rõ What & Why.
2. **Explore codebase** - Tìm patterns hoặc các module có sẵn tương tự nếu cần context hiện hành.
3. **Keep it concise** - PRD ngắn gọn, súc tích (dưới 500 dòng).
4. **Link to existing** - Reference các requirements đã có.
5. **Verify với user** - Confirm spec, yêu cầu trước khi kết thúc workflow đầu tiên. (Để user gọi tiếp /planner-track sau)

## Example Usage

```
User: /brainstorm-track Track 070 - Soft Delete, mục tiêu là...

Agent:
1. Đọc yêu cầu hoặc spec.md nếu đã có sẵn.
2. Hỏi unifying questions về business rules, impact.
3. Khai thác thông tin từ codebase nếu cần định hướng.
4. Tạo/Cập nhật PRD.md (hoặc spec.md).
5. Xác nhận hoàn tất và gợi ý dùng /planner-track cho bước Implementation.
```

## Enter Routine (Bắt buộc)

Ngay khi bắt đầu brainstorm, CS **phải** chạy lệnh sau để đánh dấu track đang active:

```bash
python conductor/status.py transition <track-id> brainstorm CS "start brainstorm"
```

Lệnh này set badge `[📅 Planned]` trong `tracks.md`, update `state.md` nếu đây là ACTIVE track, và ghi log vào `CHANGELOG.md`.

## Exit Routine (Bắt buộc)

Sau khi tạo xong `PRD.md`, CS **phải** chạy lệnh sau để cập nhật Conductor board:

```bash
python conductor/status.py transition <track-id> brainstorm CS "PRD done"
```

Thay `<track-id>` bằng ID thực tế (e.g., `112`). Lệnh này tự động:
- Cập nhật badge trong `conductor/tracks.md` → `[📅 Planned]`
- Cập nhật `conductor/state.md` nếu đây là ACTIVE track
- Ghi lịch sử vào `conductor/tracks/<id>/CHANGELOG.md`

Nếu track có API/DB changes (014+): kiểm tra `contract_delta.md` đã được tạo trong folder track.