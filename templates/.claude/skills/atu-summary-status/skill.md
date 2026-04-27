# Summary-Status-Atu Skill

Tự động cập nhật project status cho VacTours dựa trên technical-writer guidelines.

## Trigger Keywords
- "cập nhật status", "summary status", "project summary"
- "update vactours status", "tóm tắt tiến độ"

## Project Context
- **Tech Stack:** Next.js 15, Strapi v5, PostgreSQL, Tailwind
- **Frontend:** https://vactours-web.vercel.app
- **Backend:** https://lively-friends-93c5691585.strapiapp.com
- **Status File:** `T:\01-code\vactour-web\docs\VACTOURS_STATUS_updated.md`

## Workflow

### 1. Gather Information
```bash
# Recent commits
git log --oneline --since="7 days ago" --no-merges --pretty=format:"%h - %s (%cr)" | head -20

# Files changed
git diff HEAD~10..HEAD --name-status | sort | uniq

# Current status
git status
```

### 2. Use Gemini MCP for Analysis

**Tool:** `mcp__gemini__gemini-query` với model `pro` (required for deep analysis)

**Prompt Template:**
```
Sử dụng tool mcp__gemini__gemini-query với prompt:
"Phân tích git commits trong 7 ngày qua của VacTours và tạo summary với format technical-writer.md:
1. Completed features (✅ với evidence: URLs, file paths)
2. New components created
3. Bug fixes deployed
4. Documentation updates
5. Deployment status

Format: bullet points, emoji markers (✅🚀📝), include concrete evidence."
```

### 3. Update Status File Sections

**Header:**
```markdown
**Last Updated:** YYYY-MM-DD
**Current Phase:** [Phase Name] COMPLETE ✅ | Next Phase: [Next Phase]
```

**Recent Updates:**
```markdown
### Recent Updates (YYYY-MM-DD):
- ✅ **Feature Name** - Specific details with evidence (URL/file path)
- ✅ **Bug Fix** - What was broken → how fixed
- ✅ **Documentation** - What was documented
```

**Completed Phases (when phase finishes):**
```markdown
### Phase X: [Name] (COMPLETE)
- ✅ Feature 1 with specific detail
- ✅ **Deployed:** URL
- ✅ **Components:** X components (~Y lines)
- ✅ **Documentation:** File path

**Time Taken:** ~X days
```

**Roadmap Updates:**
- Move completed items: `NEXT` → `COMPLETED`
- Update checkboxes: `[ ]` → `[x]`
- Add time taken

### 4. Verification Checklist
```
Sử dụng tool mcp__gemini__gemini-query với prompt:
"Review VACTOURS_STATUS_updated.md và verify:
1. Dates chính xác
2. URLs accessible
3. Checkboxes match status
4. No vague statements
5. Evidence cho mọi achievement

Output: Checklist of issues OR 'All verified ✅'"
```

### 5. Commit
```bash
git add docs/VACTOURS_STATUS_updated.md
git commit -m "docs: Update project status - [brief summary]"
git push
```

## Documentation Principles

**From technical-writer.md:**

✅ **DO:**
- Specific action verbs (Implemented, Fixed, Deployed)
- Concrete evidence (URLs, file paths, metrics)
- Bullet points with bold keywords
- Emoji markers (✅🚀📝⚠️🎯)
- "What's working" proof
- Time estimates for major work

❌ **DON'T:**
- Vague terms ("improved" without details)
- Skip deployment URLs
- Mix completed and pending items
- Forget to update dates
- Leave broken links

## Common Patterns

### After Development Session
```markdown
### Recent Updates (2025-11-XX):
- ✅ **Collection Name Backend** - 4 files created (schema, controller, routes, services)
- ✅ **TypeScript Types** - Generated via `npm run strapi -- ts:generate-types`
- ✅ **API Live** - https://api-url.com/api/collection?populate=*
- ✅ **Documentation** - Updated skill/guide with [specific lesson]
```

