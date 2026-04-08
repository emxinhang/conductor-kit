# Technical Decisions Log (Historic)

- **[P1][2026-04-07] Track 132a — SQLAlchemy async: KHÔNG dùng `async with db.begin()` trong service nếu đã có `flush()`**:
  - **L1 — Critical Facts:** Gọi `async with db.begin()` sau khi `flush()` đã chạy sẽ raise `InvalidRequestError: A transaction is already begun on this Session`. Toàn bộ codebase TMS-2026 dùng pattern `flush() → commit()` — nhất quán, không pha trộn.
  - **L2 — Context:** Khi cần transaction safety cho clone operations (Itinerary + Quote clone cùng lúc): dùng try/except explicit `await db.rollback(); raise` thay vì `async with db.begin()`. `clone_active_quote_to_itinerary` đã KHÔNG có `db.commit()` bên trong → happy path đã atomic sẵn.
  - **L3 — References:** Track 132a Plan v2 Phase 3; `backend/app/services/itinerary_service.py:477` (`duplicate_itinerary_standalone`)

- **[P1][2026-04-07] Track 132a — `_copy_day_fields(include_media)` pattern cho Day clone**:
  - **L1 — Critical Facts:** Khi copy `ItineraryDay`, dùng `include_media=True` nếu duplicate trong cùng itinerary, `include_media=False` nếu import ngày từ itinerary khác. `hero_media_id` là conditional field.
  - **L2 — Context:** Latent bug: `_create_day_copy` và `clone_days_from_source` đều thiếu `hero_media_id` trong field list thủ công. `_copy_day_fields` helper sẽ fix cả hai. Fields luôn LOẠI BỎ: `id, itinerary_id, created_at, updated_at, day_number, sort_order, date, is_pinned`.
  - **L3 — References:** `backend/app/services/itinerary_service.py:243` (`_create_day_copy`), `:376` (`_deep_clone_itinerary_core`), `:594` (`clone_days_from_source`)

- **[P1][2026-04-02] Track 122 — Quote Grid: Plain HTML table thay vì TanStack/AG Grid**:
  - **Quyết định**: Dùng native `<table>` + Tailwind CSS thay vì TanStack Table hoặc AG Grid Community.
  - **Lý do**: (1) `rowSpan` native HTML — TanStack không hỗ trợ, cần custom DOM phức tạp; (2) Zero new dependency; (3) 100% compatible Tailwind/shadcn; (4) 15-30 rows không cần virtualization; (5) Keyboard nav vẫn là custom hook dù dùng lib nào.
  - **TanStack chỉ đáng khi**: cần sort/filter/virtual scroll trên data lớn.
  - **AG Grid chỉ đáng khi**: cần Excel-level features (formula, freeze panes) AND chấp nhận ~500KB bundle + style conflict.
  - **Áp dụng khi**: Bất kỳ grid nhỏ (< 100 rows) cần inline editing + rowSpan → plain HTML table trước tiên.

- **[P1][2026-03-27] Track 118 — Package booking design: 1 BookingItem + day-range overlay**:
  - **Vấn đề**: Landtour package (Laos/Cambodia) không có quote breakdown — chỉ có tổng giá. Itinerary vẫn có breakdown ngày. Không có guide VN. Incident vẫn cần per-day.
  - **Design**: 1 `PackageBookingItem` (type=`land_package`, supplier_id, date_from, date_to, total_cost, notes). Tour tracking: ngày trong package range render "package mode" — hiện badge `📦 Package: [Supplier]`, hotel/transport = "Included in package", guide = empty, incident = full form.
  - **Mix tour**: Một tour có thể có partial package (vd: 3 ngày HN normal + 4 ngày Laos package) — cần map "ngày nào thuộc package range" khi render.
  - **Áp dụng khi**: Bất kỳ tour nào có `other_service` type `land_package` trong quote → convert tạo `PackageBookingItem` thay vì expand thành từng hotel/transport.
  - **5 Q còn mở**: Q1 quote structure, Q2 ai map ngày vào package, Q3 booking item fields, Q4 tour tracking render detail, Q5 ops confirm workflow.
  - **PRD**: `conductor/tracks/118-package-booking-flow/PRD.md`

- **[P1][2026-03-26] Track 111e — DepartmentPermissionsPage MODULE_CONFIG là enumeration, không phải lookup**:
  - **Vấn đề**: `DepartmentPermissionsPage` dùng `Object.entries(MODULE_CONFIG).map(...)` để render toàn bộ toggle switches. Đây là enumeration source — KHÔNG phải lookup map.
  - **Hệ quả**: Thêm bất kỳ key nào vào MODULE_CONFIG → xuất hiện ngay trong admin UI như một module toggle độc lập. Thêm child nav IDs (`suppliers-all`, `guides-all`) sẽ tạo "phantom toggles" không liên kết với DB permission flow.
  - **Rule**: Chỉ thêm vào MODULE_CONFIG các **parent module codes** được lưu trực tiếp trong DB (`department_module_permissions.module_code`). Child nav IDs do backend expand — không cần toggle riêng.
  - **Áp dụng khi**: Bất kỳ track nào thêm nav entries mới vào navigation.ts → KHÔNG tự động thêm vào MODULE_CONFIG.

- **[P1][2026-03-26] Track 111e — GuidePage standalone vs wrapper (113a compatibility)**:
  - **Quyết định**: GuidePage là standalone component (own state + hooks), KHÔNG phải wrapper `<SupplierListPage lockType={true} />`.
  - **Lý do**: Track 113a cần `GuideDetailPage` + `GuideForm` với guide-specific fields. Wrapper approach → prop-drill hell qua SupplierListPage (mỗi 113x feature = 1-2 props mới). Standalone → 113a extend GuidePage tự do.
  - **Pattern**: Reuse hooks (`useSuppliers`) + sub-components (`SupplierForm`, `SupplierHistoryTable`) trực tiếp. KHÔNG wrap page-level component.
  - **Áp dụng khi**: Tạo bất kỳ "filtered view" page từ existing list page. Nếu page sẽ bị extend trong 1-2 tracks tiếp theo → luôn standalone.

