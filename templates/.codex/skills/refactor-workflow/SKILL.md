---
name: refactor-workflow
description: Guide systematic refactoring of existing modules - from Root Cause Analysis to implementation. Ensures incremental improvements with backward compatibility.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - AskUserQuestion
  - Glob
  - Grep
---

# Refactor Workflow Skill

**Purpose**: Orchestrate systematic refactoring of existing modules in TMS-2026, ensuring quality improvements without breaking existing functionality.

## When to Use

Invoke this skill when:
- User says: "Refactor module X", "Fix technical debt in Y", "Improve code quality of Z"
- Existing module has issues: performance, consistency, scalability, maintainability
- Module needs re-architecture due to new requirements
- Code smells detected (duplication, complexity, coupling)

**Do NOT use** for:
- Small bug fixes (fix directly)
- Adding new features (use `/module-workflow` instead)
- Simple renaming or formatting

---

## Workflow Overview

This skill guides through **refactoring phases** defined in [WORKFLOW_STANDARD.md](../../../docs/WORKFLOW_STANDARD.md):

```
Phase 1: Root Cause Analysis (RCA)
    ↓
Phase 2: Re-Architecture (if needed)
    ↓
Phase 3: Refactoring Plan
    ↓
Phase 4: Backend Refactoring
    ↓
Phase 5: Frontend Refactoring
    ↓
Phase 6: Quality Assurance & Verification
```

---

## Initialization

### Step 1: Gather Context

Ask user for:
1. **Module name** to refactor (e.g., "User Management")
2. **Track ID** for this refactor work (auto-suggest next available)
3. **What problems** are they seeing?
   - Performance issues?
   - Consistency problems?
   - Hard to maintain?
   - Technical debt?
4. **How critical** is this refactor?
   - P0: Critical (blocking)
   - P1: High (affects users)
   - P2: Medium (code quality)
   - P3: Low (nice to have)

### Step 2: Create Refactor Track Structure

Run initialization script:
```bash
python .claude/skills/refactor-workflow/scripts/init_refactor_track.py \
  --track-id [ID] \
  --module "[Module Name]" \
  --priority [P0-P3]
```

This creates:
```
conductor/tracks/[track-id]-refactor-[slug]/
├── README.md
├── RCA.md (Root Cause Analysis)
├── ARCHITECTURE_REFACTOR.md (if needed)
├── REFACTORING_PLAN.md
├── QA_REPORT.md
└── .phase (tracks current phase)
```

### Step 3: Update tracks.md

Add entry:
```markdown
| [ID] | [Refactor: Module Name] | 🔄 In Progress | [Date] | AG | [Description] |
```

---

## Phase 1: Root Cause Analysis (RCA)

**Goal**: Understand what's wrong and why before fixing anything.

**Process**:

1. **Code Discovery**: Explore affected files
   ```bash
   # Find all related files
   # Backend
   ls backend/models/[module]*
   ls backend/schemas/[module]*
   ls backend/services/[module]*
   ls backend/api/v1/[module]*

   # Frontend
   ls frontend/src/types/[module]*
   ls frontend/src/api/[module]*
   ls frontend/src/pages/[module]*
   ```

2. **Invoke Analysis Agent**:
   ```bash
   /refactoring-expert
   ```

   Provide context:
   - Module files to analyze
   - User-reported issues
   - Expected behavior

3. **Document Issues** in RCA.md:

   **For each issue, document**:
   - **Priority**: P0/P1/P2/P3
   - **Symptom**: What user/developer sees
   - **Root Cause**: Technical reason
   - **Impact**: Business/user/developer impact
   - **Code Example**: Snippet showing the problem

   **Categorize issues**:
   - Architecture Issues (tight coupling, missing abstraction)
   - Code Quality Issues (duplication, complexity, no error handling)
   - Performance Issues (N+1 queries, missing indexes, no pagination)
   - Consistency Issues (naming, patterns, data integrity)
   - Security Issues (vulnerabilities, missing validation)

