"""
[Phase4][L0] feat: Drift Scan CI Script
Governing: prospera-engineering-codex v1.0
# 設計: 依 Kevin 架構 ｜執行: AI 工具(claude.ai+Claude Code) ｜驗證: 無機制驗證 ｜IP: 創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
"""
import argparse, sys
from pathlib import Path

DRIFT = ["應該","建議","考慮","方向","框架","策略","願景","方針"]
SKIP  = ["99_archive","node_modules",".git","known_failures"]

def scan(path, fail):
    hits = []
    for f in Path(path).rglob("*.md"):
        if any(s in str(f) for s in SKIP): continue
        t = f.read_text(encoding="utf-8", errors="ignore")
        for d in DRIFT:
            if d in t: hits.append(f"{f}: '{d}'")
    if hits:
        print("WARN Drift signals:")
        for h in hits: print(f"  {h}")
        if fail: sys.exit(1)
    else:
        print("OK No drift signals")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--path", default=".")
    p.add_argument("--fail-on-drift", action="store_true")
    a = p.parse_args(); scan(a.path, a.fail_on_drift)
