import json
import sys
from pathlib import Path
from typing import Any, Dict

from .scanner import Scanner
from .models import TrapClassification
from .classifier import classify_todo
from .cleaner import CodeCleaner
from .trackers.github_tracker import GitHubTracker
from .trackers.mock_tracker import MockTracker
from .reporter import generate_terminal_summary, generate_markdown_report

TOOLS = [
    {
        "name": "audit_codebase",
        "description": "Scans repository for Agent Distraction traps: closed-bug references (dead-ends), open-bug scope-creep risks, and ancient fossilized TODOs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory or file to scan (defaults to current directory).",
                    "default": "."
                },
                "mock_status_file": {
                    "type": "string",
                    "description": "Optional path to JSON mapping bug IDs to statuses (for offline testing)."
                },
                "github_repo": {
                    "type": "string",
                    "description": "Optional GitHub repo in 'owner/repo' format for issue verification."
                },
                "fossil_days": {
                    "type": "integer",
                    "description": "Age in days to consider an untracked TODO a fossil (default: 365).",
                    "default": 365
                }
            }
        }
    },
    {
        "name": "clean_dead_ends",
        "description": "Removes obsolete inline TODO/FIXME comments that reference closed or resolved tickets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to clean (defaults to current directory).",
                    "default": "."
                },
                "apply": {
                    "type": "boolean",
                    "description": "If true, writes changes to files. If false, returns diff preview.",
                    "default": False
                },
                "mock_status_file": {
                    "type": "string",
                    "description": "Optional path to mock statuses JSON."
                }
            }
        }
    },
    {
        "name": "mask_triggers",
        "description": "Neutralizes active action tags (TODO, FIXME) into passive 'Note:' comments to prevent LLM agent distraction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to mask (defaults to current directory).",
                    "default": "."
                },
                "apply": {
                    "type": "boolean",
                    "description": "If true, writes changes to files. If false, returns diff preview.",
                    "default": False
                }
            }
        }
    }
]

def scan_and_classify(target_dir: Path, mock_file: str = None, gh_repo: str = None, fossil_days: int = 365):
    scanner = Scanner(target_dir)
    items = list(scanner.scan_all())
    tracker = MockTracker(mock_file) if mock_file else GitHubTracker(repo_override=gh_repo)

    for item in items:
        if item.bug_id:
            item.ticket_status = tracker.check_status(item.bug_id)
        item.classification = classify_todo(item, fossil_age_days=fossil_days)

    return items

def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    target_path = Path(arguments.get("path", ".")).resolve()

    if name == "audit_codebase":
        items = scan_and_classify(
            target_path,
            mock_file=arguments.get("mock_status_file"),
            gh_repo=arguments.get("github_repo"),
            fossil_days=arguments.get("fossil_days", 365)
        )
        summary = generate_terminal_summary(items)
        md = generate_markdown_report(items, target_path)
        return {
            "content": [
                {"type": "text", "text": f"{summary}\n\n## Full Markdown Report:\n\n{md}"}
            ]
        }

    elif name == "clean_dead_ends":
        items = scan_and_classify(
            target_path,
            mock_file=arguments.get("mock_status_file")
        )
        dead_ends = [i for i in items if i.classification == TrapClassification.DEAD_END]
        if not dead_ends:
            return {"content": [{"type": "text", "text": "No dead-end traps found. Codebase is clean."}]}

        apply = arguments.get("apply", False)
        cleaner = CodeCleaner(dry_run=not apply)
        diffs = cleaner.prune_items(dead_ends)

        diff_text = "\n".join(f"File: {p.name}\n{d}" for p, d in diffs)
        status = "APPLIED CHANGES" if apply else "DRY RUN PREVIEW (set apply=true to execute)"
        return {"content": [{"type": "text", "text": f"[{status}]\n\n{diff_text}"}]}

    elif name == "mask_triggers":
        scanner = Scanner(target_path)
        items = list(scanner.scan_all())
        apply = arguments.get("apply", False)
        cleaner = CodeCleaner(dry_run=not apply)
        diffs = cleaner.mask_triggers(items)

        diff_text = "\n".join(f"File: {p.name}\n{d}" for p, d in diffs)
        status = "APPLIED CHANGES" if apply else "DRY RUN PREVIEW (set apply=true to execute)"
        return {"content": [{"type": "text", "text": f"[{status}]\n\n{diff_text}"}]}

    else:
        return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

def run_mcp_server():
    # Make sure stdin/stdout handles UTF-8
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except Exception:
            continue

        req_id = req.get("id")
        method = req.get("method")

        if method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "agent-janitor",
                        "version": "0.1.0"
                    }
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "notifications/initialized":
            # No response needed for notification
            pass

        elif method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": TOOLS}
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            result = handle_call_tool(name, arguments)
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": result
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        else:
            if req_id is not None:
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()

if __name__ == "__main__":
    run_mcp_server()
