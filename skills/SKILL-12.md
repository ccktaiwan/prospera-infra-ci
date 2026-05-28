# SKILL-12｜GitHub Push & Remote Verification
## Document Header
- Document Type: Codex
- Version: v1.0
- Status: Approved
- Owner: prospera-ci-shared/skills/
- Governing Authority: prospera-engineering-codex v1.0
- DNA Reference: 要素四（Commit 四標準）+ 要素八（AI 協作協議）
- Last Updated: 2026-05-28

---

## 1. Identity & Scope

確保每次 git push 後，遠端 GitHub 的檔案狀態與本地一致，
Claude Code 計畫文件可以被正確找到並執行。

解決問題：
- push 後出現 hint 警告導致分叉，檔案未推上去
- Claude Code 找不到計畫文件（Already up to date 但檔案不存在）
- /tmp 工作目錄與 C:\AI_WorkDir 分叉造成衝突

觸發條件：任何 `git push` 後，無例外。

---

## 2. Non-Goals

- 不取代 SKILL-04 Pre-flight（push 前驗證）
- 不管理 CI/CD 流程（→ SKILL-01）

---

## 3. Push 標準流程（MUST，依序執行）

```
Step 1｜push 前先 rebase
  git pull --rebase origin main
  → 有衝突 → 手動解決後 git rebase --continue
  → 無衝突 → 繼續

Step 2｜執行 push
  git push origin main
  → 出現 hint 警告 → 執行 Step 1 再重試
  → push rejected → 自動執行 git pull --rebase 再 push（SKILL-CORE §19）

Step 3｜GitHub API 驗證（MUST，不得跳過）
  用 GitHub API 確認檔案實際存在於遠端：
  curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/[owner]/[repo]/contents/[目標檔案路徑]" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ VERIFIED:', d['name'])"
  → 200 + 檔案名稱 = push 成功
  → 404 = push 失敗，重回 Step 1

Step 4｜輸出驗證結果
  格式：
  PUSH VERIFIED
  =============
  Repo:   [repo 名稱]
  File:   [已驗證的檔案路徑]
  Commit: [commit hash]
  Status: ✅ CONFIRMED ON REMOTE
  =============
```

---

## 4. Claude Code 計畫文件 Push 規則

每次設計新的 Claude Code 執行計畫後：

```
□ 計畫文件包含「第一步：git pull origin main」
□ 所有路徑使用 Windows 格式（C:\AI_WorkDir\GitHub\...）
□ 不含 markdown fenced code block（SKILL-CORE §18）
□ push 後用 GitHub API 確認檔案存在（Step 3）
□ 確認後才給 Claude Code 執行指令
```

給 Claude Code 的指令格式（MUST）：
```
git -C C:\AI_WorkDir\GitHub\[repo名稱] pull origin main && claude [計畫文件路徑]
```

---

## 5. 工作目錄規則

| 環境 | 工作目錄 | 規則 |
|------|---------|------|
| Claude Sonnet（設計） | /tmp/[repo]-repo | 設計完立刻 push，不在 /tmp 長期存放 |
| Claude Code（執行） | C:\AI_WorkDir\GitHub\[repo名稱] | 永遠從這裡執行，不從 /tmp |
| 兩者同時操作 | 危險：容易分叉 | 必須先 push，再讓 Claude Code pull |

---

## 6. 分叉處理（Divergent Branches）

```bash
# 症狀：hint: You have divergent branches
# 修法：
git config pull.rebase false
git pull --no-edit origin main
git push origin main
# 然後執行 Step 3 API 驗證
```

---

## 7. known_failures 對應

| 症狀 | KF 編號 | 修法 |
|------|---------|------|
| push 後 Already up to date 但檔案不存在 | KF-012 | 執行 §3 Step 3 API 驗證，確認是否分叉 |
| hint: divergent branches | KF-013 | 執行 §6 分叉處理 |
| Claude Code 找不到計畫文件 | KF-014 | 確認 §4 計畫文件規則，重新 push 並驗證 |

---

## 8. Audit Requirements

每次 push 後記錄：
```
[日期] PUSH-VERIFIED: [repo] [檔案路徑] [commit hash] [API 驗證結果]
```

---

*v1.0 · 2026-05-28 · prospera-ci-shared/skills/ · 設計：Claude Sonnet 4.6*