4. **Recommend Approach**:

   **Option 1: Incremental Refactoring**
   - Pros: Low risk, can ship improvements incrementally
   - Cons: Slower, may leave some tech debt
   - When: Most cases, especially if module is in production

   **Option 2: Rewrite from Scratch**
   - Pros: Clean slate, apply best practices
   - Cons: High risk, long time, may introduce new bugs
   - When: Module is fundamentally broken, few users

   **Option 3: Hybrid (Refactor critical paths, leave stable parts)**
   - Pros: Balance risk and improvement
   - Cons: Need careful planning
   - When: Some parts work well, others don't

**Output**:
- File: `conductor/tracks/[track-id]/RCA.md`
- Use template from WORKFLOW_STANDARD.md

**Validation**:
- [ ] All user-reported issues documented
- [ ] Root causes identified (not just symptoms)
- [ ] Issues prioritized (P0-P3)
- [ ] Code examples included
- [ ] Approach recommended with rationale

**Checkpoint**: Ask user "RCA complete. Agree with root causes and approach? Proceed to next phase?"

---

## Phase 2: Re-Architecture (Conditional)

**When**: If RCA identified architecture-level issues

**Skip if**: Issues are code-quality only (duplication, naming, etc.)

**Process**:

1. **Invoke Architecture Agents** (as needed):
   ```bash
   /system-architect      # If component boundaries need redesign
   /backend-architect     # If database schema or API contracts need changes
   /frontend-architect    # If UI component structure needs rework
   ```

2. **Design Refactored Architecture**:
   - New component boundaries
   - Updated database schema (with migration strategy)
   - Revised API contracts (with versioning if breaking)
   - Improved frontend component hierarchy
   - Updated security/performance patterns

3. **Migration Strategy**:
   - How to go from current → new architecture?
   - Backward compatibility plan
   - Feature flags needed?
   - Data migration scripts
   - Rollback plan

**Output**:
- File: `conductor/tracks/[track-id]/ARCHITECTURE_REFACTOR.md`
- Contains:
  - Current architecture (as-is)
  - Proposed architecture (to-be)
  - Migration strategy
  - Backward compatibility plan
  - Rollback plan

**Validation**:
- [ ] New architecture solves root causes
- [ ] Migration strategy is incremental
- [ ] Backward compatibility preserved (or versioned)
- [ ] Rollback plan exists
- [ ] Breaking changes documented

**Checkpoint**: "Re-architecture design approved? Ready to create refactoring plan?"

---

## Phase 3: Refactoring Plan

**Your role** (Sonnet 4.6): Create step-by-step refactoring plan.

**Process**:

1. **Read RCA and ARCHITECTURE_REFACTOR (if exists)**

2. **Create Incremental Plan**:

   Break refactoring into **small, safe steps**:

   **Example structure**:
   ```markdown
   ## Step 1: Preparation
   - [ ] Create feature flag `refactor_user_module`
   - [ ] Write regression test suite for existing behavior
   - [ ] Backup current state (git tag)

   ## Step 2: Backend - Extract Service Layer
   - [ ] Create UserService class
   - [ ] Move business logic from Router to Service
   - [ ] Test: All endpoints still work

   ## Step 3: Backend - Optimize Database Queries
   - [ ] Add selectinload for relationships
   - [ ] Add indexes on frequently queried columns
   - [ ] Test: Performance benchmarks improved

   ## Step 4: Frontend - Remove Code Duplication
   - [ ] Extract shared component: UserInfoCard
   - [ ] Replace duplicated code in 3 places
   - [ ] Test: All pages render correctly

   ## Step 5: Integration Testing
   - [ ] Run full regression test suite
   - [ ] Check performance benchmarks
   - [ ] Verify backward compatibility
   ```

3. **For each step**:
   - Specify files to edit
   - Expected changes (pseudocode or snippets)
   - Test/verification criteria
   - Rollback procedure if step fails

4. **Testing Strategy**:
   - Regression tests (ensure nothing breaks)
   - Performance benchmarks (before/after)
   - Manual testing checklist

**Output**:
- File: `conductor/tracks/[track-id]/REFACTORING_PLAN.md`

**Validation**:
- [ ] Plan is incremental (small steps)
- [ ] Each step is testable independently
- [ ] Rollback possible at any point
- [ ] Timeline estimate provided
- [ ] Critical paths identified

**Checkpoint**: "Refactoring plan approved? Ready to start implementation?"

---

## Phase 4: Backend Refactoring

**Process**:

