# n8n Workflow Manager

> **Build n8n workflows through natural language prompts using AI + MCP.**

Remove the technical barrier. Describe what automation you want → AI creates the workflow.

---

## 🎯 What Is This?

This project enables **non-technical users** to create n8n automations by simply describing what they want. Instead of manually building workflows, you:

1. Open Antigravity IDE (or any MCP-compatible AI)
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
| **Skills** | Expert knowledge for building n8n workflows |
| **Project Templates** | Example workflow structures |

---

## ⚡ Prerequisites

Before setup, you need:

1. **n8n Instance** - Self-hosted or cloud (with API access)
2. **Antigravity IDE** - Download from [Google DeepMind](https://deepmind.google/)
3. **Node.js 18+** - For running scripts
4. **Git** - For cloning this repo

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/n8n-workflow-manager.git
cd n8n-workflow-manager/n8n-manager
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Configure Environment

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
2. Go to Settings → API
3. Create a new API key
4. Copy the key

---

## 🔌 Antigravity MCP Setup

This is the **key step** that connects AI to your n8n instance.

### Step 1: Open Antigravity IDE

### Step 2: Access MCP Settings
1. Click the **Chat** section
2. Click **Additional Options** (⚙️ icon)
3. Click **Manage MCP Servers**

### Step 3: View Raw Config
1. Click **View Raw Config** or **Edit Config**
2. You'll see a JSON file

### Step 4: Add n8n-mcp Server

Add this to your `mcp_config.json`:

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

**Replace:**
- `YOUR_N8N_URL` → Your n8n instance URL (e.g., `https://my-n8n.ngrok.dev`)
- `YOUR_MCP_ACCESS_TOKEN` → Your n8n MCP access token

**How to get your MCP access token:**
1. Open your n8n instance
2. Go to Settings → MCP Server
3. Enable MCP Server
4. Copy the access token

### Step 5: Save and Restart
1. Save the config file
2. Restart Antigravity IDE
3. The n8n-mcp server should now appear in your MCP servers list

---

## 📂 Project Structure

```
n8n-manager/
├── .env                    # Your credentials (NEVER commit!)
├── .env.example            # Template for credentials
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
│   ├── n8n-mcp-tools-expert/   # MOST IMPORTANT
│   ├── n8n-workflow-patterns/
│   ├── n8n-validation-expert/
│   ├── n8n-node-configuration/
│   ├── n8n-code-javascript/
│   └── n8n-code-python/
│
├── projects/               # Your workflow projects
│   └── job-market-analysis/    # Example project
│
└── archive/                # Large files (gitignored)
```

---

## 💡 Usage

### Using with Antigravity AI

Once MCP is configured, just describe what you want:

> "Create a workflow that monitors a Google Sheet and sends Slack notifications when new rows are added"

The AI will:
1. Find the right nodes using `search_nodes`
2. Create the workflow structure
3. Configure each node
4. Validate the workflow
5. Deploy to your n8n instance

### Using the Scripts

```bash
# Update a workflow
cd core
node update_workflow.js

# Find workflow IDs
node find_id.js
```

---

## ⚠️ Important Notes

### What NOT to Commit
- `.env` - Contains your API keys!
- `node_modules/` - Reinstall with npm
- `archive/` - Large personal files

### Updating Skills
The skills folder may become outdated. Update from the original:

```bash
cd skills
git clone https://github.com/czlonkowski/n8n-skills.git --depth 1
```

---

## 🙏 Credits

### n8n-skills & n8n-mcp
The skills and MCP server are created by **Romuald Członkowski**.

- **n8n-skills**: https://github.com/czlonkowski/n8n-skills
- **n8n-mcp**: https://github.com/czlonkowski/n8n-mcp
- **Website**: https://www.aiadvisors.pl/en

> ⚠️ **Note:** Always check the original repositories for the latest updates. Skills in this repo may be outdated.

### This Project
Built on top of n8n-mcp to provide a complete setup for non-technical users to create automations using AI.

---

## 📜 License

MIT License - See LICENSE file.

Skills are licensed under MIT by Romuald Członkowski.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

*Powered by n8n + Antigravity AI + MCP*