- **[P1][2026-03-26] Track 111e — suppliers-all missing từ PARENT_CHILD_MAP (pre-existing bug)**:
  - **Bug**: `PARENT_CHILD_MAP["hotels-mgmt"]` chỉ có 4 children (hotels-all, contracts-*). Thiếu `suppliers-all` → non-superadmin có `hotels-mgmt` permission không thấy Supplier Network nav item.
  - **Fix**: Thêm `suppliers-all` + `guides-all` vào `hotels-mgmt` expansion trong `department_permission_service.py`.
  - **Áp dụng khi**: Khi thêm nav item mới vào nhóm Partners/Hotels → phải kiểm tra PARENT_CHILD_MAP có expand nav ID đó không.

- **[P1][2026-03-26] Track 111d — Supplier sync logic ở FRONTEND, không phải backend**:
  - **Vấn đề**: PRD ban đầu spec backend sync supplier fields vào confirmation_details — sai hoàn toàn.
  - **Thực tế**: Toàn bộ sync logic nằm ở `frontend/src/pages/bookings/components/zoneGrouping.ts`:
    - `buildSupplierSyncFields(serviceType, supplier)` — line 187
    - `buildSupplierUnsyncFields(serviceType)` — line 232
  - Backend chỉ nhận `confirmation_details` JSON bất kỳ qua `PATCH /bookings/{booking_id}/ops-services/{id}`. Không tự sync gì.
  - **Áp dụng khi**: Bất kỳ track nào cần sync supplier data → phải update zoneGrouping.ts, không tạo backend logic mới.

- **[P1][2026-03-26] Track 111d — Train supplier type missing + naming conflict**:
  - **DB**: `CheckConstraint("type IN ('guide','transport','restaurant','activity')")` — không có `train` → tạo supplier type=train sẽ crash.
  - **Sync naming conflict**: `buildSupplierSyncFields` gộp `train` vào `['transport','train','flight']` và sync keys `company_name/company_phone`. Nhưng `TrainConfirmation` dùng keys `provider_name/poc_phone` → phải tách branch riêng trong zoneGrouping.
  - **Backward compat pattern**: Data cũ (company_name) → display-map trong renderTrainForm: `train.provider_name ?? (train as any).company_name`. Save luôn ghi key mới. Không migrate DB.
  - **Áp dụng khi**: Implement 111d — tách train branch trong buildSupplierSyncFields/Unsync.

- **[P1][2026-03-26] Track 113 — Guide Calendar data chain + metrics definitions**:
  - **Data chain**: `OpsService(supplier_id=X, service_type='guide', day_number=N)` → `Booking` → `Quote` → `Itinerary.start_date` → `actual_date = start_date + timedelta(days=N-1)`
  - **Null-safety**: skip OpsService row nếu `booking.quote` hoặc `quote.itinerary` là None (không crash 500)
  - **Calendar filter**: non-cancelled; `active` → sáng màu, `completed` → dimmed, `cancelled` → exclude
  - **Report metrics**: `total_tours = COUNT(DISTINCT booking_id)`, `total_days = COUNT(DISTINCT actual_date)`
  - **Permission**: cả `GET /{id}/assignments` và `GET /{id}/report` dùng `VIEW_TOUR_TRACKING` (consistent với `booking-history`)
  - **Granularity**: 1 OpsService = 1 ngày (nghiệp vụ đảm bảo 1 ngày chỉ có 1 guide service)
  - **Áp dụng khi**: Planning/implement 113b, 113c.

- **[P1][2026-03-26] Track 113a — GuideDetailPage architecture**:
  - **Structure**: `/guides/:id` với 3 tabs — Profile (inline editable) / Lịch / Báo cáo
  - **Profile tab**: inline editable, flat layout. KHÔNG dùng Sheet form.
  - **Cleanup**: Bỏ "Service History" dropdown item trong `GuidePage.tsx` khi 113a live (Calendar tab cover use case này)
  - **API files**: `GuideAssignment` + `GuideReport` types → `supplier.ts`. API functions → extend `suppliers.ts`. KHÔNG tạo `guides.ts` riêng (guide là supplier subtype)
  - **Field name**: `id_card_number` (không phải `id_number` để tránh nhầm với PK)
  - **Calendar month picker**: dùng `placeholderData: keepPreviousData` (React Query v5) tránh flicker khi switch tháng
  - **Áp dụng khi**: Implement 113a, 113b, 113c.

- **[P1][2026-03-26] Track 113 — Guide Module tách từ 111e**:
  - **Quyết định**: 111e chỉ còn navigation refactor (Hotel menu, Partners sub-items). Guide data/features → Track 113.
  - **113a**: CCCD + số thẻ HDVDL (2 fields, migration). **113b**: Calendar tour assignments. **113c**: Annual report.
  - **Sequence**: 111d → 111e → 113a → (113b ‖ 113c).
  - **Áp dụng khi**: Planning 111e — không đụng guide data model. Planning 113a — chỉ add 2 nullable columns vào suppliers table.

- **[P0][2026-03-26] Track 112d — `user.role == "admin"` Broken Bug (Critical)**:
  - **Vấn đề**: `user.role` trong model trả về `department.code` (e.g. "bod", "it", "sales"). Không bao giờ trả về `"admin"`. Do đó mọi check `current_user.role == "admin"` hoặc `role != "admin"` đều là dead code hoặc tệ hơn — **luôn True hoặc luôn False**.
  - **Nơi bị ảnh hưởng**: `discussion_service.py:359,389` (ai cũng bị deny edit/delete comment của người khác — bug thực), `users.py:105,126` (broken admin bypass — vẫn work nhờ fallback khác), `websocket/router.py:68` (dead `"admin"` branch).
  - **Fix 112d**: Thay `role != "admin"` bằng `has_capability(MANAGE_SETTINGS)` hoặc `require_capability(MANAGE_USERS)` tùy context.
  - **Lesson**: Khi refactor role sang department — audit toàn bộ `role` usages bằng grep. 5 usages đã được liệt kê trong 112d plan.