1. **Preparation**:
   ```bash
   # Create backup
   git tag refactor-[module]-backup

   # Run baseline tests (if exist)
   cd backend
   pytest tests/test_[module].py
   ```

2. **Execute Plan Step-by-Step**:

   For each step in REFACTORING_PLAN.md:
   - Make changes
   - Run verification
   - Commit if verification passes
   - If verification fails → rollback step → analyze → retry

3. **Common Refactoring Tasks**:

   **Extract Service Layer**:
   ```python
   # Before: Logic in Router
   @router.post("/")
   async def create_user(data: UserCreate, db: AsyncSession):
       # Business logic here
       ...

   # After: Logic in Service
   @router.post("/")
   async def create_user(data: UserCreate, db: AsyncSession):
       return await UserService.create(db, data)
   ```

   **Optimize Queries**:
   ```python
   # Before: N+1 queries
   users = await db.execute(select(User))

   # After: Eager loading
   users = await db.execute(
       select(User).options(selectinload(User.company))
   )
   ```

   **Add Missing Indexes**:
   ```python
   # Migration
   op.create_index('idx_users_email', 'users', ['email'])
   ```

4. **Schema changes → run Alembic** (nếu có thay đổi model):
   ```bash
   cd backend
   alembic revision --autogenerate -m "Refactor [module]: [description]"
   alembic upgrade head
   ```

5. **Verification After Each Step**:
   ```bash
   # Integrity check
   python .claude/skills/zero-loop-dev/scripts/verify_integrity.py

   # Run tests
   pytest tests/test_[module].py -v

   # Manual API testing
   # Test critical endpoints
   ```

**Validation**:
- [ ] Each step committed separately
- [ ] Alembic migration applied (if schema changed)
- [ ] Integrity check PASS
- [ ] Regression tests PASS
- [ ] Performance improved (if applicable)
- [ ] No breaking changes (or documented + versioned)

**Checkpoint**: "Backend refactoring complete. All tests pass. Proceed to frontend?"

---

## Phase 5: Frontend Refactoring

**Process**:

1. **Preparation**:
   ```bash
   cd frontend
   npm run lint    # Baseline
   npm run build   # Baseline (includes tsc type-check)
   ```

2. **Execute Frontend Steps** from REFACTORING_PLAN.md:

   **Common tasks**:

   **Remove Duplication**:
   - Extract shared components
   - Create custom hooks for repeated logic
   - Consolidate API calls

   **Improve Type Safety**:
   - Replace `any` with proper types
   - Add missing interfaces
   - Use strict TypeScript

   **Optimize Performance**:
   - Add React.memo for expensive components
   - Use useMemo/useCallback appropriately
   - Implement lazy loading

   **Fix Consistency**:
   - Standardize naming conventions
   - Use consistent UI patterns
   - Apply design system properly

3. **Verification After Each Step**:
   ```bash
   npm run lint
   npm run build   # includes tsc type-check
   # Manual testing in browser
   ```

**Validation**:
- [ ] Lint check PASS
- [ ] Build PASS (type errors caught by tsc)
- [ ] No regression in functionality
- [ ] Performance metrics improved (if applicable)

**Checkpoint**: "Frontend refactoring complete. UI tested. Ready for final QA?"

---

## Phase 6: Quality Assurance & Verification

**Your role** (Sonnet 4.6): Final review and sign-off.

**Process**:

1. **Comprehensive Testing**:
   ```bash
   # Backend
   cd backend
   pytest tests/test_[module].py -v --cov
   python .claude/skills/zero-loop-dev/scripts/verify_integrity.py

   # Frontend
   cd frontend
   npm run lint
   npm run build   # includes tsc type-check

   # End-to-end
   # Manual testing of all user flows
   # Regression testing
   ```

2. **Performance Benchmarks**:
   - Compare before/after metrics
   - Database query counts
   - API response times
   - Frontend render times

3. **Code Quality Metrics**:
   - Cyclomatic complexity reduced?
   - Code duplication eliminated?
   - Test coverage improved?

4. **Create QA Report**:
   - File: `conductor/tracks/[track-id]/QA_REPORT.md`
   - Include:
     - Issues from RCA → Status (Fixed/Deferred/Wontfix)
     - Performance before/after
     - Code quality before/after
     - Breaking changes (if any)
     - Migration notes
     - Sign-off

