<!-- Prospera SYSTEM HEADER (ADR-0032/SBOM) | 性質:architecture-decision | 設計:Kevin Chang 架構 | 執行:Claude Code | 驗證:git 實證(scripts/+templates/workflows/) | IP:創造性歸 Kevin Chang(發明人), AI 為執行工具 -->
# ADR-0001：CI 治理中央化——producer 模式 vs 各 repo 分散

- Status: Accepted
- Date: 2026-06-21
- Ring: R6 Infra｜Type: A 服務型（治理 CI 基礎設施）
- conception: Kevin Chang

## Context（背景）

37-repo 生態系每個 repo 都需 CI 治理檢查（governance_check / actions-usage-lint / 語意閘 / drift）。若**各 repo 各自複製檢查邏輯**，會產生：①邏輯漂移（37 份不同步）②修一個規則要改 37 repo ③無單一 SSOT。同時，根目錄歷史上有 `check_api_contracts.py` / `check_architecture_dependencies.py` / `check_repository_registry.py` 三個招牌檔，實為 stub（print passed 不驗），易被誤認為真治理來源。

## Decision（決策）

**CI 治理邏輯中央化於本 repo（infra-ci），下游以「消費」而非「複製」取得**：

1. **Producer 模式（curl SSOT）**：`templates/workflows/governance_check.yml` 在 runtime `curl` raw.githubusercontent 取 `scripts/governance_check.py` 執行——邏輯單一 SSOT 在本 repo，所有下游 repo 下次跑即自動取得最新規則，**零複製、零漂移**。
2. **Reusable workflow（workflow_call）**：`.github/workflows/actions-usage-lint.yml` 以 `on: workflow_call` 提供，下游 2 行 caller 即接入真 lint（`scripts/actions_usage_lint.py`，270 行真規則）。
3. **載重工具在 `scripts/`，非根目錄招牌檔**：真治理＝`scripts/`（actions_usage_lint / governance_check / artifact_semantic_validator / drift_scan）；根目錄 `check_*.py` 三件**誠實標 STUB**並指向 scripts/ 真工具（2026-06-21，不偽裝為治理來源）。

## Consequences（後果）

- 修一個治理規則 → 改本 repo 一處 → 全生態下次 CI 生效。
- 誠實邊界：招牌 check_*.py 為 stub（已明標）；`governance_check.py` 依賴的 `check_ontology_hardcode.py` 若不在本 repo 則該子檢查 no-op（PENDING 追蹤）；L3=0（本 repo 為 CI 工具非常駐服務，無 /health＝型別特性非缺陷）。
- 依賴：`requirements.txt` 已補 `pyyaml`（lint 所需）；`governance_check.py` 已補 `stdout.reconfigure` 防 cp950。

## Alternatives（替代方案）

- **各 repo 複製檢查邏輯**：拒絕——37 份漂移、改規則要動 37 repo、無 SSOT。
- **招牌 check_*.py 補成真檢查**：部分否決——OpenAPI/Protobuf 契約驗證為大工程且非當前需求；改誠實標 stub + 指向 scripts/ 真工具（不臆造）。
- **下游 vendor（複製）lint 腳本**：拒絕——失去 curl/workflow_call 的「中央改、下游自動取」優勢。

## 真實性聲明
本 ADR 對應 infra-ci 真實 code（scripts/actions_usage_lint.py / governance_check.py / templates/workflows/），非模板：producer 模式 + reusable workflow + 招牌 stub 誠實化皆本 repo 實際架構。