- **[P1][2026-03-26] Track 112d — AuthorizationService API gotchas**:
  - **Method name**: `get_data_scope(user, cap_code)` — KHÔNG phải `get_user_scope()`.
  - **Import path**: `from app.services.authorization import AuthorizationService` — KHÔNG phải `authorization_service`.
  - **Migration ON CONFLICT**: Thêm capabilities vào existing table → KHÔNG dùng `op.bulk_insert` (crash trên UniqueConstraint). Dùng raw SQL + `ON CONFLICT (department_id, capability_code) DO NOTHING`.
  - **Scope returns None**: `get_data_scope()` trả `None` nếu user không có cap → `None == "all"` = False → vào restricted branch. Cần comment rõ intent.

- **[P1][2026-03-26] Track 112d — Capability-based bypass trong WebSocket**:
  - **Pattern**: `_has_room_access` fetch user qua `load_user_with_capabilities()` → có capabilities sẵn. Dùng `AuthorizationService.has_capability(user, MANAGE_SETTINGS)` thay vì hardcode `"it" in user.department_codes` cho super-admin bypass.
  - **Tại sao**: Mixed pattern (dept-code check + capability check trong cùng 1 function) là code smell và đi ngược RBAC refactor goal. Nhất quán hoàn toàn với capability.

- **[P1][2026-03-25] Track 112c — RBAC Frontend Alignment (Planning Decisions)**:
  - **Capability hooks NO `is_super_admin` bypass**: `useHasCapability(code)` chỉ check `capabilities` dict. IT users đã có full 22 caps seeded → bypass không cần. Data IS source of truth.
  - **Dual-fetch `loadPermissions`**: `Promise.all([getMyPermissions(), getMyCapabilities()])`. `modules` chỉ có ở `/me/permissions`, `capabilities` chỉ có ở `/me/capabilities`. Merge vào 1 `UserPermissions` object.
  - **Zustand persist version migration**: v1→v2. Old `auth-storage` → `permissions: null`. `onRehydrateStorage` callback auto-triggers `loadPermissions()` khi `isAuthenticated && !permissions`.
  - **Frontend CAP constants**: Mirror backend `capabilities.py`. Full 22-entry `CAP` object trong `types/permission.ts`. Autocomplete + type safety.
  - **4 files DEFERRED to 112d** (Codex Red Team finding):
    - OpportunitiesPage/SalesPipelinePage: Backend DELETE dùng `EDIT_OPPORTUNITY`, FE restrict BoD+IT → mismatch. Cần `delete_opportunity` cap.
    - PersonListPage: Tương tự, cần `delete_contact` cap.
    - ServiceManagementPage: Backend quote_templates IT-only. `manage_settings` mở rộng BOD → confusing UX.
  - **AuditLogTab case bug**: `departments?.includes("BOD")` uppercase nhưng backend trả lowercase `"bod"` → migration sang `useHasCapability` fix tự nhiên.
  - **`useIsBodOrSuperAdmin` KEPT**: 3 deferred consumers vẫn import. Chỉ delete `useCanEditSupplier` + `useCanResolveIncident`.

- **[P0][2026-03-25] Track 112b — RBAC Authorization Service (Implementation Decisions)**:
  - **Separate `department_capabilities` table (intentional)**: Khác lifecycle vs `department_module_permissions`. Module perms = UI sidebar nav (admin toggle). Capabilities = business actions (seeded per dept, rarely changed). Hai consumer khác nhau, không merge.
  - **22 mandatory capability constants**: `app/core/capabilities.py` — Enum/constants, all code must import. Không dùng magic strings. Seed migration + router + service + test import cùng symbols.
  - **Adapter-first OwnershipResolvers**: Wrap existing logic (`_can_view_booking`, `collaborator_helper`, quote service checks) — KHÔNG copy-paste. Refactor internal logic trong 112d.
  - **Fresh auth per WS room join**: `load_user_with_capabilities(user_id, db)` per room check. Không pass hydrated User object — tránh stale auth on long-lived sockets.
  - **Split booking guards per action**: 9 callers of `_check_booking_edit_access` remapped: line 49 (convert) → `CONVERT_BOOKING`, lines 88-256 → `EDIT_BOOKING`. Không dùng 1 capability cho nhiều actions khác nhau.
  - **CheckConstraint on scope**: `scope IN ('all','team','owned')` — defense-in-depth dưới Pydantic validator.
  - **Zero extra DB queries for HTTP**: Eager-load capabilities in `get_current_user` via `selectinload(dept_memberships → department → capabilities)`. AuthorizationService reads in-memory.
  - **Manager upgrade in-memory**: `is_manager=true` on UserDepartment → "owned" scope becomes "team" automatically. Không thêm DB column.
  - **Scope union for multi-dept**: Most permissive wins (`all > team > owned`). User in BOD(all) + Sales(owned) → effective = all.
  - **25 itinerary call sites**: `_check_itinerary_edit_access` has 24 callers + `_check_bod_or_it` has 1 caller. All enumerated in plan.
  - **5 user.role bug sites**: `quotes.py:100,329,493`, `quote/service.py:422`, `audit_logs.py:24` — all to be migrated.