**Validation**:
- [ ] All P0 issues resolved
- [ ] All P1 issues resolved
- [ ] P2/P3 issues resolved or documented as deferred
- [ ] Performance improved (or no regression)
- [ ] Code quality improved
- [ ] All tests PASS
- [ ] User acceptance obtained

**Completion**:
1. Update track status:
   ```markdown
   | [ID] | [Refactor: Module Name] | ✅ Completed | [Date] | AG | [Description] |
   ```

2. Update `.phase` to "completed"

3. Ask user: "Refactoring complete! Ready to commit and deploy?"

---

## Helper Commands

```bash
# Initialize refactor track
python .claude/skills/refactor-workflow/scripts/init_refactor_track.py \
  --track-id 049 \
  --module "User Management" \
  --priority P1

# Check current phase
cat conductor/tracks/[track-id]/.phase

# Run before/after comparison
python .claude/skills/refactor-workflow/scripts/compare_metrics.py \
  --before refactor-[module]-backup \
  --after HEAD
```

---

## Guardrails

### Never:
- Skip RCA (must understand root causes first)
- Make big-bang changes (incremental only)
- Skip testing after each step
- Introduce breaking changes without versioning

### Always:
- Create backup/tag before starting
- Write regression tests if they don't exist
- Commit each step separately
- Document breaking changes
- Provide rollback plan

### Phase Skipping Rules:
- Phase 1 (RCA): **NEVER skip**
- Phase 2 (Re-Architecture): Can skip if architecture is fine
- Phase 3-6: Must complete in order

---

## Example Usage

**User says**: "Refactor User Module - it has performance issues and duplicate code"

**Skill execution**:
```
1. Ask context (priority? specific issues?)
2. Run init_refactor_track.py → Create structure
3. Phase 1: Analyze code → RCA.md with P0/P1/P2 issues ✓
4. Phase 2: Check if re-architecture needed → ARCHITECTURE_REFACTOR.md (if yes) ✓
5. Phase 3: Create incremental plan → REFACTORING_PLAN.md ✓
6. Phase 4: Execute backend steps → verify integrity ✓
7. Phase 5: Execute frontend steps → lint + type-check ✓
8. Phase 6: Comprehensive testing → QA_REPORT.md ✓
9. Update tracks.md to "Completed" ✓
```

---

## Integration with Other Skills

This skill uses:
- `/refactoring-expert` - Phase 1 (RCA)
- `/system-architect` - Phase 2 (if needed)
- `/backend-architect` - Phase 2 (if needed)
- `/frontend-architect` - Phase 2 (if needed)
- `/zero-loop-dev` - Phase 4 (verification)
- `/frontend-standard-v1` - Phase 5 (patterns)

---

## Success Criteria

A successful refactor-workflow execution means:
- ✅ Root causes identified and documented
- ✅ Refactoring plan is incremental and testable
- ✅ All P0 and P1 issues resolved
- ✅ Performance improved (or no regression)
- ✅ Code quality metrics improved
- ✅ All tests PASS
- ✅ Backward compatibility preserved (or breaking changes documented)
- ✅ User sign-off obtained
- ✅ Track marked as completed

---

## Anti-Patterns to Avoid

1. **Big-Bang Refactoring**: Never rewrite everything at once
   - ❌ "Let's rewrite the entire User module this weekend"
   - ✅ "Let's refactor the Service layer first, then optimize queries"

2. **Fixing Symptoms, Not Root Causes**:
   - ❌ "Add a try/catch to hide the error"
   - ✅ "Fix the null pointer by ensuring data is validated upstream"

3. **No Testing Between Steps**:
   - ❌ Make 10 changes → test once → everything broken
   - ✅ Make 1 change → test → commit → next change

4. **Skipping RCA**:
   - ❌ "I know what's wrong, let me just fix it"
   - ✅ "Let's analyze to understand root causes first"

---

## References

- [WORKFLOW_STANDARD.md](../../../docs/WORKFLOW_STANDARD.md) - Full workflow documentation
- [refactoring-expert](../../agents-edmund/refactoring-expert.md) - Refactoring agent
- [zero-loop-dev](../zero-loop-dev/SKILL.md) - Backend verification
