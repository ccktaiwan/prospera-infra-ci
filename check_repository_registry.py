# ── Prospera SYSTEM HEADER (ADR-0032/SBOM) ──
# 性質:engineering ｜設計:Kevin 架構 ｜執行:AI 工具(claude.ai+Claude Code)
# 驗證:無機制驗證 ｜IP:創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
"""部分驗證 —— 僅檢查 registry/repository_registry.json 是否存在且為合法 JSON。

本檔不負責完整的 registry 治理（成員清單對齊 / SSOT 比對等），
那些由 scripts/ 的真工具承擔：
  - scripts/governance_check.py        集中式治理 producer（required check）
  - scripts/drift_scan.py              漂移掃描

本檔僅做一件「低風險、無歧義」的真檢查：
  - 若 registry 檔不存在 → 警告，退出 0（此 repo 目前未放置該檔，non-blocking）。
  - 若檔存在但 JSON 格式錯誤 → 退出 1（硬失敗，擋 PR）。
  - 若檔存在且為合法 JSON → 退出 0。
"""
import json
import os
import sys

print("Repository Registry Check")

registry_file = "registry/repository_registry.json"

if not os.path.exists(registry_file):
    print(f"WARNING: registry 檔不存在（{registry_file}），跳過 JSON 驗證 (non-blocking)。")
    print("[NOTE] 完整 registry 治理由 scripts/governance_check.py / scripts/drift_scan.py 承擔。")
    sys.exit(0)

try:
    with open(registry_file, "r", encoding="utf-8") as f:
        json.load(f)
except json.JSONDecodeError as exc:
    print(f"ERROR: {registry_file} 非合法 JSON：{exc}")
    sys.exit(1)
except OSError as exc:
    print(f"ERROR: 無法讀取 {registry_file}：{exc}")
    sys.exit(1)

print(f"OK: {registry_file} 存在且為合法 JSON。")
sys.exit(0)