- **[P0][2026-03-25] Track 112 — RBAC Authorization Model (4-Layer)**:
  - **Layer 1 Module Visibility**: `DepartmentModulePermission` (existing) — sidebar navigation only.
  - **Layer 2 Capability**: `department_capabilities` table (NEW in 112b) — business actions (view_booking, edit_booking, resolve_incident...).
  - **Layer 3 Data Scope**: `all | team | owned` per capability per department. Union priority: all > team > owned. Multi-dept = most permissive wins.
  - **Layer 4 Entity Access**: `OwnershipResolver` registry (NEW in 112b) — per-entity-type ownership check (Itinerary: owner_id+collabs, Booking: via opportunity chain, etc.).
  - **`user.role` is DEPRECATED**: Chỉ check primary department. Dùng `user.department_codes` (set of ALL dept codes) thay thế. `quotes.py:100` vẫn dùng `user.role` — tech debt cho 112b.
  - **Operations bypass**: Itineraries = {"bod","it","operations"} thấy all. Opportunities = {"bod","it"} only. Bookings = existing logic giữ nguyên.
  - **`has_module_access()` default**: True → False (whitelist). Must verify seed coverage trước khi change.
  - **`is_manager` field**: Added to `user_departments` — manager gets "team" scope (thấy records của all dept members). Chưa dùng cho đến 112b.
  - **Permission Matrix Canonical**: Xem PRD Section 4.2 — full matrix Sales/Ops/Accounting/BOD/IT × 18 capabilities.

- **[P1][2026-03-25] Track 106c — Incident System Architecture**:
  - **WS Room Ownership Pattern (P0)**: `IncidentWSHandler` (app-level, mounted in MainLayout) là **sole owner** của `tour_tracking` room join. Không component nào khác được join/leave room này. `TourTrackingPage` và `BookingDetailPage` chỉ subscribe events. Lý do: backend room membership dùng Set (user_id) — leave_room từ 1 component xóa membership cho tất cả.
  - **Exclude sender in WS broadcast**: `broadcast_to_room(..., exclude_user_id=current_user.id)` cho cả `create_incident()` và `resolve_incident()`. Ngăn double toast (mutation toast + WS toast).
  - **Schema `@computed_field` cho name fields**: `IncidentResponse` dùng `@computed_field` đọc từ `reporter`/`resolver` relationships (qua selectinload). Service trả ORM objects, `response_model` serialize. Không manual mapping.
  - **API client tách riêng**: `api/incidents.ts` riêng (không merge vào `tourTracking.ts`) — incidents sẽ grow thêm endpoints.
  - **Two-way `?tab=` sync**: `useSearchParams` read + write, sanitize against `VALID_TABS`, react to back/forward.
  - **Permission hook**: `useCanResolveIncident()` trong `useAuth.ts` — check `is_super_admin` (IT) + BoD + Operations. Không hardcode department strings trong feature code.
  - **Optimistic cache**: `setQueryData` on create/resolve success, `invalidateQueries` on settled for reconciliation. WS events trigger invalidation for cross-user sync.

- **[P1][2026-03-24] Track 111c — Supplier Booking Integration Refactor**:
  - **Bo free-text bypass (hard requirement)**: SupplierCombobox khong cho go free-text nua. Ops phai chon tu DB hoac Quick Create. onChange doi tu `(id, name)` sang `(supplier: Supplier | null)` — blast radius 4 callers.
  - **Quick Create inline**: Reuse SupplierForm (111b) trong Dialog. Pre-fill name + type tu context. `onSuccess` tra full Supplier object. Form reset via `useEffect(form.reset)` keyed on props (C6).
  - **Confirmation details auto-sync**: Khi chon supplier → populate sync fields per service type (guide/transport/restaurant/activity). Khi clear → null tat ca sync fields via `buildSupplierUnsyncFields()` (C4). Giu nguyen non-sync fields (driver_name, vehicle_type...).
  - **Data source rule (C5)**: KHONG dung local `selectedSupplier` state. Derive tu booking query data + `useSupplier(id)` enrichment only.
  - **Duplicate check (C2)**: Partial unique index `(lower(name), type) WHERE is_active = true`. IntegrityError → 409 voi `{message, existing_id}`. Frontend bat 409 → "Chon NCC nay".
  - **Permission gate (C1)**: `useCanEditSupplier()` check `is_super_admin` (IT) hoac `departments.includes('bod'|'operations')`. Lowercase match backend.
  - **Header contact display**: `SupplierContactLine` component shared — hien POC + phone (tel:) + email (mailto:) + language badges (guide only).

- **[P1][2026-03-24] Track 111a — Supplier Backend Implementation Patterns**:
  - **Inline permission helper**: Không import private `_user_has_department` từ `booking_service.py` — copy 5 dòng logic inline vào router mới. Import public constants OK. Pattern: `_supplier_has_department(user, allowed_set)` inline trong `suppliers.py`.
  - **FK + name sync rule (P0)**: Khi set `supplier_id`, phải fetch supplier từ DB và overwrite `supplier_name = supplier.name`. Không để 2 field diverge. Unlink (`supplier_id=None`) giữ `supplier_name` làm fallback text.
  - **DB-level type enum**: Thêm `CheckConstraint("type IN (...)", name="ck_suppliers_type")` vào `__table_args__` — defense-in-depth dưới Pydantic validator.
  - **permission matrix mới**: GET list/detail = Any auth; POST/PATCH/DELETE = `OPS_SERVICE_EDIT_DEPARTMENTS`; booking-history = `TOUR_TRACKING_VIEW_DEPARTMENTS`.

