# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-11-09

### Added
- **Core Scanner Engine:** Multi-language scanner supporting 30+ programming languages to detect `TODO`, `FIXME`, `BUG`, `HACK`, and issue references (`#123`, `b/456`, Jira keys, and URLs).
- **Issue Tracker Connectors:** GitHub CLI (`gh`) integration and mock tracker for offline audits.
- **Git Blame Age Analyzer:** Porcelain git parser extracting commit date, author, and age to classify fossilized debt.
- **Distraction Trap Classifier:** Classifies findings against Google empirical benchmarks into Dead-End Traps (41%), Scope-Creep Risks (57%), and Fossilized Debt.
- **AST / Safe Code Cleaner:**
  - Automated pruning of dead-end comments with dry-run diff preview.
  - Keyword masking converting active action tags (`TODO`, `FIXME`) into passive developer notes (`Note:`).
- **Universal MCP Server:** Zero-dependency stdio Model Context Protocol server exposing `audit_codebase`, `clean_dead_ends`, and `mask_triggers`.
- **Multi-App Integrations & Skills:**
  - Google Antigravity Plugin & `anti-distraction` skill.
  - Claude Code `CLAUDE.md` and custom slash command `/janitor`.
  - Cursor `.cursor/rules/anti-distraction.mdc` and `.cursorrules`.
  - Windsurf `.windsurfrules`.
  - GitHub Copilot `.github/copilot-instructions.md`.
- **One-Click Multi-App Installer:** `agent-janitor init [path] [--all|--claude|--cursor|--windsurf|--copilot|--antigravity]`.
- **CI Presubmit Gate:** GitHub Actions matrix test workflow and `agent-janitor check` presubmit validator.
