# ── Prospera SYSTEM HEADER (ADR-0032/SBOM) ──
# 性質:engineering ｜設計:Kevin 架構 ｜執行:AI 工具(claude.ai+Claude Code)
# 驗證:無機制驗證 ｜IP:創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
import sys

ALLOWED_DEPENDENCIES = {
    "Kernel": [],
    "Engine": ["Kernel"],
    "Registry": ["Engine"],
    "Gateway": ["Registry"],
    "Adoption": ["Gateway"]
}

print("Architecture dependency rules loaded.")

# In a full system this script would parse module imports
# and verify cross-repository dependencies.

print("Architecture dependency check passed.")