- **[P1][2026-03-24] Track 111 — Supplier Module Architecture**:
  - **4 supplier types**: `guide | transport | restaurant | activity` (enum, không có `other`)
  - **Service type → supplier type mapping**: localguide→guide; train/flight→transport; lunch/dinner→restaurant; boat/massage→activity; hotel→dùng `hotel_id` FK riêng; custom/other→any (không filter)
  - **Contact constraint**: `CHECK (phone IS NOT NULL OR email IS NOT NULL)` — không bắt buộc cả 2
  - **Guide language**: `language_codes: string[]` (PostgreSQL array) — guide có thể nói nhiều ngôn ngữ
  - **Soft delete only**: `is_active=false`, hard delete bị cấm vì mất booking history
  - **Source-of-truth**: chọn supplier → pre-fill `supplier_name` snapshot. Supplier đổi info sau KHÔNG auto-refresh booking cũ
  - **Quick Create inline**: tại booking combobox, nếu NCC chưa có → dialog nhỏ (name+type+phone/email) → POST /suppliers → auto-select. Không cho free-text bypass DB
  - **No backfill**: existing `supplier_name` free-text rows không migrate tự động (out of scope)
  - **Inactive supplier**: ẩn khỏi default combobox, vẫn hiển thị trong booking history cũ
  - **Sub-tracks**: 111a (Backend) → 111b (Supplier List/Detail) → 111c (Booking integration)

- **[P1][2026-03-23] Track 106 — Real-time Tour Tracking Architecture**:
  - **departure_date không phải DB column**: Phải JOIN `bookings → quotes → itineraries` lấy `i.start_date` + `i.total_days`. Query active: `i.start_date <= today AND i.start_date + total_days - 1 >= today`.
  - **`pax_count` trên Quote, không phải Itinerary**: `Booking.quote_id → Quote.pax_count`. Itinerary model chỉ có `start_date` + `total_days`.
  - **WebSocket room `tour_tracking`**: Là bare name, không theo format `entity_type:id` → cần **special-case branch** trong `_has_room_access()` của `websocket/router.py`. Access: Ops/BoD/IT via `UserDepartment JOIN Department WHERE code IN (...)`.
  - **Reuse `_can_view_booking`**: Hàm này đã có tại `booking_service.py`, được dùng bởi `change_request_service`, `discussion_service`. Bao gồm FULL_ACCESS_DEPARTMENTS (BOD, IT), itinerary owner, collaborator. Không viết lại helper permission riêng.
  - **Atomic resolve — tránh TOCTOU**: `UPDATE incidents SET status='resolved'... WHERE id=X AND status='open'` → check rowcount=0 → 409. KHÔNG check-then-update (2 bước).
  - **`reported_by` server-set**: Không nhận từ body. Service tự gán `reported_by = current_user.id`. Tránh impersonation.
  - **Idempotency race-safe**: Payload hash `(booking_id, reported_by, incident_type, severity, description)` trong 10s. Dùng `INSERT ... ON CONFLICT DO NOTHING` hoặc serializable tx thay vì SELECT-only check.
  - **OpsServiceStatus warning matrix**: `pending|reserved` → ⚠️ warning; `confirmed|not_available|self_arranged` → ✅ OK.
  - **Email**: Resend SDK (`EmailService`), fire-and-forget `asyncio.create_task()`. Dedupe recipients by user_id. Dùng `User.email` (không `email_work`).
  - **WS broadcast failure**: Log error, KHÔNG rollback incident, vẫn trả 201.
  - **days split**: `days_remaining` (active, >= 0) vs `days_until_start` (upcoming) — tách rõ semantic.
  - **Track splits**: 106a (Backend), 106b (Frontend Dashboard), 106c (Full-stack Incident System).

- **[P0][2026-03-18] FastAPI route ordering — literal vs path param**:
  - **Vấn đề**: Route `/{id}/ops-services/segment-review` nếu đăng ký SAU `/{id}/ops-services/{service_id}`, FastAPI hiểu `"segment-review"` là giá trị `service_id` → raise 422 (string != int).
  - **Giải pháp**: Luôn đăng ký literal routes TRƯỚC path-param routes trong cùng prefix. Áp dụng ngay khi có pattern `/something/literal-action` và `/something/{id}` cùng prefix.
  - **Áp dụng khi**: Thêm bất kỳ endpoint action-style nào cạnh CRUD endpoint có `{id}` param.

- **[P1][2026-03-18] Track 102g — Hotel Room Type Verification Gate**:
  - **Vấn đề**: Sau khi đổi `hotel_id`, `room_type` cũ trong `confirmation_details` vẫn giữ nguyên, Ops phải tự double-check.
  - **Giải pháp**: Field `room_type_needs_review: Boolean DEFAULT false` trên `OpsService`. Backend auto set `true` khi `hotel_id` thay đổi. Chặn `status=confirmed` nếu flag còn true. Endpoint riêng `POST /segment-review` để Ops clear flag (keep/reset).
  - **Design constraint**: Field là server-controlled — KHÔNG expose trong `OpsServiceUpdate` hay `OpsServiceBulkUpdateItem`. Chỉ clear qua endpoint dedicated.
  - **Segment derive server-side**: Backend dùng `anchor_service_id` để tự build segment (cùng hotel grouping key + contiguous days), không trust client-sent `service_ids`. Tránh IDOR và partial clear.

- **[P1][2026-03-18] JSONB safe partial update — pop key, không replace**:
  - **Vấn đề**: Khi muốn xóa 1 key trong JSONB (ví dụ: `room_type`), nếu replace toàn bộ object sẽ mất các key khác (`check_in`, `check_out`, `contact_name`...).
  - **Giải pháp**: `details = dict(service.confirmation_details); details.pop("room_type", None); service.confirmation_details = details if details else None`
  - **Áp dụng khi**: Bất cứ khi nào cần clear 1 key trong `confirmation_details` JSONB mà không mất data khác. Pattern này đã áp dụng cả ở Guide merge flow và 102g reset flow.

