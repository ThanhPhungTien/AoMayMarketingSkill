#!/usr/bin/env python3
"""Build the full release zip for ChatGPT's update_plugin.

  python3 tools/build_release.py                  # runs preflight --strict first
  python3 tools/build_release.py --allow-missing  # release without some images

Output: dist/ao-may-marketing_v<version>.zip with root folder ao-may-marketing/
(always the FULL skill, never a partial zip).
"""
import argparse
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "ao-may-marketing"
SKIP = {".DS_Store", "Thumbs.db"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow-missing", action="store_true",
                    help="cho phép phát hành khi cửa hàng active còn thiếu ảnh")
    args = ap.parse_args()

    cmd = [sys.executable, str(ROOT / "tools" / "preflight.py")]
    if not args.allow_missing:
        cmd.append("--strict")
    if subprocess.run(cmd).returncode != 0:
        sys.exit("Preflight FAIL — sửa lỗi trước khi đóng gói.")

    v = re.search(r"^\s*version:\s*([0-9.]+)", (SKILL / "SKILL.md").read_text(encoding="utf-8"), re.M).group(1)
    out = ROOT / "dist" / f"ao-may-marketing_v{v}.zip"
    out.parent.mkdir(exist_ok=True)
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(SKILL.rglob("*")):
            if p.is_file() and p.name not in SKIP:
                z.write(p, Path("ao-may-marketing") / p.relative_to(SKILL))
                n += 1
    print(f"\n{out.relative_to(ROOT)} · {n} file · version {v}")


if __name__ == "__main__":
    main()
