# Agent Distraction Audit Report

> **Audit Target:** `D:\Codes\Google Blog\benchmark\corpus`  
> **Total Traps Identified:** `8`  

## Executive Summary

According to Google's engineering blog on *Agent Distraction*, unprompted inline bug references cause **70% more steps**, **77% more tokens**, and **105% more wait time** per session. This audit identifies traps in this codebase categorized by failure mode:

| Category | Count | Potential Agent Impact | Remediation |
| :--- | :---: | :--- | :--- |
| 🛑 **Dead-End Traps** | `4` | Agent wastes tokens querying closed bugs | **Safe to prune** |
| ⚠️ **Scope-Creep Traps** | `3` | Agent attempts unprompted fixes | **Mask or enforce rule** |
| ⏳ **Fossilized Debt** | `0` | Misleads agent on system assumptions | **Review or prune** |
| ℹ️ **Other / Unverified** | `1` | Standard commentary | Keep / monitor |

---

## Detailed Inventory

| File | Line | Identifier | Status | Age | Summary |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `auth_service.py` | 11 | `TODO(AUTH-101)` | `RESOLVED` | - | remove deprecated sha1 fallback once migration com |
| `auth_service.py` | 17 | `TODO(SEC-606)` | `RESOLVED` | - | rotate session key on refresh |
| `database_pool.rs` | 7 | `TODO(DB-404)` | `CLOSED` | - | upgrade connection health check to ping socket dir |
| `database_pool.rs` | 11 | `TODO` | `UNKNOWN` | - | ancient untracked note left behind without ticket |
| `payment_gateway.ts` | 8 | `TODO(PAY-202)` | `OPEN` | - | implement webhook idempotency key deduplication |
| `payment_gateway.ts` | 14 | `TODO(CORE-707)` | `OPEN` | - | rewrite retry logic to use exponential backoff wit |
| `render_pipeline.cpp` | 7 | `TODO(GFX-303)` | `WONT_FIX` | - | increase to 32 once legacy Vulkan driver is deprec |
| `render_pipeline.cpp` | 11 | `TODO(NET-505)` | `OPEN` | - | streaming asset decompression in background thread |

---

## Action Plan to Neutralize Agent Distraction

1. **Prune Dead Ends:** Run `agent-janitor clean --dead-ends --apply` to automatically remove obsolete comments referencing closed issues.
2. **Neutralize Triggers:** Run `agent-janitor mask --apply` to convert active action verbs (`TODO`, `FIXME`) into passive `Note:` comments.
3. **Enforce Agent Directives:** Add `rules/agent-focus.md` to your repository instructions or `.cursorrules` / `.gemini/rules/`.
4. **Presubmit CI Check:** Add `agent-janitor check` to your CI pipeline or pre-commit hook.