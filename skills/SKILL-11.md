# SKILL-11｜Human-Readable Execution Report
## Document Header
- Document Type: Codex
- Version: v1.0
- Status: Approved
- Owner: prospera-ci-shared/skills/
- Governing Authority: prospera-engineering-codex v1.0
- DNA Reference: 要素八（AI 協作協議）+ 要素五（可工程實作）
- Last Updated: 2026-05-24

---

## 1. Identity & Scope

Claude Code 完成任務後，產出一份人類 30 秒內可讀完的執行摘要。
解決問題：PHASE SUMMARY 是給 AI 看的技術記錄，人類不可能逐行閱讀。
核心原則：結論先行，細節後置，問題高亮。
觸發條件：每次 PHASE SUMMARY 輸出後，緊接輸出本格式。

---

## 2. Non-Goals

- 不取代 PHASE SUMMARY（技術記錄仍需保留）
- 不取代 git log（commit 記錄仍是 SSOT）

---

## 3. Human Report 標準格式

```
HUMAN REPORT
============
✅ 完成：[1-3 條最重要的完成項目，每條 ≤ 20 字]
⚠️ 注意：[需要人類知道的問題或偏差，沒有填「無」]
🔜 下一步：[下一個需要人類決策或等待的事，沒有填「無」]
============
耗時：[執行時間估算] | Commits：[本次 commit 數] | CI：[Green / Red / Pending]
```

**格式規則：**
- 每個 ✅ 條目只寫結果，不寫過程（錯誤：「執行了 git add 和 git commit」，正確：「SKILL-11 已建立並 push」）
- ⚠️ 有問題必須列出，不可省略或輕描淡寫
- 🔜 若任務完全結束填「無需等待，任務完成」

---

## 4. 範例

**正確範例（Phase 0 新增 SKILL）：**
```
HUMAN REPORT
============
✅ 完成：SKILL-11.md 建立完成
✅ 完成：SKILL-CORE §6 新增 SKILL-11 條目，版本升至 v2.2
✅ 完成：SKILL-06 §9 新增 SKILL-11 觸發參考，commit 並 push
⚠️ 注意：無
🔜 下一步：無需等待，任務完成
============
耗時：< 5 分鐘 | Commits：1 | CI：Pending
```

**錯誤範例（過度技術化）：**
```
HUMAN REPORT
============
✅ 完成：執行了 Write 工具寫入 SKILL-11.md 至 skills/ 目錄，然後 Edit SKILL-CORE.md 的第 82 行新增 SKILL-11 row，再 Edit SKILL-06.md...
```

---

## 5. 版本記錄

| 版本 | 日期 | 變更 |
|------|------|------|
| v1.0 | 2026-05-24 | 初版發布 |

---

*v1.0 · 2026-05-24 · prospera-ci-shared/skills/*
