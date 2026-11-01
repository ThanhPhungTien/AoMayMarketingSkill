#!/usr/bin/env python3
"""Dựng thanh liên hệ (CTA) của một cửa hàng bằng HTML rồi chụp ra PNG nền trong suốt.

  python3 tools/make_cta_bar.py CH            # ghi assets/stores/CH/cta-bar.png
  python3 tools/make_cta_bar.py CH --out x.png

Đọc hotline, địa chỉ từ stores/<MÃ>/spec.json (mục contacts), font Montserrat từ
assets/chain/fonts. Cần Chrome hoặc Edge trên máy (chạy ngầm), không cần cài thêm.
Chữ trong ảnh là chữ của cửa hàng; đổi hotline hay địa chỉ thì chạy lại lệnh này
rồi cập nhật sha256 trong spec nếu có khai báo.
"""
import argparse
import html
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "skills" / "ao-may-marketing" / "assets"
FONT = ASSETS / "chain" / "fonts" / "Montserrat-VariableFont_wght.ttf"
BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

TEMPLATE = """<!doctype html>
<html lang="vi"><meta charset="utf-8">
<style>
@font-face{font-family:"Mont";src:url("__FONT__");font-weight:100 900}
:root{--teal-d:__TEAL_D__;--teal-l:__TEAL_L__}
html,body{margin:0;background:transparent}
.canvas{position:relative;width:1080px;height:1080px;font-family:"Mont",sans-serif;color:#fff}
.bar{position:absolute;left:36px;top:992px;width:1008px;height:71px;border-radius:36px;
  background:linear-gradient(90deg,var(--teal-d),var(--teal-l));display:flex;align-items:center;
  box-shadow:0 5px 12px rgba(8,80,86,.30)}
.badge{width:44px;height:44px;border-radius:50%;background:#fff;display:grid;place-items:center;flex:none}
.addr{display:flex;align-items:center;gap:16px;padding-left:10px;width:590px;font-weight:600;font-size:21px}
.div{width:2px;height:48px;background:rgba(255,255,255,.45);margin-right:16px}
.tel{display:flex;align-items:center;gap:12px}
.tel small{font-weight:600;font-size:17px}
.tel b{font-weight:700;font-size:32px}
svg{display:block}
</style>
<div class="canvas">
  <div class="bar">
    <div class="addr"><span class="badge"><svg width="22" height="26" viewBox="0 0 22 26"><path d="M11 1C5.5 1 1.5 5 1.5 10.3 1.5 17 11 25 11 25s9.5-8 9.5-14.7C20.5 5 16.5 1 11 1z" fill="__TEAL_D__"/><circle cx="11" cy="10.3" r="3.6" fill="#fff"/></svg></span>
      <span>__ADDRESS__</span></div>
    <div class="div"></div>
    <div class="tel"><span class="badge"><svg width="24" height="24" viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z" fill="__TEAL_D__"/></svg></span>
      <small>HOTLINE:</small><b>__HOTLINE__</b></div>
  </div>
</div>
"""


def find_browser():
    for p in BROWSERS:
        if Path(p).exists():
            return p
    return shutil.which("chrome") or shutil.which("msedge") or shutil.which("chromium")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("--out")
    ap.add_argument("--teal-dark", default="#08656c")
    ap.add_argument("--teal-light", default="#168c94")
    a = ap.parse_args()

    spec_path = ASSETS / "stores" / a.code / "spec.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    c = spec.get("contacts") or {}
    if not c.get("hotline") or not c.get("address"):
        sys.exit(f"{a.code}: spec.json thiếu contacts.hotline hoặc contacts.address, không dựng.")
    if not FONT.exists():
        sys.exit(f"thiếu font {FONT.relative_to(ROOT)}")
    exe = find_browser()
    if not exe:
        sys.exit("không tìm thấy Chrome hoặc Edge để chụp.")

    page = (TEMPLATE.replace("__FONT__", FONT.as_uri())
            .replace("__TEAL_D__", a.teal_dark).replace("__TEAL_L__", a.teal_light)
            .replace("__ADDRESS__", html.escape(c["address"]))
            .replace("__HOTLINE__", html.escape(c["hotline"])))
    out = Path(a.out) if a.out else ASSETS / "stores" / a.code / "cta-bar.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / "cta.html"
        h.write_text(page, encoding="utf-8")
        r = subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--default-background-color=00000000", "--window-size=1080,1080",
                            f"--screenshot={out.resolve()}", h.as_uri()],
                           capture_output=True, text=True)
    if not out.exists():
        sys.exit("chụp thất bại:\n" + (r.stderr or "")[-500:])
    try:
        from PIL import Image
        im = Image.open(out)
        print(f"{out} · {im.size[0]}x{im.size[1]} {im.mode} · vùng nội dung {im.getchannel('A').getbbox()}")
    except Exception:
        print(out)


if __name__ == "__main__":
    main()
