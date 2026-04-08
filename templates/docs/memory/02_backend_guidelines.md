# Backend Guidelines & Architecture

> Chỉ chứa P0/P1 patterns còn actively relevant. WeasyPrint/PDF details → `pdf-generation` skill. Architecture decisions đã implement → git history.

---

## SQLAlchemy & Async

### [P0] MissingGreenlet — Eager Loading bắt buộc (merged)
**L1 — Critical Facts:** Async SQLAlchemy không hỗ trợ lazy load. Mọi relation cần trong response PHẢI được `selectinload`/`joinedload` trong query, không phải sau `db.refresh()`.
**L2 — Context:** Pattern đúng cho nested: `.options(selectinload(Model.items).joinedload(Item.owner))`. Sau Create/Update phải re-query với options đầy đủ thay vì dùng object vừa commit. Tree structures: query flat, build tree bằng Python — không iterate children trong async context.
**L3 — References:** `app/services/pdf_service.py:38` (pattern mẫu với selectinload chain)

### [P1] SQLAlchemy Ambiguous Foreign Keys
**L1 — Critical Facts:** Khi Model có ≥2 relations trỏ về cùng 1 bảng (ví dụ `created_by` và `locked_by_id` cùng trỏ `User`), phải khai báo `foreign_keys=[ColumnName]` tường minh trong `relationship()`.
**L2 — Context:** Track 014a: Quote model gặp lỗi này với `created_by` + `locked_by_id`.

### [P1] Boolean Column Nullable Default
**L1 — Critical Facts:** Column `Boolean` thêm vào bảng có dữ liệu sẽ là `NULL` cho rows cũ. Schema phải dùng `Optional[bool] = False`.

### [P1] SQLAlchemy Registry cho Independent Scripts
**L1 — Critical Facts:** Scripts độc lập (`create_admin.py`, migration scripts) phải `import` tường minh model cha trước khi dùng relationship. Thiếu → `KeyError: 'ModelName'` hoặc `InvalidRequestError`.

### [P1] Enum Single Source of Truth
**L1 — Critical Facts:** Enum (`ItemCategory`, `RoomType`, `QuoteStatus`...) chỉ define 1 nơi duy nhất trong models. Schemas import từ models — không redefine.

### [P1] COUNT Query thay vì Load All
**L1 — Critical Facts:** Kiểm tra số lượng records dùng `select(func.count()).select_from(Model).where(...)`, không phải `len(result.scalars().all())`.

---

## FastAPI & Pydantic

### [P0] FastAPI response_model + @computed_field
**L1 — Critical Facts:** `@computed_field` chỉ được gọi khi router có `response_model=Schema`. Thiếu `response_model` → `@computed_field` bị bỏ qua hoàn toàn (không raise error, trả về `None`).
**L2 — Context:** Áp dụng cho `url`, `avatar_url` trên MediaResponse. Pattern: luôn đặt `response_model` explicit trên mọi endpoint trả về object.

### [P0] Pydantic V2 — ConfigDict
**L1 — Critical Facts:** Pydantic V2 bắt buộc dùng `model_config = ConfigDict(from_attributes=True)`. Class syntax cũ `class Config: from_attributes = True` không hoạt động → `Unable to serialize unknown type`.

### [P0] FastAPI 204 No Content
**L1 — Critical Facts:** Endpoint `status_code=204` không được có return type annotation (`-> None`, `-> Any`) và không có `return` statement. Bất kỳ type hint nào → `AssertionError: Status code 204 must not have a response body` khi start server.

### [P1] Pydantic Schema Integrity — bộ ba
**L1 — Critical Facts:** Khi thêm field vào Model, phải cập nhật đồng thời cả 3: `CreateSchema`, `UpdateSchema`, `ResponseSchema`. Thiếu `UpdateSchema` → "Silent Drop" (Frontend gửi nhưng Backend không lưu).

### [P1] Timezone Serializing
**L1 — Critical Facts:** Pydantic serialize datetime không có timezone suffix → browser coi là local time → sai 7 tiếng (GMT+7). Phải dùng `@field_serializer` force format `dt.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'`.

### [P1] Trailing Slash — redirect_slashes=False
**L1 — Critical Facts:** `redirect_slashes=False` trong `main.py`. Endpoint List/Create dùng `@router.get("")` (không có slash). Router prefix trong `__init__.py` dùng hyphen `-` không phải underscore `_`.
**L2 — Context:** CORS error giả: khi Frontend thấy CORS error nhưng OPTIONS pass → thực ra là Backend crash (IntegrityError, NameError). Đọc Uvicorn log thay vì debug frontend.

### [P1] boto3 Sync trong Async Context
**L1 — Critical Facts:** Mọi boto3 method (upload, delete, presign) là synchronous. Trong FastAPI async handler phải wrap: `await asyncio.to_thread(self.storage.method, args)`. Gọi trực tiếp block event loop.

### [P1] db.bind.url Deprecated
**L1 — Critical Facts:** `Session.bind` removed trong SQLAlchemy 2.x. Dùng `str(settings.DATABASE_URL)` thay thế khi cần connection string cho background tasks.

