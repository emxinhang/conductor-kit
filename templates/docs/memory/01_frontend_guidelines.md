# Frontend Guidelines & QA

👉 **Tài liệu tham khảo nhanh**: **[UI Design System & Visual Language (TMS-2026)](./05_ui_design_system.md)** — Chứa các Design Tokens (Typography, Spacing, Card Shapes) chuẩn cho dự án.

## 🎨 UI/UX & React Rules

### [P0] ⚠️ Không gọi hooks bên trong regular functions dù function đó nằm trong component (2026-04-03)
- **Vấn đề**: `renderDayView()` là arrow function thông thường bên trong component, bên trong có `React.useMemo(...)`. Khi function được gọi có điều kiện (`viewMode === 'day' ? renderDayView() : renderServiceView()`), React thấy số hooks thay đổi giữa các renders → white screen crash.
- **Error message**: "Rendered more hooks than during the previous render."
- **Fix**: Chuyển TẤT CẢ hook calls (`useState`, `useMemo`, `useCallback`, `useEffect`...) lên component top-level. Dùng guard condition BÊN TRONG hook nếu cần tránh compute: `if (viewMode !== 'day') return [];`
- **Áp dụng khi**: Bất kỳ khi nào muốn viết `renderXxx()` helper function mà bên trong có hook calls.

### [P1] Drawer/Sheet form với mutation: `isDirty` phải reset sau `mutateAsync` success (2026-04-03)
- **Vấn đề**: Pattern `handleFieldUpdate` gọi `await onUpdate()` rồi để `isDirty = true` → sau khi save thành công, dialog confirm discard vẫn hiện. Drawer đóng rồi nhưng dialog đòi confirm.
- **Fix**: Wrap trong `try/catch`:
  ```tsx
  const handleFieldUpdate = async (serviceId: number, data: OpsServiceUpdate) => {
    setIsDirty(true);
    try {
      await onUpdate(serviceId, data);
      setIsDirty(false); // Reset after successful save
    } catch {
      // Keep isDirty = true on failure so user can retry
    }
  };
  ```
- **Áp dụng khi**: Bất kỳ drawer/sheet form nào gọi mutation và có discard confirmation dialog.

### [P1] Inline cell save: dùng onBlur, KHÔNG dùng debounced useEffect (2026-04-02)
- **Vấn đề**: Pattern `useEffect(() => { if (isEditing) updateItem(...) }, [debouncedSave])` sẽ fire API call trong khi user đang typing. Khi Tab qua nhiều cells nhanh → parallel mutations → stale API response overwrite giá trị user vừa nhập.
- **Fix**: Dùng `onBlur={() => { if (parsed !== item[field]) updateItem(...).catch(() => { revert; toast.error(...) }) }}` — y như pattern `QuoteItemRow.tsx` hiện tại.
- **Sync state**: Chỉ sync `localValue` từ store khi cell KHÔNG đang focus: `if (!isFocused) setLocalValue(item[field])`.
- **Áp dụng khi**: Bất kỳ component nào có inline editing + Zustand store update (grid cells, editable table rows).

### [P0] SupplierCombobox portal bị pointer-events:none trong Radix Dialog (2026-03-31)
- **Vấn đề**: Radix Dialog set `pointer-events: none` lên `body` để trap interaction. SupplierCombobox dùng `createPortal(..., document.body)` → buttons trong portal inherit `pointer-events: none` → click xuyên thẳng xuống element bên dưới, không chọn được supplier.
- **Triệu chứng**: Supplier hiện trong dropdown, click thì dropdown đóng nhưng không select được. `getComputedStyle(btn).pointerEvents === 'none'`.
- **Fix**: Thêm `pointerEvents: 'auto'` vào style của portal container div trong `SupplierCombobox.tsx` (line 218).
- **Áp dụng khi**: Bất kỳ custom portal nào render ra `document.body` trong context Radix Dialog đều cần override `pointerEvents: 'auto'`.

### [P1] useEffect reset form Dialog — chỉ reset khi mở, không reset khi đóng (2026-03-31)
- **Vấn đề**: `useEffect([..., open])` với deps chứa `open` → effect fire cả khi dialog close → `setSupplierName(null)` + `reset()` → xóa mất selections user vừa làm.
- **Fix**: Thêm `if (!open) return` ở đầu effect → chỉ reset khi dialog opens (false→true).
- **Áp dụng khi**: Mọi Dialog form có reset logic trong useEffect có `open` trong deps.

