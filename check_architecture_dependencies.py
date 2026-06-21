# ── Prospera SYSTEM HEADER (ADR-0032/SBOM) ──
# 性質:engineering ｜設計:Kevin 架構 ｜執行:AI 工具(claude.ai+Claude Code)
# 驗證:真實 import 掃描（非 stub）｜IP:創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
"""check_architecture_dependencies.py — 真實架構依賴守門（2026-06-21 真補，原 stub 升級）。

驗：repo 的 .py 是否在 import / sys.path / 路徑 中引用**已刪 repo**（架構依賴違規——
依賴一個不存在的 repo＝死依賴，會在 runtime 斷裂）。只看 code（去 # 註解），避免註解誤判。

用法: python check_architecture_dependencies.py [ROOT=.]
退出碼: 0 = 無死依賴；1 = 偵測到對已刪 repo 的架構依賴（CI 應擋）。
"""
import os
import re
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 已刪 repo（git 取證；對齊 FRS FR4 DEAD_REPOS）。對這些的 import/path 依賴＝架構違規。
DELETED_REPOS = ["prospera-execution-layer", "Governance-Core", "prospera-governance-core", "prospera-ci-shared"]
SKIP_DIRS = {".git", "__pycache__", "tests", "11_tests", "99_archive", "10_archive", "node_modules", ".github"}
# 只在「依賴 context」算違規：import / from / sys.path / Path( / open( / 路徑分隔
_DEP_CTX = re.compile(r"\b(import|from)\b|sys\.path|Path\(|open\(|[/\\]")


def scan(root: str):
    violations = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if not fn.endswith(".py"):
                continue
            fp = os.path.join(dp, fn)
            try:
                lines = open(fp, encoding="utf-8", errors="replace").read().splitlines()
            except OSError:
                continue
            for i, raw in enumerate(lines, 1):
                code = raw.split("#", 1)[0]   # 去註解
                for dead in DELETED_REPOS:
                    if dead in code and _DEP_CTX.search(code):
                        violations.append((os.path.relpath(fp, root), i, dead, code.strip()[:80]))
    return violations


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"[arch-deps] 掃描 {os.path.abspath(root)} 對已刪 repo 的架構依賴…")
    v = scan(root)
    if not v:
        print("[arch-deps] PASS — 無對已刪 repo 的 import/path 依賴。")
        return 0
    print(f"[arch-deps] FAIL — {len(v)} 處依賴已刪 repo（架構違規，runtime 會斷）：")
    for rel, ln, dead, snippet in v[:30]:
        print(f"  {rel}:{ln} → {dead}  「{snippet}」")
    print("[arch-deps] 修復：移除死依賴或改 env-only（見 prospera-os 2026-06-21 清理範例）。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
