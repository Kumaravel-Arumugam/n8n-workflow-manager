# n8n Skills Reference

> Expert guidance for building n8n workflows via MCP. Based on [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills).

---

## 📚 The 7 Skills

| # | Skill | When to Use | Key File |
|---|-------|-------------|----------|
| 1 | **n8n-expression-syntax** | Writing `{{}}` expressions, $json/$node | `SKILL.md` |
| 2 | **n8n-mcp-tools-expert** | Using MCP tools, validation, templates | `SKILL.md` |
| 3 | **n8n-workflow-patterns** | Designing workflow architecture | `SKILL.md` |
| 4 | **n8n-validation-expert** | Debugging validation errors | `SKILL.md` |
| 5 | **n8n-node-configuration** | Setting up node parameters | `SKILL.md` |
| 6 | **n8n-code-javascript** | JS in Code nodes | `SKILL.md` |
| 7 | **n8n-code-python** | Python in Code nodes (limited) | `SKILL.md` |

---

## 📁 Folder Structure

```
skills/
├── CLAUDE.md                    # AI guidance for this skill set
├── .mcp.json.example            # MCP config example
├── docs/                        # Documentation
│   ├── CODE_NODE_BEST_PRACTICES.md
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   └── ...
│
├── n8n-expression-syntax/       # Skill 1
│   └── SKILL.md                 # Main skill file
├── n8n-mcp-tools-expert/        # Skill 2 (HIGHEST PRIORITY)
│   ├── SKILL.md
│   ├── SEARCH_GUIDE.md
│   ├── VALIDATION_GUIDE.md
│   └── WORKFLOW_GUIDE.md
├── n8n-workflow-patterns/       # Skill 3
├── n8n-validation-expert/       # Skill 4
├── n8n-node-configuration/      # Skill 5
├── n8n-code-javascript/         # Skill 6
└── n8n-code-python/             # Skill 7
```

---

## ⚡ Quick Reference

### Expression Syntax
```javascript
// Access data
{{ $json.fieldName }}

// Webhook body (CRITICAL - not $json directly!)
{{ $json.body }}

// Previous node data
{{ $node["NodeName"].json.field }}

// Current time
{{ $now.format('YYYY-MM-DD') }}
```

### Code Node Return Format
```javascript
// JavaScript - MUST return array with json key
return [{ json: { result: "value" } }];
```

### Most Used MCP Tools
| Tool | Purpose | Speed |
|------|---------|-------|
| `search_nodes` | Find nodes by keyword | <20ms |
| `get_node` | Get node operations | <10ms |
| `validate_node` | Check configuration | <100ms |
| `n8n_update_partial_workflow` | Edit workflows (MOST USED!) | 50-200ms |

---

## 🔗 How Skills Work Together

1. **n8n Workflow Patterns** → Identify structure
2. **n8n MCP Tools Expert** → Find nodes
3. **n8n Node Configuration** → Setup parameters
4. **n8n Expression Syntax** → Map data
5. **n8n Code JavaScript/Python** → Custom logic
6. **n8n Validation Expert** → Validate & fix

---

## 📖 Documentation

See `docs/` folder:
- `CODE_NODE_BEST_PRACTICES.md` - Writing good Code nodes
- `INSTALLATION.md` - Setup guide
- `USAGE.md` - Usage patterns

---

*Source: [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) - MIT License*
