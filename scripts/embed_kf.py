# ── Prospera SYSTEM HEADER (ADR-0032/SBOM) ──
# 性質:engineering ｜設計:Kevin 架構 ｜執行:AI 工具(claude.ai+Claude Code)
# 驗證:無機制驗證 ｜IP:創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
"""Embed updated known_failures.md into write_skills.py"""
kf_path = r"C:\AI_WorkDir\GitHub\prospera-infra-ci\skills\known_failures.md"
ws_path = r"C:\AI_WorkDir\GitHub\prospera-infra-ci\scripts\write_skills.py"

kf_content = open(kf_path, encoding="utf-8").read()
kf_escaped = kf_content.replace("\n", "\\n").replace("'", "\\'")

ws = open(ws_path, encoding="utf-8").read()

fname_idx = ws.find("fname = 'known_failures.md'")
content_start = ws.rfind("content = '", 0, fname_idx)
content_val_start = content_start + len("content = '")
end_quote = ws.rfind("'", content_val_start, fname_idx)

new_ws = ws[:content_val_start] + kf_escaped + ws[end_quote:]
open(ws_path, "w", encoding="utf-8").write(new_ws)
print(f"write_skills.py updated, size={len(new_ws)}")

ws2 = open(ws_path, encoding="utf-8").read()
print(f"KF-021 in write_skills.py: {'KF-021' in ws2}")
print(f"KF-022 in write_skills.py: {'KF-022' in ws2}")
