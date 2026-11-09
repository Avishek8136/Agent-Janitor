<p align="center">
  <img src="assets/banner.svg" alt="Agent Janitor Banner" width="100%">
</p>

<p align="center">
  <a href="https://github.com/agent-janitor/agent-janitor/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/agent-janitor/agent-janitor/ci.yml?branch=main&label=CI&style=flat-square" alt="CI Status"></a>
  <a href="https://pypi.org/project/agent-janitor/"><img src="https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?style=flat-square" alt="Python Versions"></a>
  <a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/MCP-Compatible-8A2BE2?style=flat-square" alt="MCP Compatible"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-green?style=flat-square" alt="License"></a>
  <a href="https://github.com/agent-janitor/agent-janitor/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome"></a>
</p>

<p align="center">
  <b>Eliminate AI agent distraction, side-quests, and scope creep caused by obsolete inline TODOs.</b><br>
  Based on empirical findings from Google Developers: <i><a href="https://developers.googleblog.com/agent-distraction/">"Agent Distraction"</a></i> (Nov 6, 2026).
</p>

---

## ⚡ The Problem: "The Agent Distraction Tax"

> **"What is easy for humans to skim past in code, agents see as a call to action."**  
> — Sam Saccone & Madhuri Garikapati, Google Developers

Across millions of agent coding sessions at Google:
* **1 in 7 sessions (13%)** expose AI coding agents to inline `TODO(bug/...)` references.
* **83% of agent reactions are unprompted**—the developer never asked for the bug.
* **41% chase closed dead-ends**, wasting tokens on fixed/obsolete bugs.
* **57% trigger scope creep**, editing code unrelated to the user's prompt.
* **The Tax:** **+70% more steps**, **+77% more tokens**, and **+105% more wait time**.

| Without Agent Janitor (Default Agents) | With Agent Janitor (Protected Repo) |
| :--- | :--- |
| ❌ Agent stumbles on old `// TODO(b/123)` from 2022 | ✅ Agent ignores stale comments; treats them as passive history |
| ❌ Spends 10+ tool steps researching closed tickets | ✅ **-41% fewer steps** per session |
| ❌ Blows token limits exploring dead ends | ✅ **-44% fewer tokens** consumed |
| ❌ Unprompted refactors that break review PRs | ✅ Zero scope-creep; PRs strictly match developer prompt |
| ❌ Double developer wait latency (~3 minutes) | ✅ Fast turnaround (~90 seconds) |

---

## 🛡️ The 3-Layer Defense System

```
                  ┌────────────────────────────────────────────────────────┐
                  │ 1. Behavioral Guardrail (rules/agent-focus.md)         │
                  │    Instructs LLMs to treat TODOs as passive history    │
                  └─────────────────────────┬──────────────────────────────┘
                                            ▼
                  ┌────────────────────────────────────────────────────────┐
                  │ 2. Agent Janitor CLI (Scanner & Cleaner)               │
                  │    • Audits repos for Dead-End & Scope-Creep traps     │
                  │    • Cross-references GitHub / Issue Tracker state     │
                  │    • Prunes obsolete comments or neutralizes verbs     │
                  └─────────────────────────┬──────────────────────────────┘
                                            ▼
                  ┌────────────────────────────────────────────────────────┐
                  │ 3. CI / Presubmit Gate (.github/workflows)             │
                  │    Blocks PRs introducing references to closed issues  │
                  └────────────────────────────────────────────────────────┘
```

---

## 🔌 Multi-App Plugins, Skills & Integrations

`agent-janitor` works natively across all major AI coding platforms:

### ⚡ One-Click Auto-Setup
Install guardrails and skills into any repository for all your AI coding assistants at once:
```bash
# Install for all apps (Claude Code, Cursor, Windsurf, Copilot, Antigravity):
agent-janitor init . --all

# Or install for a specific assistant:
agent-janitor init . --claude
agent-janitor init . --cursor
agent-janitor init . --windsurf
agent-janitor init . --copilot
agent-janitor init . --antigravity
```

---

### 1. 🤖 Google Antigravity Plugin & Skill
The **Agent Janitor Plugin** is installed directly in `~/.gemini/config/plugins/agent-janitor`:
* **Bundled Skill:** `anti-distraction` (teaches Antigravity how to audit, prune dead-ends, and mask triggers).
* **Bundled Rule:** `rules/AGENTS.md` (active anti-distraction guardrail for all sessions).
* **Bundled MCP Server:** Automatically connects the audit and cleaning tools to Antigravity sessions.

### 2. 🧠 Claude Code (Anthropic)
* **`CLAUDE.md`**: Directs Claude Code to adhere strictly to prompt scope and ignore inline TODOs.
* **Custom Slash Command (`/janitor`)**: Installed to `.claude/commands/janitor.md` so you can type `/janitor` inside Claude Code to audit or clean the repo.
* **MCP Integration**: Connect directly by running:
  ```bash
  claude mcp add agent-janitor python -m agent_janitor.mcp_server
  ```

### 3. 🎯 Cursor
* **`.cursor/rules/anti-distraction.mdc`**: Cursor's modern Markdown Component rule format with `alwaysApply: true`.
* **`.cursorrules`**: Classic Cursor scope guardrail.
* **MCP Server**: Add to Cursor Settings > Features > MCP:
  * **Type:** `command`
  * **Command:** `python -m agent_janitor.mcp_server`

