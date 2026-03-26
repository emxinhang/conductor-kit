---
name: module-workflow
description: Guide end-to-end workflow for building new modules - from Requirements to QA. Auto-creates track structure, templates, and validates each phase.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - AskUserQuestion
---

# Module Workflow Skill

**Purpose**: Orchestrate the complete 6-phase workflow for building new modules, ensuring architecture-first approach and quality at every step.

## When to Use

Invoke this skill when:
- Starting a new module/feature (e.g., Invoice, Booking, Reports)
- User says: "Create new module X", "Build feature Y", "Start track for Z"
- Beginning a new track that involves both backend and frontend work

**Do NOT use** for:
- Small bug fixes
- UI-only changes
- Quick refactors
- Documentation updates

---

## Workflow Overview

This skill guides through **6 phases** defined in [WORKFLOW_STANDARD.md](../../../docs/WORKFLOW_STANDARD.md):

```
Phase 1: Requirements Discovery (optional)
    ↓
Phase 2: Architecture Design
    ↓
Phase 3: Detailed Planning (Sonnet 4.5)
    ↓
Phase 4: Backend Implementation
    ↓
Phase 5: Frontend Implementation
    ↓
Phase 6: Quality Assurance & Review
```

---

## Initialization

### Step 1: Gather Context

Ask user for:
1. **Module name** (e.g., "Invoice Management")
2. **Track ID** (auto-suggest next available, e.g., "048")
3. **Brief description** (1-2 sentences)
4. **Do they have requirements ready?**
   - If YES → Skip Phase 1
   - If NO → Start with Phase 1

### Step 2: Create Track Structure

Run initialization script:
```bash
python .claude/skills/module-workflow/scripts/init_track.py \
  --track-id [ID] \
  --name "[Module Name]" \
  --description "[Description]"
```

This creates:
```
conductor/tracks/[track-id]-[slug]/
├── README.md
├── PRD.md (if Phase 1 needed)
├── ARCHITECTURE.md (template)
├── IMPLEMENTATION_PLAN.md (template)
└── .phase (tracks current phase)
```

### Step 3: Update tracks.md

Add entry to `conductor/tracks.md`:
```markdown
| [ID] | [Module Name] | 🔄 In Progress | [Date] | AG | [Description] |
```

---

## Phase 1: Requirements Discovery

**When**: User doesn't have clear requirements

**Process**:
1. Invoke `/requirements-analyst` agent
2. Guide user through:
   - What problem does this solve?
   - Who are the users?
   - What are the must-have features?
   - What are nice-to-haves?
   - Success criteria?

**Output**:
- File: `conductor/tracks/[track-id]/PRD.md`
- Contains:
  - Problem statement
  - User stories
  - Acceptance criteria
  - Success metrics

**Validation**:
- [ ] PRD has clear user stories
- [ ] Acceptance criteria defined
- [ ] Success metrics measurable
- [ ] User approved PRD

**Checkpoint**: Ask user "PRD looks good? Can we proceed to Architecture phase?"

---

## Phase 2: Architecture Design

**Always required** - Never skip this phase.

**Process**:
1. Launch architecture agents **in parallel**:
   ```bash
   /system-architect    # High-level design
   /backend-architect   # Database + API design
   /frontend-architect  # UI components + state management
   ```

2. Guide agents to produce:
   - **System Architecture**: Component diagram, data flow
   - **Database Schema**: ERD, tables, relationships, indexes
   - **API Specification**: Endpoints, request/response schemas
   - **Frontend Architecture**: Component hierarchy, state management
   - **Security & Performance considerations**
   - **Technology choices with rationale**

**Output**:
- File: `conductor/tracks/[track-id]/ARCHITECTURE.md`
- Use template from WORKFLOW_STANDARD.md

**Validation**:
- [ ] Database schema complete (tables, columns, relationships, indexes)
- [ ] API endpoints defined (method, path, auth, params, response)
- [ ] Frontend components mapped
- [ ] Security considerations documented
- [ ] Performance strategy defined
- [ ] Technology choices justified

**Checkpoint**: Ask user "Architecture design approved? Ready for detailed planning?"

