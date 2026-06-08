#!/usr/bin/env python3
"""actions_usage_lint.py — 掃描 repo 的 .github/workflows/*.yml，對照 Actions 用量治理政策
MUST 1-5 / SHOULD 6 判定 FAIL/WARN。

SSOT 規範：prospera-constitution-governance/governance/ACTIONS_USAGE_POLICY.md
等級分層：唯一 FAIL = 高頻 cron（MUST 5，可靜態證明灌量）；其餘為 WARN（衛生 / 無法靜態證明）。

用法：
    python actions_usage_lint.py [--target <repo_root>]
    --target 預設為當前目錄；掃描 <target>/.github/workflows/*.yml
退出碼：任一 FAIL → 1；只有 WARN / 全 PASS → 0。
"""
import argparse
import glob
import os
import re
import sys

# Windows 主控台預設 cp950 無法輸出 emoji；統一切 utf-8（CI ubuntu 不受影響）
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

try:
    import yaml
except ImportError:
    print("ERROR: 需要 PyYAML（pip install pyyaml）", file=sys.stderr)
    sys.exit(2)

GIT_PUSH_RE = re.compile(r"\bgit\s+push\b")
# actor 守衛：if 條件含 github-actions[bot] 或 github.actor 比對
ACTOR_GUARD_RE = re.compile(r"github-actions|github\.actor", re.IGNORECASE)
# runner OS 倍率
MULTIPLIER_OS_RE = re.compile(r"windows|macos|macOS", re.IGNORECASE)
# windows/macos 理由註解（任一關鍵字出現在註解行即視為已說明）
REASON_RE = re.compile(r"#.*(理由|reason|required|必須|because|build|需求)", re.IGNORECASE)


def load_yaml(path):
    """以 utf-8-sig 讀檔（剝 BOM），safe_load。回傳 (cfg, raw_text, error)。"""
    with open(path, "r", encoding="utf-8-sig") as f:
        raw = f.read()
    try:
        cfg = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return None, raw, f"YAML 解析失敗: {e}"
    if not isinstance(cfg, dict):
        return None, raw, "頂層非 mapping"
    return cfg, raw, None


def get_on_block(cfg):
    """取 on 區塊。YAML 1.1 把裸 on: 解析成 True key → 同時檢查 'on' 與 True。
    回傳正規化 dict：{event: spec_or_None}。"""
    on_raw = cfg.get("on")
    if on_raw is None and True in cfg:
        on_raw = cfg[True]
    if on_raw is None:
        return {}
    if isinstance(on_raw, str):
        return {on_raw: None}
    if isinstance(on_raw, list):
        return {str(e): None for e in on_raw}
    if isinstance(on_raw, dict):
        return on_raw
    return {}


def iter_steps(cfg):
    """產生 (job_name, step_dict)。"""
    jobs = cfg.get("jobs") or {}
    if not isinstance(jobs, dict):
        return
    for jname, job in jobs.items():
        if not isinstance(job, dict):
            continue
        for step in (job.get("steps") or []):
            if isinstance(step, dict):
                yield jname, step


def collect_runner_os(cfg):
    """蒐集所有 runner OS 字串（runs-on 直值 + matrix 展開值）。"""
    osv = []
    jobs = cfg.get("jobs") or {}
    if not isinstance(jobs, dict):
        return osv
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        ro = job.get("runs-on")
        if isinstance(ro, str):
            osv.append(ro)
        elif isinstance(ro, list):
            osv.extend(str(x) for x in ro)
        # matrix 展開（runs-on: ${{ matrix.os }}）
        strat = job.get("strategy") or {}
        matrix = strat.get("matrix") if isinstance(strat, dict) else None
        if isinstance(matrix, dict):
            for v in matrix.values():
                if isinstance(v, list):
                    osv.extend(str(x) for x in v)
                elif isinstance(v, str):
                    osv.append(v)
    return osv


def cron_subdaily(expr):
    """判斷 cron 是否觸發間隔 < 1 天。回傳 True=高頻（FAIL）。
    cron 欄位：min hour dom mon dow"""
    parts = str(expr).split()
    if len(parts) < 5:
        return False  # 格式異常，不誤判
    minute, hour = parts[0], parts[1]

    def multi(field):
        # step（*/N 或 a/b）、萬用 *、逗號列、區間 → 多值
        return ("/" in field) or (field == "*") or ("," in field) or ("-" in field)

    # 分鐘多值 → 一小時內多次 → 高頻
    if multi(minute):
        return True
    # 分鐘單值但小時多值 → 一天內多次 → 高頻
    if multi(hour):
        return True
    # 分鐘單值 + 小時單值 → 一天 <=1 次 → 合規
    return False


