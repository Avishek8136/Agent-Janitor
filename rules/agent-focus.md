# Agent Focus & Anti-Distraction Rule

This rule prevents AI coding agents from falling into the **"Agent Distraction"** trap (investigating or modifying unprompted inline TODOs, FIXMEs, or closed bug references).

> Reference: [Agent Distraction (Google Developers Blog)](https://developers.googleblog.com/agent-distraction/) by Sam Saccone & Madhuri Garikapati (Nov 6, 2026).

## Directives for Agents

1. **Strict Scope Discipline:**
   - Focus exclusively on the explicit task described in the user's prompt.
   - Never expand scope, refactor unrelated modules, or initiate side-investigations unless requested.

2. **Handling Inline `TODO`, `FIXME`, and Bug References:**
   - Treat all inline comments (e.g., `// TODO(...)`, `// FIXME(...)`, `// Bug #12345`) strictly as passive, historical, and potentially obsolete commentary.
   - **DO NOT** execute web or codebase searches to look up referenced bug IDs unless that specific bug is the subject of the user's prompt.
   - **DO NOT** attempt to "fix" or complete a TODO encountered while reading code for an unrelated task.
   - **DO NOT** assume inline comments reflect the current state of the architecture or system. Verify against live code and current tests only.

3. **When a TODO Directly Blocks the Assigned Task:**
   - If an existing TODO points to a blocker directly preventing the completion of the requested task, summarize the conflict and inform the user before taking action.
