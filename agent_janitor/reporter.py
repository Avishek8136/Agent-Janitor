from pathlib import Path
from typing import List
from .models import TodoItem, TrapClassification

def generate_terminal_summary(items: List[TodoItem]) -> str:
    total = len(items)
    dead_ends = [i for i in items if i.classification == TrapClassification.DEAD_END]
    scope_creeps = [i for i in items if i.classification == TrapClassification.SCOPE_CREEP_RISK]
    fossils = [i for i in items if i.classification == TrapClassification.FOSSIL]
    unknowns = [i for i in items if i.classification in (TrapClassification.UNKNOWN, TrapClassification.ACTIVE)]

    lines = [
        "============================================================",
        "          AGENT DISTRACTION AUDIT REPORT                    ",
        "============================================================",
        f"Total Comment References Scanned: {total}",
        "",
        "Risk Breakdown (vs Google Empirical Benchmarks):",
        f"  🛑 Dead-End Traps (Closed/Won't Fix)  : {len(dead_ends):>3}  (41% blog benchmark)",
        f"  ⚠️  Scope-Creep Traps (Open Tickets)    : {len(scope_creeps):>3}  (57% blog benchmark)",
        f"  ⏳ Fossilized Debt (> 1 year old)     : {len(fossils):>3}",
        f"  ℹ️  Other / Unverified                 : {len(unknowns):>3}",
        "------------------------------------------------------------",
    ]

    if dead_ends:
        lines.append("\n🛑 High-Risk Dead Ends (Agent will waste tokens investigating):")
        for item in dead_ends[:10]:
            ticket_str = f"[{item.ticket_status.value}]"
            lines.append(f"  • {item.file_path.name}:{item.line_number} -> {item.display_tag} {ticket_str}: {item.description[:60]}")
        if len(dead_ends) > 10:
            lines.append(f"  ... and {len(dead_ends) - 10} more.")

    if scope_creeps:
        lines.append("\n⚠️  Scope Creep Risks (Agent may attempt unprompted code edits):")
        for item in scope_creeps[:10]:
            lines.append(f"  • {item.file_path.name}:{item.line_number} -> {item.display_tag} [OPEN]: {item.description[:60]}")
        if len(scope_creeps) > 10:
            lines.append(f"  ... and {len(scope_creeps) - 10} more.")

    lines.append("============================================================")
    return "\n".join(lines)


def generate_markdown_report(items: List[TodoItem], repo_dir: Path) -> str:
    total = len(items)
    dead_ends = [i for i in items if i.classification == TrapClassification.DEAD_END]
    scope_creeps = [i for i in items if i.classification == TrapClassification.SCOPE_CREEP_RISK]
    fossils = [i for i in items if i.classification == TrapClassification.FOSSIL]
    unknowns = [i for i in items if i.classification in (TrapClassification.UNKNOWN, TrapClassification.ACTIVE)]

    md = [
        "# Agent Distraction Audit Report",
        "",
        f"> **Audit Target:** `{repo_dir}`  ",
        f"> **Total Traps Identified:** `{total}`  ",
        "",
        "## Executive Summary",
        "",
        "According to Google's engineering blog on *Agent Distraction*, unprompted inline bug references cause **70% more steps**, **77% more tokens**, and **105% more wait time** per session. This audit identifies traps in this codebase categorized by failure mode:",
        "",
        "| Category | Count | Potential Agent Impact | Remediation |",
        "| :--- | :---: | :--- | :--- |",
        f"| 🛑 **Dead-End Traps** | `{len(dead_ends)}` | Agent wastes tokens querying closed bugs | **Safe to prune** |",
        f"| ⚠️ **Scope-Creep Traps** | `{len(scope_creeps)}` | Agent attempts unprompted fixes | **Mask or enforce rule** |",
        f"| ⏳ **Fossilized Debt** | `{len(fossils)}` | Misleads agent on system assumptions | **Review or prune** |",
        f"| ℹ️ **Other / Unverified** | `{len(unknowns)}` | Standard commentary | Keep / monitor |",
        "",
        "---",
        "",
        "## Detailed Inventory",
        "",
        "| File | Line | Identifier | Status | Age | Summary |",
        "| :--- | :---: | :--- | :---: | :---: | :--- |",
    ]

    for item in items:
        rel_path = item.file_path.relative_to(repo_dir) if repo_dir in item.file_path.parents else item.file_path.name
        age_str = f"{item.age_days}d" if item.age_days is not None else "-"
        status_badge = f"`{item.ticket_status.value}`"
        desc_escaped = item.description.replace("|", "\\|")[:50]
        md.append(f"| `{rel_path}` | {item.line_number} | `{item.display_tag}` | {status_badge} | {age_str} | {desc_escaped} |")

    md.extend([
        "",
        "---",
        "",
        "## Action Plan to Neutralize Agent Distraction",
        "",
        "1. **Prune Dead Ends:** Run `agent-janitor clean --dead-ends --apply` to automatically remove obsolete comments referencing closed issues.",
        "2. **Neutralize Triggers:** Run `agent-janitor mask --apply` to convert active action verbs (`TODO`, `FIXME`) into passive `Note:` comments.",
        "3. **Enforce Agent Directives:** Add `rules/agent-focus.md` to your repository instructions or `.cursorrules` / `.gemini/rules/`.",
        "4. **Presubmit CI Check:** Add `agent-janitor check` to your CI pipeline or pre-commit hook.",
    ])

    return "\n".join(md)
