---
name: agent-janitor
description: Eliminates AI agent distraction, side-quests, and scope creep caused by obsolete inline TODOs. Audits codebases for distraction traps, prunes dead-end comments referencing closed bug tickets, and neutralizes trigger keywords using the Agent-Janitor MCP server.
---

# Agent-Janitor: Codebase Anti-Distraction & Scope Protection

This skill protects AI coding agents (Claude, Cursor, Windsurf, Copilot, Antigravity) from the **"Agent Distraction"** trap identified in Google's empirical research (Nov 2026). When agents read code containing stale `TODO(bug/...)` comments, 83% of reactions are unprompted, inflating session steps by 70%, tokens by 77%, and wait time by 105%.

Use this skill whenever you need to audit repository hygiene, eliminate stale comment debt, or prevent unprompted agent side-quests.

---

## 🛠️ Available MCP Tools

When the `agent-janitor` MCP server is active, the following tools are available:

### 1. `audit_codebase`
Scans a repository or directory for distraction traps and classifies comments against Google's empirical failure modes:
* **Parameters:**
  * `path` (string, optional, default: `.`): Path to the codebase or directory to scan.
  * `github_repo` (string, optional): Target GitHub repository in `owner/repo` format for live issue lookup.
  * `mock_status_file` (string, optional): Path to a JSON file mapping bug IDs to statuses for offline auditing.
  * `fossil_days` (integer, optional, default: `365`): Age threshold in days to flag an untracked comment as fossil debt.
* **Returns:**
  * Comprehensive risk breakdown:
    * 🛑 **Dead-End Traps (41%):** Comments referencing tickets that are `CLOSED`, `RESOLVED`, or `WONT_FIX`.
    * ⚠️ **Scope-Creep Traps (57%):** Comments referencing active `OPEN` tickets that tempt unprompted agent edits.
    * ⏳ **Fossil Debt:** Comments untouched for > 1 year.
  * Full file-by-file inventory and line numbers.

### 2. `clean_dead_ends`
Safely prunes obsolete inline `TODO`/`FIXME` comments that point to resolved, closed, or won't-fix tickets.
* **Parameters:**
  * `path` (string, optional, default: `.`): Directory or file to clean.
  * `apply` (boolean, optional, default: `false`): If `false`, generates and returns a unified git diff preview without modifying files. If `true`, applies the edits safely.
  * `mock_status_file` (string, optional): Path to mock ticket status registry.
* **Safety:** Standalone comment lines are cleanly removed. Inline comments trailing code (`int x = 5; // TODO(...)`) are trimmed while preserving code syntax and formatting.

### 3. `mask_triggers`
Neutralizes active action verbs (`TODO`, `FIXME`, `BUG`) into passive developer notes (`Note:`) for comments that developers wish to keep.
* **Parameters:**
  * `path` (string, optional, default: `.`): Directory to mask.
  * `apply` (boolean, optional, default: `false`): Preview diff if `false`, apply edits if `true`.
* **Benefit:** Preserves human developer context while preventing LLMs from misinterpreting comments as actionable instructions.

---

## 💻 CLI Fallback (If MCP Server is Not Configured)

If the MCP tools are not directly loaded in the agent session, invoke the equivalent CLI commands in the workspace terminal:

```bash
# 1. Audit repository for traps
agent-janitor audit . --output audit_report.md

# 2. Preview dead-end comment pruning diffs
agent-janitor clean .

# 3. Apply dead-end comment pruning
agent-janitor clean . --apply

# 4. Neutralize trigger keywords into passive notes
agent-janitor mask . --apply

# 5. Run CI presubmit check (fails if closed-bug comments exist)
agent-janitor check .
```

---

## 📋 Directives for Agents

When operating inside any codebase:
1. **Strict Scope Discipline:** Focus exclusively on the user's prompt. Do not pursue inline bugs or TODOs found during exploration unless explicitly asked.
2. **Treat Inline Comments as Passive History:** 41% of unprompted detours chase tickets that are already closed or obsolete. Never assume inline comments reflect the current state of the architecture.
3. **Safe Cleanup:** Always review diffs before applying changes, and run project tests afterward to verify that syntax and logic remain 100% intact.
