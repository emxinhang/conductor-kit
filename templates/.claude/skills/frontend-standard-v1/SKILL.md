---
name: frontend-standard-v1
description: Frontend Standard - quy chuẩn và quy trình xây dựng các tính năng Frontend (Module-based). Sử dụng khi bắt đầu module mới, thêm trang List/Detail, hoặc tích hợp API từ backend.
---

# Frontend Standard (V1)

Skill này hướng dẫn xây dựng các module Frontend mới (List, Detail, Modal) theo đúng kiến trúc và thẩm mỹ của dự án.

## 1. When to use (Khi nào dùng)
- Khi bắt đầu xây dựng một module mới.
- Khi cần thêm trang List, Detail hoặc Modal cho các dữ liệu.
- Khi tích hợp API từ backend FastAPI sang frontend React.

## 2. Core Principles (Nguyên tắc cốt lõi)
- **Aesthetic First**: UI phải trông hiện đại, "premium", sử dụng Glassmorphism (blur), shadow mịn, và typography tinh tế (Inter/Geist).
- **Type Safety**: Mọi dữ liệu từ API phải có interface TypeScript tương ứng trong `src/types`.
- **Atomic API**: Chia nhỏ các file API theo module trong `src/api` (vd: `opportunities.ts`, `quotes.ts`).
- **Standard Layout**: Sử dụng Layout chuẩn của dự án với Sidebar, Breadcrumbs, và Header hành động.

## 3. Workflow (Quy trình thực hiện)

### Bước 1: Define Types (`src/types/<module>.ts`)
Dựa trên backend Pydantic schemas, tạo các interface:
- `Entity`: Chứa đầy đủ các trường từ DB (id, created_at, updated_at).
- `EntityCreate`: Các trường bắt buộc khi POST.
- `EntityUpdate`: Các trường optional khi PUT.
- `Enum/Status`: Dùng string union hoặc enum.

### Bước 2: API Client (`src/api/<module>.ts`)
Sử dụng `client` từ `./client` để viết các hàm:
- `getEntities(params)`: Hỗ trợ skip, limit, filter.
- `getEntity(id)`: Lấy chi tiết.
- `createEntity(data)`: Tạo mới.
- `updateEntity(id, data)`: Cập nhật.
- *Custom endpoints*: Ví dụ `duplicateVersion`, `syncStatus`.

### Bước 3: List Page Implementation
- **Vị trí**: `src/pages/<module>/<Module>Page.tsx`.
- **Thư viện**: `@tanstack/react-query` cho fetching.
- **Component**: `DataTable` (hoặc Table custom), `SearchInput`, `FilterDropdown`.
- **Tính năng bắt buộc**: Phân trang (skip/limit), Search, Create Modal.
- **React Query Key Consistency**: Luôn đảm bảo kiểu dữ liệu trong `queryKey` nhất quán với kiểu dữ liệu khi fetch (Ví dụ: Luôn dùng `Number(id)` cho cả fetch và key nếu ID là số).

### Bước 4: Detail & Management Page
- **Vị trí**: `src/pages/<module>/<Module>DetailPage.tsx`.
- **Layout**:
    - Header: Breadcrumb + Title + Action Buttons (Save/Duplicate).
    - Tabs: Overview, Financials, Documents, Timeline.
    - Side Panels: Versioning, Quick Info.
- **Versioning Pattern**: Nếu module hỗ trợ version, sử dụng UI "Version Switcher" ở cột bên phải hoặc trong tab riêng.

### Bước 5: Navigation Integration
- Sửa `src/lib/navigation.ts`: Thêm item vào `navigationItems`.
- Sửa `src/App.tsx`: Đăng ký Route (nhớ bọc trong `ProtectedRoute` và `MainLayout`).