---

## Phase 3: Detailed Planning (Sonnet 4.5)

**Your role** (Sonnet 4.5): Create step-by-step implementation plan.

**Process**:
1. Read PRD (if exists) and ARCHITECTURE.md
2. Create detailed plan structured as:
   - **Backend Tasks**
     - Database & Models (scaffold, relationships, migrations)
     - Schemas (Create, Update, Response)
     - Service Layer (business logic)
     - API Router (endpoints with error handling)
     - Verification steps
   - **Frontend Tasks**
     - Types definitions
     - API Client
     - List Page (with search, filter, pagination)
     - Detail Page (with tabs, edit, delete)
     - Navigation integration
     - Verification steps
   - **Integration Tasks**
     - End-to-end testing scenarios
     - Edge cases to handle

3. For each task, specify:
   - File path to create/edit
   - Code snippets or pseudocode
   - Dependencies (what needs to be done first)
   - Verification criteria

**Output**:
- File: `conductor/tracks/[track-id]/IMPLEMENTATION_PLAN.md`
- Use template from WORKFLOW_STANDARD.md

**Validation**:
- [ ] Plan has concrete file paths
- [ ] Each step has verification criteria
- [ ] Critical decisions documented
- [ ] Timeline estimate provided

**Checkpoint**: Ask user "Implementation plan approved? Ready to start coding?"

---

## Phase 4: Backend Implementation

**Process**:
1. Invoke `/zero-loop-dev` skill
2. Run scaffold script:
   ```bash
   python .claude/skills/zero-loop-dev/scripts/scaffold_backend.py [entity_name]
   ```

3. Implement according to IMPLEMENTATION_PLAN.md:
   - Define Model relationships
   - Complete Pydantic schemas (Create, Update, Response)
   - Implement Service layer methods
   - Add Router endpoints with error handling
   - Create Alembic migration

4. Verify integrity:
   ```bash
   python .claude/skills/zero-loop-dev/scripts/verify_integrity.py
   ```

**Validation**:
- [ ] Scaffold completed
- [ ] Model has relationships
- [ ] All 3 schemas complete (Create, Update, Response)
- [ ] Service methods implemented
- [ ] Router has error handling
- [ ] Migration created and applied
- [ ] Integrity check PASS
- [ ] Manual API testing with sample requests

**Checkpoint**:
- Run verify_integrity.py
- Show results to user
- Ask "Backend complete and verified. Proceed to Frontend?"

---

## Phase 5: Frontend Implementation

**Process**:
1. Invoke `/frontend-standard-v1` skill
2. Follow 5-step workflow:

   **Step 1: Types**
   - File: `frontend/src/types/[module].ts`
   - Define interfaces matching backend schemas

   **Step 2: API Client**
   - File: `frontend/src/api/[module].ts`
   - Implement CRUD functions with proper typing

   **Step 3: List Page**
   - File: `frontend/src/pages/[module]/[Module]Page.tsx`
   - DataTable + Search + Filter + Pagination + Create Modal

   **Step 4: Detail Page**
   - File: `frontend/src/pages/[module]/[Module]DetailPage.tsx`
   - Header + Tabs + Edit + Delete

   **Step 5: Navigation**
   - Update `frontend/src/lib/navigation.ts`
   - Register routes in `frontend/src/App.tsx`

3. Run verification:
   ```bash
   cd frontend
   npm run lint
   npm run type-check
   ```

**Validation**:
- [ ] Types defined in src/types/
- [ ] API client type-safe
- [ ] No `any` types
- [ ] No unused imports
- [ ] List page responsive
- [ ] Detail page functional
- [ ] Routes registered
- [ ] Lint check PASS
- [ ] Type check PASS

**Checkpoint**:
- Show lint/type-check results
- Ask user to test UI manually
- Ask "Frontend complete and verified. Ready for final QA?"

---

## Phase 6: Quality Assurance & Review

**Your role** (Sonnet 4.5): Final code review and sign-off.

