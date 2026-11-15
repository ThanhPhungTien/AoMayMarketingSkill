#!/usr/bin/env python3
"""Dán ảnh thật (ảnh cửa hàng) vào khung đã chừa trống trên poster, bằng code.

  python3 tools/batch/paste_photo.py poster.png anh.jpg ra.png --crop 0,640,1280,2246 [--rect 60,225,470,590]

poster.png: poster đã dán logo + CTA (restyle_poster.py paste).
--crop x0,y0,x1,y1: vùng cắt trên ảnh gốc (px ảnh gốc), nên cùng tỉ lệ với --rect để không méo.
--rect x,y,rộng,cao: khung trên poster (mặc định 60,225,470,590, tỉ lệ ~4:5).
Ảnh gốc không bị sửa; chỉ cắt, đổi cỡ, bo góc, viền trắng và bóng nhẹ trên bản ra.
Cảnh báo nếu vùng quanh khung trên nền không trơn (ChatGPT lỡ vẽ khung/vật thể sát khung).
"""
import argparse
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

RADIUS = 30
BORDER = 10


def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    out = im.convert("RGBA")
    out.putalpha(m)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("poster")
    ap.add_argument("photo")
    ap.add_argument("out")
    ap.add_argument("--crop", help="x0,y0,x1,y1 trên ảnh gốc")
    ap.add_argument("--rect", default="60,225,470,590")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    x, y, w, h = (int(v) for v in a.rect.split(","))
    base = Image.open(a.poster).convert("RGBA")
    ph = Image.open(a.photo).convert("RGB")
    if a.crop:
        ph = ph.crop(tuple(int(v) for v in a.crop.split(",")))
    asp_ph, asp_rect = ph.width / ph.height, w / h
    if abs(asp_ph - asp_rect) > 0.03:
        print(f"CẢNH BÁO: tỉ lệ cắt {asp_ph:.3f} lệch khung {asp_rect:.3f}, ảnh sẽ bị cắt thêm cho vừa")
        if asp_ph > asp_rect:   # quá ngang: cắt hai bên
            nw = int(ph.height * asp_rect)
            ph = ph.crop(((ph.width - nw) // 2, 0, (ph.width - nw) // 2 + nw, ph.height))
        else:                   # quá dọc: cắt trên dưới
            nh = int(ph.width / asp_rect)
            ph = ph.crop((0, (ph.height - nh) // 2, ph.width, (ph.height - nh) // 2 + nh))
    iw, ih = w - 2 * BORDER, h - 2 * BORDER
    ph = ph.resize((iw, ih), Image.LANCZOS)

    # kiểm: dải 24px quanh khung trên nền gốc phải trơn (không khung/vật thể ChatGPT lỡ vẽ)
    m = 24
    band = base.convert("L").crop((max(0, x - m), max(0, y - m), min(base.width, x + w + m), min(base.height, y + h + m)))
    inner = Image.new("L", band.size, 0)
    ImageDraw.Draw(inner).rectangle([m, m, m + w, m + h], fill=255)
    blur = band.filter(ImageFilter.GaussianBlur(4))
    d = ImageChops.difference(band, blur)
    d = ImageChops.multiply(d.point(lambda v: 255 if v >= 23 else 0), ImageChops.invert(inner))
    share = sum(1 for v in d.getdata() if v) / max(1, band.width * band.height - w * h)
    print(f"vùng quanh khung ảnh: chi tiết sắc {share:.4f} (nên ≤ 0.02) -> {'OK' if share <= 0.02 else 'CẢNH BÁO: nền quanh khung không trơn'}")

    # bóng nhẹ + viền trắng + ảnh bo góc
    pad = 40
    shadow = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([pad, pad + 8, pad + w, pad + h + 8], RADIUS + BORDER, fill=(10, 60, 70, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    base.alpha_composite(shadow, (x - pad, y - pad))
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(frame).rounded_rectangle([0, 0, w - 1, h - 1], RADIUS + BORDER, fill=(255, 255, 255, 255))
    base.alpha_composite(frame, (x, y))
    base.alpha_composite(rounded(ph, RADIUS), (x + BORDER, y + BORDER))
    base.convert("RGB").save(a.out)
    print("đã ghi", a.out)


if __name__ == "__main__":
    main()
