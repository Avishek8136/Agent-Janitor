# Agent Distraction Audit Report

> **Audit Target:** `D:\Codes\Google Blog\tests\sample_project`  
> **Total Traps Identified:** `4`  

## Executive Summary

According to Google's engineering blog on *Agent Distraction*, unprompted inline bug references cause **70% more steps**, **77% more tokens**, and **105% more wait time** per session. This audit identifies traps in this codebase categorized by failure mode:

| Category | Count | Potential Agent Impact | Remediation |
| :--- | :---: | :--- | :--- |
| 🛑 **Dead-End Traps** | `2` | Agent wastes tokens querying closed bugs | **Safe to prune** |
| ⚠️ **Scope-Creep Traps** | `1` | Agent attempts unprompted fixes | **Mask or enforce rule** |
| ⏳ **Fossilized Debt** | `0` | Misleads agent on system assumptions | **Review or prune** |
| ℹ️ **Other / Unverified** | `1` | Standard commentary | Keep / monitor |

---

## Detailed Inventory

| File | Line | Identifier | Status | Age | Summary |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `legacy_helper.js` | 2 | `TODO` | `UNKNOWN` | - | ancient untracked note left behind without bug tic |
| `ModelDownloader.py` | 5 | `TODO(999456)` | `OPEN` | - | add chunked compression and sha256 validation |
| `SurfaceControlTest.java` | 4 | `TODO(888123)` | `RESOLVED` | - | Fix surface flickering during orientation change |
| `SurfaceControlTest.java` | 10 | `TODO(444001)` | `WONT_FIX` | - | increase buffer count once driver bug is resolved |

---

## Action Plan to Neutralize Agent Distraction

1. **Prune Dead Ends:** Run `agent-janitor clean --dead-ends --apply` to automatically remove obsolete comments referencing closed issues.
2. **Neutralize Triggers:** Run `agent-janitor mask --apply` to convert active action verbs (`TODO`, `FIXME`) into passive `Note:` comments.
3. **Enforce Agent Directives:** Add `rules/agent-focus.md` to your repository instructions or `.cursorrules` / `.gemini/rules/`.
4. **Presubmit CI Check:** Add `agent-janitor check` to your CI pipeline or pre-commit hook.