- **[P1][2026-03-18] Track 103 — Change Request Workflow (PRD v3 decisions)**:
  - **No type enum**: CR dung `reason` free-text thay vi enum type → flexible tracking moi case
  - **`affected_service_ids` JSON**: Segment-level CR luu all ops_service_ids → update ca block khi approve
  - **`version` field**: Optimistic concurrency → 409 Conflict khi stale
  - **`awaiting_proposal` status**: Khi Sales tao CR khong co de xuat → Ops submit proposal → pending
  - **Soft revert khi cancel**: Confirm dialog cho phep revert hoac giu nguyen (tranh overwrite data moi hon)
  - **Snapshot immutable**: `original_*` fields derive tu DB khi tao CR, khong sync tu canonical Hotel table
  - **Itinerary sync**: Chi hotel name + room type, KHONG touch pricing/quoted_cost
  - **Codex review 8 fixes**: (1) Server-side snapshots - khong trust FE, (2) Application-level segment overlap check, (3) FOR UPDATE ca CR + affected ops_services, (4) Reuse ItineraryDay update truc tiep, (5) Notification type lowercase, (6) OpsServiceStatus khong co 'cancelled', (7) Match API client pattern bookingApi, (8) Reuse hotel picker tu HotelGroupCard
- **[P0][2026-03-18] Zero-Handoff V3 — Workflow chuẩn mới toàn hệ thống**:
  - **Vấn đề cũ**: Codex review mọi bước Claude → context fragmentation. Gemini thụ động "thợ xây". Thiếu shift-left testing. Không có code review sau implementation.
  - **Workflow mới (3 giai đoạn)**:
    - **Giai đoạn 1 — Architect Council (Claude + Codex + ATu)**:
      - `/brainstorm-track` → `/planner-track` → `[PostToolUse Hook: Codex auto-review]` → `/red-team-reviewer` (Claude "đóng vai ác" với Codex data) → `/review-plan` (technical checklist) → ATu approve → `IMPLEMENTATION_PLAN.md final`
    - **Giai đoạn 2 — Execution (Gemini làm chủ)**:
      - `/handoff` → Gemini đọc plan, check codebase state → code từng task → `verification-before-completion` tự verify (HTTP 200 / npm run build) → đánh `[x]` → tiếp
    - **Giai đoạn 3 — Human Acceptance (ATu)**:
      - ATu manual test → nếu có bug: `/bug-report` → Claude RCA (không gọi Codex) → fix → capture learning inline
  - **Skills mới tạo**: `red-team-reviewer` (4 lăng kính critique), `handoff` (kickoff Giai đoạn 2), `zero-loop-dev V3` (upgrade)
  - **Hook automation**: `PostToolUse` hook → detect write `PRD.md`/`IMPLEMENTATION_PLAN.md` → auto chạy Codex CLI → ghi `*_codex_review.md` → notify Claude
  - **Codex CLI syntax**: `codex exec "prompt" --ask-for-approval never --output-last-message`
  - **Key principle**: Codex chỉ ở Giai đoạn 1 (Plan). Gemini owns Giai đoạn 2 (Code+Verify). Claude owns bug RCA.
- **[2026-03-17] Track 102e — Guide & Transport Logistics (Implementation Plan v1.0)**:
  - **Scope v1**: `guide` + `localguide` cùng flow; `transport` flow riêng; `boat`/`train` giữ flat rows.
  - **No DB migration**: Data trong `OpsService` hiện tại — `supplier_name` (zone shared), `confirmation_details` JSONB (segment-specific + `assignment_group`).
  - **Zone detection**: `GET /bookings/{id}/itinerary-context → { day_titles }` + keyword map city→zone từ `system_settings.booking_zone_city_map`. Không nhet thêm vào GET booking detail.
  - **Split**: Chỉ tạo `assignment_group` cho segment phải; trái giữ cũ/null. Reset contact fields segment mới, giữ actual_cost/confirmation_no.
  - **Merge**: Copy metadata segment đầu sang tất cả rows gộp, đồng nhất assignment_group. KHÔNG chỉ xoá group.
  - **JSONB merge rule (P0)**: Frontend PHẢI merge `confirmation_details` per-row trước khi gửi — backend overwrite nguyên object.
  - **Segment status**: Vừa aggregate display (derived) VÀ editable ở segment header — khi đổi → bulk update all rows trong segment. Daily rows vẫn giữ per-row status override.
  - **actual_cost / confirmation_no**: Chỉ edit ở daily row level; segment header chỉ summary.
  - **[P1] onBulkUpdateItems contract**: Tất cả bulk ops trong zone/segment/form dùng `onBulkUpdateItems(updates: OpsServiceBulkUpdate[])` — không dùng `onBulkUpdate(ids, singleData)`. Lý do: form cần build per-row updates khác nhau để merge JSONB riêng từng row.
  - **[P1] Reset fields = explicit null**: `buildContactResetFields(flow)` trả object với null values (không phải undefined/omit). `undefined` bị JSON.stringify bỏ qua → reset không có tác dụng. `null` được ghi vào JSONB → backend ghi null đúng.
  - **[P1] Fallback behavior**: `zoneCityMap === undefined` (query loading/error) → flat rows như cũ. `zoneCityMap` loaded + `dayTitles = {}` (empty) → tất cả rows vào zone "Other". Guard bằng `isZoneConfigLoaded = zoneCityMap !== undefined`.
- **[2026-03-16] Track 102d — Smart Hotel Stay Blocks**:
  - Stay block grouping vẫn là **frontend-only**, vì `OpsService` hiện tại là `1 row = 1 day/service item`; không đổi sang model `start_day/end_day`.
  - Split hotel block **không create/delete row**. V1 dùng `bulk-update` trên các rows sau `split_after_day`, reset thành block mới với placeholder `service_name = "TBD Hotel"` + `hotel_id = null`.
  - Merge hotel block **không có API/nút riêng** trong v1. Khi 2 block liên tiếp cùng grouping key (`hotel_id` ưu tiên, fallback `service_name`), UI sẽ tự regroup và merge.
  - Date logic chốt theo code thực tế: `Day 1-3 => 3N`, công thức là `nights = last_day - first_day + 1`, `check_in = getDayDate(departure, first_day)`, `check_out = getDayDate(departure, last_day + 1)`. *(Fix 2026-03-18: align đúng 3N theo code thực tế.)*
  - Convert flow hotel chỉ best-effort trace `hotel_id` qua `QuoteItem.source_type == "hotel_contract"` + `source_id`; **không** trace qua `service_rate_id`, vì `quote_templates` hiện không có quan hệ trực tiếp tới `contracts`.
  - **Optimistic Updates**: Áp dụng cho cả single và bulk update trên Ops Board qua `onMutate` của TanStack Query, đảm bảo trải nghiệm 0ms latency ngay cả khi xử lý các chuỗi khách sạn dài ngày.
  - **Backend Eager Loading Requirement**: Sau các lệnh update `ops_services`, backend bắt buộc dùng `selectinload(OpsService.hotel)` khi re-query để trả về full payload cho frontend, tránh lỗi async lazy-load (`MissingGreenlet`).
