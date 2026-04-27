# Compact-Atu Skill

## Description
Compact conversation context của session hiện tại bằng cách sử dụng MCP gemini-server với model gemini-2.5-flash. Tóm tắt toàn bộ cuộc trò chuyện thành một summary ngắn gọn, giữ lại thông tin quan trọng và loại bỏ chi tiết không cần thiết.

## Trigger Keywords
Use this skill when the user mentions:
- "compact session này"
- "compact context"
- "tóm tắt session"
- "summarize conversation"

## Project Context

### VacTours Project Information
- **Project:** VacTours Web - Private customizable tours website
- **Tech Stack:** Next.js 15, Strapi v5, PostgreSQL, Tailwind CSS
- **Working Directory:** `T:\01-code\vactour-web\`

### MCP Gemini Configuration
- **MCP Server:** gemini (RLabs-Inc/gemini-mcp)
- **Model:** `pro`
- **Tool:** `mcp__gemini__gemini-summarize`
- **Purpose:** Compact long conversations while preserving critical information

## Core Capabilities

### 1. Analyze Conversation

**What to extract:**
- Main tasks completed
- Technical decisions made
- Code changes (files created/modified)
- Issues encountered and resolved
- Skills/tools used
- Next steps planned

### 2. Compact Strategy

**Keep:**
- ✅ Final solutions (working code, correct approaches)
- ✅ Important decisions and rationale
- ✅ File paths and URLs
- ✅ Error messages and fixes
- ✅ Commands that worked
- ✅ Next action items

**Remove:**
- ❌ Trial-and-error iterations
- ❌ Incorrect attempts
- ❌ Verbose explanations
- ❌ Duplicate information
- ❌ Debug conversations
- ❌ Tool call details

### 3. Output Format

**Structured Summary:**
```markdown
# Session Summary - [Date]

## 🎯 Main Goals
- Goal 1
- Goal 2

## ✅ Completed Tasks
1. **Task Name** - Brief description
   - Files: `path/to/file.ts`
   - Key changes: What was done

2. **Task Name** - Brief description
   - Commands: `command here`
   - Result: What was achieved

## 🔧 Technical Details
- **Stack:** Technologies used
- **APIs:** Endpoints created/modified
- **Components:** Components created

## ⚠️ Issues & Solutions
- **Issue:** Brief description
  - **Solution:** How it was fixed

## 📝 Key Learnings
- Learning 1
- Learning 2

## 🎯 Next Steps
- [ ] Task 1
- [ ] Task 2
```

## Workflow

### Step 1: Prepare Context

Gather conversation summary:
- What was the initial request?
- What tasks were completed?
- What files were created/modified?
- What issues were encountered?
- What solutions were found?
- What's pending/next?

### Step 2: Use MCP Gemini Summarize

**Use the MCP tool `mcp__gemini__gemini-summarize`:**

Parameters:
- `content`: The conversation context to summarize
- `length`: "brief" | "moderate" | "detailed" (use "moderate")
- `format`: "bullet-points" | "paragraph" | "outline" (use "bullet-points")

**Prompt Template:**
```
[Conversation context here]

Hãy compact cuộc trò chuyện này thành một summary ngắn gọn với format sau:

# Session Summary - [Date]

## 🎯 Main Goals
[List main objectives]

## ✅ Completed Tasks
[List what was done with file paths and key changes]

## 🔧 Technical Details
[Technologies, APIs, components]

## ⚠️ Issues & Solutions
[Problems encountered and how they were solved]

## 📝 Key Learnings
[Important takeaways]

