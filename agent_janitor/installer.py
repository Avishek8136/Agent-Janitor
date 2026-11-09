import shutil
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent.parent

def install_claude(target_dir: Path):
    src_claude = SOURCE_ROOT / "integrations" / "claude-code"
    if not src_claude.exists():
        return False

    # Copy CLAUDE.md
    shutil.copy2(src_claude / "CLAUDE.md", target_dir / "CLAUDE.md")

    # Copy .claude commands
    cmd_dir = target_dir / ".claude" / "commands"
    cmd_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_claude / ".claude" / "commands" / "janitor.md", cmd_dir / "janitor.md")
    return True

def install_cursor(target_dir: Path):
    src_cursor = SOURCE_ROOT / "integrations" / "cursor"
    if not src_cursor.exists():
        return False

    # Copy .cursorrules
    shutil.copy2(src_cursor / ".cursorrules", target_dir / ".cursorrules")

    # Copy .cursor/rules/*.mdc
    rules_dir = target_dir / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_cursor / ".cursor" / "rules" / "anti-distraction.mdc", rules_dir / "anti-distraction.mdc")
    return True

def install_windsurf(target_dir: Path):
    src_windsurf = SOURCE_ROOT / "integrations" / "windsurf"
    if not src_windsurf.exists():
        return False
    shutil.copy2(src_windsurf / ".windsurfrules", target_dir / ".windsurfrules")
    return True

def install_copilot(target_dir: Path):
    src_copilot = SOURCE_ROOT / "integrations" / "copilot"
    if not src_copilot.exists():
        return False
    target_gh = target_dir / ".github"
    target_gh.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_copilot / ".github" / "copilot-instructions.md", target_gh / "copilot-instructions.md")
    return True

def install_antigravity():
    src_plugin = SOURCE_ROOT / "plugins" / "antigravity-agent-janitor"
    if not src_plugin.exists():
        return False
    dst_plugin = Path.home() / ".gemini" / "config" / "plugins" / "agent-janitor"
    shutil.copytree(src_plugin, dst_plugin, dirs_exist_ok=True)
    return True
