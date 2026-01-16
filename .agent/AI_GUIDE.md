# AI Guide for n8n Workflow Manager

> Instructions for AI assistants working with this MCP server.

---

## 📂 File Management

**This project uses a dedicated `workspace/` folder for all temporary files.**

- When you need to save a workflow JSON to disk: Save it to `workspace/<name>.json`
- When reading local files: Look in `workspace/` first
- **Do not create files in the root directory.**
- **Do not commit files from the `workspace/` folder.**

---

## Available MCP Tools

### `n8n_list_workflows`
List all workflows in the n8n instance.

**Best Practice:** Always run this first to check if a workflow exists before creating/updating.

**Parameters:**
- `limit` (optional): Max number of results (default: 50)

---

### `n8n_get_workflow`
Get full details of a specific workflow.

**Parameters:**
- `id` (required): Workflow ID

**Recommendation:** Save the output to `workspace/<workflow_name>.json` for reference before modifying.

---

### `n8n_create_workflow`
Create a new n8n workflow.

**Parameters:**
- `name` (required): Workflow name
- `nodes` (required): Array of node objects
- `connections` (required): Connections object
- `tags` (optional): Array of tag names

---

### `n8n_update_workflow`
Update an existing workflow.

**Parameters:**
- `id` (required): Workflow ID
- `nodes` (required): Array of node objects
- `connections` (required): Connections object
- `name` (optional): New workflow name

---

### `n8n_activate_workflow`
Activate or deactivate a workflow.

**Parameters:**
- `id` (required): Workflow ID
- `active` (required): `true` to activate, `false` to deactivate

---

## Workflow Structure Example

```javascript
{
  name: "My Workflow",
  nodes: [
    {
      id: "unique-uuid",
      name: "Webhook",
      type: "n8n-nodes-base.webhook",
      typeVersion: 1,
      position: [0, 0],
      parameters: { path: "webhook" }
    }
  ],
  connections: {
    "Webhook": {
      main: [[{ node: "Next Node", type: "main", index: 0 }]]
    }
  }
}
```

---

## Error Handling

If an API call fails:
1. Check the inputs (IDs, names)
2. Verify the `.env` credentials are correct
3. Check `workspace/` for any saved error logs or partial data
