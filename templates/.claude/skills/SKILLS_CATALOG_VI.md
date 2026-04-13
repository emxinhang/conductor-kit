# Danh Mục Skills - TMS-2026

Catalog các skills được tối ưu hóa cho dự án TMS-2026 (React 19 + FastAPI + PostgreSQL).

---

## 🚀 Core Project Management

### conductor
Quản lý task theo quy trình Conductor - theo dõi tiến độ tracks, cập nhật status, và duy trì documentation.

### module-workflow
Hướng dẫn quy trình xây dựng module từ Requirements đến QA - tự động tạo track structure, templates, validate mỗi phase.

### planner-track
Lập kế hoạch triển khai (Implementation Plan) theo chuẩn technical-writer dựa trên spec.md hoặc PRD đã có.

### red-team-reviewer
Đóng vai Senior Principal Engineer "Red Team" — nhận IMPLEMENTATION_PLAN + Codex codebase context, phản biện gay gắt Plan theo 4 lăng kính (Reinvent Wheel / State Race / Defense-in-Depth / Future-Proof), xuất Plan tối ưu. Chạy sau /planner-track, trước /review-plan.

### handoff
Chuyển giao từ Giai đoạn 1 (Plan) sang Giai đoạn 2 (Execution) — AG tiếp quản từ Claude/Codex, đọc plan, kiểm tra codebase state, thực thi từng task theo Zero-Loop V3 với Task Bundle context isolation. Gọi khi Plan final đã được ATu approve.

### new-conversation
Khởi động phiên làm việc mới, nạp context từ Project Memory và kiểm tra tiến độ dự án.

### update-knowledge
Tổng kết phiên làm việc, lưu kiến thức vào Project Memory và chuẩn bị cho phiên tiếp theo.

---

## 🎨 Frontend (React 19 + Vite)

### frontend-standard-v1
TMS-2026 Frontend Standard - quy chuẩn và quy trình xây dựng tính năng Frontend (Module-based). Dùng khi bắt đầu module mới, thêm trang List/Detail, hoặc tích hợp API từ backend.

### frontend-development
Guidelines cho React/TypeScript - Suspense, lazy loading, useSuspenseQuery, file organization, MUI v7 styling, TanStack Router, performance optimization, TypeScript best practices.

### frontend-design
Tạo UI components đẹp, production-grade với design quality cao - tránh generic AI aesthetics.

### frontend-architect
Thiết kế UI accessible, performant với focus trên UX, responsive design, component architecture.

### frontend-qa-gatekeeper
Enforce Frontend UI/UX standards, TypeScript integrity, Automated QA cho React application trước khi Done.

### shadcn-ui
Xây dựng UI components đẹp và accessible với Radix UI + Tailwind CSS - design systems cho React.

### tailwindcss
Styling ứng dụng với utility-first CSS framework - responsive design, dark mode, custom themes, design systems.

---

## 🔌 Backend (FastAPI + PostgreSQL)

### backend-development
Xây dựng backend robust với NestJS, FastAPI - databases (PostgreSQL, MongoDB, Redis), APIs (REST, GraphQL), authentication (OAuth 2.1, JWT), testing, security (OWASP), performance optimization.

### backend-architect
Thiết kế backend reliable với focus data integrity, security, fault tolerance. API development, database design, security implementation.

### zero-loop-dev
Enforce "Zero-Loop" development workflow với automated backend scaffolding và mandatory integrity checks. Dùng khi tạo backend entities hoặc trước khi "Backend Done".

### postgresql-psql
Làm việc với PostgreSQL qua psql terminal - execute queries, manage databases/tables, transactions, scripting, database administration.

### cloudflare-r2
Triển khai object storage tương thích S3 không phí egress - upload/download files, migration, cấu hình buckets, tích hợp Workers.

---

## 🐛 Debugging & Quality Assurance

### debugging-systematic-debugging
Debug theo framework 4 giai đoạn - điều tra nguyên nhân gốc trước khi fix. Dùng khi gặp bug, test failure, unexpected behavior.

### debugging-verification-before-completion
Chạy lệnh kiểm tra và xác nhận output trước khi kết luận thành công. Dùng trước khi commit hoặc create PRs.

### debugging-defense-in-depth
Validate dữ liệu ở mọi layer nhằm ngăn chặn bugs từ gốc.