### Phase Completion
```markdown
### ✅ COMPLETED: Phase Name (YYYY-MM-DD)
**Status:** DEPLOYED to Production
**URL:** https://...

**Completed Tasks:**
- [x] Task 1
- [x] Task 2

**Time Taken:** ~X days
```

### Verification Only (No Changes)
```bash
git commit -m "docs: Verify project status (no changes)"
```

## Gemini MCP Tools Reference

### Available Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `mcp__gemini__gemini-query` | General queries to Gemini | `prompt`, `model` (pro/flash) |
| `mcp__gemini__gemini-brainstorm` | Collaborative ideation Claude + Gemini | `prompt`, `claudeThoughts`, `maxRounds` |
| `mcp__gemini__gemini-analyze-code` | Code analysis | `code`, `language`, `focus` (quality/security/performance/bugs) |
| `mcp__gemini__gemini-analyze-text` | Text analysis | `text`, `type` (sentiment/summary/entities/key-points) |
| `mcp__gemini__gemini-summarize` | Summarize content | `content`, `length` (brief/moderate/detailed), `format` (paragraph/bullet-points/outline) |
| `mcp__gemini__gemini-image-prompt` | Create image generation prompts | `description`, `style`, `mood`, `details` |

## Gemini MCP Examples

**Weekly Summary:**
```
mcp__gemini__gemini-query với prompt:
"Phân tích 7 ngày commits VacTours: features, components, fixes, docs, deployments.
Format: technical-writer.md với bullet points + evidence."
```

**Phase Report:**
```
mcp__gemini__gemini-query với prompt:
"Phase completion report cho [Phase]: components count, features, URLs, time, next recommendations.
Format: technical-writer.md."
```

**Verification:**
```
mcp__gemini__gemini-query với prompt:
"Review VACTOURS_STATUS_updated.md: dates, URLs, checkboxes, evidence. Output issues or 'All verified ✅'"
```

**Brainstorm Feature Ideas:**
```
mcp__gemini__gemini-brainstorm với:
- prompt: "Đề xuất features mới cho VacTours booking system"
- claudeThoughts: "Cần focus vào UX, performance, và conversion rate"
- maxRounds: 3
```

**Analyze Code Quality:**
```
mcp__gemini__gemini-analyze-code với:
- code: [paste component code]
- language: "typescript"
- focus: "quality" (hoặc security/performance/bugs)
```

**Summarize Documentation:**
```
mcp__gemini__gemini-summarize với:
- content: [paste long doc content]
- length: "brief"
- format: "bullet-points"
```

**Analyze User Feedback:**
```
mcp__gemini__gemini-analyze-text với:
- text: [user feedback content]
- type: "sentiment" (hoặc key-points/entities)
```

## Emoji Reference
- ✅ Completed/Working
- 🚀 Deployed/Live
- 📝 Documentation
- ⚠️ Warning/Issue
- 🎯 Goal/Target
- 🏆 Achievement

## Example Update

**Before:**
```markdown
**Last Updated:** 2025-11-05
### Recent Updates (2025-11-05):
- ✅ Homepage redesign live
```

**After:**
```markdown
**Last Updated:** 2025-11-06
### Recent Updates (2025-11-06):
- ✅ **Team Collection Backend** - 4 files with avatar & socialLinks populate
- ✅ **Types Generated** - Resolved TS2345 errors via type generation
- ✅ **API Live** - https://api-url.com/api/teams?populate=*

### Previous Updates (2025-11-05):
- ✅ Homepage redesign live
```

## Quick Reference

**Git Commands:**
```bash
git log --oneline --since="7 days ago" --no-merges
git diff HEAD~10..HEAD --stat
```

**Status File:** `docs/VACTOURS_STATUS_updated.md`

**Gemini Tool:** `mcp__gemini__gemini-query` với model `pro`

**Update Frequency:** After every significant change (deployment, phase completion, major feature)