## 4. UI Patterns & Best Practices (Tham chiếu)
- **Status Badges**: Dùng màu sắc chuẩn (blue=new, emerald=active/won, amber=proposal). Mặc định các nhãn tạo cảm giác an tâm (VD: `Saved` thay vì `Draft`).
- **Glassmorphism**: Dùng `backdrop-blur-md bg-background/95` cho sticky headers.
- **Micro-animations**: Dùng `animate-in fade-in duration-500` cho trang mới.
- **Combobox over Input**: Ưu tiên dùng `Combobox` (Shadcn `Popover` + `Command`) thay vì Input Text hoặc Select Dropdown tĩnh đối với các tìm kiếm Data có quan hệ. Tính năng search phải có filter chuẩn hóa tiếng Việt không dấu (dùng `normalize("NFD")`).
- **Select sentinel value**: Khi dùng Shadcn `<Select>` có option "không chọn" (optional field), KHÔNG dùng `value=""` vì sẽ conflict với placeholder. Dùng sentinel `"__none__"` thay thế:
  ```tsx
  // ✅ Đúng
  <SelectItem value="__none__">-- Không chọn --</SelectItem>
  // Khi submit: value === "__none__" ? null : value

  // ❌ Sai — "" conflict với placeholder logic của Shadcn Select
  <SelectItem value="">-- Không chọn --</SelectItem>
  ```
- **AlertDialog**: Tuyệt đối sử dụng `AlertDialog` của Shadcn cho các tác vụ quan trọng / xóa. Không dùng `window.confirm` hay `window.prompt`.
- **Inline Editing**: Data click vào chuyển thành `<Input/>`, lưu trên `onBlur` hoặc nhấn `Enter`, hủy trên `Escape`.

## 5. Performance & Data Flow (Luồng dữ liệu)
- **Zero-Latency Mutation**: Khi gửi 1 item mới bằng `useMutation`, dùng `queryClient.setQueryData` để append trực tiếp vào List thay vì `queryClient.invalidateQueries`. Tránh Full Re-fetch gây giật lag.
- **Fail-safe Mutations**: Mọi hàm Mutation bắt buộc phải có block `onError` để thả `toast.error` và rollback về state cũ. Không để giao diện "Silent fail".

## 6. Checklist trước khi hoàn tất
- [ ] File API đã dùng đúng `client` (Không trailing slashes).
- [ ] Các lỗi Lint (unused imports, unused variables, any types) đã được xử lý ("Zero-Lint Policy").
- [ ] Route đã được đăng ký trong `App.tsx`.
- [ ] Navigation sidebar đã hiển thị đúng item mới.
- [ ] Mọi mutations sửa/xóa đều có `onError` toast và `AlertDialog` xác nhận.
- [ ] Đã kiểm tra responsive cho Mobile.

## 7. Zero-Lint Strategy (Chiến lược sạch lỗi)
Để hạn chế việc liên tục gặp lỗi Lint khi chỉnh sửa Frontend:

1. **Read before code**: Trước khi viết component mới, **bắt buộc** đọc file hiện tại để biết chính xác những gì đã import, đã khai báo. Không code từ trí nhớ.
2. **Always Check Imports**: Trước khi thêm Component mới, **luôn** kiểm tra đã import chưa trong cùng một lượt edit.
3. **Validation-First**: Đừng "đoán" tên component. Dùng tìm kiếm / Read tool trước khi code.
4. **Atomic Edits & Cleanup**: Xóa biến thì xóa luôn import. Chạy Build / Lint không để lại file rác.
5. **No `any`**: Sử dụng interface từ đầu hoặc dùng `unknown`.
6. **Self-Correction**: Ưu tiên sửa lỗi báo đỏ của IDE/tsc trước khi test tính năng.

## 8. Helper UI Pattern (Quy chuẩn Component & Utils)
Để đảm bảo tính nhất quán (UI Consistency) và dễ dàng bảo trì, **BẮT BUỘC** áp dụng Helper UI Pattern:
- **Bóc tách Render Logic (Utils)**: Tuyệt đối không viết logic switch/case dài dòng trong JSX. Bất kỳ logic quy đổi trạng thái sang màu sắc/icon nào BẮT BUỘC phải chuyển thành Helper Functions (vd: `getStatusColor()`, `getServiceIcon()`) và đưa vào file trong `src/utils/`.
- **Shared Components (DRY UI)**: Mọi pattern UI lặp lại xuất hiện từ 2 lần trở lên phải được bóc tách ngay thành Shared Component.
- **Consistency Check**: Trước khi code một khối UI mới, BẮT BUỘC kiểm tra xem dự án đã có Helper Pattern nào xử lý phần này chưa. Nếu có → tái sử dụng và đồng bộ, không tự "phát minh" ra khối UI mới lệch chuẩn.

## References
- `references/api-pattern.md` — API integration template
- `references/ui-layout.md` — Glassmorphism UI snippets
