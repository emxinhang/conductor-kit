#!/usr/bin/env python3
"""
Initialize track structure for new module development.

Usage:
    python init_track.py --track-id 048 --name "Invoice Management" --description "Manage invoices and payments"
"""

import argparse
import os
from pathlib import Path
from datetime import date


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    return text.lower().replace(" ", "-").replace("_", "-")


def create_track_structure(track_id: str, name: str, description: str):
    """Create track folder structure and template files."""

    # Create track folder
    slug = slugify(name)
    track_folder = Path(f"conductor/tracks/{track_id}-{slug}")
    track_folder.mkdir(parents=True, exist_ok=True)

    print(f"✓ Created track folder: {track_folder}")

    # Create README.md
    readme_content = f"""# Track {track_id}: {name}

**Status**: 🔄 In Progress
**Created**: {date.today().isoformat()}
**Type**: Module Development

## Description

{description}

## Workflow Phases

- [ ] Phase 1: Requirements Discovery
- [ ] Phase 2: Architecture Design
- [ ] Phase 3: Detailed Planning
- [ ] Phase 4: Backend Implementation
- [ ] Phase 5: Frontend Implementation
- [ ] Phase 6: Quality Assurance & Review

## Files

- [README.md](./README.md) - This file
- [PRD.md](./PRD.md) - Product Requirements Document (if Phase 1)
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Architecture design
- [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) - Detailed implementation plan
- [QA_REPORT.md](./QA_REPORT.md) - Quality assurance report

## References

- [WORKFLOW_STANDARD.md](../../.claude/docs/WORKFLOW_STANDARD.md)
- [module-workflow skill](../../.agent/skills/module-workflow/SKILL.md)
"""

    (track_folder / "README.md").write_text(readme_content, encoding="utf-8")
    print(f"✓ Created README.md")

    # Create template files
    templates = {
        "ARCHITECTURE.md": f"""# Architecture Design - {name}

## Overview

[Brief 1-2 paragraph description of this module]

## System Architecture

### Component Diagram

```
[Add diagram here - can use Mermaid or ASCII art]
```

### Data Flow

1. User action → Frontend Component
2. API call → Backend Router
3. Service Layer → Database
4. Response → Frontend update

## Database Schema

### Tables

#### `table_name`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | Primary key |

### Relationships

- `table_a.fk_id` → `table_b.id` (Many-to-One)

### Indexes

- `idx_table_column` on `table(column)` - For WHERE queries

## API Specification

### Endpoints

#### `GET /api/v1/entities`
- **Purpose**: List entities with pagination
- **Query Params**: skip, limit
- **Response**: `Entity[]`
- **Auth**: Required

## Frontend Architecture

### Component Hierarchy

```
EntitiesPage
├── EntityList
│   ├── EntityCard
│   └── Pagination
└── CreateEntityModal
```

### State Management

- **React Query**: Server state
- **Zustand**: Client state

## Security Considerations

- [ ] Authentication: JWT required
- [ ] Authorization: Role-based
- [ ] Input validation: Pydantic schemas
- [ ] SQL injection: Parameterized queries

## Performance Considerations

- [ ] Database indexes
- [ ] API pagination
- [ ] Frontend lazy loading

## Technology Choices

### Backend
- FastAPI + SQLAlchemy 2.0 Async

### Frontend
- React Query v5 + shadcn/ui + Zod

## Trade-offs & Decisions

### Decision 1: [Title]
- **Context**: [Why]
- **Options**: A vs B
- **Decision**: Chose A
- **Rationale**: [Why A]
""",

        "IMPLEMENTATION_PLAN.md": f"""# Implementation Plan - {name}

## Backend Tasks

### 1. Scaffold Entities
- [ ] Run scaffold script
  ```bash
  python .agent/skills/zero-loop-dev/scripts/scaffold_backend.py [entity_name]
  ```

### 2. Database Models
- [ ] Define relationships
- [ ] Create migration

### 3. Schemas (Pydantic)
- [ ] Create schema
- [ ] Update schema
- [ ] Response schema

### 4. Service Layer
- [ ] Implement CRUD methods
- [ ] Add business logic

### 5. API Router
- [ ] GET / - List
- [ ] GET /:id - Detail
- [ ] POST / - Create
- [ ] PATCH /:id - Update
- [ ] DELETE /:id - Delete

### 6. Verification
- [ ] Run verify_integrity.py
- [ ] Test endpoints

---

## Frontend Tasks

### 1. Types
- [ ] Define interfaces in `src/types/[module].ts`

### 2. API Client
- [ ] Implement in `src/api/[module].ts`

### 3. List Page
- [ ] Create `src/pages/[module]/[Module]Page.tsx`
- [ ] DataTable + Search + Filter

### 4. Detail Page
- [ ] Create `src/pages/[module]/[Module]DetailPage.tsx`
- [ ] Header + Tabs + Edit

### 5. Navigation
- [ ] Update `src/lib/navigation.ts`
- [ ] Register routes in `src/App.tsx`

### 6. Verification
- [ ] Lint check
- [ ] Type check
- [ ] Responsive test

---

## Verification Checklist

### Backend ✓
- [ ] Integrity check PASS
- [ ] All endpoints working
- [ ] Error handling tested

### Frontend ✓
- [ ] Lint PASS
- [ ] Type check PASS
- [ ] Responsive layout

### Integration ✓
- [ ] CRUD operations work
- [ ] No console errors
"""
    }

    for filename, content in templates.items():
        (track_folder / filename).write_text(content, encoding="utf-8")
        print(f"✓ Created {filename}")

    # Create .phase file
    (track_folder / ".phase").write_text("phase-1", encoding="utf-8")
    print(f"✓ Created .phase (current: phase-1)")

    print(f"\n✅ Track {track_id} initialized successfully!")
    print(f"\nNext steps:")
    print(f"1. Update conductor/tracks.md to add this track")
    print(f"2. Start with Phase 1 or Phase 2 depending on requirements clarity")

    return track_folder


def main():
    parser = argparse.ArgumentParser(description="Initialize new module track")
    parser.add_argument("--track-id", required=True, help="Track ID (e.g., 048)")
    parser.add_argument("--name", required=True, help="Module name (e.g., 'Invoice Management')")
    parser.add_argument("--description", required=True, help="Brief description")

    args = parser.parse_args()

    create_track_structure(args.track_id, args.name, args.description)


if __name__ == "__main__":
    main()
