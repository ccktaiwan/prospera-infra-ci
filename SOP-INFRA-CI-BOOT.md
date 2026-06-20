<!-- Prospera SYSTEM HEADER (ADR-0032/SBOM) | 性質:sop | 設計:Kevin Chang 架構 | 執行:Claude Code | 驗證:啟動實證 | IP:創造性歸 Kevin Chang(發明人), AI 為執行工具 -->
# SOP-INFRA-CI-BOOT — prospera-infra-ci 啟動/收工 SOP

## 前置確認
- Python 3.11；`python -m pip install -r requirements.txt`（若有）。
- 確認治理件齊：manifest.json / CONTRACT.md / ECOSYSTEM_ROLE.md。

## 啟動步驟
```bash
cd prospera-infra-ci
python -c "import check_api_contracts"   # import 驗證主模組可載入
# 若為服務：python check_api_contracts.py
```

## 健康確認
```bash
python fitness/infra-ci_fitness.py   # 結構 fitness 全 pass
```

## 收工步驟
1. 確認無未提交變更（git status）。
2. 變更走本 repo PR；治理 SSOT 仍在 prospera-constitution-governance。
