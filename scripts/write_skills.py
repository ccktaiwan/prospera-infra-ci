#!/usr/bin/env python3
# ── Prospera SYSTEM HEADER (ADR-0032/SBOM) ──
# 性質:engineering ｜設計:Kevin 架構 ｜執行:AI 工具(claude.ai+Claude Code)
# 驗證:無機制驗證 ｜IP:創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
"""
write_skills.py — Skills 同步器（A2 修復版，2026-06-11）

★ 修復前的問題（漂移族 A2，反向漂移）：
   - 內容**寫死**在腳本（過時 v1.6 SKILL-CORE，缺 2026-06-08 協作準則段）。
   - 寫到**死路徑** `prospera-infra-ci\skills`（repo 已 rename 為 prospera-infra-ci）。
   - 跑它會**覆蓋 live 手改**的 `infra-ci/skills/*.md`（live 才是 SSOT）。
★ 修復後（本版）：
   - **以 live `infra-ci/skills/*.md` 為單一真相源**（read-only），不再內嵌任何寫死內容。
   - **移除死路徑** `prospera-infra-ci\skills` 寫入。
   - 只**單向同步到 OneDrive 備份**；**絕不回寫 live skills**（live 是源，不被覆蓋）。
   - 對齊 ADR-0019 漂移族原則：產生器/同步器以 .md 為源、禁內容寫死。

用法：python3 write_skills.py        # 同步 live skills/*.md → OneDrive
退出碼：0 成功 / 1 失敗
"""
import os
import sys
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── 路徑（live 為源，OneDrive 為備份目的地）─────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent           # …/prospera-infra-ci/scripts
REPO_ROOT = SCRIPT_DIR.parent                          # …/prospera-infra-ci
LIVE_SKILLS = REPO_ROOT / "skills"                     # ★ SSOT（read-only source）
ONEDRIVE = Path(os.environ.get(
    "PROSPERA_SKILLS_ONEDRIVE",
    r"C:\Users\mouse\OneDrive\Prospera_KB\10_線一_GitHub治理\skills",
))
# 死路徑 prospera-infra-ci\skills：已移除，不再寫入。


def main() -> int:
    if not LIVE_SKILLS.is_dir():
        print(f"[ERROR] live skills 來源不存在：{LIVE_SKILLS}")
        return 1
    md_files = sorted(LIVE_SKILLS.glob("*.md"))
    if not md_files:
        print(f"[ERROR] live skills 無 .md 檔：{LIVE_SKILLS}")
        return 1

    try:
        ONEDRIVE.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[WARN] OneDrive 目錄不可用（{e}）→ 僅列出 live，未同步")
        for f in md_files:
            print(f"  - {f.name}（live）")
        return 0

    copied = 0
    for f in md_files:
        # 讀 live 為源（不修改 live），複製到 OneDrive 備份
        shutil.copy2(f, ONEDRIVE / f.name)
        copied += 1
        print(f"[SYNC] {f.name} → OneDrive")

    print(f"[DONE] {copied} skills 自 live 同步至 OneDrive（live 未被覆蓋；死路徑已移除）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
