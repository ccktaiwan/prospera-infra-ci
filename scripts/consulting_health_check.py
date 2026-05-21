# ══════════════════════════════════════
# AI-GENERATED DOCUMENT
# ══════════════════════════════════════
# Generated:        2026-05-22
# Model:            claude-sonnet-4-6
# Phase:            Phase 2 - Infrastructure
# Layer:            L1 Governance & Audit
# Target Repo:      prospera-ci-shared
# Governing Codex:  prospera-engineering-codex v1.0
# Human-Reviewed:   AI
# Review By:        Kevin Chang
# Review Date:      2026-05-22
# ══════════════════════════════════════
"""
Prospera Consulting System Health Check
用法：python scripts/consulting_health_check.py
輸出：PASS / FAIL / WARNING 健康報告
"""

import sys
import pathlib
import re

CONSULTING_ROOT = pathlib.Path(r"C:\AI_WorkDir\GitHub\prospera-consulting-system")
GATEWAY_ROOT    = pathlib.Path(r"C:\AI_WorkDir\GitHub\prospera-api-gateway")

results = []

def check(name: str, passed: bool, detail: str = "", level: str = "FAIL"):
    status = "[PASS]" if passed else ("[WARN]" if level == "WARNING" else "[FAIL]")
    results.append((status, name, detail))
    return passed


# ── Check 1: consulting_orchestrator.py AI Header ────────────────
orch = CONSULTING_ROOT / "consulting_orchestrator.py"
if orch.exists():
    content = orch.read_text(encoding="utf-8", errors="replace")
    has_header = "AI-GENERATED DOCUMENT" in content
    check("orchestrator AI Header", has_header,
          "consulting_orchestrator.py 缺少 AI Header" if not has_header else "")
    has_real_data = "RealDataInput" in content
    check("orchestrator RealDataInput", has_real_data,
          "缺少真實數據欄位（fbFollowers 等）" if not has_real_data else "")
    has_single_call = "run_single_call" in content
    check("orchestrator single-call fn", has_single_call,
          "缺少 run_single_call() (ADR-CS-001)" if not has_single_call else "")
else:
    check("orchestrator file exists", False, f"找不到 {orch}")


# ── Check 2: gateway /v1/consulting/run endpoint ─────────────────
gw = GATEWAY_ROOT / "gateway_v1.2.py"
if gw.exists():
    gw_content = gw.read_text(encoding="utf-8", errors="replace")
    has_consulting = "/v1/consulting/run" in gw_content
    check("gateway /v1/consulting/run", has_consulting,
          "gateway_v1.2.py 缺少 /v1/consulting/run endpoint" if not has_consulting else "")
    has_static = "StaticFiles" in gw_content
    check("gateway static UI serving", has_static,
          "缺少 StaticFiles（UI 無法從 gateway 服務）" if not has_static else "", level="WARNING")
    has_status = "/v1/status" in gw_content
    check("gateway /v1/status endpoint", has_status,
          "缺少 /v1/status 監控端點" if not has_status else "", level="WARNING")
else:
    check("gateway file exists", False, f"找不到 {gw}")


# ── Check 3: reports/ 資料夾 ─────────────────────────────────────
reports_dir = CONSULTING_ROOT / "reports"
check("reports/ directory exists", reports_dir.exists(),
      f"reports/ 不存在（{reports_dir}）" if not reports_dir.exists() else
      f"{sum(1 for d in reports_dir.iterdir() if d.is_dir())} 客戶資料夾",
      level="WARNING")


# ── Check 4: KB 文件存在 ─────────────────────────────────────────
kb = CONSULTING_ROOT / "00_governance" / "CONSULTING_SYSTEM_KB_v1_0.md"
check("governance KB exists", kb.exists(),
      f"找不到 {kb.name}" if not kb.exists() else "")
if kb.exists():
    kb_content = kb.read_text(encoding="utf-8", errors="replace")
    has_adr_cs001 = "ADR-CS-001" in kb_content
    check("KB contains ADR-CS-001", has_adr_cs001,
          "KB 缺少 ADR-CS-001 單次API呼叫原則" if not has_adr_cs001 else "")


# ── Check 5: HTML 表單存在 ───────────────────────────────────────
html = CONSULTING_ROOT / "11_interfaces" / "consulting_engine_v1.html"
check("HTML form exists", html.exists(),
      f"找不到 consulting_engine_v1.html" if not html.exists() else "")
if html.exists():
    html_content = html.read_text(encoding="utf-8", errors="replace")
    has_real_data_ui = "fbFollowers" in html_content
    check("HTML real data accordion", has_real_data_ui,
          "HTML 缺少真實數位數據輸入欄位" if not has_real_data_ui else "")


# ── Report ───────────────────────────────────────────────────────
print("\n" + "═" * 60)
print("  Prospera Consulting System Health Check")
print("═" * 60)
for status, name, detail in results:
    line = f"  {status}  {name}"
    if detail:
        line += f"\n         → {detail}"
    print(line)

total   = len(results)
passed  = sum(1 for s, _, _ in results if "PASS" in s)
warned  = sum(1 for s, _, _ in results if "WARN" in s)
failed  = sum(1 for s, _, _ in results if "FAIL" in s)

print("═" * 60)
print(f"  結果：{passed} PASS  {warned} WARN  {failed} FAIL  / {total} 項")
if failed == 0 and warned == 0:
    print("  Overall: HEALTHY")
elif failed == 0:
    print("  Overall: DEGRADED (warnings present, functional)")
else:
    print("  Overall: UNHEALTHY")
print("═" * 60 + "\n")

sys.exit(0 if failed == 0 else 1)
