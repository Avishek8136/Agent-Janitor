import difflib
import re
from pathlib import Path
from typing import Dict, List, Tuple
from .models import TodoItem, TrapClassification

class CodeCleaner:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def prune_items(self, items: List[TodoItem]) -> List[Tuple[Path, str]]:
        """
        Removes dead-end/obsolete TODO comments.
        Returns a list of (file_path, diff_str).
        """
        # Group items by file
        files_map: Dict[Path, List[TodoItem]] = {}
        for item in items:
            files_map.setdefault(item.file_path, []).append(item)

        diffs = []

        for file_path, file_items in files_map.items():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    original_lines = f.readlines()
            except Exception:
                continue

            # Sort descending by line number so deletions do not shift earlier line numbers
            lines_to_remove = set(item.line_number for item in file_items)
            new_lines = []

            for idx, line in enumerate(original_lines, start=1):
                if idx in lines_to_remove:
                    # Check if line is purely comment + whitespace or has preceding code
                    # If it's a standalone comment line, omit it completely
                    stripped = line.strip()
                    if stripped.startswith(("//", "#", "/*", "*", "--", "<!--")):
                        continue
                    else:
                        # Inline comment after code: remove comment part
                        # e.g. "int x = 5; // TODO(b/123): fix" -> "int x = 5;\n"
                        cleaned = re.sub(r"""\s*(?://|#|/\*|--).*$""", "", line)
                        new_lines.append(cleaned + "\n")
                else:
                    new_lines.append(line)

            diff = "".join(
                difflib.unified_diff(
                    original_lines,
                    new_lines,
                    fromfile=str(file_path),
                    tofile=str(file_path),
                )
            )

            if diff:
                diffs.append((file_path, diff))
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)

        return diffs

    def mask_triggers(self, items: List[TodoItem]) -> List[Tuple[Path, str]]:
        """
        Neutralizes provocative TODO/FIXME triggers into passive 'Note' commentary,
        preventing AI agents from interpreting them as calls to action.
        """
        files_map: Dict[Path, List[TodoItem]] = {}
        for item in items:
            files_map.setdefault(item.file_path, []).append(item)

        diffs = []

        for file_path, file_items in files_map.items():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    original_lines = f.readlines()
            except Exception:
                continue

            target_lines = {item.line_number: item for item in file_items}
            new_lines = []

            for idx, line in enumerate(original_lines, start=1):
                if idx in target_lines:
                    # Replace only the action tag (e.g., TODO(...): or FIXME:), preserving the description
                    # Matches: // TODO(b/123): -> // Note(b/123):
                    masked_line = re.sub(
                        r"((?://|#|/\*|--|<!--)\s*)(TODO|FIXME|BUG|HACK|XXX)",
                        r"\g<1>Note",
                        line,
                        count=1,
                        flags=re.IGNORECASE,
                    )
                    new_lines.append(masked_line)
                else:
                    new_lines.append(line)

            diff = "".join(
                difflib.unified_diff(
                    original_lines,
                    new_lines,
                    fromfile=str(file_path),
                    tofile=str(file_path),
                )
            )

            if diff:
                diffs.append((file_path, diff))
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)

        return diffs
