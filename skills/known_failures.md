# ProsperaGen Known Failures
## Document Header
- Document Type: Audit
- Version: v1.0
- Status: Active（Append-only，不可修改已有記錄）
- Owner: prospera-ci-shared/skills/
- Governing Authority: prospera-engineering-codex v1.0
- Last Updated: 2026-05-19

---

## 使用規則

CI 失敗時：
1. 先查這個檔案
2. 找到匹配症狀 → 直接套標準修法，不試錯
3. 找不到 → 允許試錯 → 成功後補進本檔案
4. 新增記錄格式見 §新增規則

---

## 新增規則

```
## [KF-序號]｜[症狀簡述]
- 症狀：[觸發條件或錯誤訊息]
- 根本原因：[為什麼發生]
- 影響 Repo：[哪些 repo 出現過]
- 標準修法：[可直接執行的指令或步驟]
- 首次發現：[日期]
- DNA 要素：[對應哪個 DNA 要素]
```

---

## KF-001｜YAML 中的 PowerShell 多行註解

- 症狀：CI Fail，`yaml: line 4: could not find expected ':'` 或 `mapping values are not allowed`
- 根本原因：GPT 用 PowerShell `<# ... #>` 包裹 disabled workflow，YAML parser 不認識
- 影響 Repo：Prospera-Governance-Core、prospera-engineering-codex、prospera-generation-layer、prospera-ci-shared
- 標準修法：
  ```powershell
  $template = @'
  # DISABLED [日期] - unified under prospera_guard.yml
  name: [原名稱] (Disabled)
  on:
    workflow_dispatch:
  jobs:
    disabled:
      runs-on: ubuntu-latest
      steps:
        - run: echo "This workflow is disabled"
  '@
  $template | Out-File ".github\workflows\[檔名].yml" -Encoding utf8 -NoNewline
  git add .github\workflows\[檔名].yml
  git commit -m "[P1][CI] fix: replace invalid PS comment with valid YAML disabled stub"
  git push
  ```
- 首次發現：2026-05-07
- DNA 要素：要素四（Commit 四標準）、要素五（可工程實作）

---

## KF-002｜Windows Case-Only 目錄重命名失敗

- 症狀：`git mv 00_GOVERNANCE 00_governance` 在 Windows 無效，git index 仍顯示大寫
- 根本原因：Windows NTFS 不區分大小寫，case-only rename 在 git index 不生效
- 影響 Repo：prospera-registry、prospera-ci-shared、prospera-codex-documentation-standard、prospera-ontology-engine
- 標準修法：三步走
  ```bash
  # 有衝突檔案先撤出
  git mv 00_governance/FILE.md _FILE.tmp
  # 大寫改中性暫名
  git mv 00_GOVERNANCE _gov_tmp
  # 暫名改目標小寫
  git mv _gov_tmp 00_governance
  # 放回檔案
  git mv _FILE.tmp 00_governance/FILE.md
  git commit -m "fix: normalize governance dir to lowercase"
  git push
  ```
- 首次發現：2026-05-17
- DNA 要素：要素六（Repo 六種類型）

---

## KF-003｜GitHub Secret Token 未設定

- 症狀：`Input required and not supplied: token` 或 `terminal prompts disabled`
- 根本原因：workflow 使用 `${{ secrets.PROSPERA_DASHBOARD_TOKEN }}` 但 repo 沒設定這個 Secret
- 影響 Repo：prospera-governance-dashboard、任何使用 checkout 的私有 repo
- 標準修法：
  1. 查 `C:\AI_WorkDir\prospera-credentials.md` 找到 PAT 值
  2. 前往 `https://github.com/ccktaiwan/[repo]/settings/secrets/actions`
  3. New repository secret → Name: `PROSPERA_DASHBOARD_TOKEN` → 貼上 PAT
  4. 確認 workflow 的 checkout 步驟有 `with: token: ${{ secrets.PROSPERA_DASHBOARD_TOKEN }}`
  5. workflow_dispatch 觸發驗證
- 首次發現：2026-05-08
- DNA 要素：要素八（AI 協作協議）

---

## KF-004｜Scanner 判定 Level 0（GOVERNANCE_STATUS.md 缺失）

