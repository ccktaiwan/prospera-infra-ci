<!-- Prospera SYSTEM HEADER (ADR-0032/SBOM) | 性質:idea | 設計:Kevin Chang 架構 | 執行:Claude Code | 驗證:無機制驗證 | IP:創造性歸 Kevin Chang(發明人), AI 為執行工具 -->
# ECOSYSTEM_ROLE | prospera-infra-ci
Ring: R6 Infra
Type: A 服務型
Date: 2026-06-20

## Unique Role in Ecosystem
中央 CI 治理檢查——check_*.py（架構依賴/契約/registry）

## Tenant Model
非租戶

## What This Repo Monitors (L5)
gate 攔截率 / CI 成功率

## What This Repo Evolves (L7)
check 規則

## KPI
gate_block_rate / ci_pass_rate

## Dependencies
被全 ecosystem CI 引用（governance_check）。詳見 CONTRACT.md。
