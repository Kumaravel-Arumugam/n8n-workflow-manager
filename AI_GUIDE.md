# AI Guide for Agentic IDEs

This file provides guidance to AI assistants (Antigravity, Cursor, Claude, GPT, etc.) when working with this repository.

---

## Project Overview

**n8n Workflow Manager** - A toolkit for building n8n workflows using AI + MCP.

**Purpose:** Enable non-technical users to create n8n automations by describing what they want in natural language.

**Repository:** https://github.com/Kumaravel-Arumugam/n8n-workflow-manager

---

## Folder Priority (Read First → Last)

| Priority | Folder | Purpose |
|----------|--------|---------|
| 1️⃣ | `skills/n8n-mcp-tools-expert/` | HOW to use MCP tools correctly |
| 2️⃣ | `skills/n8n-workflow-patterns/` | Workflow architecture patterns |
| 3️⃣ | `skills/n8n-expression-syntax/` | n8n expression syntax |
| 4️⃣ | `skills/n8n-node-configuration/` | Node setup guidance |
| 5️⃣ | `skills/n8n-validation-expert/` | Debugging validation errors |
| 6️⃣ | `skills/n8n-code-javascript/` | JS in Code nodes |
| 7️⃣ | `skills/n8n-code-python/` | Python in Code nodes |
| 8️⃣ | `core/` | Utility scripts for workflow management |

---

## Where to Create New Workflows

When user asks to create a new workflow project:

```
projects/{project-name}/
├── README.md           # REQUIRED: Project description
├── workflow.json       # Current active workflow
└── versions/           # Version history (optional)
    ├── v1.json
    └── v2.json
```

**README.md template for new projects:**
```markdown
# {Project Name}

**Workflow ID:** {from n8n after creation}
**Created:** {date}
**Status:** draft | active | archived

## Purpose
{One paragraph description}

## Inputs
- {input_name}: {description}

## Outputs
- {output_name}: {description}
```

---

## What Can Be Deleted Safely

| ✅ Safe to Delete | ❌ Never Delete |
|-------------------|-----------------|
| `projects/{name}/versions/*.json` (old versions) | `.env` (credentials) |
| `archive/*` (reference files) | `skills/` (knowledge base) |
| Empty project folders | `core/` (utility scripts) |
| | `package.json` / `node_modules` |

---

## Working with n8n MCP

### Available MCP Tools (Most Used)

```
search_nodes        → Find nodes by keyword
get_node            → Get node operations  
validate_node       → Check configuration
n8n_create_workflow → Create new workflow
n8n_update_partial_workflow → Edit workflows (MOST USED!)
validate_workflow   → Check complete workflow
```

### Typical Workflow Creation Pattern

1. **Understand requirements** → Ask user what they want
2. **Find nodes** → `search_nodes` with keywords
3. **Get node details** → `get_node` for operations
4. **Create workflow** → `n8n_create_workflow`
5. **Validate** → `validate_workflow`
6. **Deploy** → Activate in n8n

---

## Important Rules

### DO
- Read `skills/n8n-mcp-tools-expert/SKILL.md` before using MCP tools
- Ask user for n8n credentials if not configured
- Validate workflows before deployment
- Create project README for new workflows
- Store workflows in `projects/{name}/`

### DON'T
- Never commit `.env` or credentials
- Don't modify `skills/` content (update from original repo)
- Don't delete `core/` scripts
- Don't hardcode URLs or API keys

---

## User Interaction Patterns

### When user says "create a workflow for X":
1. Ask clarifying questions about requirements
2. Suggest workflow architecture (from patterns skill)
3. Find required nodes
4. Build incrementally, validating each step
5. Offer to save in `projects/` folder

### When user says "fix this workflow":
1. Ask for workflow ID or JSON
2. Use `validate_workflow` to find issues
3. Read validation skill for error interpretation
4. Fix issues one by one
5. Re-validate after each fix

### When user says "update the skills":
```bash
cd skills
rm -rf n8n-*
git clone https://github.com/czlonkowski/n8n-skills.git --depth 1
cp -r n8n-skills/skills/* .
rm -rf n8n-skills
```

---

## Configuration Files

| File | Purpose |
|------|---------|
| `.env` | n8n API credentials (N8N_API_KEY, N8N_BASE_URL) |
| `.env.example` | Template for new users |
| `package.json` | npm dependencies |
| `.gitignore` | Files to exclude from Git |

---

## Credits

- **Skills:** From [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) - MIT License
- **Project:** Created by Kumaravel Arumugam using AI-assisted development

---

*Always prioritize user intent. Ask clarifying questions when uncertain.*