def lint_file(path):
    """回傳 (findings, parse_error)。findings = [(level, rule, msg)]。"""
    findings = []
    cfg, raw, err = load_yaml(path)
    if err:
        # 解析失敗本身不當 FAIL（避免假 FAIL），列 WARN 提示人工檢查
        return [("WARN", "PARSE", err)], True

    on_block = get_on_block(cfg)
    events = set(on_block.keys())
    on_is_list_shorthand = isinstance(cfg.get("on"), list) or (
        True in cfg and isinstance(cfg.get(True), list)
    )

    # ---- 蒐集 git push 與 actor 守衛 ----
    has_git_push = False
    has_actor_guard = False
    for _, step in iter_steps(cfg):
        run = step.get("run")
        if isinstance(run, str) and GIT_PUSH_RE.search(run):
            has_git_push = True
        ifc = step.get("if")
        if isinstance(ifc, str) and ACTOR_GUARD_RE.search(ifc):
            has_actor_guard = True
    # job 層級 if 守衛
    jobs = cfg.get("jobs") or {}
    if isinstance(jobs, dict):
        for job in jobs.values():
            if isinstance(job, dict) and isinstance(job.get("if"), str) and ACTOR_GUARD_RE.search(job["if"]):
                has_actor_guard = True

    push_triggered = "push" in events

    # ---- MUST 1：push 觸發 + git push（保守 → WARN）----
    if push_triggered and has_git_push:
        if has_actor_guard:
            pass  # 有 actor 守衛 → PASS
        else:
            findings.append(("WARN", "MUST1",
                "push 觸發且 job 內含 `git push`、無 `if` actor 守衛 → 人工確認是否帶 [skip ci]/防循環"))

    # ---- MUST 2：缺 concurrency ----
    if "concurrency" not in cfg:
        findings.append(("WARN", "MUST2", "缺頂層 concurrency 去重區塊"))
    else:
        # 寫入型補充提醒
        if has_git_push:
            conc = cfg.get("concurrency") or {}
            if isinstance(conc, dict) and conc.get("cancel-in-progress") is True:
                findings.append(("WARN", "MUST2+",
                    "寫入型 workflow（含 git push）建議 cancel-in-progress: false，避免中斷 commit"))

    # ---- MUST 3：push/PR 缺 paths 過濾 ----
    for ev in ("push", "pull_request"):
        if ev not in events:
            continue
        if on_is_list_shorthand:
            findings.append(("WARN", "MUST3",
                f"`on` 用陣列簡寫，`{ev}` 無法帶 paths → 請展開成 map 並加 paths/paths-ignore"))
            continue
        spec = on_block.get(ev)
        if not isinstance(spec, dict) or not ({"paths", "paths-ignore"} & set(spec.keys())):
            findings.append(("WARN", "MUST3", f"`{ev}` 缺 paths/paths-ignore 過濾"))

    # ---- MUST 4：windows/macos runner 無理由 ----
    runner_os = collect_runner_os(cfg)
    if any(MULTIPLIER_OS_RE.search(o) for o in runner_os):
        if not REASON_RE.search(raw):
            hit = [o for o in runner_os if MULTIPLIER_OS_RE.search(o)]
            findings.append(("WARN", "MUST4",
                f"runs-on 用倍率 runner {hit} 且無理由註解（Windows ×2 / macOS ×10）"))

    # ---- MUST 5：高頻 cron（唯一 FAIL）----
    sched = on_block.get("schedule")
    if isinstance(sched, list):
        for entry in sched:
            if isinstance(entry, dict) and "cron" in entry:
                if cron_subdaily(entry["cron"]):
                    findings.append(("FAIL", "MUST5",
                        f"cron '{entry['cron']}' 觸發間隔 < 1 天（高頻灌量）"))

    # ---- SHOULD 6：job 缺 timeout-minutes ----
    if isinstance(jobs, dict):
        no_timeout = [n for n, j in jobs.items()
                      if isinstance(j, dict) and "uses" not in j and "timeout-minutes" not in j]
        if no_timeout:
            findings.append(("WARN", "SHOULD6", f"job 缺 timeout-minutes: {no_timeout}"))

    return findings, False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=".", help="repo root（掃描 <target>/.github/workflows）")
    args = ap.parse_args()

    wf_dir = os.path.join(args.target, ".github", "workflows")
    files = sorted(glob.glob(os.path.join(wf_dir, "*.yml")) +
                   glob.glob(os.path.join(wf_dir, "*.yaml")))

    print(f"=== Actions Usage Lint ===")
    print(f"target: {os.path.abspath(args.target)}")
    print(f"workflows: {len(files)} 支\n")

    if not files:
        print("（無 workflow 檔，跳過）")
        return 0

    total_fail = total_warn = 0
    for path in files:
        name = os.path.basename(path)
        findings, _ = lint_file(path)
        fails = [f for f in findings if f[0] == "FAIL"]
        warns = [f for f in findings if f[0] == "WARN"]
        total_fail += len(fails)
        total_warn += len(warns)
        if not findings:
            print(f"✅ {name}  PASS")
        else:
            mark = "🔴" if fails else "🟡"
            print(f"{mark} {name}")
            for level, rule, msg in findings:
                icon = "🔴 FAIL" if level == "FAIL" else "🟡 WARN"
                print(f"     {icon} [{rule}] {msg}")
        print()

    print("=== 彙總 ===")
    print(f"FAIL: {total_fail}   WARN: {total_warn}")
    if total_fail:
        print("結果：FAIL（擋合入）")
        return 1
    print("結果：PASS（僅 WARN，不擋合入）" if total_warn else "結果：PASS（全乾淨）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
