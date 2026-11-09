# Agent-Janitor Setup & Configuration Guide

This guide walks you through installing the **Agent-Janitor** MCP server, connecting it to your AI coding agent (Claude Code, Cursor, Windsurf, Copilot, Antigravity), and invoking the skill.

Repository: [https://github.com/Avishek8136/Agent-Janitor](https://github.com/Avishek8136/Agent-Janitor)

---

## 1. Prerequisites

* **Python:** Version 3.9 or higher installed. Verify with:
  ```bash
  python --version
  ```
* **Git:** Installed on your system.

---

## 2. Install Agent-Janitor

Install `agent-janitor` into your environment:

```bash
# Option A: From PyPI
pip install agent-janitor

# Option B: Direct from GitHub
pip install git+https://github.com/Avishek8136/Agent-Janitor.git
```

Verify that the CLI is accessible:
```bash
agent-janitor --help
```

---

## 3. Configure the MCP Server in Your AI Agent

Agent-Janitor includes a native, zero-dependency stdio **Model Context Protocol (MCP)** server:
`python -m agent_janitor.mcp_server`

Add this configuration to your preferred coding agent:

### 🤖 Claude Code (Anthropic)
Run this single command in your terminal:
```bash
claude mcp add agent-janitor python -m agent_janitor.mcp_server
```

### 🖥️ Claude Desktop
Add to your `claude_desktop_config.json`:
* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "agent-janitor": {
      "command": "python",
      "args": ["-m", "agent_janitor.mcp_server"]
    }
  }
}
```

### 🎯 Cursor
1. Go to **Cursor Settings** ➔ **Features** ➔ **MCP**.
2. Click **+ Add New MCP Server**.
3. Set the fields:
   * **Name:** `agent-janitor`
   * **Type:** `command`
   * **Command:** `python -m agent_janitor.mcp_server`

### 🌊 Windsurf (Codeium)
Add to your Windsurf MCP configuration (`~/.codeium/windsurf/mcp_config.json`):
```json
{
  "mcpServers": {
    "agent-janitor": {
      "command": "python",
      "args": ["-m", "agent_janitor.mcp_server"]
    }
  }
}
```

### 🌌 Google Antigravity
Add to your `mcp_config.json` (or install the plugin via `agent-janitor init . --antigravity`):
```json
{
  "mcpServers": {
    "agent-janitor": {
      "command": "python",
      "args": ["-m", "agent_janitor.mcp_server"]
    }
  }
}
```

---

## 4. How to Invoke the Skill

Once configured, your agent automatically recognizes the `audit_codebase`, `clean_dead_ends`, and `mask_triggers` tools. You can invoke the skill simply by talking to your agent:

### Example Prompts:

* *"Audit this repository for agent distraction traps and stale TODOs."*
* *"Check if any inline TODOs in our codebase point to closed or resolved tickets."*
* *"Prune all obsolete TODO comments referencing closed issues in this repository."*
* *"Mask active TODO trigger keywords into passive developer notes to prevent LLM distractions."*
* *"Run an agent distraction presubmit check before I push this PR."*

---

## 5. Verification

To verify that the MCP server runs correctly on your machine, run:
```bash
agent-janitor audit .
```
You should see the ASCII report categorizing Dead-End Traps, Scope-Creep Risks, and Fossil Debt across your files.
