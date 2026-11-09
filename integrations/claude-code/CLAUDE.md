# CLAUDE.md - Anti-Distraction & Scope Discipline

## Scope Discipline & Handling Inline Bug/TODO Comments
According to research by Google (Nov 2026, [Agent Distraction](https://developers.googleblog.com/agent-distraction/)), 83% of agent reactions to inline TODOs/bugs are unprompted, leading to 70% more steps and 77% more tokens.

1. **Strict Prompt Boundaries:**
   - Focus exclusively on the user's requested task.
   - Never initiate unprompted investigations, searches, or code modifications for inline `TODO`, `FIXME`, or bug tickets (`#123`, `b/456`, Jira keys) encountered during code reading.
2. **Treat Stale Comments as Passive History:**
   - 41% of unprompted bug detours chase tickets that are already closed or obsolete. Do not assume comments reflect current code state.
3. **Repository Grooming:**
   - When requested to clean or audit the repository, run `agent-janitor audit .` or `agent-janitor clean . --apply`.