**Process**:
1. **Code Review Checklist**:
   - [ ] Code follows architecture design
   - [ ] All edge cases handled
   - [ ] Security: No SQL injection, XSS, etc.
   - [ ] Performance: No N+1 queries, proper indexes
   - [ ] Consistency: Follows project patterns
   - [ ] Documentation: Complex logic commented

2. **If issues found**:
   - Invoke `/refactoring-expert`
   - Fix root causes (not quick fixes)
   - Re-verify after fixes

3. **Final Verification**:
   ```bash
   # Backend
   python .claude/skills/zero-loop-dev/scripts/verify_integrity.py

   # Frontend
   cd frontend && npm run lint && npm run type-check

   # End-to-end test
   # Manual testing of CRUD operations
   ```

4. **Create Review Report**:
   - File: `conductor/tracks/[track-id]/QA_REPORT.md`
   - Include:
     - Code quality score
     - Issues found and fixed
     - Test coverage
     - Performance notes
     - Security notes
     - Sign-off

**Validation**:
- [ ] All automated checks PASS
- [ ] End-to-end testing completed
- [ ] No critical issues remaining
- [ ] Review report created
- [ ] User sign-off obtained

**Completion**:
1. Update track status in `conductor/tracks.md`:
   ```markdown
   | [ID] | [Module Name] | ✅ Completed | [Date] | AG | [Description] |
   ```

2. Update `.phase` file to "completed"

3. Ask user: "Module complete! Ready to commit and deploy?"

---

## Helper Commands

The skill provides these helper commands:

```bash
# Initialize new track
python .claude/skills/module-workflow/scripts/init_track.py \
  --track-id 048 \
  --name "Invoice Management" \
  --description "Manage invoices and payments"

# Check current phase
cat conductor/tracks/[track-id]/.phase

# Skip to specific phase (use with caution)
echo "phase-4" > conductor/tracks/[track-id]/.phase
```

---

## Guardrails

### Never Skip:
- Phase 2 (Architecture Design)
- Verification steps at each phase

### Always Do:
- Create track structure before starting
- Document decisions in appropriate files
- Get user approval at checkpoints
- Run automated checks before moving to next phase

### Phase Skipping Rules:
- Phase 1 (Requirements): Can skip if user has clear requirements
- Phase 2 (Architecture): **NEVER skip**
- Phase 3-6: Must complete in order

---

## Example Usage

**User says**: "Create new Invoice Management module"

**Skill execution**:
```
1. Ask context questions (track ID, requirements ready?)
2. Run init_track.py → Create structure
3. Phase 1: /requirements-analyst → PRD.md ✓
4. Phase 2: /system-architect + /backend-architect + /frontend-architect → ARCHITECTURE.md ✓
5. Phase 3: Sonnet 4.5 creates IMPLEMENTATION_PLAN.md ✓
6. Phase 4: /zero-loop-dev + implement → verify_integrity.py ✓
7. Phase 5: /frontend-standard-v1 → lint + type-check ✓
8. Phase 6: Code review → QA_REPORT.md ✓
9. Update tracks.md to "Completed" ✓
```

---

## Integration with Other Skills

This skill orchestrates other skills:
- `/requirements-analyst` - Phase 1
- `/system-architect` - Phase 2
- `/backend-architect` - Phase 2
- `/frontend-architect` - Phase 2
- `/zero-loop-dev` - Phase 4
- `/frontend-standard-v1` - Phase 5
- `/refactoring-expert` - Phase 6 (if needed)

---

## Success Criteria

A successful module-workflow execution means:
- ✅ Track structure created and organized
- ✅ Architecture designed before coding
- ✅ Implementation plan detailed and approved
- ✅ Backend passes integrity checks
- ✅ Frontend passes lint and type checks
- ✅ Code review completed
- ✅ User sign-off obtained
- ✅ Track marked as completed

---

## References

- [WORKFLOW_STANDARD.md](../../../docs/WORKFLOW_STANDARD.md) - Full workflow documentation
- [zero-loop-dev](../zero-loop-dev/SKILL.md) - Backend scaffolding
- [frontend-standard-v1](../frontend-standard-v1/SKILL.md) - Frontend patterns