### [P1] backdrop-blur tạo CSS stacking context → dropdown bị che bởi sibling cards (2026-03-27)
- **Vấn đề**: Card component dùng `backdrop-blur-sm` (hoặc bất kỳ `backdrop-filter`, `filter`, `transform`, `opacity<1`) sẽ tạo new stacking context. `z-index` cao (vd `z-[100]`) trong đó chỉ compete trong card đó — dropdown từ card trên bị che bởi card phía dưới ở page level.
- **Giải pháp**: Dùng `createPortal(dropdown, document.body)` với `position: fixed`. Track vị trí bằng `getBoundingClientRect()` + listen `scroll`/`resize` để update. Tách `dropdownRef` riêng cho click-outside detection (portal đã ra ngoài `containerRef`).
- **Áp dụng khi**: Bất kỳ custom dropdown/combobox nào nằm trong element có `backdrop-blur`, `filter`, `transform`, hoặc `will-change`. SupplierCombobox đã implement pattern này.

### [P1] Tailwind arbitrary child selector `[&_child]` để override nested element (2026-03-27)
- **Pattern**: `className="[&_input]:h-8 [&_input]:text-xs"` trên parent → override tất cả `<input>` bên trong mà không cần sửa child component.
- **Dùng khi**: Cần compact/variant của shared component trong specific context (vd: SupplierCombobox trong card header cần `h-8` thay vì `h-9` mặc định).
- **Lưu ý**: Chỉ dùng cho visual override nhỏ; nếu cần nhiều thay đổi thì thêm prop vào component.

### [P2] Meal ConfirmationDetails — field mismatch với sync fields (2026-03-27)
- **Vấn đề**: `buildSupplierSyncFields` cho meal/lunch/dinner set `poc_name`, `provider_phone`, `provider_email`, `provider_address`. Nhưng `renderGenericForm()` đọc `contact_name`, `contact_phone` → chọn supplier xong form vẫn trống.
- **Giải pháp**: Tạo `renderMealForm()` riêng đọc đúng fields (`poc_name`, `provider_phone`, v.v.). Route meal/lunch/dinner → `renderMealForm()`.
- **File**: `ConfirmationDetailsForm.tsx`

### [P1] SupplierForm useEffect dep — không re-sync sau save (2026-03-26)
- **Vấn đề**: `SupplierForm.tsx` line 119 — dep array `[supplier?.id, ...]`. Sau `useUpdateSupplier()` save, `updated_at` thay đổi nhưng `id` không đổi → useEffect không fire → form không reset về server values. Bug rõ nhất khi dùng inline in detail page (không phải sheet).
- **Giải pháp**: Thêm `supplier?.updated_at` vào dep array: `[supplier?.id, supplier?.updated_at, defaultName, defaultType, form]`
- **Áp dụng khi**: Bất kỳ form nào reuse `SupplierForm` inline (GuideDetailPage Tab Profile) — không phải sheet vì sheet đóng sau save.

### [P1] date-fns đã có trong codebase — dùng cho month/date navigation (2026-03-26)
- **Pattern**: Codebase dùng `date-fns` (`lib/datetools.ts` + `timelineUtils.ts`). Cho month navigation trong calendar components:
  - Prev/next month: `format(addMonths(parseISO(month + "-01"), ±1), "yyyy-MM")`
  - All days in month: `eachDayOfInterval({ start: startOfMonth(ref), end: endOfMonth(ref) })`
  - First day offset: `getDay(startOfMonth(ref))` (Sunday=0)
  - Date display: reuse `formatDate()` từ `lib/datetools`
- **Áp dụng khi**: Bất kỳ calendar grid/month picker component mới nào.

### [P1] Day selector build từ `totalDays`, không phải `dayTitles.length` (Track 106c2 — 2026-03-26)
- **Vấn đề**: `ItineraryContext.day_titles: Record<number, string>` chỉ chứa days ĐÃ ĐẶT TITLE. Dùng `Object.keys(dayTitles).length > 0` làm guard hoặc `Object.entries(dayTitles)` làm options list sẽ bỏ sót ngày hợp lệ chưa đặt tên.
- **Giải pháp**: Build options từ `1..totalDays` (số ngày hành trình), dùng `dayTitles[n]` chỉ như label phụ. Cần truyền `totalDays` prop riêng từ `booking.total_days`.
- **Pattern**: `Array.from({length: totalDays}, (_, i) => i+1).map(n => ({value: String(n), label: dayTitles?.[n] ? \`Ngày ${n}: ${dayTitles[n]}\` : \`Ngày ${n}\`}))`
- **Áp dụng khi**: Bất kỳ day picker nào cần hiển thị đủ tất cả ngày trong hành trình.

