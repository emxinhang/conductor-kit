# Tech Decisions Log

> Lịch sử quyết định kiến trúc quan trọng

## Core Architecture
- **Platform App**: Expo React Native — APK Android, không cần App Store
- **AI/RAG**: Python + Gemini API (không OpenAI, không Vertex)
- **Vector DB**: PostgreSQL + pgvector trên Railway (thay ChromaDB — cần structured + vector search kết hợp)
- **Trường phái**: Vương Hổ Ứng — gần đời sống, có kho ebook 9 files
- **Loại trừ**: Bát Tự, Tử Vi, Mai Hoa Dịch Số (khác phương pháp)

## OCR Pipeline
- **V4 "Mắt AI - Não Code"**: AI extract → Engine tính → 87.5% score pilot
- **V5 Golden Prompt**: Merge V4 + backup, Visual Layout Rules, edge cases null/[]
- **Tooling per format**: Scan=Gemini, DOCX=python-docx, Text=pdfplumber
- **reverse_hao_dong = PRIMARY**: AI đọc tên 2 quẻ (chính xác) → Engine diff → ra hao_dong 100%.
- **Lỗi nhận diện quẻ**: Chú ý các quẻ có tên gần giống hoặc lỗi chính tả (đã fix qua normalizer).
- **Bấm nút Full Batch file 1** (2026-03-14): Chốt strategy "Mắt AI - Não Code" sau Pilot 40 trang thành công 100% nhờ Engine sửa lỗi hào động nhầm lẫn từ text/Thế Ứng.

## Data Architecture
- `hexagram_standard_v1.json` = Single Source of Truth (OCR + Engine + App)
- Engine = Dual-purpose: OCR reconstruct + App gieo quẻ (xây 1 lần, dùng 2 nơi)
- Engine move sang `engine/`, re-export tại `scripts/backend/` — 1 nguồn duy nhất

## Track Decisions
- Track 005b split → 5 sub-tracks (005b-1 đến 005b-5) để implement dần
- Track 006 (DB) và 007 (Embedding) tách riêng, sau khi dữ liệu thô xong
- Track 008: Xử lý Large Batch PDF. Đã quét hoàn tất toàn bộ 4 file: `du-trac-hoc`, `hoa-giai-tam-phap`, `kinh-te`, và `phong-thuy` (Tổng cộng ~1400 trang). Tất cả đều đạt tỷ lệ trích xuất 100% (không lỗi `failed`, không `skipped`) nhờ quy chuẩn Pilot 40 trang -> Audit -> Full Batch. Thuật toán `reverse_hao_dong` đã chứng minh hiệu quả tuyệt đối khi tự động sửa hàng trăm lỗi vị trí hào động từ AI nhìn sai layout. Toàn bộ dữ liệu PDF Scan thô đã sẵn sàng để chuyển sang giai đoạn Validation (Track 005b-5).
- Track 009: Quyết định siết kỷ luật đặt tên của AI bằng Text Rule (Golden Prompt v6) THAY VÌ dùng Fuzzy Matching để đảm bảo không map nhầm. Mở rộng Tool Audit để dò 1 chạm các file bị ngoại lệ `failed`. Kết quả: Áp dụng v6 và Engine Hardening đã đưa tỷ lệ lỗi của file `du-trac-hoc` về 0 (Pass 100%).
- Track 005b-5 (Validation): **Skipped** — Track 008 đạt 100% audit, ATu confirmed không cần validation report riêng.

## Embedding (2026-03-14)
- **Model**: `gemini-embedding-2-preview` (thay `gemini-embedding-001` và `text-embedding-004`)
- **Dimensions**: 768 (MRL configurable 128-3072, chọn 768 vì data ~2400 units nhỏ, tiết kiệm storage)
- **Input limit**: 8192 tokens (gấp 4x model cũ)
- **Multimodal**: text, image, video, audio, PDF
- **Task types**: `RETRIEVAL_DOCUMENT` (indexing), `RETRIEVAL_QUERY` (search)

## Database Schema (2026-03-14)
- 4 tables: `books`, `pages` (raw audit), `hexagrams` (structured), `text_chunks` (+ vector(768))
- Dedup Lớp 1: SHA-256 hash, merge `sources[]` — làm trong seed script
- Dedup Lớp 2: Semantic cosine > 0.95 — chờ Track 007 có embeddings
- Migration: Alembic. Seed: Python script riêng (tách DDL vs DML)

