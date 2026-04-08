---
name: qa-verify-expert
description: A specialized skill to audit Data Integrity, API Contracts, and perform Automated QA for the project to ensure maximum reliability before marking tasks as Done.
---

# QA Verify Expert Skill

This skill provides a strict, automated approach to verifying the integrity of the project's data layer, API contracts, and business logic. It ensures that changes in the database model are properly reflected in schemas and frontend interfaces, avoiding silent runtime errors.

## Core Capabilities

### 1. Data Integrity Audit (`scripts/audit_schemas.py`)
Compares SQLAlchemy Models against Pydantic Schemas to identify missing or mismatched fields.
- **Goal**: Prevent "Silent Drop" issues where a field exists in the DB but is forgotten in the `UpdateSchema` or `ResponseSchema`.
- **Target**: Ensure 100% alignment between `app.models.*` and `app.schemas.*`.

### 2. End-to-End Contract Check
Ensures that the Backend's `ResponseSchema` exactly matches the Frontend's TypeScript `Interfaces/Types`.
- **Goal**: Prevent build-time and runtime crashes (e.g., `AttributeError` or missing `data.key` in React).
- **Target**: Synchronize `backend/app/schemas/` with `frontend/src/types/` and `frontend/src/api/`.

### 3. Automated QA Generation
Generates quick, standalone Python or Node scripts to perform API-level QA against the live or local environment.
- **Goal**: Programmatically verify that nested relationships (e.g., eager loaded lists) are serialized correctly without manual browser clicking.
- **Target**: Specifically designed to catch `MissingGreenlet` errors in complex SQLAlchemy queries before the UI team discovers them.

## Usage

### Phase 1: Audit Data Layer Integration
After finishing backend development and BEFORE pushing code or writing frontend logic:
```bash
python scripts/audit_schemas.py
```
*(Note: Expand the script to perform deeper AST or introspective scanning as needed by the module size).*

### Phase 2: Interface Contract Sync
Whenever a backend schema changes, manually invoke this skill or ask CS to:
1. "Verify the contract for `EntityX` between Backend and Frontend."
2. CS will read the Backend Schema, read the Frontend Type, and point out any missing or typed-wrong fields.

### Phase 3: Behavior Verification (The Acid Test)
Before declaring "Track Done", ask CS to write a short Verification Script.
1. "Generate a QA script to fetch the new endpoint and verify eager loading."
2. Run the script in terminal. If it returns `200 OK` with full nested JSON, it passes.

## Rules of Engagement

1. **Verify Beyond Types**: Passing `tsc` (TypeScript compiler) or Pyre does NOT guarantee runtime safety if the database query is lazy-loading a relationship outside an async session. **Always verify actual API responses.**
2. **Schema Triad Rule**: Every new or altered column in a SQLAlchemy Model MUST be manually audited across exactly three places:
   - `Create/Update Schema` (Pydantic)
   - `Response Schema` (Pydantic)
   - `TypeScript Interface` (React)
3. **No Silent Failures**: If the audit script or contract check fails, the task is NOT DONE. The developer must align the schemas before moving forward.
4. **Repo-Aware Artifact Placement**: Before writing any QA script or evidence file, check `.gitignore` to confirm the target directory is NOT ignored. QA artifacts MUST be saved to `conductor/tracks/<id>/qa/` (never to `scripts/` or `tmp/` which are typically gitignored). This ensures test evidence is versioned alongside the track.

## QA Artifact Standard

Mỗi track khi chuyển sang phase QA phải có folder `conductor/tracks/<id>/qa/` chứa:
- `qa_script.py` hoặc `qa_check.sh` — script kiểm tra API/logic
- `qa_result.log` hoặc output paste — bằng chứng đã chạy và pass

Cấu trúc:
```
conductor/tracks/106c2-incident-enhancements/
  qa/
    qa_script.py     ← script chạy được
    qa_result.log    ← output thực tế (không mock)
```