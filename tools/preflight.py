#!/usr/bin/env python3
"""Offline preflight for the ao-may-marketing skill.

Mirrors the checks SKILL.md §3 asks the model to run, so problems are caught
before a release instead of in ChatGPT.

  python3 tools/preflight.py            # missing assets of active stores = WARN
  python3 tools/preflight.py --strict   # missing assets = FAIL (use before release)

Exit code 1 if any FAIL.
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "ao-may-marketing"
ASSETS = SKILL / "assets"

# Every Vietnamese letter (upper + lower) plus digits and common punctuation.
VI_UPPER = "AĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXY"
TONES = ["", "́", "̀", "̉", "̃", "̣"]  # sắc huyền hỏi ngã nặng
VOWELS = "AĂÂEÊIOÔƠUƯY"
CHARSET = set(VI_UPPER + VI_UPPER.lower() + "0123456789 .,:;!?-–/&%+()\"'")
for v in VOWELS + VOWELS.lower():
    for t in TONES:
        CHARSET.add(unicodedata.normalize("NFC", v + t))
CHARSET = {c for c in CHARSET if len(c) == 1}

rows = []  # (store, item, status, reason)


def add(store, item, status, reason=""):
    rows.append((store, item, status, reason))


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_rgba(p: Path):
    try:
        from PIL import Image
    except ImportError:
        return "WARN", "Pillow chưa cài, bỏ qua kiểm tra RGBA"
    im = Image.open(p)
    if im.mode != "RGBA":
        return "FAIL", f"mode {im.mode}, cần RGBA"
    lo, _ = im.getchannel("A").getextrema()
    if lo == 255:
        return "FAIL", "RGBA nhưng không có điểm trong suốt"
    return "OK", "RGBA, có nền trong suốt"


def check_font(p: Path):
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return "WARN", "fontTools chưa cài, bỏ qua kiểm tra dấu"
    cmap = TTFont(str(p)).getBestCmap()
    missing = sorted(c for c in CHARSET if ord(c) not in cmap)
    if missing:
        return "FAIL", "thiếu ký tự: " + "".join(missing[:30])
    return "OK", "đủ dấu tiếng Việt"


def check_store(spec_path: Path, strict: bool):
    code = spec_path.parent.name
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        add(code, "spec.json", "FAIL", f"JSON lỗi: {e}")
        return
    status, route = spec.get("status"), spec.get("route")
    if spec.get("store_code") != code:
        add(code, "spec.json", "FAIL", f"store_code {spec.get('store_code')!r} khác tên thư mục")
    if status not in ("active", "draft"):
        add(code, "spec.json", "FAIL", f"status {status!r} không hợp lệ")
    if route not in ("direct", "compose", "restyle"):
        add(code, "spec.json", "FAIL", f"route {route!r} không hợp lệ")
    add(code, "spec.json", "OK", f"status={status} route={route}")

    missing_level = "FAIL" if (strict and status == "active") else "WARN"
    for key, f in (spec.get("files") or {}).items():
        rel = f.get("path", "")
        p = ASSETS / rel
        if f.get("optional"):
            add(code, rel, "OK" if p.exists() else "WARN", "tuỳ chọn")
            continue
        if not p.exists():
            add(code, rel, missing_level if status == "active" else "WARN", "thiếu file")
            continue
        want = (f.get("sha256") or "").lower()
        if want:
            got = sha256(p)
            if got != want:
                add(code, rel, "FAIL", f"SHA-256 lệch: {got[:12]}… ≠ {want[:12]}…")
                continue
        if f.get("require_rgba"):
            st, why = check_rgba(p)
            add(code, rel, st, why)
        else:
            add(code, rel, "OK", "có file" + (", SHA khớp" if want else ""))

    for role, rel in (spec.get("fonts") or {}).items():
        p = ASSETS / rel
        if not p.exists():
            add(code, rel, "FAIL", f"font {role} không tồn tại")
            continue
        st, why = check_font(p)
        add(code, rel, st, f"{role}: {why}")


def check_versions():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^\s*version:\s*([0-9.]+)", text, re.M)
    v = m.group(1) if m else None
    add("skill", "SKILL.md", "OK" if v else "FAIL", f"version {v}")
    changelog = Path(__file__).resolve().parent.parent / "CHANGELOG.md"
    if changelog.exists():
        top = re.search(r"^##\s*\[?([0-9.]+)", changelog.read_text(encoding="utf-8"), re.M)
        cv = top.group(1) if top else None
        add("skill", "CHANGELOG.md", "OK" if cv == v else "FAIL",
            f"mục mới nhất {cv}" + ("" if cv == v else f" ≠ SKILL.md {v}"))
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="thiếu tài sản của cửa hàng active = FAIL")
    args = ap.parse_args()
    check_versions()
    for spec in sorted(ASSETS.glob("stores/*/spec.json")):
        check_store(spec, args.strict)
    w = max(len(r[1]) for r in rows)
    for store, item, st, why in rows:
        print(f"{store:5} {item:<{w}}  {st:4}  {why}")
    fails = sum(1 for r in rows if r[2] == "FAIL")
    warns = sum(1 for r in rows if r[2] == "WARN")
    print(f"\n{fails} FAIL · {warns} WARN")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