## Track 010 — Module Hà Lạc Lý Số (2026-03-14)
- **Platform**: Web first (React 19 Vite → Vercel). Mobile app (SaaS/PWA) sau monetize.
- **Lịch Vạn Niên**: Pure Python math (Jean Meeus / Hồ Ngọc Đức) — không dependency ngoài.
- **Embedding không cần cho MVP**: Luận giải sách = exact match (query theo quẻ + hào). Embedding chỉ cần cho 010f (AI luận giải, P1).
- **Engine reuse**: `engine/hexagram_engine.py` (64 quẻ) tái sử dụng cho Hà Lạc. Thêm `calendar_engine.py` + `ha_lac_engine.py`.
- **Monetize direction**: Free (quẻ cơ bản + luận giải giới hạn) vs Premium (Đại Vận/Lưu Niên + AI cá nhân hóa + lưu lá số). Chưa implement gate.
- **Nguồn tri thức**: "Bát Tự Hà Lạc" — Học Năng, 267 trang. Phần I: lý thuyết tính toán. Phần II: ý nghĩa 64 quẻ theo Hà Lạc giải đoán.

## Track 010a — Review Plan Findings (2026-03-15)
- **sun_longitude phải trả float (0-360°)**: Trả int section mất precision ±7.5° ≈ 7-8 ngày, sai tháng cho người sinh gần boundary Tiết/Khí. Mapping: `int((sun_lon - 315) % 360 / 30)`.
- **TIET_KHI_NAMES bắt đầu từ Lập Xuân**: Index chẵn = Tiết (Bát Tự), lẻ = Khí (Hà Lạc Nguyệt Lệnh). Sách: "Bát tự căn cứ vào Tiết, Hà lạc căn cứ vào Khí" (trang 58).
- **correct_hour_to_gmt7 → tuple[int, int]**: Trả (hour, day_offset) vì correction có thể vượt nửa đêm → ảnh hưởng Can Chi ngày.
- **get_bat_tu + gender → 010b**: CalendarEngine chỉ cung cấp primitives, HaLacEngine xử lý Lập Xuân boundary + gender.
- **Can Chi Month (Ngũ Hổ Độn) — đã verify**: `(can_year_idx * 2 + 2 + mm_lunar - 1) % 10`. Kiểm tra: Giáp→Bính Dần, Ất→Mậu Dần, Bính→Canh Dần, Đinh→Nhâm Dần, Mậu→Giáp Dần ✅

## Track 010a — Code Review (2026-03-15)
- **9 issues found, all fixed**: 3 BUG (Can Chi Month lệch 1, Tết logic fragile, Tiết khí UTC), 3 Medium (Newton 3→10 iter, Delta-T post-2000, dead code), 3 Minor (naming, magic numbers)
- **ATu tự implement + tự fix**: Code quality tốt sau 2 rounds review

## Track 010b — Plan Review (2026-03-15)
- **6 bugs fixed trong plan** (trước khi implement): Thìn→Tốn confirmed, compute_full gọi sai compute_nguyen_khi, _reduce_tong thiếu self., section boundaries Hóa Công sai (<5/<17 → <6/<18), TNK/ĐNK loop chỉ check 2/4 quẻ, duplicate code năm 4-9 Lưu Niên.
- **3 clarifies resolved**: (1) TNK/ĐNK scope = 4 quẻ giống Hóa Công ✅ (2) Nguyên Đường HT = que_bien['the_hao'] từ JSON ✅ (3) get_can_chi_year() nhận lunar year ✅
- **HexagramEngine API verified**: bat_quai_pattern, pattern_to_quai, reconstruct(), compute_que_bien(), get_que_name_from_pattern() — tất cả tồn tại đúng format.
- **get_tiet_khi() order**: idx 0=Đông Chí, 6=Xuân Phân, 12=Hạ Chí, 18=Thu Phân — boundaries Hóa Công dùng <6/<12/<18.
## Session & State Management (2026-03-20)
- **Role-based Session Management**: Tách biệt `session_save_cs.md` (Planner/CS) và `[track]/SESSION.md` (Implementer/AG/CD). Loại bỏ `session_save.md` chung để tránh ghi đè context khi đổi role giữa các phiên làm việc.
- **Conductor State as Source of Truth**: Sử dụng `.agents/conductor/state.md` làm nguồn sự thật duy nhất cho trạng thái track hiện tại (Active/Pipeline/Upcoming), thay vì chỉ dựa vào `tracks.md` tĩnh.
- **Project Memory Sync**: Đồng bộ hóa danh sách Master Tracks trong `docs/project_memory.md` định kỳ với `conductor/tracks.md` để AG luôn có cái nhìn tổng quan chính xác khi `new-conversation`.

