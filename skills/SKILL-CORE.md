# SKILL-CORE｜ProsperaGen AI Execution Core
## Document Header
- Document Type: Codex
- Version: v1.6
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
| v1.3 | 2026-05-21 | 新增 §12 指令必須單一完整區塊 |
| v1.4 | 2026-05-21 | 新增 §13 API Key 使用規則（防止意外收費）|
| v1.5 | 2026-05-21 | 新增 §17 Human-Reviewed v2.0 + §18 指令格式禁止事項 |
| v1.6 | 2026-05-21 | 新增 §19 Claude Code 行為規則（禁止詢問句/純指令） |

---

## 10. 限流自動處理（Rate Limit）

遇到以下情況，自動等待後繼續，不中斷任務：

| 錯誤類型 | 處理方式 |
|---------|----------|
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

## 12. 指令必須單一完整區塊（Single-Block Instruction Rule）

**MUST：** 所有給 Claude Code 執行的指令，必須是單一完整的程式碼區塊。
**MUST NOT：** 不可分段貼入（分段 = 需要人工判斷順序 = 違反自動化治理哲學）。

```
✅ 正確：從第一行到 Write-Host "[DONE]" 一次完整貼入
❌ 錯誤：分成多個訊息分段貼入指令
```

**原因：** 分段 = 增加人工介入 = 違反「AI 治理的摩擦最小化」核心哲學。

---

## 13. API Key 使用規則（防止意外收費）

MUST NOT：不可把 Anthropic API key 存進 .env 或系統環境變數
MUST NOT：不可在 agent 程式碼裡直接呼叫 Anthropic API（會產生費用）
MUST：所有 AI 呼叫透過 Claude.ai 或 Claude Code（月費制，不另計費）
例外：明確需要 API 呼叫時，人工確認後才設定，用完立刻刪除

---

## 17. Human-Reviewed 欄位定義（v2.0）

| 值 | 意義 |
|----|------|
| `YES` | 架構方向、專案定位、重大決策 — 需人工確認 |
| `AI`  | 所有程式碼、文件、測試、工程執行 — **預設值** |
| `NO`  | 需人工審閱但尚未審（例外，需說明原因）|

**廢除 `PENDING`：** 違反 AI as Engineering Worker 哲學。
工程產出一律使用 `Human-Reviewed: AI`。

```
# 正確
# Human-Reviewed:   AI

# 錯誤（已廢除）
# Human-Reviewed:   PENDING
```

---

## 18. 給 Claude Code 的指令格式禁止事項

**MUST NOT：** 指令內不可有 markdown fenced code block（三個反引號）
**原因：** Claude.ai 介面會把 code fence 切斷指令，造成無法完整複製貼上
**替代方案：** 改用 PowerShell here-string 或純文字行內描述

---

*v1.5 · 2026-05-21 · prospera-ci-shared/skills/ · Kevin Chang（張淳嘉）*
