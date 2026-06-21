<!-- Prospera SYSTEM HEADER (ADR-0032/SBOM) | 性質:idea | 設計:Kevin Chang 架構 | 執行:Claude Code | 驗證:無機制驗證 | IP:創造性歸 Kevin Chang(發明人), AI 為執行工具 -->
# ECOSYSTEM_ROLE | prospera-infra-ci
Ring: R6 Infra
Type: A 服務型
Date: 2026-06-20

## Unique Role in Ecosystem
中央 CI 治理檢查的 SSOT。真正承載檢查的工具在 scripts/：
- scripts/governance_check.py —— 集中式治理 producer，由各 repo 的
  governance_check.yml 以 curl 取本檔執行（= branch protection required context）。
- scripts/actions_usage_lint.py / artifact_semantic_validator.py / drift_scan.py
  —— Actions 用量 lint、產出物語意驗證、漂移掃描。
- templates/workflows/ 的可重用 workflow —— 全生態系引用入口。

註：根目錄 check_*.py（check_api_contracts / check_architecture_dependencies /
check_repository_registry）為 stub/占位，不執行實質驗證（check_repository_registry
僅做 registry JSON 合法性檢查），勿視為治理保證來源。

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