- **[2026-03-16] Track 102 — Booking Module Architecture**:
  - OpsService reuse `ItemCategory` enum (15 loại) từ QuoteItem thay vì simplified 5-type enum trong PRD → giữ nguyên granularity khi clone, không mất thông tin.
  - `confirmation_details` dùng **JSONB polymorphic** thay vì nhiều nullable columns → mỗi service_type có schema riêng (Hotel: room_type/check-in/out/contact, Guide: name/phone, Transport: driver/vehicle). Dễ mở rộng khi Module 6 (Supplier DB) xong.
  - OpportunityStatus cần thêm `WON` (hiện thiếu). ALTER TYPE enum trong PostgreSQL không thể rollback `ADD VALUE`.
  - Booking ID sequence: `<LANG>-YYYY-<SEQ>` (e.g. FR-2026-0001) dùng `SELECT ... FOR UPDATE` để tránh race condition.
- **[2026-03-09] Track 100 — Hotkey System Standard**:
  - Toàn bộ hotkey navigation chuyển sang `Alt+số` (Alt+1..9 theo thứ tự sidebar) để tránh conflict Chrome browser (Ctrl+letter) và Unikey Vietnamese input (Ctrl+Shift+...).
  - Giữ `Ctrl+K` (command palette chuẩn web) và `Ctrl+/` (toggle sidebar).
  - Thay `Ctrl+Shift+/` (shortcuts help) bằng `Alt+/`. Sub-items Hotels dùng `Alt+Shift+letter`.
  - Sidebar order chốt: Dashboard → Tasks → CRM → Sales → Itineraries → Hotels & Contracts → Bookings → Finance → Settings.
- **[2026-03-07] Master Brainstorm Operations**:
  - Hệ thống Điều hành tách biệt ra 7 phân hệ quản lý độc lập. Các nhân sự Operations thao tác dựa trên hệ lưới `actual_cost` và `supplier`. Vactours cấm sửa giá/code qua lưới chéo `sales_price` của đội báo giá. 
  - Workflow gửi Mail Tự động Booking cho NCC được quy hoạch thành Template bấm nút "Copy/Mailto" local bằng client có sẵn, tôn trọng custom edit của nhân sự Operations thay vì xây dựng Notification/Automation Server Auto-Mail (gây khó quản lý Reply và Spam filter).
- **[2026-03-06] Product Methodology Shift**: 
  - Chuyển từ thói quen "Cứ code build dần trên Live" sang AGM Standard 7-Phases Workflow (Shift-Left PRD/Plan Review) giúp chặn lỗi cấu trúc từ sớm, đạt mục tiêu Zero-Loop với AI Agent.
- **[2026-03-04] Day Library Extraction Pivot**: 
  - Chuyển đổi định hướng tính năng "Import Excel Hành trình" thô/nguềnh ngoàng thành "AI Normalize Pipeline" (Track 090a, 090b). Chấp nhận sự kiện AI LLM cleaning text mất 10-15s trên Backend thay vì import raw data vào phá UI. Quá trình Import sẽ đọc DB tree trực tiếp từ file JSON lưu trữ.
- **[2026-02-11] UI Task Unification**: 
  - Gộp List Task và Calendar Tracker Task vào 1 Menu `/tasks`. Cấp 1 hệ thống Sidebar Widget (Global Sheet) cho tác vụ gán nhắc nhở nhanh trực tiếp trên ngữ cảnh các màn hình chi tiết Deals/Itineraries mà không cần đổi Tab dài.
- **[2026-02-10] WebSocket Replacement**: 
  - Thay thế hoàn toàn cơ chế Polling HTTP GET 30s của Comments/Tasks Box bằng cơ chế WebSocket tiêu chuẩn. Tránh crash Router Socket/TCP connections limit do ngốn tài nguyên vô ích của Client.
- **[2026-02-10] Itinerary/Opportunity Auto-Linking Polymorphic**:
  - Liên kết Comment và Task theo dạng Polymorphic Type (`entity_type`, `entity_id`). Khi Itinerary thuộc một Opportunity deal cấp cha, toàn bộ feed Tasks Timeline sẽ tự loop inject gộp ID cha/con để lấy bức tranh Activity Overview tổng thể, thay vì user lật 2 tab hồ sơ riêng biệt.
- **[2026-02-04] User Department Paradigm Change**: 
  - Thiết kế System role phân tách, vứt bỏ kiểu Admin/Member cũ, chuyển dọc trục xoay sang hệ Model Role-Based Access Control từ Level Department (Permissions quyền truy xuất gắn cứng với level Phòng Ban/Team). 
  - Primary Assignment gán role user một cách linh hoạt, dễ scale. Xóa bỏ bảng Enum type tĩnh `department` qua tables.
