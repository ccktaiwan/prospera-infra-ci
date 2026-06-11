"""
[Phase6][L0] feat: Artifact Semantic Validation Layer
獨立於格式層 CI 三分類驗證（commit f590d77）
Governing: prospera-engineering-codex v1.0
# 設計: 依 Kevin 架構 ｜執行: AI 工具(claude.ai+Claude Code) ｜驗證: 無機制驗證 ｜IP: 創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
"""
import sys
from pathlib import Path
from enum import Enum

class AType(Enum):
    RUNTIME_CODE="runtime_code"; STATE_SPEC="state_spec"
    GOVERNANCE_DOC="governance_doc"; AUDIT_RECORD="audit_record"
    UNKNOWN="unknown"

PHASE_RULES = {
    4:[AType.RUNTIME_CODE, AType.STATE_SPEC],
    0:[AType.GOVERNANCE_DOC],
    1:[AType.GOVERNANCE_DOC, AType.STATE_SPEC],
    2:[AType.GOVERNANCE_DOC, AType.STATE_SPEC],
    3:[AType.GOVERNANCE_DOC, AType.STATE_SPEC],
}

def classify(p: Path) -> AType:
    s = p.suffix.lower()
    if s in [".py",".js",".ts"]: return AType.RUNTIME_CODE
    if s == ".jsonl":            return AType.AUDIT_RECORD
    if s == ".json":
        t = p.read_text(encoding="utf-8", errors="ignore")
        return AType.STATE_SPEC if ("$schema" in t or "state_machine" in t) else AType.GOVERNANCE_DOC
    if s == ".md":               return AType.GOVERNANCE_DOC
    return AType.UNKNOWN

def validate(filepath, phase):
    p = Path(filepath); at = classify(p)
    allowed = PHASE_RULES.get(phase, list(AType))
    if at not in allowed:
        return False, f"SEMANTIC VIOLATION: {p.name} is {at.value}, Phase {phase} allows {[a.value for a in allowed]}"
    return True, f"OK: {p.name} -> {at.value}"

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("filepath"); ap.add_argument("--phase", type=int, required=True)
    a = ap.parse_args(); ok, msg = validate(a.filepath, a.phase)
    print(msg); sys.exit(0 if ok else 1)
