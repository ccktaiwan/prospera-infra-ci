# Prospera SYSTEM HEADER (ADR-0032/SBOM) | 性質:engineering | 設計:Kevin 架構 | 執行:AI 工具(claude.ai+Claude Code) | 驗證:審計注入 | IP:創造性歸 Kevin(發明人)
"""
[Phase4][L0] feat: Drift Scan CI Script
Governing: prospera-engineering-codex v1.0
# 設計: 依 Kevin 架構 ｜執行: AI 工具(claude.ai+Claude Code) ｜驗證: 無機制驗證 ｜IP: 創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
"""
import argparse, sys, subprocess
from pathlib import Path

DRIFT = ["應該","建議","考慮","方向","框架","策略","願景","方針"]
SKIP  = ["99_archive","node_modules",".git","known_failures"]

def _report(hits, fail):
    if hits:
        print("WARN Drift signals:")
        for h in hits: print(f"  {h}")
        if fail: sys.exit(1)
    else:
        print("OK No drift signals")

def scan(path, fail):
    """全 repo 掃（保留供本地巡檢；CI 改用 --changed 只檢 PR 真正改動）。"""
    hits = []
    for f in Path(path).rglob("*.md"):
        if any(s in str(f) for s in SKIP): continue
        t = f.read_text(encoding="utf-8", errors="ignore")
        for d in DRIFT:
            if d in t: hits.append(f"{f}: '{d}'")
    _report(hits, fail)

def scan_changed(base, fail):
    """gate-design 修正（ADR-0061，範圍非標準）：只掃 PR 對 base 的**新增行**（+ 行），
    非全 repo/全檔——既有內容由獨立巡檢處理，CI gate 只擋 PR 真正引入的 drift。"""
    diff = subprocess.run(["git", "diff", f"{base}...HEAD", "--", "*.md"],
                          capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout
    hits = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            for d in DRIFT:
                if d in line:
                    hits.append(f"added '{d}': {line[1:90].strip()}")
    _report(hits, fail)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--path", default=".")
    p.add_argument("--changed", action="store_true", help="只掃對 --base 的新增行（CI gate 範圍修正）")
    p.add_argument("--base", default="origin/main")
    p.add_argument("--fail-on-drift", action="store_true")
    a = p.parse_args()
    if a.changed:
        scan_changed(a.base, a.fail_on_drift)
    else:
        scan(a.path, a.fail_on_drift)
