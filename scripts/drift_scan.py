"""
[Phase4][L0] feat: Drift Scan CI Script
Governing: prospera-engineering-codex v1.0
Human-Reviewed: AI
"""
import argparse, sys
from pathlib import Path

DRIFT = ["應該","建議","考慮","方向","框架","策略","願景","方針"]
SKIP  = ["99_archive","node_modules",".git","known_failures"]

def scan(path, fail):
    hits = []
    for f in Path(path).rglob("*.md"):
        if any(s in str(f) for s in SKIP): continue
        t = f.read_text(encoding="utf-8", errors="ignore")
        for d in DRIFT:
            if d in t: hits.append(f"{f}: '{d}'")
    if hits:
        print("WARN Drift signals:")
        for h in hits: print(f"  {h}")
        if fail: sys.exit(1)
    else:
        print("OK No drift signals")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--path", default=".")
    p.add_argument("--fail-on-drift", action="store_true")
    a = p.parse_args(); scan(a.path, a.fail_on_drift)
