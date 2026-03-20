---
product: I-Ching AI Project
status: Active
---

# Tracks

| ID | Title | Status | Related Files |
|----|-------|--------|---------------|
| 001 | Setup Project & Core Structure | ✅ Completed | - |
| 002 | Install Conductor & Skills Audit | ✅ Completed | [spec.md](tracks/002/spec.md), [plan.md](tracks/002/plan.md) |
| 003 | Brainstorming I-Ching (Lục Hào) Project | ✅ Spec Done | [spec.md](tracks/003/spec.md), [plan.md](tracks/003/plan.md) |
| 004 | PRD: RAG Pipeline cho App Lục Hào | 🔄 In Review | [PRD.md](tracks/004/PRD.md), [spec.md](tracks/004/spec.md) |
| 005 | Document Processing Pipeline (Phase 0+1) | 🔀 Split → 005a + 005b | [spec.md](tracks/005/spec.md) |
| 005a | Pilot Test Document Processing | ✅ Completed | [PRD.md](tracks/005a/PRD.md), [spec.md](tracks/005a/spec.md), [IMPLEMENTATION_PLAN.md](tracks/005a/IMPLEMENTATION_PLAN.md) |
| 005b | Full Document Processing Pipeline (Planning) | ✅ Completed | [PRD.md](tracks/005b/PRD.md), [spec.md](tracks/005b/spec.md), [IMPLEMENTATION_PLAN.md](tracks/005b/IMPLEMENTATION_PLAN.md) |
| 005b-1 | Foundation: Engine Module + Config + Tests | ✅ Completed | Sub-track of 005b |
| 005b-2 | DOCX Processing (2 files Lục Hào) | ✅ Completed | Sub-track of 005b |
| 005b-3 | PDF Text Processing — Module Hà Lạc | ✅ Completed | Sub-track of 005b |
| 005b-4 | PDF Scan Processing Local (4 files Lục Hào) | 🔀 Moved → 008 | Sub-track of 005b |
| 005b-5 | Validation & Final Report | ⏭️ Skipped | 008 dat 100% audit, ATu confirmed skip |
| 008 | PDF Scan Processing (Large Batch) | ✅ Completed | [spec.md](tracks/008/spec.md), [plan.md](tracks/008/plan.md) |
| 009 | Golden Prompt V6 & Engine Audit | ✅ Completed | [spec.md](tracks/009/spec.md) |
| 006 | Database Setup (PostgreSQL + pgvector) | ✅ Completed | [PRD.md](tracks/006/PRD.md), [spec.md](tracks/006/spec.md), [IMPLEMENTATION_PLAN.md](tracks/006/IMPLEMENTATION_PLAN.md) |
| 007 | Embedding & Chunking Pipeline | 📅 Planned | - |
| 010 | Module Hà Lạc Lý Số | 📋 Spec Done | [PRD.md](tracks/010/PRD.md), [spec.md](tracks/010/spec.md) |
| 010a | Lịch Vạn Niên Engine (Solar↔Lunar, Tiết khí, Can Chi) | ✅ Completed | [calendar_engine.py](../../engine/calendar_engine.py) |
| 010b | Hà Lạc Computation Engine (Bát Tự → Quẻ → Đại Vận → Lưu Niên) | 🔄 In Progress | Sub-track of 010, depends: 010a |
| 010b-1 | Bát Tự + Phối số + Lập Quẻ (core) | ✅ Completed | Sub-track of 010b |
| 010b-2 | Hóa Công + TNK/ĐNK + Đại Vận + Lưu Niên (complex) | 📅 Planned | Sub-track of 010b, depends: 010b-1 |
| 010b-3 | Theory Layer — explanations field (Premium) | 📅 Planned | Sub-track of 010b, depends: 010b-2 |
| 010c | API endpoints + Database integration | 📅 Planned | Sub-track of 010, depends: 010b, Track 006 |
| 010d | Frontend — Input form + Result display | 📅 Planned | Sub-track of 010, depends: 010c |
| 010e | Luận giải sách (tra cứu nguyên văn) | 📅 Planned | Sub-track of 010, depends: 010c, Track 006 |
| 010f | Luận giải AI (LLM tổng hợp cá nhân hóa) | 📅 Planned | Sub-track of 010, depends: 010e, Track 007 |
| 010g | Module hướng dẫn (step-by-step + glossary) | 📅 Planned | Sub-track of 010, depends: 010d |