## Track 010b-1 — Plan Review Final (2026-03-15 session 3)
- **JD Convention confirmed + fix**: `solar_to_jd()` trả int JD tại **noon UT**. Formula `solar_to_jd() + hour/24.0` sai (lệch 12h). Fix: thêm static helper `solar_hour_to_jd_local(dd, mm, yyyy, hour)` = `solar_to_jd() - 0.5 + hour/24.0`. Dùng nhất quán thay mọi inline formula.
- **gender bỏ khỏi get_bat_tu()**: Gender không ảnh hưởng Bát Tự. Chỉ cần ở `compute_que()` (sắp Thượng/Hạ quái) và 010b-2 (chiều Đại Vận). PRD Bước 1 + spec.md `compute_bat_tu` đã update đồng bộ.
- **can_chi_year_ref trong BatTu**: Thêm field `can_chi_year_ref: int` vào `BatTu` dataclass. Downstream (compute_que, 010b-2) PHẢI dùng `bat_tu.can_chi_year_ref`, KHÔNG tự tính.
- **hour: float (minute-level)**: `hour: int` → `hour: float` toàn bộ signatures (solar_hour_to_jd_local, correct_hour_to_gmt7, get_tiet_khi_for_date, get_bat_tu). `get_can_chi_hour` vẫn dùng `int(corrected_hour)` (canh giờ 2h blocks). MVP input form có thể thu giờ nguyên nhưng engine sẵn sàng nhận 6.783 = 6h47'.
- **Phase 0 có 4 helpers**: get_lap_xuan, correct_hour_to_gmt7, solar_hour_to_jd_local, get_tiet_khi_for_date.
- **Test boundary quan trọng**: (1) UTC+12 → day_offset=-1. (2) 5/2/2026 lúc 6.783 → section 3 (Lập Xuân, tháng 1 Dần).

## Track 010b — Sub-track Split + Plan Fix (2026-03-15 session 2)
- **Split xong**: `conductor/tracks/010b-1/IMPLEMENTATION_PLAN.md`, `010b-2/IMPLEMENTATION_PLAN.md`, `010b-3/IMPLEMENTATION_PLAN.md`
- **5 bugs fixed trong plan 010b-1** (từ refactoring-expert review):
  - **Critical 1**: `get_tiet_khi_for_date` thiếu `hour` — so sánh boundary Tiết chỉ theo ngày, sai case sinh đúng ngày đổi Tiết. Fix: thêm `hour: int`, dùng `jd + hour/24.0`.
  - **Critical 2**: `lunar.year - 1` khi < Lập Xuân sai — sinh 20/1/2026 → lunar.year=2025 → 2024=Giáp Thìn ❌. Fix: dùng `can_chi_year_ref = adj_yyyy if birth >= lap_xuan else adj_yyyy - 1`, dùng nhất quán cho year_cc/month_cc/resolve_five/compute_que.
  - **Important formula**: `((section//2)+11)%12` sai — section 3 → 0 → 12 (Sửu) thay vì 1 (Dần). Fix: dùng lookup table `SECTION_TO_LUNAR_MONTH[24]`.
  - **Important timezone**: `timezone_offset=0` mơ hồ. Fix: đổi thành `utc_offset: int = 7`, formula `hour + 7 - utc_offset`.
  - **Minor scope**: dataclass 010b-2/3 trong plan 010b-1 đánh dấu "declare-only, implement 010b-2".
- **Pending — chưa resolve**: JD convention có thể lệch nửa ngày. `solar_to_jd()` trả int (0h UT), TietKhi.jd là float (UT). Code dùng `int(jd_local + 0.5)` để convert về civil date. Khi so sánh `birth_jd_full = solar_to_jd() + hour/24.0` với `tiet.jd + TIMEZONE/24.0` — cần verify có cùng epoch (Julian Day starts at noon UT) không, hay cần thêm `+ 0.5` offset. **Review kỹ trước khi implement.**

## Project Structure (2026-03-14)
- **Decision**: Tách folder `backend/` chứa models và migrations độc lập.
- **Context**: Tránh lẫn lộn dependencies giữa Data Pipeline (Python) và API server sau này, đồng thời chuẩn bị cấu trúc Mono-repo cho Frontend.

## Track 010b-1 — Core Logic Implementation (2026-03-15)
- **Quy tắc lập quẻ Tiên Thiên**: Cố định **Dương sinh quẻ Hạ (Nội), Âm sinh quẻ Thượng (Ngoại)** (Sách trang 22). Loại bỏ logic đảo quẻ theo Nam/Nữ ở bước này (chỉ dùng cho Đại Vận).
- **Trụ Ngày Bát Tự**: Đã xác minh ngày 04/02/2026 là ngày **Mậu Tý** (Lịch chuẩn), không phải Kỷ Hợi. Toàn bộ logic Can Chi ngày của `CalendarEngine` đã vượt qua đợt "giải phẫu" JDN.
- **JD Boundary Fix**: Sử dụng `solar_hour_to_jd_local` kết hợp với `TIMEZONE/24.0` để đồng bộ hoàn toàn giữa thời điểm sinh (Local) và thời điểm Tiết khí (UTC).
- **Luật Tam Nguyên số 5**: Refactor bảng lookup thành `(period, is_positive_flow)`. Trong đó `is_positive_flow = (is_male == is_duong_can_year)`.
- **Can Chi Tháng**: Chốt dùng `SECTION_TO_LUNAR_MONTH` để map Section Index (0-23) sang tháng (1-12) thay cho công thức toán học bị lệch boundary tại một số điểm.