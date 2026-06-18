# Prospera SYSTEM HEADER (ADR-0032/SBOM) | 性質:engineering | 設計:Kevin 架構 | 執行:AI 工具(claude.ai+Claude Code) | 驗證:審計注入 | IP:創造性歸 Kevin(發明人)
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

def validate(filepath, phases):
    """gate-design 修正（ADR-0061）：phases 為 list（多 phase tag union）——合法混類 sync PR
    宣告 [Phase0][Phase4] 即 union 允許 governance_doc+runtime_code，不再強制單一 phase。"""
    if isinstance(phases, int):
        phases = [phases]
    p = Path(filepath); at = classify(p)
    allowed = set()
    for ph in phases:
        allowed |= set(PHASE_RULES.get(ph, list(AType)))
    if at not in allowed:
        return False, f"SEMANTIC VIOLATION: {p.name} is {at.value}, Phases {phases} allow {sorted(a.value for a in allowed)}"
    return True, f"OK: {p.name} -> {at.value}"

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("filepath")
    # --phases 接逗號分隔多 phase（如 "0,4"）；保留 --phase 單值向後相容。
    ap.add_argument("--phases", default=None)
    ap.add_argument("--phase", type=int, default=None)
    a = ap.parse_args()
    if a.phases:
        phases = [int(x) for x in a.phases.split(",") if x.strip() != ""]
    elif a.phase is not None:
        phases = [a.phase]
    else:
        phases = [4]
    ok, msg = validate(a.filepath, phases)
    print(msg); sys.exit(0 if ok else 1)