- 症狀：repo 在 dashboard 顯示 Level 0，但目錄結構存在
- 根本原因：Scanner 找不到 `GOVERNANCE_STATUS.md`，或檔案內容缺少 `maturityLevel` 欄位
- 影響 Repo：prospera-engine（2026-05-18）
- 標準修法：
  ```powershell
  $content = @"
  # GOVERNANCE_STATUS.md
  maturityLevel: 3
  owner: [repo-name]
  governingAuthority: prospera-engineering-codex v1.0
  ciStatus: green
  lastAudit: $(Get-Date -Format 'yyyy-MM-dd')
  "@
  $content | Out-File "GOVERNANCE_STATUS.md" -Encoding utf8
  git add GOVERNANCE_STATUS.md
  git commit -m "[P0][INFRA] chore: add GOVERNANCE_STATUS.md for scanner (Level 3 declaration)"
  git push
  ```
- 首次發現：2026-05-18
- DNA 要素：要素六（Repo 成熟度標準）

---

## KF-005｜JSON 解析失敗（API 回傳 markdown 包裹）

- 症狀：`Expecting value: line 1 column 1 (char 0)` 或 `JSON parse failed`
- 根本原因：Claude API 回傳的 JSON 被 markdown ` ```json ` 包裹，直接 `json.loads()` 失敗
- 影響 Repo：prospera-os（generation_engine.py）
- 標準修法：
  ```python
  import re, json

  def parse_json_robust(raw: str) -> dict:
      cleaned = raw.strip()
      # 清除 markdown code block
      if "```" in cleaned:
          match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
          if match:
              cleaned = match.group(1).strip()
      # 找第一個完整 JSON 物件
      start = cleaned.find("{")
      if start == -1:
          return {"raw_output": raw}
      brace = 0
      for i, c in enumerate(cleaned[start:], start):
          if c == "{": brace += 1
          elif c == "}":
              brace -= 1
              if brace == 0:
                  try:
                      return json.loads(cleaned[start:i+1])
                  except:
                      break
      return {"raw_output": raw}
  ```
- 首次發現：2026-05-17
- DNA 要素：要素五（可工程實作）

---

## KF-006｜PAT 找不到（token 未存檔）

- 症狀：需要設定 Secret 但不知道 PAT 在哪裡
- 根本原因：PAT 產生後沒有存到固定路徑，只存在 GitHub Secrets 中
- 影響 Repo：所有需要設定 PROSPERA_DASHBOARD_TOKEN 的 repo
- 標準修法：
  1. 前往 `https://github.com/settings/tokens`
  2. 找到 `prospera-dashboard-classic` → Regenerate（或建新的）
  3. Expiry 改為 No expiration
  4. 複製 token
  5. 立即存到 `C:\AI_WorkDir\prospera-credentials.md`（見 SKILL-03 格式）
  6. 才去設定 GitHub Secret
- 首次發現：2026-05-08
- DNA 要素：要素八（AI 協作協議）

---

## KF-007｜Dashboard daily schedule 與治理 CI 衝突

- 症狀：prospera-governance-dashboard CI 100% Fail（daily-report workflow 定時觸發失敗）
- 根本原因：`daily-report.yml` 含 `schedule: cron` trigger，定時與治理 CI 同時執行衝突，且 `dashboard_server.py --health-check` 在 Ubuntu CI 環境無法執行（有 Windows 硬編碼路徑 + FastAPI 依賴）
- 影響 Repo：prospera-governance-dashboard
- 標準修法：
  ```yaml
  # 把 on: 區塊從 schedule+workflow_dispatch 改為只有 workflow_dispatch
  on:
    workflow_dispatch:
  # 移除：
  # schedule:
  #   - cron: '30 1 * * *'
  ```
  ```powershell
  git add .github/workflows/daily-report.yml
  git commit -m "[P1][CI] fix: remove schedule trigger prevent governance conflict (manual only)"
  git push
  ```
- 首次發現：2026-05-20
- DNA 要素：要素四（Commit 四標準）

---

*v1.0 · 2026-05-19 · prospera-ci-shared/skills/ · Append-only*
