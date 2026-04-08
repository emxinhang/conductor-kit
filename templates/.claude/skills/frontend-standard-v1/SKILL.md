---
name: frontend-standard-v1
description: TMS-2026 Frontend Standard - quy chuẩn và quy trình xây dựng các tính năng Frontend (Module-based). Sử dụng khi bắt đầu module mới, thêm trang List/Detail, hoặc tích hợp API từ backend.
---

# TMS-2026 Frontend Standard (V1)

Skill này hướng dẫn xây dựng các module Frontend mới (Opportunity, Quote, Booking, CRM...) theo đúng kiến trúc và thẩm mỹ của dự án TMS-2026.

## 1. When to use (Khi nào dùng)
- Khi bắt đầu xây dựng một module mới.
- Khi cần thêm trang List, Detail hoặc Modal cho các dữ liệu ERP.
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
- **Versioning Pattern**: Nếu module hỗ trợ version (Itinerary, Quote), sử dụng UI "Version Switcher" ở cột bên phải hoặc trong tab riêng.

### Bước 5: Navigation Integration
- Sửa `src/lib/navigation.ts`: Thêm item vào `navigationItems`.
- Sửa `src/App.tsx`: Đăng ký Route (nhớ bọc trong `ProtectedRoute` và `MainLayout`).

## 4. UI Patterns & Best Practices (Tham chiếu)
- **Status Badges**: Dùng màu sắc chuẩn (blue=new, emerald=won/active, amber=proposal). Mặc định các nhãn tạo cảm giác an tâm (VD: `Saved` thay vì `Draft`).
- **Glassmorphism**: Dùng `backdrop-blur-md bg-background/95` cho sticky headers.
- **Micro-animations**: Dùng `animate-in fade-in duration-500` cho trang mới.
- **Combobox over Input**: Luôn ưu tiên dùng `Combobox` (Shadcn `Popover` + `Command`) thay vì Input Text hoặc Select Dropdown tĩnh đối với các tìm kiếm Data có quan hệ (Customers, Owners). Tính năng search phải có filter chuẩn hóa tiếng Việt không dấu (dùng `normalize("NFD")`).
- **Select sentinel value**: Khi dùng Shadcn `<Select>` có option "không chọn" (optional field), KHÔNG dùng `value=""` vì sẽ conflict với placeholder. Dùng sentinel `"__none__"` thay thế:
  ```tsx
  // ✅ Đúng
  <SelectItem value="__none__">-- Không chọn --</SelectItem>
  // Khi submit: value === "__none__" ? null : value

  // ❌ Sai — "" conflict với placeholder logic của Shadcn Select
  <SelectItem value="">-- Không chọn --</SelectItem>
  ```
  Áp dụng cho tất cả Select optional: room_type, guide, supplier, status filter.
- **AlertDialog**: Tuyệt đối sử dụng `AlertDialog` của Shadcn cho các tác vụ quan trọng / xóa. Không dùng `window.confirm` hay `window.prompt`.
- **Inline Editing (In-place Editing)**: Tốc độ chỉnh sửa phải đặt lên hàng đầu (giảm thiểu click lưu). Data click vào chuyển thành `<Input/>`, lưu trên sự kiện `onBlur` hoặc nhấn `Enter`.

## 5. Performance & Data Flow (Luồng dữ liệu)
- **Zero-Latency Mutation**: Khi gửi 1 item mới bằng `useMutation` (VD: Add Day, Thêm Task), hãy dùng `queryClient.setQueryData` để append data mới trực tiếp vào List thay vì gọi `queryClient.invalidateQueries`. Tránh tình trạng Full Re-fetch làm ứng dụng bị giật, lag.
- **Fail-safe Mutations**: Bất kỳ hàm Mutation nào cũng bắt buộc phải thiết kế block `onError` để thả `toast.error` thông báo và rollback về state cũ. Không được để giao diện rơi vào trạng thái "Silent fail" (Click nút nhưng không có phản hồi gì khi mạng lỗi).

## 6. Checklist trước khi hoàn tất
- [ ] File API đã dùng đúng `client` (Không trailing slashes).
- [ ] Các lỗi Lint (unused imports, unused variables, any types) đã được xử lý ("Zero-Lint Policy").
- [ ] Route đã được đăng ký trong `App.tsx`.
- [ ] Navigation sidebar đã hiển thị đúng item mới.
- [ ] Mọi mutations sửa/xóa đều có `onError` toast và `AlertDialog` xác nhận.
- [ ] Đã kiểm tra responsive cho Mobile.