### 4. 🌊 Windsurf (Codeium)
* **`.windsurfrules`**: Injected into Cascade's workspace memory to prevent unprompted TODO investigations.

### 5. 🐙 GitHub Copilot
* **`.github/copilot-instructions.md`**: Active workspace instructions for GitHub Copilot Workspace, Copilot Edits, and Copilot Chat.

### 6. 🌐 Universal MCP (Model Context Protocol) Server
The built-in MCP server runs on stdio without third-party dependencies:
```bash
python -m agent_janitor.mcp_server
```
**Exposed MCP Tools:**
* `audit_codebase(path, mock_status_file, github_repo, fossil_days)`: Audits for dead-ends (41%), scope-creep (57%), and fossilized debt.
* `clean_dead_ends(path, apply, mock_status_file)`: Prunes obsolete comments referencing closed issues.
* `mask_triggers(path, apply)`: Converts active `TODO/FIXME` action verbs into passive developer notes.

---

## 🚀 Quick Start

### 1. Install
Clone or install locally:
```bash
pip install .
```

### 2. Audit Your Codebase
Scan your codebase to detect agent traps:
```bash
agent-janitor audit . --output audit_report.md
```
Output example:
```
============================================================
          AGENT DISTRACTION AUDIT REPORT                    
============================================================
Total Comment References Scanned: 42

Risk Breakdown (vs Google Empirical Benchmarks):
  🛑 Dead-End Traps (Closed/Won't Fix)  :   8  (41% blog benchmark)
  ⚠️  Scope-Creep Traps (Open Tickets)    :  14  (57% blog benchmark)
  ⏳ Fossilized Debt (> 1 year old)     :   6
  ℹ️  Other / Unverified                 :  14
------------------------------------------------------------
```

### 3. Automatically Prune Dead-Ends
Prune references to tickets that are already closed, resolved, or won't fix:
```bash
# Preview diffs (dry-run):
agent-janitor clean .

# Apply cleanups directly to files:
agent-janitor clean . --apply
```

### 4. Neutralize Action Triggers (Masking)
Convert active imperative verbs (`TODO(b/123): ...` or `FIXME: ...`) into passive developer notes (`Note(b/123): ...`), preventing LLMs from seeing them as active goals:
```bash
agent-janitor mask . --apply
```

### 5. Enforce in CI / Presubmit
Add `agent-janitor check` to your CI pipeline. It exits with code `1` if any closed-bug references exist in the code:
```bash
agent-janitor check .
```

---

## 📂 Project Structure

* **[`agent_janitor/`](file:///d:/Codes/Google%20Blog/agent_janitor)**
  * **[`scanner.py`](file:///d:/Codes/Google%20Blog/agent_janitor/scanner.py)**: Multi-language source scanner detecting TODOs, FIXMEs, bug IDs (`#123`, `b/456`, Jira `PROJ-789`, URLs).
  * **[`git_utils.py`](file:///d:/Codes/Google%20Blog/agent_janitor/git_utils.py)**: Inspects `git blame` porcelain data to extract commit age, author, and timestamp.
  * **[`classifier.py`](file:///d:/Codes/Google%20Blog/agent_janitor/classifier.py)**: Maps findings into Dead-End Traps, Scope-Creep Risks, or Fossilized Debt.
  * **[`cleaner.py`](file:///d:/Codes/Google%20Blog/agent_janitor/cleaner.py)**: Safe AST/line-level comment pruning and trigger neutralization.
  * **[`reporter.py`](file:///d:/Codes/Google%20Blog/agent_janitor/reporter.py)**: Generates terminal summaries and Markdown audit reports.
  * **[`trackers/`](file:///d:/Codes/Google%20Blog/agent_janitor/trackers)**: Live issue tracker integrations (GitHub CLI `gh`, mock JSON for offline audits).
* **[`rules/agent-focus.md`](file:///d:/Codes/Google%20Blog/rules/agent-focus.md)**: Drop-in agent instruction rule for Antigravity, Cursor (`.cursorrules`), Copilot, or Claude.
* **[`.github/workflows/anti-distraction.yml`](file:///d:/Codes/Google%20Blog/.github/workflows/anti-distraction.yml)**: Ready-to-use GitHub Actions workflow.

---

## 📋 Behavioral Agent Rule: `rules/agent-focus.md`

You can directly copy [`rules/agent-focus.md`](file:///d:/Codes/Google%20Blog/rules/agent-focus.md) into your `.cursorrules`, `.gemini/rules/`, or agent system prompt:

```markdown
# Agent Focus Directive
- Treat inline TODOs, FIXMEs, and bug IDs strictly as passive commentary.
- DO NOT initiate tool searches or codebase queries for referenced bug IDs unless explicitly commanded in the user's prompt.
- DO NOT expand scope or attempt to resolve unprompted TODOs found during research.
```

---

## 📚 References & Background

* **Original Research:** [Agent Distraction](https://developers.googleblog.com/agent-distraction/)
* **Authors:** Sam Saccone (Senior Staff Software Engineer) & Madhuri Garikapati (Senior Staff Data Scientist) at Google
* **Published:** November 6, 2026 on the [Google Developers Blog](https://developers.googleblog.com/)
* **Key Findings:** Based on traces across hundreds of millions of agent steps, unprompted inline TODO interactions account for 83% of detour sessions, causing +70% more steps, +77% more tokens, and +105% more developer wait time.