### [P1] Optimistic `setQueryData` trước `invalidateQueries` trong edit mutation (Track 106c2 — 2026-03-26)
- **Vấn đề**: Chỉ gọi `invalidateQueries` sau khi mutation success → UI phải đợi re-fetch mới update. API response đã có full object (IncidentResponse) → có thể update UI ngay.
- **Giải pháp**: Trong `onSuccess`: dùng `setQueryData(['incidents', bookingId], old => {...old, items: old.items.map(...)})`. Trong `onSettled`: invalidate nền cho eventual consistency.
- **Pattern đã dùng**: `IncidentCreateDialog`, `IncidentResolveDialog` đều đã dùng pattern này — mọi mutation edit cũng phải follow.
- **Áp dụng khi**: Bất kỳ mutation PATCH/PUT nào có API response là full updated object.

### [P1] Shadcn Select clear-option dùng sentinel value, không dùng empty string (Track 106c2 — 2026-03-27)
- **Vấn đề**: Trong Radix/Shadcn `Select`, dùng `SelectItem value=""` cho option "clear" dễ gây trạng thái form không ổn định (khó phân biệt placeholder vs selected value rỗng), đặc biệt với flow PATCH partial update (`null` = clear).
- **Giải pháp**: Dùng sentinel value cố định (ví dụ `__none__`), rồi map về `undefined/null` ở `z.preprocess` hoặc `onSubmit`.
- **Pattern**:
  - UI option: `<SelectItem value="__none__">Không gán ngày</SelectItem>`
  - Form value: `value={field.value != null ? String(field.value) : "__none__"}`
  - Submit: `__none__ -> null` để gửi PATCH clear field.
- **Áp dụng khi**: Form edit có Select optional và backend phân biệt rõ `omit` vs `null` semantics.

### [P1] Supplier Integration Pattern (Track 111c)
- **Sync/Unsync**: Luôn dùng `buildSupplierSyncFields` và `buildSupplierUnsyncFields` để đồng bộ dữ liệu nhà cung cấp vào `confirmation_details` khi `onChange`.
- **Duplicate UX**: Xử lý lỗi 409 từ backend để tự động fetch và chọn nhà cung cấp hiện có (ID-based auto-select).
- **Header Display**: Sử dụng `SupplierContactLine` và `useSupplier(id)` (read-through enrichment) thay vì dual source of truth state.

### [P1] Ghost Row & Negative ID Pattern (Track 118h — 2026-04-01)
- **Vấn đề**: Các dịch vụ kéo dài nhiều ngày (như `land_package`) chỉ hiện ở ngày bắt đầu, gây hiểu lầm ngày sau bị "trống".
- **Giải pháp (The Ghost Row Pattern)**:
    - **ID Strategy**: Tạo các hàng ảo (Ghost Rows) với **ID âm** (`id = -(originalId * 10000 + day)`) để đảm bảo Type Safety (`number`) và tránh trùng lặp React key.
    - **Isolation**: Chỉ "tiêm" ghost rows tại View Layer (trong `useMemo` của component render), không làm bẩn dữ liệu upstream/store.
    - **Anti-Leak Guard**: Bắt buộc dùng `isRealService (id > 0)` để lọc ghost rows trước khi tính toán Cost hoặc gửi Bulk Update API.
    - **Interaction**: Click Ghost Row -> `setExpandedId(originalId)` -> `scrollIntoView` hàng gốc + Pulse Highlight hiệu ứng.
- **Áp dụng khi**: Bất kỳ thực thực thể nào cần hiển thị sự hiện diện trên nhiều ngày/vị trí nhưng chỉ có 1 bản ghi gốc trong DB.

