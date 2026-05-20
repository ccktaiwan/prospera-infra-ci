# ══════════════════════════════════════
# AI-GENERATED DOCUMENT
# ══════════════════════════════════════
# Generated:        2026-05-21T00:00:00Z
# Model:            claude-sonnet-4-6
# Phase:            Phase 4
# Layer:            L4
# Target Repo:      prospera-ci-shared
# Governing Codex:  prospera-engineering-codex v1.0
# Human-Reviewed:   PENDING
# ══════════════════════════════════════
"""Plane Boundary Validator — 確保動態狀態內容不進入 KB 治理檔案"""
import sys
from pathlib import Path

DYNAMIC_TERMS = [
    "current blocker", "this week", "last completed",
    "weekly status", "in progress", "當前阻擋", "本週目標",
    "上次進度", "待辦", "TODO", "FIXME"
]

KB_GOVERNANCE_FILES = [
    "SKILL-CORE.md", "SKILL-01.md", "SKILL-02.md", "SKILL-03.md",
    "SKILL-04.md", "SKILL-05.md", "SKILL-06.md", "SKILL-07.md",
    "SKILL-08.md", "SKILL-09.md", "SKILL-10.md",
    "ProsperaGen_Engineering_DNA_v1_0.md",
    "PROSPERA_ARCHITECTURE_v1_0.md",
]


def validate(path: Path) -> list[str]:
    violations = []
    if path.name in KB_GOVERNANCE_FILES:
        content = path.read_text(encoding="utf-8", errors="ignore")
        for term in DYNAMIC_TERMS:
            if term.lower() in content.lower():
                violations.append(f"{path.name}: contains dynamic term '{term}'")
    return violations


def scan_directory(root: Path) -> list[str]:
    all_violations: list[str] = []
    for f in root.rglob("*.md"):
        all_violations.extend(validate(f))
    return all_violations


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    violations = scan_directory(root)
    if violations:
        print(f"[FAIL] {len(violations)} plane boundary violations:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print(f"[PASS] No plane boundary violations found in {root}")
        sys.exit(0)
