# 📦 Agensi.io Listing Information for Agent-Janitor

Use this exact information when uploading your skill on [https://www.agensi.io/sell](https://www.agensi.io/sell).

---

### 1. General Listing Details

* **Skill Name:** `Agent-Janitor`
* **Headline / Subtitle:** `Stop AI coding agents from chasing stale TODOs and embarking on unprompted side-quests.`
* **Pricing:** **Free ($0)** *(as recommended by Joeri for direct self-hosted MCP skill listings)*
* **Category:** `Developer Tools` / `Code Quality` / `Agent Guardrails`
* **Tags:** `mcp`, `claude-code`, `cursor`, `copilot`, `code-quality`, `anti-distraction`, `todo-cleaner`, `developer-tools`
* **File to Upload:** `agent-janitor-skill.zip` (located in your repository root)
* **Project / Server Repository:** [https://github.com/Avishek8136/Agent-Janitor](https://github.com/Avishek8136/Agent-Janitor)

---

### 2. Full Description (Copy & Paste into Agensi.io)

```markdown
### 🧹 Eliminate AI Agent Distraction & Stale TODO Side-Quests

According to empirical research by Google Developers (*"Agent Distraction"*, Nov 2026), **83% of agent actions triggered by inline TODOs are unprompted**, causing **70% more steps**, **77% more tokens**, and **105% more developer wait latency**. 

When AI coding agents read code during exploration, they don't filter out stale `// TODO` or bug comments like humans do—they treat them as literal calls to action, frequently chasing tickets that were closed years ago.

**Agent-Janitor** pairs your AI coding assistant with an automated Model Context Protocol (MCP) server that audits repositories for distraction traps, prunes confirmed dead-end comments, and neutralizes trigger keywords.

---

### 🚀 What This Skill Does

* **Audits Codebase for Traps:** Categorizes comments against Google's empirical benchmarks:
  * 🛑 **Dead-End Traps (41%):** Comments referencing tickets that are already closed or resolved.
  * ⚠️ **Scope-Creep Risks (57%):** Comments referencing open tickets that tempt agents into unauthorized code edits.
  * ⏳ **Fossil Debt:** Comments untouched for > 1 year.
* **Prunes Obsolete Dead Ends:** Automatically removes closed-ticket TODO comments without breaking code formatting or syntax.
* **Neutralizes Trigger Verbs:** Converts active action verbs (`TODO`, `FIXME`) into passive developer notes (`Note:`) so agents treat them as informational history rather than active instructions.
* **Presubmit Gate:** Provides a check command for CI/CD or pre-commit hooks to prevent closed-ticket comments from entering production.

---

### 🛠️ Compatible Coding Assistants

Works with 20+ agent platforms via stdio Model Context Protocol (MCP):
* **Claude Code & Claude Desktop**
* **Cursor (Composer / Agent)**
* **Windsurf (Cascade)**
* **GitHub Copilot**
* **Google Antigravity**

---

### 📦 Setup & Installation

This skill includes `SKILL.md`, step-by-step setup documentation, and ready-to-use MCP configuration templates for all major coding agents.

1. **Install Server:** `pip install agent-janitor` (or `pip install git+https://github.com/Avishek8136/Agent-Janitor.git`)
2. **Add MCP Config:** Copy the provided config snippet into your agent's MCP settings.
3. **Invoke:** Simply ask your agent:
   * *"Audit this repository for agent distraction traps."*
   * *"Prune all obsolete TODO comments referencing closed issues."*
   * *"Mask active TODO keywords into passive notes."*

Open-source and self-hosted: [https://github.com/Avishek8136/Agent-Janitor](https://github.com/Avishek8136/Agent-Janitor)
```
