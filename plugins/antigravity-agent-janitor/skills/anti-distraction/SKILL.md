---
name: anti-distraction
description: Audit and eliminate agent distraction traps, prune obsolete TODOs, and prevent AI scope creep in any repository. Use when reviewing codebase hygiene for AI agents, pruning dead comments, or preventing unprompted detours.
---

# Anti-Distraction & Codebase Janitor Skill

This skill allows agents to inspect and remediate "Agent Distraction" traps as discovered by Google (Nov 2026).

## Capabilities

When auditing or cleaning a codebase:
1. **Audit Traps:** Run `agent-janitor audit <path>` or use the `audit_codebase` MCP tool.
   - Categorizes traps into:
     - 🛑 **Dead-End Traps (41% risk):** Closed/resolved bugs causing wasted queries.
     - ⚠️ **Scope-Creep Traps (57% risk):** Open bugs tempting eager agents into unauthorized edits.
     - ⏳ **Fossilized Debt:** Untracked TODOs older than 1 year.
2. **Prune Obsolete Dead Ends:** Run `agent-janitor clean <path> --apply` or use the `clean_dead_ends` MCP tool with `apply: true`.
3. **Neutralize Triggers:** Run `agent-janitor mask <path> --apply` or use the `mask_triggers` MCP tool to convert `TODO/FIXME` into passive `Note:`.

## Guidelines for Agents
- Always preview diffs before applying modifications.
- Check git status after cleanups to confirm formatting and syntax are preserved.