### debugging-root-cause-tracing
Truy vết bug ngược qua call stack và tìm nguyên nhân gốc rễ.

### code-review
Tiếp nhận code review feedback, request reviews, verification gates trước khi completion claims.

### qa-verify-expert
Audit Data Integrity, API Contracts, Automated QA để đảm bảo maximum reliability trước khi Done.

---

## 🧠 Problem Solving

### when-stuck
Dispatch đến kỹ thuật giải quyết vấn đề phù hợp dựa trên cách bạn bị stuck.

### collision-zone-thinking
Kết hợp các concepts không liên quan và khám phá emergent properties - 'What if we treated X like Y?'

### inversion-exercise
Đảo ngược assumptions và tìm hidden constraints - 'what if the opposite were true?'

### meta-pattern-recognition
Nhận diện patterns xuất hiện ở 3+ domains và tìm universal principles.

### scale-game
Test ở extremes (1000x bigger/smaller, instant/year-long) và expose fundamental truths ẩn ở normal scales.

### simplification-cascades
Tìm one insight loại bỏ multiple components - 'if this is true, we don't need X, Y, or Z'.

---

## 📋 Refactoring & Architecture

### refactor-workflow
Hướng dẫn refactoring systematic - từ Root Cause Analysis đến implementation. Đảm bảo incremental improvements và backward compatibility.

### refactoring-expert
Cải thiện code quality và reduce technical debt - complexity reduction, SOLID principles, clean code.

### system-architect
Thiết kế scalable system architecture - architecture design, scalability analysis, technology selection.

---

## 📚 Documentation & Research

### technical-writer
Tạo documentation rõ ràng, comprehensive - API docs, user guides, tutorials.

### requirements-analyst
Transform ambiguous project ideas thành specifications - PRD creation, stakeholder analysis, scope definition.

### docs-seeker
Tìm kiếm documentation kỹ thuật qua llms.txt standard, GitHub repositories qua Repomix, parallel exploration.

### tech-stack-researcher
Research và recommend technology choices - planning features, comparing technologies, architecture decisions.

### repomix
Pack entire repositories thành single AI-friendly files - codebase analysis, LLM context, snapshots, security audits.

### brainstorm-track
Brainstorm feature mới và tạo PRD theo chuẩn technical-writer - requirements analysis, solution design cho track mới.

---

## 🔐 Security & Performance

### security-engineer
Identify security vulnerabilities, compliance checking - vulnerability assessment, threat modeling, compliance verification.

### performance-engineer
Optimize system performance - speed optimization, load times, resource usage, Core Web Vitals.

---

## 🛠️ Development Tools

### mcp-builder
Tạo MCP (Model Context Protocol) servers chất lượng cao - tích hợp external APIs/services với Python (FastMCP) hoặc TypeScript (MCP SDK).

### skill-creator
Tạo skills mới cho Claude Code - framework để develop custom skills.

### claude-code
Tìm hiểu complete feature guide của Claude Code - tất cả tính năng và cách sử dụng hiệu quả.

---

## 📖 Learning & Support

### learning-guide
Dạy programming concepts và explain code - tutorials, concept explanations, learning paths.

---

## 👤 ATu-specific Skills

### atu-compact
Custom skill cho compact mode ATu.

### atu-hub-components
Custom skill cho ATu hub components.

### atu-react-component
Custom skill cho ATu React component development.

### atu-summary-status
Custom skill cho ATu summary status display.

### atu-typo-standard
Custom skill cho ATu typo standard.

---

## 📊 Tổng kết

- **Tổng số skills:** 53 (sau khi optimize)
- **Cập nhật:** 2026-03-03
- **Scope:** React 19 + FastAPI + PostgreSQL + Railway + Vercel
- **Loại bỏ:** 27 skills không liên quan (Google AI, Cloudflare Workers, Next.js, MongoDB, Docker, Multimedia, E-commerce, Document processing)

---

## 💡 Cách sử dụng

Khi làm việc với Claude Code, chỉ cần đề cập tên skill hoặc mô tả công việc, Claude sẽ tự động load skill phù hợp.

**Ví dụ:**
- "Sử dụng frontend-standard-v1 để tạo module mới"
- "Dùng zero-loop-dev để tạo backend entity mới"
- "Chạy debugging-systematic-debugging khi gặp bug"
- "Tạo UI component với shadcn-ui + tailwindcss"

---

*Cập nhật lần cuối: 2026-03-03*
