# Active Context

## Current Context (Cập nhật 2026-04-07 — Track 132a Planning Done)
- **Track 132a**: Itinerary Refactor — Service Decomposition — **[📅 Planned / Ready for Dev]**
  - Plan v2 hoàn chỉnh sau Red Team review: xóa 2 file service mới không cần thiết, thêm explicit field list + transaction fix.
  - Điểm then chốt: `_copy_day_fields(include_media=True/False)` — latent bug `hero_media_id` thiếu ở `_create_day_copy` + `clone_days_from_source`.
  - Plan: `conductor/tracks/132a-itinerary-refactor-service-decomposition/IMPLEMENTATION_PLAN.md`
  - Tasks: `conductor/tracks/132a-itinerary-refactor-service-decomposition/tasks.md`

## Current Context (Cập nhật 2026-04-07 — Track 134 Ported to .agents)
- **Track 134**: Skill System Upgrade — **✅ Ported to .agents**
  - **Mục tiêu**: Port các skill mới và cập nhật từ `.claude` sang `.agents`.
  - **Kết quả**:
    - ✅ Tạo mới: `done-checklist`, `alembic-workflow`, `pdf-generation`.
    - ✅ Cập nhật: `zero-loop-dev` (V3, tsc check), `frontend-standard-v1` (No `any` rule).
    - ✅ Đồng bộ: Scripts (`scaffold_backend.py`, `verify_integrity.py`) và Frontend References.
    - ✅ Đã sửa đường dẫn `.agent` → `.agents` trong nội dung skill.

## Current Context (Cập nhật 2026-04-07 — Track 133 Done)
- **Track 133**: Booking Summary Card Debug — **✅ Completed**
  - **Issue**: `bg-slate-50` trên Booking Summary card bị Dark Reader extension override → hiển thị dark bg dù light mode.
  - **Root Cause**: Dark Reader hook vào `prefers-color-scheme` media query, conflict với Tailwind `dark:*` variants.
  - **Fix**: Không fix code — accept behavior. Card render đúng khi inspect trực tiếp qua Chrome DevTools. User cần disable Dark Reader hoặc dùng Incognito mode để test.
  - **Session**: `conductor/tracks/133-booking-summary-card-debug/SESSION.md` (Đã đóng).

## Current Context (Cập nhật 2026-04-07 — Track 132 Done)
- **Track 132**: Itinerary Refactor — Backend Cleanup — **✅ Completed**
  - Mục tiêu: Tách business logic khỏi router, chuẩn hóa Eager Loading và fix Datetime serialization.
  - Kết quả:
    - ✅ **Phase 1**: `field_serializer("created_at", "updated_at")` + `serialize_dt` cho 4 Response classes (`ItineraryDayResponse`, `ItineraryHotelResponse`, `ItineraryPriceResponse`, `ItineraryResponse`)
    - ✅ **Phase 2**: 3 static helpers `_list_query_options()`, `_detail_query_options()`, `_clone_query_options()` + `create_itinerary()` trong service. **Fix latent bug**: `_detail_query_options()` giờ include `owner` (was missing)
    - ✅ **Phase 3**: Router refactor — `create_itinerary` (79→8 lines), `list_itineraries`/`get_itinerary`/`activate_itinerary_version` dùng helpers. Xóa duplicate imports. Fix docstring placement (6 endpoints).
    - ✅ **verify_integrity**: All checks passed
  - **Files changed**: `app/schemas/itinerary.py`, `app/services/itinerary_service.py`, `app/api/v1/itineraries.py`
  - **Out of scope** (Track 132a): `update_itinerary` logic refactor

## Current Context (Cập nhật 2026-04-07 — Track 130 Done)
- **Track 130**: Invoice Facture Module — **✅ Completed**
  - Mục tiêu: Hoàn thiện luồng Invoice, tích hợp Inline view và xử lý i18n/Header.
  - Kết quả:
    - ✅ **Inline Detail Flow**: Tích hợp `InvoiceDetailManager` vào tab Invoices của Opportunity, thay thế việc nhảy trang bằng hiển thị inline mượt mà.
    - ✅ **UI/UX Refinement**: Cải thiện ô nhập liệu Price/Qty (font-medium, no Check/Cancel icons, auto-save on blur/enter).
    - ✅ **Backend Context Filtering**: Thêm `opportunity_id` vào API List Invoices để lọc chính xác dữ liệu trong tab.
    - ✅ **i18n & Header**: Cập nhật tiếng Ý (`it.json`) chuẩn xác (Circuito, Date, Durata...) và tự động đổi email/site sang `.it` cho thị trường Ý.
  - Session: `conductor/tracks/130-invoice-facture-module/SESSION.md` (Đã đóng).

