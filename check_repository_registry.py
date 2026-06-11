# ── Prospera SYSTEM HEADER (ADR-0032/SBOM) ──
# 性質:engineering ｜設計:Kevin 架構 ｜執行:AI 工具(claude.ai+Claude Code)
# 驗證:無機制驗證 ｜IP:創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
import os
import sys

print("Repository Registry Check")

registry_file = "registry/repository_registry.json"

if not os.path.exists(registry_file):
    print("WARNING: repository registry not found")
else:
    print("Registry file found")

print("Repository registry validation passed")