## 🎯 Next Steps
[What's next]

Loại bỏ:
- Trial-and-error details
- Verbose explanations
- Duplicate information
- Debug conversations

Giữ lại:
- Final working solutions
- File paths and URLs
- Error messages and fixes
- Commands that worked
- Next action items
```

### Step 3: Save Summary

Save to: `T:\01-code\vactour-web\.claude\session-summaries\session-[YYYYMMDD-HHMM].md`

### Step 4: Inform User

Let user know:
- Summary location
- Key highlights
- Next steps from summary

## Consult Prompt Template

```
Cuộc trò chuyện này bàn về: [Brief context]

Các công việc đã làm:
1. [Task 1]
2. [Task 2]
...

Files created/modified:
- path/to/file1.ts
- path/to/file2.json

Issues encountered:
- Issue 1 → Solution 1
- Issue 2 → Solution 2

Next steps:
- Step 1
- Step 2

---

Hãy compact cuộc trò chuyện thành summary ngắn gọn với format markdown, giữ lại thông tin quan trọng (file paths, solutions, next steps) và loại bỏ chi tiết không cần thiết (trial-and-error, verbose explanations).

Format:
# Session Summary - [Date]

## 🎯 Main Goals
## ✅ Completed Tasks
## 🔧 Technical Details
## ⚠️ Issues & Solutions
## 📝 Key Learnings
## 🎯 Next Steps
```

## Example Output

### Input (Long Conversation)
```
User: Tạo Team collection trong Strapi
Assistant: OK, tôi sẽ tạo...
[100+ messages about creating schema, fixing errors, etc.]
```

### Output (Compact Summary)
```markdown
# Session Summary - 2025-11-06

## 🎯 Main Goals
- Create Team collection in Strapi for staff/author profiles
- Prepare for blog system with author relationships

## ✅ Completed Tasks
1. **Team Collection Backend** - Created complete Strapi collection
   - Files:
     - `backend/src/api/team/content-types/team/schema.json`
     - `backend/src/api/team/controllers/team.ts`
     - `backend/src/api/team/routes/team.ts`
     - `backend/src/api/team/services/team.ts`
   - Fields: name, slug, role, avatar, bio, socialLinks, featured, order

2. **Social Links Component** - Reusable component
   - File: `backend/src/components/shared/social-links.json`
   - Fields: twitter, linkedin, website

3. **TypeScript Types** - Generated and committed
   - Command: `npm run strapi -- ts:generate-types`
   - Files: `backend/types/generated/contentTypes.d.ts`, `components.d.ts`
   - Frontend: `frontend/types/strapi.ts` (TeamMember, SocialLinks interfaces)

4. **Strapi-Atu Skill Updated** - Added type generation workflow
   - File: `.claude/skills/strapi-atu/skill.md`
   - Added: TS2345 troubleshooting, type generation step

5. **Summary-status-Atu Skill** - New documentation skill
   - File: `.claude/skills/summary-status-atu/skill.md`

## 🔧 Technical Details
- **Stack:** Strapi v5, TypeScript
- **API:** https://lively-friends-93c5691585.strapiapp.com/api/teams?populate=*
- **Components:** Team collection (4 files), Social Links component

## ⚠️ Issues & Solutions
1. **404 Error** - Missing controller
   - Solution: Created controller.ts with populate config

2. **TS2345 Build Error** - Types not generated
   - Error: `Argument of type '"api::team.team"' is not assignable to parameter of type 'ContentType'`
   - Solution: Run `npm run strapi -- ts:generate-types`
   - Fixed by generating types, NOT using `as const`

3. **403 Forbidden** - Permissions not set
   - Solution: Configure permissions in Strapi Admin (Settings → Users & Permissions → Public → Team → Check find/findOne)

## 📝 Key Learnings
- Strapi v5 requires ALL 4 files: schema, controller, routes, services
- Type generation is CRITICAL - must run before build
- `as const` is NOT the solution - proper type generation is
- Permissions must be configured in Admin UI for public access

## 🎯 Next Steps
- [ ] Configure Team permissions in Strapi Admin (Public role)
- [ ] Test API endpoint with populated data
- [ ] Create Blog/Article collection with author relationship to Team
- [ ] Build Équipes frontend pages (/equipe, /equipe/[slug])
```

## Best Practices

### Summary Quality
- ✅ Keep final solutions, remove attempts
- ✅ Include file paths for all changes
- ✅ Note commands that worked
- ✅ Capture error messages and fixes
- ✅ List next steps clearly
- ✅ Use emoji markers for scanning
- ✅ Keep under 200 lines if possible

### Accuracy
- ✅ Verify file paths are correct
- ✅ Include actual URLs tested
- ✅ Note exact error messages
- ✅ Capture working commands
- ✅ List all files created/modified

### Usefulness
- ✅ Someone should be able to understand what was done
- ✅ Should help resume work later
- ✅ Should document solutions for similar issues
- ✅ Should guide next steps

## File Organization

### Session Summaries Location
```
T:\01-code\vactour-web\.claude\session-summaries\
├── session-20251106-1430.md  # Today's session
├── session-20251105-0900.md  # Yesterday
└── README.md                  # Index of summaries
```

### Naming Convention
- Format: `session-YYYYMMDD-HHMM.md`
- Example: `session-20251106-1430.md` (Nov 6, 2025 at 14:30)

## Quick Reference

### MCP Tool
`mcp__gemini__gemini-summarize`

### Parameters
- `content`: Text to summarize
- `length`: "moderate"
- `format`: "bullet-points"

### Output Location
`T:\01-code\vactour-web\.claude\session-summaries\session-[YYYYMMDD-HHMM].md`

### Model Used
Gemini via MCP gemini server

## Gemini MCP Tools Reference

### Available Tools for Compact

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `mcp__gemini__gemini-summarize` | Primary - summarize conversations | Default choice for compacting |
| `mcp__gemini__gemini-query` | Complex analysis with custom prompt | When need specific formatting |
| `mcp__gemini__gemini-analyze-text` | Extract key points | For structured extraction |

### Alternative: Using gemini-query

For more control over output format:
```
mcp__gemini__gemini-query với:
- prompt: "[conversation context] + Compact thành summary với format: Main Goals, Completed Tasks, Technical Details, Issues & Solutions, Key Learnings, Next Steps"
- model: "pro"
```

### Alternative: Using gemini-analyze-text

For extracting structured information:
```
mcp__gemini__gemini-analyze-text với:
- text: [conversation context]
- type: "key-points"
```

### Choosing the Right Tool

| Scenario | Tool | Why |
|----------|------|-----|
| Quick compact | `gemini-summarize` | Fast, automatic formatting |
| Custom format needed | `gemini-query` | Full control over output |
| Extract specific info | `gemini-analyze-text` | Structured key-points |
| Code-heavy session | `gemini-analyze-code` + `gemini-summarize` | Analyze code first |

## Notes

- Skill should run AUTOMATICALLY when triggered
- No need to ask user for confirmation
- Save summary and inform user where it's saved
- Summary should be standalone (readable without original context)
- Keep technical accuracy high
- Remove conversational fluff