## Current Context (Cập nhật 2026-04-06 — Track 131 Done)
- **Track 131**: Invoice PDF & UI Finetune — **✅ Completed**
  - Mục tiêu: Triển khai module xuất hóa đơn (Invoice) PDF theo bộ nhận diện Vactours 2026 và tích hợp Live Preview.
  - Kết quả:
    - ✅ Backend: Hệ thống i18n JSON (`fr`, `en`, `it`) và logic load Bank Info động từ `SystemSettings`.
    - ✅ PDF: Redesign template HTML/CSS (WeasyPrint) chuẩn mockup 2 cột, hỗ trợ logo/footer/highlight reference.
    - ✅ Frontend: Thêm Tabs Details/Preview trong trang chi tiết Invoice, tích hợp `iframe` Live Preview tự động làm mới khi dữ liệu thay đổi.
  - Plan: `conductor/tracks/131-invoice-ui-finetune/IMPLEMENTATION_PLAN.md`

## Current Context (Cập nhật 2026-04-02 — Track 121 Active)
- **Track 121**: Ops Service Sales Note Mapping — **[💻 Dev]** — AG tiếp nhận thực hiện.
  - Mục tiêu: Map `sales_note` từ Quote sang OpsService.
  - Plan: `conductor/tracks/121-ops-service-sales-note-mapping/IMPLEMENTATION_PLAN.md`
  - Note: Cần tích hợp vào `_apply_single_ops_service_update` vừa refactor ở Track 123.

## Current Context (Cập nhật 2026-04-02 — Track 123 Done)
- **Track 123**: Booking Service Refactor — **✅ Completed**
  - Refactor `update` & `bulk_update` dùng chung helper `_apply_single_ops_service_update`.
  - Fix Security Gap: Thêm auth check cho `/itinerary-context`.
  - SQL Pagination: `list_bookings` hỗ trợ limit/offset/order_by trực tiếp trong SQL cho `created_at`.
  - Lightweight fetch: Thêm `_get_booking_for_auth` cho mutation endpoints.

## Current Context (Cập nhật 2026-04-05 — Track 128 QA/Fixing)
- **Track 128**: OpsService Drawer Refactor — **✅ Completed**
  - Đã triển khai xong Resizable Drawer, Split Segment và Change Request inline.
  - Đang tồn tại 9 vấn đề QA (lỗi resize, lỗi 422, thiếu field cho Hotel/Guide/Transport, thêm tab Contact).
  - Mục tiêu tiếp theo: Xử lý triệt để danh sách `QA_ISSUES.md`.
  - Session: `conductor/tracks/128-drawer-refactor/SESSION.md`

## Current Context (Cập nhật 2026-04-05 — Track 127 Pipeline)
- **Track 127**: Finetune Booking UI v2 — Ultra-Compact Table — **[⏸ Paused/Pipeline]**
... (phần còn lại giữ nguyên)

## Current Context (Cập nhật 2026-04-03 — Track 126 ⏸ Paused)
- **Track 126**: Refactor Booking UI — **[⏸ Paused]** — tạm dừng, chờ ATu review
  - Phase 1-6 ✅: Tất cả complete (BookingHeader, ToolsSidebar, OpsServiceDrawer, J/K hotkeys)
  - **Bug fixes vừa làm** (2026-04-03):
    - Fix 1: `isDirty` reset sau save thành công trong OpsServiceDrawer
    - Fix 2: Day context amber collapsible box (QuoteGrid style)
    - Fix 3: Drawer width `560px/680px` (trước `480px/560px`)
  - **Note**: `ItineraryContext` API chỉ có `day_titles`, không có `day_description`. Day context box hiển thị `day_titles`.
  - Plan: `conductor/tracks/126-refactor-booking-ui/IMPLEMENTATION_PLAN.md`
  - Session: `conductor/tracks/126-refactor-booking-ui/SESSION.md`

## Current Context (Cập nhật 2026-04-02 — Track 122 QA)
- **Track 122**: Quote Editor Grid Upgrade — **✅ Completed** — Implementation DONE, chờ ATu test local.
  - ✅ Thay Accordion List → Native HTML `<table>` với rowSpan Day (cột sticky 200px)
  - ✅ `useGridNavigation.ts` — Tab/Arrow/Enter/Escape keyboard nav
  - ✅ `useQuoteDayGrouping.ts` — group items by day + join itinerary days
  - ✅ `QuoteGrid.tsx` — main component với inline editing Description/Qty/Price
  - ✅ `QuoteItemSidePanel.tsx` — panel 320px: Notes/Markup/VAT/ServiceRate
  - ✅ `AddServiceDialog` — per_pax services default qty = `quote.pax_count`
  - ⏳ Sau QA pass: xoá `QuoteItemTable.tsx` + `QuoteItemRow.tsx`
  - Plan: `conductor/tracks/122-quote-editor-grid-upgrade/IMPLEMENTATION_PLAN.md`

... (rest of the file remains for history)