### [P1] Enable Global Page Scroll cho ERP List (Track 119 - 2026-04-01)
- **Vấn đề**: Việc sử dụng `overflow-hidden` và `flex-1` trên các container bọc ngoài khiến trang bị bó hẹp trong viewport, làm mất khả năng cuộn tự nhiên của trình duyệt và gây khó khăn cho người dùng khi làm việc với bảng dữ liệu lớn.
- **Giải pháp**: 
    - Loại bỏ các class giới hạn chiều cao cố định (`h-full`, `h-screen`) và ngắt cuộn (`overflow-hidden`) tại các div cha cấp cao của trang List.
    - Thay thế `flex-1` bằng nội dung tự giãn nở tự nhiên.
    - Table header nên dùng `sticky top-0` thay vì dựa vào inner-scroll container để giữ header luôn hiển thị.
- **Lợi ích**: UI mượt mà hơn, hỗ trợ tốt các thiết bị có viewport thấp, tận dụng tốt các tính năng cuộn mặc định của OS/Trình duyệt.
- **Áp dụng khi**: Các trang List/Dashboard dữ liệu quan trọng (Booking, Opportunity, CRM).

### [P1] Block Rendering Pattern cho Tables phức tạp (Track 127 — 2026-04-05)
- **Vấn đề**: Khi render bảng có `rowSpan` (gộp ô), việc map từng dòng lẻ trong component cha dễ dẫn đến lỗi lệch cột hoặc nhảy layout nếu logic `rowSpan` phức tạp (ví dụ: gộp không liên tiếp).
- **Giải pháp (Block Rendering)**: Thay vì map `<tr>` đơn lẻ, hãy pass toàn bộ cụm dữ liệu (ví dụ: một khách sạn có nhiều đợt ở) vào một component Row chuyên biệt (ví dụ: `HotelRows`). Component này sẽ chịu trách nhiệm render toàn bộ khối `<tr>` của cụm đó một cách nguyên khối.
- **Nguyên tắc**: Dòng đầu tiên của khối render đầy đủ tất cả cột (bao gồm ô gộp); các dòng tiếp theo trong khối tuyệt đối không render các ô đã bị gộp. Việc tập trung logic này vào một component giúp đảm bảo cấu trúc HTML `<table>` luôn hợp lệ.
- **Áp dụng khi**: Bất kỳ bảng nào có logic gộp dòng theo nhóm (Hotel stay periods, Guide/Transport segments).

### [P1] Live Preview PDF với iframe & Auto-refresh (Track 131 — 2026-04-06)
- **Vấn đề**: User cần xem ngay thay đổi trên bản in PDF khi sửa dữ liệu (Invoice/Itinerary) mà không muốn click Download liên tục.
- **Giải pháp**: 
    - Sử dụng `iframe` nhúng trong `TabsContent`. 
    - URL của iframe trỏ đến một `blob` (Object URL) được tạo từ API response (với `responseType: 'blob'`). 
    - **Refresh logic**: Theo dõi sự kiện thành công của các mutations cập nhật dữ liệu. Khi mutation success, fetch lại blob mới và `window.URL.revokeObjectURL(oldUrl)` để giải phóng bộ nhớ, sau đó gán `newUrl` vào iframe.
    - **UX**: Thêm `loading` state (spin icon) bên trong Card chứa iframe để báo hiệu bản preview đang được generate lại.
- **Áp dụng khi**: Các trang chi tiết cần tính năng Xem trước bản in (Invoice Detail, Itinerary Detail).

### [P1] Inline Master-Detail Pattern cho Tabs (Track 130 — 2026-04-07)
- **Vấn đề**: Việc chuyển hướng sang trang chi tiết (`/entity/:id`) làm đứt quãng luồng làm việc (context) khi user đang thao tác trong một Parent Entity (như Opportunity).
- **Giải pháp**: 
    - Render Component chi tiết (`DetailManager`) ngay bên trong `TabsContent`.
    - Sử dụng một local state `activeId` để quyết định hiển thị danh sách (List) hay chi tiết (Detail).
    - Cung cấp nút `onBack` trong component chi tiết để reset `activeId` về `null`, giúp quay lại danh sách mà không làm reload trang hay đổi URL.
- **Áp dụng khi**: Các thực thể con (Invoice, Payment, Task) cần thao tác nhanh mà không muốn rời khỏi trang Parent.

## 🏗 General Patterns (Legacy/Context)

