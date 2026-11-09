# Agent Distraction & Scope Protection

According to empirical research by Google (Nov 2026, [Agent Distraction](https://developers.googleblog.com/agent-distraction/)), 83% of agent actions triggered by inline TODOs are unprompted, increasing session steps by 70% and tokens by 77%.

## Directives for All Agents
1. **Strict Scope Discipline:**
   - Adhere strictly to the explicit goal requested in the user's prompt.
   - Do not investigate, research, or modify code related to inline `TODO(bug/...)`, `FIXME`, or bug references unless that bug was explicitly commanded by the user.

2. **Treat Inline Bugs & Comments as Passive History:**
   - Do not query bug trackers or search the codebase to understand old TODOs found during unrelated exploration.
   - 41% of unprompted detours chase tickets that are already closed or obsolete. Do not assume comments reflect current truth.

3. **Grooming Codebase:**
   - When asked to clean or audit the codebase for agent friendliness, use the `agent-janitor` tools or CLI to prune dead-ends and mask actionable trigger words.
