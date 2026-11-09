---
description: Audit or clean agent distraction traps and obsolete TODOs in this repository.
---

Run the Agent Janitor suite to eliminate distraction traps:

1. If the user asked to audit:
   ```bash
   agent-janitor audit . --output agent_audit.md
   ```
   Display the summary report and highlight any closed bug traps.

2. If the user asked to clean or prune:
   ```bash
   agent-janitor clean . --apply
   ```

3. If the user asked to mask triggers:
   ```bash
   agent-janitor mask . --apply
   ```