- **Frontend/Backend Schema Symmetry**: Khi xây dựng Form hoặc Page chi tiết, key trong `formData` phải khớp 100% với Pydantic Response Schema từ Backend.
- **React Inline Edit Performance**: Bắt buộc dùng **Local State** (`useState`) để quản lý thay đổi nội bộ khi gõ. Chỉ gọi hàm Update lên Global Store/Backend qua sự kiện `onBlur` hoặc phím `Enter`.
- **Hotkey Typing Guard (UX Rule)**: Khi đăng ký hotkey global, BẮT BUỘC kiểm tra `document.activeElement` để chặn trigger khi đang gõ.
- **Enterprise Delete Strategy**: Ưu tiên dùng **Soft Delete** (`deleted_at`) thay vì xóa cứng.
- **Zustand Selector Array Mutations**: Dùng `useShallow()` khi selector trả về array/object mới để tránh infinite re-render.
- **Tailwind v4 OKLCH**: Tránh wrap biến CSS bằng `hsl()`. Dùng `color-mix(in oklab, var(--border) 50%, transparent)` cho opacity.
- **Finance Numeric Formatting**: Sử dụng **khoảng trắng** làm dấu phân cách hàng nghìn (vd: `2 500 000`) cho VND.
- **Ops Board - Date Mapping**: Luôn hiển thị ngày thực tế cạnh Day number (vd: `Day 2 (17/03)`).

## 7. Common Components
### 7.1. InlineEditableField (Updated 2026-04-02)
- **Hỗ trợ `type="date"`**: Tự động chuyển sang mode Date Picker (Popover + Calendar của Shadcn UI).
- **Hiển thị format**: `dd/MM/yyyy` (dùng date-fns). Lưu trong DB dưới dạng `yyyy-MM-dd`.
- **Trạng thái Edit**:
    - Input type khác: Giữ nguyên logic Input/Textarea tùy theo `multiline` prop.
    - Click vào Pencil hoặc text để mở mode edit (hoặc mở Popover nếu là date).
- **Lưu ý**: Khi dùng trong Dialog/Sheet, Popover có thể bị che khuất do z-index hoặc stacking context. Đảm bảo dùng `PopoverContent` có portal hoặc kiểm tra `pointer-events: auto`.
- **Hành vi**: Tự động gọi `onSave` ngay sau khi chọn ngày trên Calendar và đóng Popover.

## 8. UI/UX Standard (Updated 2026-04-06 — Track 128)
- **Day Format (The "D" Prefix Rule)**: 
    - Sử dụng format compact `D1`, `D2`, `D1–4` cho tất cả các bảng Ops (Table rows, Drawer headers). 
    - Tránh dùng từ "Day" dài dòng trên Table để tối ưu diện tích.
    - Tất cả các loại dịch vụ (Meal, Entrance, Activity...) đều phải có prefix `D` (ví dụ: `D3`) thay vì số thuần túy.
- **Payment Status Badge**:
    - `Đã TT`: Màu **Emerald** (bg-emerald-500 text-white), text rút gọn "Đã TT" để đồng bộ thị giác với status "Confirmed".
    - `Hạn [Date]`: Màu **Amber** (bg-amber-500 text-white) để đồng bộ với tone "Pending", giúp Ops dễ dàng nhận diện các khoản sắp đến hạn thanh toán.
    - `Quá hạn`: Màu **Red** (Destructive).
- **Ops Drawer Layout**:
    - Sử dụng **Resizable Panels** (2-panel layout) cho Drawer chi tiết để Ops linh hoạt thay đổi không gian giữa Form edit và các công cụ hỗ trợ (Split/CR).
    - **Sales Notes Visibility**: Sales Notes PHẢI hiển thị ngay đầu form Drawer (vùng nền Amber nhạt) và luôn mở (không collapse). Đây là chỉ thị quan trọng nhất từ Sales mà Ops không bao giờ được phép bỏ qua.
    - **Sticky Header & Context**: Luôn giữ thông tin tên dịch vụ, badge trạng thái và Itinerary Context (sticky) khi scroll để Ops luôn nắm bắt được ngữ cảnh hành trình.

## 9. TypeScript & Build Integrity
- **Build First**: Luôn chạy `npm run build` hoặc `tsc -b` trước khi hoàn thành task để phát hiện sớm các lỗi linter (`unused imports`) hoặc type mismatch.
- **Clean Cache**: Nếu gặp lỗi `Cannot find global type 'Array/String'`, hãy xóa `.tsbuildinfo` trong `node_modules/.tmp` và chạy lại `npm install` để reset liên kết thư viện chuẩn của TypeScript.

