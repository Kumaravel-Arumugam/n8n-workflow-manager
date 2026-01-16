# n8n Workflow Manager

> **Remove the technical barrier. Manage n8n workflows through natural language with AI.**

This project is created for **non-technical persons** to remove their technical barrier in executing n8n with Antigravity Agentic IDE. Instead of manually building workflows, describe what you want and the AI handles the rest.

[![n8n](https://img.shields.io/badge/n8n-workflow%20automation-orange)](https://n8n.io/)

---

## 🎯 What Is This?

An **MCP server** that gives AI assistants the ability to manage your n8n workflows:

- **Create** new workflows from natural language descriptions
- **Update** existing workflows
- **Delete** workflows you no longer need
- **List** all your workflows
- **Activate/Deactivate** workflows

**Example prompt:**
> "Create a workflow that monitors a Google Sheet and sends Slack notifications when new rows are added"

---

## ⚡ Prerequisites

| Requirement | Description |
|-------------|-------------|
| **n8n Instance** | Self-hosted or cloud with API access enabled |
| **Node.js 18+** | For running the MCP server |
| **AI IDE** | Antigravity, Cursor, Claude Desktop, or any MCP-compatible IDE |

> 🐳 **Need to deploy n8n?** See [n8n-docker-deploy](https://github.com/Kumaravel-Arumugam/n8n-docker-deploy)

---

## 🤖 Installation via AI (Recommended)

**Let your AI assistant handle the setup for you.**

Open your Agentic IDE (Antigravity, Cursor, etc.) and paste this prompt:

```text
Help me set up the n8n-workflow-manager Project.

Phase 1: Environment Check
1. Ask me if I have a running n8n instance.
2. If NO: Guide me to deploy using n8n-docker-deploy (https://github.com/Kumaravel-Arumugam/n8n-docker-deploy).
3. If YES: Ask for my n8n API Key and Base URL.

Phase 2: Project Setup
1. Clone the repository: https://github.com/Kumaravel-Arumugam/n8n-workflow-manager.git
2. Install dependencies (npm install).
3. Create a .env file from .env.example.
4. Populate .env with the API Key and Base URL I provided.

Phase 3: MCP Configuration
1. Analyze the README.md to understand the MCP structure.
2. Guide me to configure the MCP server settings in this IDE.
3. Use the absolute path for the script location.
4. Remind me to restart the IDE after saving the config.

Begin via Phase 1.
```

---

## 🛠️ Manual Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Kumaravel-Arumugam/n8n-workflow-manager.git
cd n8n-workflow-manager
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your n8n credentials:
```env
N8N_API_KEY=your-n8n-api-key-here
N8N_BASE_URL=https://your-n8n-instance.com
```

**How to get your n8n API key:**
1. Open your n8n instance
2. Go to **Settings → API**
3. Create a new API key
4. Copy the key

---

## 🔌 MCP Configuration

### For Antigravity IDE

1. Go to **Chat → ⚙️ → Manage MCP Servers → View Raw Config**
2. Add this configuration:

```json
{
  "mcpServers": {
    "n8n-manager": {
      "command": "node",
      "args": ["/full/path/to/n8n-workflow-manager/core/index.js"],
      "cwd": "/full/path/to/n8n-workflow-manager",
      "env": {
        "DOTENV_CONFIG_QUIET": "true"
      }
    }
  }
}
```

3. Replace `/full/path/to/` with your actual path
4. Save and **restart the IDE**

---

## 🛠️ Available MCP Tools

| Tool | Description |
|------|-------------|
| `n8n_list_workflows` | List all workflows with ID, name, and status |
| `n8n_get_workflow` | Get full details of a specific workflow |
| `n8n_create_workflow` | Create a new workflow |
| `n8n_update_workflow` | Update an existing workflow |
| `n8n_activate_workflow` | Activate or deactivate a workflow |

---

## 📂 Project Structure

```
n8n-workflow-manager/
├── .env.example      # Environment template
├── package.json      # Dependencies
├── core/
│   └── index.js      # MCP server
├── .agent/           # AI instructions (read .agent/AI_GUIDE.md)
└── workspace/        # Temporary working files (gitignored)
```

---

## 💡 Usage Examples

Once MCP is configured, try these prompts:

> "List all my n8n workflows"

> "Get the details of workflow ID abc123"

> "Create a workflow that sends a daily email summary"

> "Activate workflow xyz789"

---

## ⚠️ Troubleshooting

### Error: "Cannot find module"
- Use **absolute paths** in your MCP config, not relative paths

### Error: "invalid character 'd' looking for beginning of value"
- Add `"DOTENV_CONFIG_QUIET": "true"` to the `env` section in your MCP config

### MCP not connecting
- Restart your IDE after changing MCP config
- Check that Node.js 18+ is installed

---

## 🙏 Credits

**Created by Kumaravel Arumugam** using AI-assisted development (Antigravity IDE).

---

## 🔗 Related Projects

| Repository | Description |
|------------|-------------|
| [n8n-docker-deploy](https://github.com/Kumaravel-Arumugam/n8n-docker-deploy) | Docker Compose deployment for n8n |

---

*Powered by n8n + MCP + AI*
