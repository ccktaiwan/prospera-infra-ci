<!-- Prospera SYSTEM HEADER (ADR-0032/SBOM) | 性質:doc | 設計:Kevin 架構 | 執行:AI 工具(claude.ai+Claude Code) | 驗證:審計注入 | IP:創造性歸 Kevin(發明人) -->
# AGENTS.md — prospera-infra-ci
# AI Agent Operating Contract | L3 — CI/CD Infrastructure
# Version: 1.0 | 2026-04-30
# Governance Reference: prospera-constitution-governance v3.0
# Pipeline Reference: prospera-engine-workflow v1.0
# Codex Reference: prospera-standard-engineering v2.0

## 1. REPO IDENTITY
Repo: ccktaiwan/prospera-infra-ci
Layer: L3 — CI/CD Infrastructure（共用 CI 驗證）
Role: 所有 Repo 的 CI/CD 治理閘門，不合規不通過
Palantir Equivalent: Apollo CI/CD Pipeline

## 2. 生態系定位
此 Repo 是 Prospera 生態系的執行品質閘門：
任何 Repo 的 commit → CI 驗證 → 三分類結果 → 允許/阻擋合併

三分類驗證標準：
【驗證成功】VERIFIED → 所有治理檢查通過
【可接受失敗】ACCEPTABLE_FAIL → 已知問題，可繼續
【結構警訊】STRUCTURAL_WARNING → 必須修正才能合併

## 3. Pipeline-Thread-Container 角色
Pipeline：此 Repo 執行 Layer 5 VALIDATION 的機制
Thread：每個 PR 是一個獨立的驗證 Thread
Container：每個 Repo 是獨立的驗證 Container

## 4. AGENT RULES

### PERMIT — 允許自動執行
- 執行三分類 Governance Validation
- 檢查 AGENTS.md 存在性
- 檢查 SYSTEM_INDEX.md 存在性
- 檢查命名規範合規性
- 生成驗證報告
- 寫入稽核記錄

### ESCALATE — 執行前必須確認（J點）
- 修改三分類的判定標準 → J3（影響所有 Repo）
- 新增 CI 驗證規則 → J2
- 豁免特定 Repo 的某項驗證 → J3

### BLOCK — 禁止執行
- 自行修改驗證標準不通過 PR
- 允許【結構警訊】的 PR 合併
- 繞過任何驗證步驟
- 自行決定「不合規也可以繼續」

## 5. Decision Engine 四問法
Q1 Should → CI 任務在 PERMIT 清單內？
Q2 Can    → GitHub Actions 環境可用？
Q3 Fit    → 驗證規則符合 engineering-codex 定義？
Q4 Profit → 有明確的品質目標？

## 6. 三分類驗證規則
VERIFIED（驗證成功）條件：
  - AGENTS.md 存在
  - SYSTEM_INDEX.md 存在
  - 命名規範合規
  - 無結構性問題

ACCEPTABLE_FAIL（可接受失敗）條件：
  - AGENTS.md 缺失（repo 尚未注入）
  - 非核心文件格式問題

STRUCTURAL_WARNING（結構警訊）條件：
  - SYSTEM_INDEX.md 缺失
  - 核心治理文件被修改未經審查
  - 命名嚴重違規

## 7. J 點確認
J1 技術確認：CI 環境健康狀態
J2 品質審閱：新驗證規則的影響範圍
J3 架構決策：驗證標準修改、豁免授權

## 8. 稽核要求
Commit 格式：ci(scope): [change] - reason: [why] - phase: [N]

# Version: 1.0 | 2026-04-30
# 設計: 依 Kevin 架構 ｜執行: AI 工具(claude.ai+Claude Code) ｜驗證: 無機制驗證 ｜IP: 創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
## Living Organism Role
philosophy: PROSPERA_OS_PHILOSOPHY.md
organism_role: 自主神經（自動化維護）
