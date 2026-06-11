<!-- Prospera SYSTEM HEADER (ADR-0032/SBOM) | 性質:idea | 設計:Kevin 架構 | 執行:AI 工具(claude.ai+Claude Code) | 驗證:無機制驗證 | IP:創造性歸 Kevin(發明人), AI 為執行工具 -->
# CONTRACT｜prospera-infra-ci
Ring: R6 Infrastructure
Version: v1.0
Date: 2026-05-31

## 定位
共享 CI/CD 模板。所有 repo 的自動化測試和部署流程來源。

## 提供
- ci.yml 基礎測試模板
- governance-check.yml 治理檢查
- prospera_guard.yml 安全守門

## Boundary
- 不執行業務邏輯
- 所有 repo 繼承此 CI，不可各自定義衝突規則