## 7. Zero-Lint Strategy (Chiến lược sạch lỗi)
Để hạn chế việc liên tục gặp lỗi Lint khi chỉnh sửa Frontend, tuân thủ các quy tắc:

1. **Read before code**: Trước khi viết component mới, **bắt buộc** đọc file hiện tại để biết chính xác những gì đã import, đã khai báo. Không code từ trí nhớ.
2. **Always Check Imports**: Trước khi thêm Component mới (`Button`, `Dialog`), **luôn** kiểm tra đã import chưa trong cùng một lượt edit.
3. **Validation-First**: Đừng "đoán" tên component (VD: `ExportIcon` hay `DownloadIcon`?). Dùng tìm kiếm / Read tool trước khi code.
4. **Atomic Edits & Cleanup**: Xóa biến thì xóa luôn import. Chạy Build / Lint không để lại file rác.
5. **No `any` (Hard Rule)**: Xem Section 9 bên dưới.
6. **Self-Correction**: Ưu tiên sửa lỗi báo đỏ của IDE/tsc trước khi test tính năng.

## 9. No `any` — Hard Rule (Zero Tolerance)

**`any` là bug tiềm ẩn, không phải shortcut.** Tất cả 14+ `any` types phát hiện trong track 132b đều là tech debt tích lũy từ nhiều feature tracks. Rule này là **không thỏa hiệp**.

### Cấm tuyệt đối
```typescript
// ❌ SAI — không được commit
const data: any = response.data
function handler(event: any) { ... }
const items = [] as any[]
(something as any).method()
```

### Pattern thay thế đúng

**Trường hợp 1: Không biết type từ API**
```typescript
// ✅ Dùng unknown + narrowing
const data: unknown = response.data
if (typeof data === 'object' && data !== null && 'id' in data) {
  const typed = data as MyEntity
}
```

**Trường hợp 2: Event handler**
```typescript
// ✅ Dùng đúng event type
function handleChange(event: React.ChangeEvent<HTMLInputElement>) { ... }
function handleSubmit(event: React.FormEvent<HTMLFormElement>) { ... }
```

**Trường hợp 3: Array chưa biết type**
```typescript
// ✅ Define interface trước
interface ServiceRow { id: number; name: string; price: number }
const items: ServiceRow[] = []
```

**Trường hợp 4: Response API**
```typescript
// ✅ Type API response ngay tại api/*.ts
export async function getBookings(): Promise<BookingListResponse> {
  const res = await client.get<BookingListResponse>('/bookings')
  return res.data
}
```

**Trường hợp 5: Generic helper không biết shape**
```typescript
// ✅ Dùng generic thay any
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> { ... }
```

### Enforcement
- `npx tsc --noEmit` phải chạy xanh — `any` sẽ không fail tsc nhưng là nợ kỹ thuật
- Review checklist: grep `": any"` và `"as any"` trong file đã sửa trước khi mark done
- Nếu type thực sự phức tạp (third-party lib không có types): dùng `// @ts-expect-error` + comment giải thích, KHÔNG dùng `any`

---

## 8. Helper UI Pattern (Quy chuẩn Component & Utils)
Để đảm bảo tính nhất quán (UI Consistency) và dễ dàng bảo trì, **BẮT BUỘC** áp dụng Helper UI Pattern trong luồng thiết kế Frontend:
- **Bóc tách Render Logic (Utils)**: Tuyệt đối không viết logic switch/case dài dòng trong JSX. Bất kỳ logic quy đổi trạng thái sang màu sắc/icon nào (như `Pending` -> màu vàng + icon Clock) BẮT BUỘC phải chuyển thành Helper Functions (vd: `getStatusColor()`, `getServiceIcon()`) và đưa vào file trong `src/utils/` (vd: `bookingUtils.ts`).
- **Shared Components (DRY UI)**: Mọi pattern UI lặp lại xuất hiện từ 2 lần trở lên (như Card Segment, Status Select Dropdown) phải được bóc tách ngay thành Shared Component (vd: `<StatusDropdown />`, `<ServiceCard />`).
- **Consistency Check**: Trước khi code một khối UI mới, BẮT BUỘC kiểm tra xem dự án đã có Helper Pattern nào xử lý phần này chưa. Nếu có → tái sử dụng và đồng bộ, không tự "phát minh" ra khối UI mới lệch chuẩn.