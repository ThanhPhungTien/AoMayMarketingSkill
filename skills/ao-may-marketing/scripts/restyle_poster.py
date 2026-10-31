#!/usr/bin/env python3
"""Route `restyle`: kiểm đủ thông tin cửa hàng, rồi dán khối cố định + logo thật lên nền.

  python3 scripts/restyle_poster.py check MM
  python3 scripts/restyle_poster.py paste MM nen.png MiuMiu_mau01.png [--block cta|ticket]

check: in bảng (mục · OK/FAIL · lý do); thoát mã 1 nếu có FAIL. Chạy TRƯỚC khi sinh nền.
paste: chạy check, kiểm vùng logo của nền trơn, dán bằng Pillow (không dùng công cụ ảnh),
       đọc lại file đã lưu rồi so từng pixel với chính file asset. Mã 1 nếu lỗi.
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

ASSETS = Path(__file__).resolve().parent.parent / "assets"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
REQUIRED_COLORS = ("text_accent", "logo_accent", "on_pink")
VI = "AĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXYaăâbcdđeêghiklmnoôơpqrstuưvxy0123456789"
TONES = ["", "́", "̀", "̉", "̃", "̣"]
CHARSET = set(VI)
for v in "AĂÂEÊIOÔƠUƯYaăâeêioôơuưy":
    for t in TONES:
        c = unicodedata.normalize("NFC", v + t)
        if len(c) == 1:
            CHARSET.add(c)

rows = []


def add(item, status, why=""):
    rows.append((item, status, why))


def load_spec(code):
    p = ASSETS / "stores" / code / "spec.json"
    if not p.exists():
        add("spec.json", "FAIL", f"không có {p}")
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        add("spec.json", "FAIL", f"JSON lỗi: {e}")
        return None


def check_font(p):
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return "WARN", "fontTools chưa cài, bỏ qua kiểm dấu"
    cmap = TTFont(str(p)).getBestCmap()
    miss = sorted(c for c in CHARSET if ord(c) not in cmap)
    return ("FAIL", "thiếu ký tự: " + "".join(miss[:30])) if miss else ("OK", "đủ dấu tiếng Việt")


def check(code):
    rows.clear()
    spec = load_spec(code)
    if not spec:
        return None
    if spec.get("store_code") != code:
        add("store_code", "FAIL", f"{spec.get('store_code')!r} khác thư mục {code}")
    add("status", "OK" if spec.get("status") == "active" else "FAIL", f"status={spec.get('status')}")
    add("route", "OK" if spec.get("route") == "restyle" else "FAIL", f"route={spec.get('route')} (cần restyle)")
    rs = spec.get("restyle") or {}
    if not rs:
        add("restyle", "FAIL", "thiếu mục restyle trong spec.json")
        return spec

    canvas = tuple(rs.get("canvas") or ())
    add("canvas", "OK" if len(canvas) == 2 else "FAIL", f"{canvas}")

    files = spec.get("files") or {}
    for need in ("logo", "cta"):
        if need not in files:
            add(f"files.{need}", "FAIL", "chưa khai báo")
    for key, f in files.items():
        p = ASSETS / f.get("path", "")
        opt = f.get("optional")
        if not p.exists():
            add(f"files.{key}", "WARN" if opt else "FAIL", f"thiếu file {f.get('path')}")
            continue
        want = (f.get("sha256") or "").lower()
        if want and hashlib.sha256(p.read_bytes()).hexdigest() != want:
            add(f"files.{key}", "FAIL", "SHA-256 không khớp")
            continue
        im = Image.open(p)
        if f.get("require_rgba"):
            if im.mode != "RGBA" or im.getchannel("A").getextrema()[0] == 255:
                add(f"files.{key}", "FAIL", f"cần RGBA có nền trong suốt (mode {im.mode})")
                continue
        if key in ("cta", "ticket") and canvas and im.size != canvas:
            add(f"files.{key}", "FAIL", f"cỡ {im.size} khác canvas {canvas}")
            continue
        if key == "logo" and im.width < rs.get("logo_width", 0):
            add(f"files.{key}", "FAIL", f"rộng {im.width}px < {rs.get('logo_width')}px cần dán")
            continue
        add(f"files.{key}", "OK", f"{im.size[0]}x{im.size[1]}" + (", SHA khớp" if want else ", chưa khai báo SHA"))

    for role in ("headline", "body"):
        rel = (spec.get("fonts") or {}).get(role)
        if not rel:
            add(f"fonts.{role}", "FAIL", "chưa khai báo")
        elif not (ASSETS / rel).exists():
            add(f"fonts.{role}", "FAIL", f"thiếu {rel}")
        else:
            st, why = check_font(ASSETS / rel)
            add(f"fonts.{role}", st, why)

    colors = spec.get("colors") or {}
    for k in REQUIRED_COLORS:
        v = colors.get(k, "")
        add(f"colors.{k}", "OK" if HEX.match(v) else "FAIL", v or "chưa khai báo")

    ct = spec.get("contacts") or {}
    for k in ("hotline", "address"):
        add(f"contacts.{k}", "OK" if ct.get(k) else "FAIL", ct.get(k) or "chưa khai báo")

    for k in ("logo_paste_at", "logo_width", "logo_zone", "blocks"):
        if not rs.get(k):
            add(f"restyle.{k}", "FAIL", "chưa khai báo")
    for name, b in (rs.get("blocks") or {}).items():
        ok = b.get("file") in files and len(b.get("paste_at") or ()) == 2 and len(b.get("reserve") or ()) == 4
        add(f"restyle.blocks.{name}", "OK" if ok else "FAIL", "file, paste_at, reserve")
    add("restyle.forbid_text", "OK" if rs.get("forbid_text") else "WARN", str(rs.get("forbid_text") or "chưa khai báo"))
    return spec


def show():
    w = max(len(r[0]) for r in rows)
    for item, st, why in rows:
        print(f"{item:<{w}}  {st:4}  {why}")
    bad = [r for r in rows if r[1] == "FAIL"]
    print("\nCHECK:", "FAIL — dừng, báo người dùng bổ sung" if bad else "OK")
    return not bad


def blank_ok(base, zone):
    """Vùng logo của nền phải trơn: chấp nhận chuyển sắc nhẹ, từ chối chữ/vật thể."""
    patch = base.crop(tuple(zone)).convert("RGB")
    diff = ImageChops.difference(patch, patch.filter(ImageFilter.GaussianBlur(4))).convert("L")
    hist = diff.histogram()
    share = sum(hist[23:]) / float(patch.width * patch.height)
    return share <= 0.018, round(share, 5)


def paste(code, base_path, out_path, block_name):
    spec = check(code)
    if not show():
        return 1
    rs, files = spec["restyle"], spec["files"]
    blk = rs["blocks"].get(block_name)
    if not blk:
        print(f"FAIL: không có block {block_name!r}")
        return 1
    canvas = tuple(rs["canvas"])
    block = Image.open(ASSETS / files[blk["file"]]["path"]).convert("RGBA")
    logo = Image.open(ASSETS / files["logo"]["path"]).convert("RGBA")
    lw = rs["logo_width"]
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)

    base = Image.open(base_path).convert("RGBA")
    if base.size != canvas:
        print(f"FAIL: nền {base.size}, cần {canvas} (không tự resize)")
        return 1
    ok, share = blank_ok(base, rs["logo_zone"])
    print(f"vùng logo của nền: chi tiết sắc {share} (≤0.018) -> {'OK' if ok else 'FAIL'}")
    if not ok:
        print("FAIL: vùng logo không trống — sinh lại nền")
        return 1

    out = base.copy()
    out.alpha_composite(block, tuple(blk["paste_at"]))
    pos = tuple(rs["logo_paste_at"])
    out.alpha_composite(logo, pos)
    out.convert("RGB").save(out_path)

    # Kiểm độc lập: đọc lại file đã lưu, so với chính file asset (không so với phép dựng lại).
    got = Image.open(out_path).convert("RGB")
    box = (*pos, pos[0] + logo.width, pos[1] + logo.height)

    def worst(a, b, mask_img, skip=None):
        d = ImageChops.difference(a, b).convert("L")
        m = mask_img.getchannel("A").point(lambda v: 1 if v == 255 else 0)
        d = ImageChops.multiply(d, m)
        if skip:
            d.paste(0, skip)
        return d.getextrema()[1]

    full_block_mask = Image.new("RGBA", canvas)
    full_block_mask.paste(block, tuple(blk["paste_at"]))
    block_rgb = Image.new("RGB", canvas)
    block_rgb.paste(block.convert("RGB"), tuple(blk["paste_at"]))
    cta_diff = worst(got, block_rgb, full_block_mask, skip=box)
    logo_mask = Image.new("RGBA", canvas)
    logo_mask.paste(logo, pos)
    logo_rgb = Image.new("RGB", canvas)
    logo_rgb.paste(logo.convert("RGB"), pos)
    logo_diff = worst(got, logo_rgb, logo_mask)

    good = cta_diff == 0 and logo_diff <= 4
    print(f"khối {block_name}: chênh tối đa {cta_diff} (phải 0)")
    print(f"logo: chênh tối đa {logo_diff} (≤4)")
    print("PASTE:", "OK" if good else "FAIL")
    return 0 if good else 1


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("code")
    p = sub.add_parser("paste")
    p.add_argument("code")
    p.add_argument("base")
    p.add_argument("out")
    p.add_argument("--block", default="cta")
    a = ap.parse_args()
    if a.cmd == "check":
        check(a.code)
        sys.exit(0 if show() else 1)
    sys.exit(paste(a.code, a.base, a.out, a.block))


if __name__ == "__main__":
    main()