### [P1] FastAPI Auth Dependency Path
**L1 — Critical Facts:** `get_current_user` nằm ở `app.api.v1.auth`, không phải `app.api.deps`. Import sai → `ModuleNotFoundError` khi start.

---

## Booking Module Specifics

### [P1] convert_to_booking — 2 code paths
**L1 — Critical Facts:** `booking_service.convert_to_booking` xử lý `land_package` (~line 309) và normal items (~line 350) trong 2 branch riêng biệt. Field mới mapping từ QuoteItem PHẢI thêm vào CẢ 2 branch.

### [P1] Booking — departure_date field
**L1 — Critical Facts:** `Itinerary` không có field `departure_date`. Phải hydrate từ `Quote.itinerary.start_date`. Dùng sai tên field → crash toàn bộ list/detail/convert.

### [P1] Booking — Full Access check
**L1 — Critical Facts:** Full access check phải duyệt ALL `department_memberships`, không chỉ `user.role`. User có bất kỳ membership nào với `code in ('it', 'bod')` → full access.

### [P1] Booking — ops_progress computed
**L1 — Critical Facts:** `ops_progress` trong `BookingListItem` phải được compute từ `ops_services` đã eager-load. Không được khai báo là required field mà không populate → Pydantic fail validation.

---

## Patterns & Architecture

### [P1] SARGable Monthly Filter
**L1 — Critical Facts:** Không dùng `extract('month', col)` — ngăn index. Dùng range query: `>= start_date AND <= end_date` với `calendar.monthrange` tính biên.
**L2 — Context:** Nếu filter theo field của bảng khác (như `itinerary.start_date` cho Booking), phải `join()` tường minh trước `where()` — `selectinload` không filter được qua SQL.

### [P1] Batch Query Pattern (N+1 prevention)
**L1 — Critical Facts:** Khi có vòng lặp N items, mỗi iteration query DB → pre-load toàn bộ data trước vòng lặp, resolve bằng dict lookup in-memory. Bulk insert dùng `db.add_all()`.
**L3 — References:** Track 076: `auto_populate_quote()` từ 84+ queries → ~7 queries.

### [P1] Contextual Filtering trong List APIs
**L1 — Critical Facts:** List API của entity con (Invoices, OpsServices) phải có tham số lọc theo parent ID (`opportunity_id`, `booking_id`). Filter trực tiếp trong SQL: `stmt.where(Model.parent_id == parent_id)`.

### [P1] Backend Schema Completeness
**L1 — Critical Facts:** Thiếu relation object trong ResponseSchema (chỉ có ID) → Frontend filter logic `.id` bị fail thầm lặng. Luôn kết hợp `joinedload` với Schema đầy đủ.

### [P1] Vietnamese Accent-Insensitive Search
**L1 — Critical Facts:** Không dùng `func.unaccent()` (cần extension). Dùng `func.translate(col, VN_FROM, VN_TO)` kết hợp `func.lower()` + `.ilike()`. Python-side normalize search term trước.

### [P1] Backend Migration Blocker
**L1 — Critical Facts:** `UndefinedColumnError` trên Railway thường do quên commit file `.py` mới trong `alembic/versions/`. Luôn `git status` sau `alembic revision`.

### [P1] Alembic Migration Conflict
**L1 — Critical Facts:** Xóa file migration nhưng DB còn revision ID cũ → `Can't locate revision`. Fix: script asyncpg update trực tiếp bảng `alembic_version` về revision hợp lệ.

### [P1] Polymorphic Audit Log
**L1 — Critical Facts:** Bảng `audit_logs` dùng `entity_type` (String) + `entity_id` (Integer) thay vì FK cụ thể. 2 response schemas: `AuditLogSummaryResponse` (Sales) và `AuditLogResponse` (Manager+).

### [P1] Bidirectional Sync Loop Prevention
**L1 — Critical Facts:** Sync 2 chiều (Opportunity ↔ Itinerary) PHẢI dùng flag `_skip_sync` truyền qua hàm service để ngăn infinite loop.

### [P1] Quote Lock — Computed via Pydantic
**L1 — Critical Facts:** `is_locked` tính động trong Schema dựa trên `locked_at + 30min vs datetime.utcnow()`. Không dùng background job. BOD/IT có quyền force unlock bất kỳ lúc.

### [P1] @computed_field cho URL hydration
**L1 — Critical Facts:** URL (presigned R2, avatar) phải dùng `@computed_field @property` trong Schema, không phải regular field `Optional[str] = None`. Regular field không có code populate → luôn `None`.
**L2 — Context:** Kết hợp với `contextvars.ContextVar` để lưu DB session. Yêu cầu `response_model` trên router (xem rule trên).

### [P1] Media Object Key — không bao gồm bucket name
**L1 — Critical Facts:** `object_key` trong DB lưu dạng sạch (`uploads/2026/02/...`), không có tên bucket. boto3 tự thêm bucket → nếu DB có bucket prefix sẽ bị duplicate path → R2 404 `NoSuchKey`.