- **[2026-01-29] Hotel & Inventory AI OCR Flow**:
  - Không auto-tạo dữ liệu Hotel/Room rác lộn xộn mỗi khi LLM chạy OCR bóc băng các file hợp đồng PDF. 
  - Đưa vào 1 process tuyến tính: Phải tạo Master Hotel Framework Data tay => Kế tiếp OCR Contract chạy Map room tên/chủng loại vào. 
  - Track mapping lỗi/fail/null giữ cấu trúc Fallback AI lưu JSON vào column `extracted_data` thô thay vì ép force insert vào bảng SQL Prices báo giá sai lệch.
- **[2026-01-28] Architectural Split Environment**:
  - Hệ thống DB PosgresSQL, Worker AI, FastAPI lên Railway Cloud.
  - Phân vùng Client UI/UX Node.js lên Vercel Edge Cache.
  - Chốt luồng phát triển logic phân hệ doanh nghiệp 4 Lớp Core: **CRM** (Hồ sơ contact đối tác/khách hàng tĩnh) -> **Sales** (Xử lý Deal/Sinh Báo giá chốt Sales) -> **Operations** (Triển khai dịch vụ thực tế/Task điều hành) -> **Supplier** (Cung ứng data/Kho dữ liệu Master của hệ thống). Cấm các code logic controller nhập nhằng vượt biên giới/scope tính năng.
- **[P1][2026-03-20] Track 102j â€” Booking Discussion Sidebar architecture**:
  - **Bai toan**: Can gom discussion cua `booking` va toan bo `change_request` vao 1 sidebar, nhung server WS co `_JOIN_ROOM_RATE_LIMIT = 10` va `CommentList` hien mang behavior chat-stream.
  - **Giai phap chot**:
    - Backend them entity `booking`, aggregated endpoint `GET /discussions/bookings/{booking_id}/aggregated`
    - Permission HTTP va WS room access cung bam `_can_view_booking`
    - Backend bridge CR comment events toi `booking:{booking_id}` room -> frontend join 1 room duy nhat
    - `all` tab la read-only aggregated timeline; specific tabs (`booking`, `change_request:{id}`) reuse `DiscussionFeed`
    - Pagination aggregated dung local accumulated list + dedupe theo `comment.id`, reset theo context/filter
  - **Design constraints**:
    - `all` tab tuyet doi khong render editor/reply/actions
    - Shared UI chi sua toi thieu, generic (`composerPlaceholder`, badge support, auto-scroll opt-out)
    - Realtime payload create nen chua attachments; neu khong du thi frontend phai invalidate/refetch

- **[P1][2026-03-27] Track 114 — buildMergeUpdates phải exclude *_notes khi merge segments**:
  - **Vấn đề**: Copy-all `confirmation_details` từ first segment sang second segment khi merge sẽ overwrite `guide_notes`/`transport_notes` do ops nhập tay riêng cho segment 2 — **data loss**.
  - **Fix**: Dùng `buildMergeContactFields(serviceType, firstDetails)` helper — chỉ pick supplier-synced fields theo service type. Guide: `guide_name/phone/email/language/poc_name/guide_id_number/guide_license_number`. Transport: `company_name/poc_name/company_phone/company_email`. Train: `provider_name/poc_name/poc_phone`. Meal: thêm `provider_phone/email/address`. Default: `provider_name/poc_name/phone/email`.
  - **Áp dụng khi**: Bất kỳ track nào thêm field mới vào sync → nhớ update `buildMergeContactFields` picker list.

- **[P1][2026-03-27] Track 114 — Split UX: bỏ auto-reset, dùng post-split AlertDialog**:
  - **Cũ**: `buildSplitUpdates(segment, breakpointDay, flow)` tự động reset contact fields của segment mới via `buildContactResetFields(flow)` — không hỏi user.
  - **Mới**: `buildSplitUpdates` chỉ set `assignment_group` mới cho half-second. Sau split: show `AlertDialog` → user chọn "Giữ supplier hiện tại" hoặc "Reset — gán supplier mới".
  - **Reset handler**: Chỉ send `resetFields` thuần — **KHÔNG spread stale `svc.confirmation_details`**. API là PATCH/merge, backend tự merge JSONB. Spread stale sẽ clobber `assignment_group` vừa được set bởi split.
  - **Áp dụng khi**: Bất kỳ post-mutation dialog nào cần update confirmation_details → check xem data đã stale chưa trước khi spread.

- **[P1][2026-03-27] Track 114 — Hotel sync qua hotel_id (khác Supplier sync)**:
  - **Cơ chế**: Hotel không dùng `supplier_id` — dùng `hotel_id` riêng. Khi link hotel segment, `handleSegmentLinkHotel` (OpsServiceTable.tsx) gọi `buildHotelSyncFields(hotel)`.
  - **Mapping**: `hotel.contact_person → poc_name`, `hotel.phone → contact_phone`, `hotel.email → contact_email` trong `HotelConfirmation`.
  - **Không có unsync**: Không có "unlink hotel" flow trong UI → KHÔNG tạo `buildHotelUnsyncFields` (dead code).
  - **Áp dụng khi**: Bất kỳ track nào sync hotel contact info → dùng `buildHotelSyncFields`, không tạo logic riêng.

- **[P1][2026-03-26] Track 111d — Snapshot Principle & Manual Migration**:
  - **Snapshot Principle**: Các trường thông tin từ Supplier Master (name, phone, email) khi link vào booking sẽ được lưu thành bản sao (snapshot) trong `confirmation_details`. Mục đích: Đảm bảo dữ liệu booking không bị thay đổi nếu Supplier Master cập nhật sau này, phục vụ in ấn và vận hành chính xác.
  - **Manual Migration**: Alembic `--autogenerate` không phát hiện thay đổi trong SQL `CheckConstraint`. Khi thêm type `train` vào `ck_suppliers_type`, phải viết tay logic `DROP CONSTRAINT` và `ADD CONSTRAINT` mới trong file migration.
  - **UI Standard**: Dịch vụ `train` sử dụng icon `Train` và màu `violet-600` để phân biệt hoàn toàn với `transport` (blue).