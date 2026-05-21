# SKILL-CORE｜ProsperaGen AI Execution Core
## Document Header
- Document Type: Codex
- Version: v1.2
- Status: Approved
- Owner: prospera-ci-shared/skills/
- Governing Authority: prospera-engineering-codex v1.0
- DNA Reference: 要素一～十（全部）
- Last Updated: 2026-05-21

---

## 1. 強制讀取規則

**每次任務開始前**：讀完本文件再執行。
**特定情境**：查 §6 → 讀對應完整 Skill → 再執行。
**CI 失敗**：先查 §7 → 查 known_failures.md → 找到即套標準修法，不試錯。
不讀直接執行 = Governance Breach → CI 自動 BLOCK。

---

## 2. 標準任務流程

```
[開始] → 讀 SKILL-CORE §6 → 讀對應 Skill → 執行
       → 每完成重要步驟 → Checkpoint (SKILL-06)
       → git commit 前 → Pre-flight (SKILL-04)
       → CI 失敗 → 先查 known_failures.md (§7)
       → 新錯誤 → 補進 known_failures.md
```

---

## 3. 命名規則

```
目錄：全小寫    ✅ 00_governance  ❌ 00_GOVERNANCE
檔案：全大寫    ✅ README.md      ❌ readme.md
```

---

## 4. Commit Message 格式

```
[Phase][Layer] 動作: 描述 (為什麼) ≤ 72 字元
範例：[P3][L2] feat: add authority-matrix (enforce access boundary)
禁用：update / fix / change / misc / WIP
```

---

## 5. AI Header 必要欄位

```
Generated / Model / Phase / Layer / Target Repo / Governing Codex / Human-Reviewed
```

---

## 6. Skill 查閱表

| Skill | 觸發條件 | 完整文件 |
|-------|---------|----------|
| SKILL-01 | 任何 .yml 寫入或修改前 | SKILL-01.md |
| SKILL-02 | 任何目錄建立或 git mv 前 | SKILL-02.md |
| SKILL-03 | 任何 token/PAT/secret 操作前 | SKILL-03.md |
| SKILL-04 | 任何 git commit 前 | SKILL-04.md |
| SKILL-05 | 每次任務開始前 + 每個 Stage 完成後 | SKILL-05.md |
| SKILL-06 | 多步驟任務每完成一個重要步驟後 | SKILL-06.md |
| SKILL-07 | 任何文件提交前 | SKILL-07.md |
| SKILL-08 | 每個新機制或新引擎建立後 | SKILL-08.md |
| SKILL-09 | 任何 99_archive 救援或檔案遷移前 | SKILL-09.md |
| SKILL-10 | 任何新 repo 建立或 repo 封存前 | SKILL-10.md |

---

## 7. CI 失敗第一動作（CI-Fail-First）

**CI 失敗時，第一步永遠是查 `known_failures.md`，不試錯。**

```
Step 1｜查 known_failures.md（路徑：prospera-ci-shared/skills/）
  找到匹配症狀 → 直接套標準修法 → commit → push
  找不到 → 允許試錯 → 成功後補進 known_failures.md

Step 2｜常見失敗快查
  YAML 語法錯誤（<# 語法）           → KF-001
  Windows 目錄大小寫衝突             → KF-002
  GitHub Secret Token 未設定        → KF-003
  Scanner 判定 Level 0              → KF-004
  JSON 解析失敗（markdown 包裹）      → KF-005
  PAT 找不到                        → KF-006
  Dashboard schedule 與 CI 衝突     → KF-007
```

新增格式：`## KF-[序號]｜[症狀]` → 症狀 / 根本原因 / 影響 Repo / 標準修法 / 首次發現 / DNA 要素

---

## 8. RESTART DECLARATION（記憶清空後必用）

```
RESTART DECLARATION
===================
Last Known State: [從 git log --oneline -5 重建]
Pending Tasks:    [未完成項目]
Starting From:    [從哪個步驟繼續]
===================
```
詳細重啟流程 → SKILL-06 §5

---

## 9. 版本記錄

| 版本 | 日期 | 變更 |
|------|------|------|
| v1.0 | 2026-05-19 | 初版發布 |
| v1.1 | 2026-05-20 | 新增 §7 CI-Fail-First（KF-007）、§8 RESTART DECLARATION 快查 |
| v1.2 | 2026-05-21 | 新增 §10 限流自動處理、§11 CI 觸發後不用 sleep 等待 |

---

## 10. 限流自動處理（Rate Limit）

遇到以下情況，自動等待後繼續，不中斷任務：

| 錯誤類型 | 處理方式 |
|---------|---------|
| 429 / rate limit / secondary rate | 等 60 秒繼續 |
| 403 Forbidden | 等 30 秒繼續 |
| Connection reset / timeout | 等 15 秒，最多重試 3 次 |
| push rejected fetch first | 自動 `git pull --rebase` 再 push |
| sleep 被封鎖 | 改用 `gh run watch --exit-status` |

---

## 11. CI 觸發後不用 sleep 等待

```
❌ sleep 35 && gh run view [id]      ← Claude Code 會封鎖 sleep
✅ gh run watch [id] --exit-status   ← 正確做法（阻塞直到完成）
✅ 分兩步：先觸發，後續再查結果       ← 不需要等待時用此模式
```

---

*v1.2 · 2026-05-21 · prospera-ci-shared/skills/ · Kevin Chang（張淳嘉）*
