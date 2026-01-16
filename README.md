# n8n Workflow Manager

> **Build n8n workflows through natural language prompts using AI + MCP.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![n8n](https://img.shields.io/badge/n8n-workflow%20automation-orange)](https://n8n.io/)

Remove the technical barrier. Describe what automation you want → AI creates the workflow.

---

## 🎯 What Is This?

This project enables **non-technical users** to create n8n automations by simply describing what they want. Instead of manually building workflows, you:

1. Open an Agentic IDE (Antigravity, Cursor, VS Code + MCP)
2. Describe your automation in plain English
3. AI creates the workflow using n8n-mcp tools

**Example:**
> "Create a workflow that scrapes job postings and sends a daily report to Telegram"

The AI handles the rest.

---

## 🛠️ What's Included

| Component | Purpose |
|-----------|---------|
| **Core Scripts** | Update, create, and manage workflows via API |
| **Skills** | 7 expert knowledge modules for building n8n workflows |
| **Project Templates** | Example workflow structures |
| **Documentation** | Best practices and guides |

---

## ⚡ Prerequisites

Before installation, ensure you have:

| Requirement | Description |
|-------------|-------------|
| **n8n Instance** | Self-hosted or cloud (with API & MCP access enabled) |
| **Node.js 18+** | For running utility scripts |
| **Git** | For cloning this repository |
| **Agentic IDE** | Antigravity, Cursor, or any MCP-compatible AI IDE |

---

## 🚀 Installation

You can install this project in **two ways**:

### Option A: Installation with Agentic IDE (Recommended)

Use AI to set everything up for you! Open your Agentic IDE (Antigravity, Cursor, etc.) and paste this prompt:

```
Clone the n8n-workflow-manager repository from https://github.com/Kumaravel-Arumugam/n8n-workflow-manager.git and help me set it up.

Guide me through:
1. Cloning the repository
2. Installing npm dependencies
3. Creating my .env file with my n8n credentials
4. Configuring the MCP server in my IDE settings

Ask me for any information you need (my n8n URL, API key, etc.) and explain each step.
```

The AI will interactively guide you through the complete setup!

### Option B: Manual Installation

#### Step 1: Clone the Repository

```bash
git clone https://github.com/Kumaravel-Arumugam/n8n-workflow-manager.git
cd n8n-workflow-manager
```

#### Step 2: Install Dependencies

```bash
npm install
```

#### Step 3: Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit with your credentials
notepad .env  # Windows
# or: nano .env  # Linux/Mac
```

Fill in your values:
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

## 🔌 Agentic IDE MCP Setup

This connects your AI assistant to your n8n instance.

### For Antigravity IDE

1. Open Antigravity IDE
2. Go to **Chat → Additional Options (⚙️) → Manage MCP Servers**
3. Click **View Raw Config** or **Edit Config**
4. Add this configuration:

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--streamableHttp",
        "YOUR_N8N_URL/mcp-server/http",
        "--header",
        "authorization:Bearer YOUR_MCP_ACCESS_TOKEN"
      ]
    }
  }
}
```

5. Replace:
   - `YOUR_N8N_URL` → Your n8n instance URL
   - `YOUR_MCP_ACCESS_TOKEN` → Your n8n MCP token

6. Save and restart the IDE

**How to get your MCP access token:**
1. Open your n8n instance
2. Go to **Settings → MCP Server**
3. Enable MCP Server
4. Copy the access token

### For Other IDEs (Cursor, VS Code, etc.)

Check your IDE's MCP documentation and use the same configuration structure above.

---

## 📂 Project Structure

```
n8n-workflow-manager/
├── .env.example            # Environment template
├── README.md               # This file
├── package.json            # Dependencies
│
├── core/                   # Utility scripts
│   ├── index.js            # Main API functions
│   ├── update_workflow.js  # Push workflow updates
│   ├── upload_workflow.js  # Upload new workflows
│   └── find_id.js          # Find workflow IDs
│
├── skills/                 # n8n development knowledge
│   ├── n8n-expression-syntax/
│   ├── n8n-mcp-tools-expert/   # ⭐ MOST IMPORTANT
│   ├── n8n-workflow-patterns/
│   ├── n8n-validation-expert/
│   ├── n8n-node-configuration/
│   ├── n8n-code-javascript/
│   └── n8n-code-python/
│
└── projects/               # Your workflow projects
    └── job-market-analysis/    # Example project
```

---

## 💡 Usage

### With Agentic IDE

Once MCP is configured, describe what you want:

> "Create a workflow that monitors a Google Sheet and sends Slack notifications when new rows are added"

The AI will:
1. Find the right nodes using `search_nodes`
2. Create the workflow structure
3. Configure each node
4. Validate the workflow
5. Deploy to your n8n instance

### With Scripts

```bash
# Navigate to core folder
cd core

# Update a workflow
node update_workflow.js

# Find workflow IDs
node find_id.js
```

---

## 📖 Skills Reference

| Skill | Use When |
|-------|----------|
| `n8n-expression-syntax` | Writing `{{}}` expressions |
| `n8n-mcp-tools-expert` | Using MCP tools (HIGHEST PRIORITY) |
| `n8n-workflow-patterns` | Designing workflow architecture |
| `n8n-validation-expert` | Debugging validation errors |
| `n8n-node-configuration` | Setting up node parameters |
| `n8n-code-javascript` | Writing JS in Code nodes |
| `n8n-code-python` | Writing Python in Code nodes |

---

## ⚠️ Important Notes

### Security
- **Never commit `.env`** - It contains your API keys!
- The `.gitignore` already protects sensitive files

### Updating Skills
The skills may become outdated. Update from the original:

```bash
cd skills
rm -rf n8n-*  # Remove old skills
git clone https://github.com/czlonkowski/n8n-skills.git --depth 1
cp -r n8n-skills/skills/* .
rm -rf n8n-skills
```

---

## 🙏 Credits & Acknowledgments

### Skills Reference
The `skills/` folder contains knowledge modules from **Romuald Członkowski**:
- 🔗 [n8n-skills](https://github.com/czlonkowski/n8n-skills) - MIT License
- 🌐 [AI Advisors](https://www.aiadvisors.pl/en)

> ⚠️ **Note:** The skills may become outdated. Always check the [original repository](https://github.com/czlonkowski/n8n-skills) for the latest updates.

### This Project
**Created by Kumaravel Arumugam** using AI-assisted development (Antigravity IDE).

This includes:
- Core scripts (`core/` folder)
- Project structure and documentation
- MCP configuration guides
- Workflow templates

Built to remove technical barriers for non-technical users who want to create n8n automations.

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file.

Skills are licensed under MIT by Romuald Członkowski.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🐛 Issues & Support

Found a bug or have a question?
- Open an issue on [GitHub Issues](https://github.com/Kumaravel-Arumugam/n8n-workflow-manager/issues)

---

*Powered by n8n + Agentic AI + MCP*
