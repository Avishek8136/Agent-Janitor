import argparse
import sys
from pathlib import Path
from typing import List

# Ensure utf-8 stdout on Windows consoles if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from .scanner import Scanner
from .models import TodoItem, TrapClassification
from .classifier import classify_todo
from .git_utils import is_git_repo, get_git_blame_info
from .trackers.github_tracker import GitHubTracker
from .trackers.mock_tracker import MockTracker
from .cleaner import CodeCleaner
from .reporter import generate_terminal_summary, generate_markdown_report

def run_scan_and_classify(
    target_dir: Path,
    mock_status_file: str = None,
    github_repo: str = None,
    fossil_days: int = 365
) -> List[TodoItem]:
    scanner = Scanner(root_dir=target_dir)
    raw_items = list(scanner.scan_all())

    # Set up tracker
    if mock_status_file:
        tracker = MockTracker(mock_status_file)
    else:
        tracker = GitHubTracker(repo_override=github_repo)

    has_git = is_git_repo(target_dir)

    for item in raw_items:
        # Check tracker status if bug_id exists
        if item.bug_id:
            item.ticket_status = tracker.check_status(item.bug_id)

        # Check git blame if inside git repo
        if has_git:
            h, auth, dt, age = get_git_blame_info(item.file_path, item.line_number)
            item.commit_hash = h
            item.author = auth
            item.commit_date = dt
            item.age_days = age

        # Classify
        item.classification = classify_todo(item, fossil_age_days=fossil_days)

    return raw_items


def handle_audit(args):
    target_dir = Path(args.path).resolve()
    print(f"Scanning '{target_dir}' for agent distraction traps...")

    items = run_scan_and_classify(
        target_dir=target_dir,
        mock_status_file=args.mock_status,
        github_repo=args.github_repo,
        fossil_days=args.fossil_days
    )

    summary = generate_terminal_summary(items)
    print("\n" + summary)

    if args.output:
        out_path = Path(args.output).resolve()
        md = generate_markdown_report(items, target_dir)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"\n[OK] Detailed Markdown report written to: {out_path}")


def handle_clean(args):
    target_dir = Path(args.path).resolve()
    print(f"Checking for obsolete dead-end traps in '{target_dir}'...")

    items = run_scan_and_classify(
        target_dir=target_dir,
        mock_status_file=args.mock_status,
        github_repo=args.github_repo,
        fossil_days=args.fossil_days
    )

    # Filter for dead ends
    dead_ends = [i for i in items if i.classification == TrapClassification.DEAD_END]
    if not dead_ends:
        print("[OK] No dead-end traps found! Repository is clean.")
        return

    print(f"Found {len(dead_ends)} dead-end traps (closed/resolved bug references).")
    cleaner = CodeCleaner(dry_run=not args.apply)
    diffs = cleaner.prune_items(dead_ends)

    for file_path, diff in diffs:
        print(f"\n--- Changes for {file_path.name} ---")
        print(diff)

    if not args.apply:
        print("\n[DRY RUN] No files modified. Run with '--apply' to apply these changes.")
    else:
        print(f"\n[APPLIED] Successfully cleaned up {len(dead_ends)} obsolete TODO comments.")


def handle_mask(args):
    target_dir = Path(args.path).resolve()
    print(f"Masking provocative agent triggers in '{target_dir}'...")

    scanner = Scanner(root_dir=target_dir)
    items = list(scanner.scan_all())

    cleaner = CodeCleaner(dry_run=not args.apply)
    diffs = cleaner.mask_triggers(items)

    for file_path, diff in diffs:
        print(f"\n--- Changes for {file_path.name} ---")
        print(diff)

    if not args.apply:
        print("\n[DRY RUN] No files modified. Run with '--apply' to neutralize triggers.")
    else:
        print(f"\n[APPLIED] Successfully neutralized triggers across {len(diffs)} files.")


def handle_check(args):
    target_dir = Path(args.path).resolve()
    items = run_scan_and_classify(
        target_dir=target_dir,
        mock_status_file=args.mock_status,
        github_repo=args.github_repo,
        fossil_days=args.fossil_days
    )

    dead_ends = [i for i in items if i.classification == TrapClassification.DEAD_END]
    if dead_ends:
        print(f"[CI FAIL] Detected {len(dead_ends)} dead-end traps in code!")
        for item in dead_ends:
            print(f"  • {item.file_path.name}:{item.line_number} -> {item.display_tag} [{item.ticket_status.value}]")
        sys.exit(1)
    else:
        print("[CI PASS] No dead-end distraction traps found.")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        prog="agent-janitor",
        description="Neutralize agent distraction traps, prune obsolete TODOs, and prevent AI scope creep."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Audit codebase for agent distraction traps")
    audit_parser.add_argument("path", nargs="?", default=".", help="Path to repository or directory")
    audit_parser.add_argument("--output", "-o", help="Path to write Markdown audit report")
    audit_parser.add_argument("--mock-status", help="JSON file mapping bug IDs to statuses (for offline/testing)")
    audit_parser.add_argument("--github-repo", help="Target GitHub repo (e.g. owner/repo)")
    audit_parser.add_argument("--fossil-days", type=int, default=365, help="Days threshold for fossil debt (default: 365)")
    audit_parser.set_defaults(func=handle_audit)

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Prune obsolete/closed TODO references")
    clean_parser.add_argument("path", nargs="?", default=".", help="Path to repository or directory")
    clean_parser.add_argument("--apply", action="store_true", help="Apply file edits (default is dry-run preview)")
    clean_parser.add_argument("--mock-status", help="JSON file mapping bug IDs to statuses")
    clean_parser.add_argument("--github-repo", help="Target GitHub repo")
    clean_parser.add_argument("--fossil-days", type=int, default=365)
    clean_parser.set_defaults(func=handle_clean)

    # Mask command
    mask_parser = subparsers.add_parser("mask", help="Neutralize TODO action words into passive Notes")
    mask_parser.add_argument("path", nargs="?", default=".", help="Path to repository or directory")
    mask_parser.add_argument("--apply", action="store_true", help="Apply file edits (default is dry-run preview)")
    mask_parser.set_defaults(func=handle_mask)

    # Check command (CI)
    check_parser = subparsers.add_parser("check", help="Run CI check (fails if closed bug references exist)")
    check_parser.add_argument("path", nargs="?", default=".", help="Path to repository or directory")
    check_parser.add_argument("--mock-status", help="JSON file mapping bug IDs to statuses")
    check_parser.add_argument("--github-repo", help="Target GitHub repo")
    check_parser.add_argument("--fossil-days", type=int, default=365)
    check_parser.set_defaults(func=handle_check)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
