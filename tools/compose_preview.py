#!/usr/bin/env python3
"""Local preview of a route-compose poster, built only from the store's spec.json.

  python3 tools/compose_preview.py DQH
  python3 tools/compose_preview.py DQH --headline "GIẶT HẤP" --subline "Áo dài, vest, đầm" \
      --benefits "Giao nhận miễn phí|Hấp đúng chất liệu|Gấp gọn" --subject ao.jpg

Output in dist/:
  preview_<CODE>.png          the poster as the spec describes it
  preview_<CODE>_guides.png   same + spec boxes outlined (+ ref_approved blended 50% if present)
  preview_<CODE>_compare.png  preview | ref_approved side by side (only if ref_approved exists)

Missing asset files are drawn as grey placeholders in the preview only;
nothing under assets/ is created or modified. Needs Pillow.
"""
import argparse
import json
import sys
import unicodedata
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "skills" / "ao-may-marketing" / "assets"
GREY = (150, 150, 150, 255)
LABEL_FONT = ASSETS / "chain" / "fonts" / "BeVietnamPro-SemiBold.ttf"  # has Vietnamese, unlike Pillow default
report = []  # (status, item, detail)


def note(status, item, detail):
    report.append((status, item, detail))


def asset(spec, key):
    """Open files.<key> as RGBA, or None (logged) if missing."""
    rel = spec["files"][key]["path"]
    p = ASSETS / rel
    if not p.exists():
        note("WARN", rel, "thiếu file, vẽ ô xám thay thế")
        return None
    return Image.open(p).convert("RGBA")


def put(canvas, img, xy):
    """Alpha-composite img onto canvas at xy (xy may be negative / off-canvas)."""
    layer = Image.new("RGBA", canvas.size)
    layer.paste(img, (int(xy[0]), int(xy[1])))
    return Image.alpha_composite(canvas, layer)


def placeholder(canvas, box, label):
    x, y, w, h = box
    d = ImageDraw.Draw(canvas)
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(220, 220, 220, 255), outline=GREY, width=3)
    d.text((x + 10, y + 8), label, fill=(80, 80, 80, 255), font=ImageFont.truetype(str(LABEL_FONT), 18))


CAP_AS_HEIGHT = False  # set by --cap-as-height


def font_for_cap(path, cap_px):
    """*_cap_px read as font size (default) or, with --cap-as-height, as height of 'H'.

    ponytail: spec/SKILL.md don't define it; font-size reading is the one where short
    headlines fit the zone width. Confirm against ref_approved, then drop the flag.
    """
    if not CAP_AS_HEIGHT:
        return ImageFont.truetype(path, cap_px)
    ref = ImageFont.truetype(path, 1000)
    t, b = ref.getbbox("H")[1::2]
    return ImageFont.truetype(path, max(1, round(1000 * cap_px / (b - t))))


def fit_font(path, text, w, h, stroke=0):
    """Largest font size whose ink box (with stroke) fits w×h."""
    for size in range(h * 2, 5, -1):
        f = ImageFont.truetype(path, size)
        l, t, r, b = f.getbbox(text, stroke_width=stroke)
        if r - l <= w and b - t <= h:
            return f
    return ImageFont.truetype(path, 6)


def line_width(font, text, tracking):
    return font.getlength(text) + tracking * (len(text) - 1)


def render_line(text, font, hs):
    """One headline line: shadow → white stroke → black fill, tracked per char, then sheared."""
    emb, stroke = hs.get("embolden_px", 0), hs.get("stroke_px", 0)
    track = hs.get("tracking_px", 0)
    dx, dy = hs.get("shadow_offset_px", [0, 0])
    pad = emb + stroke + abs(dx) + abs(dy) + font.size // 2
    w = int(line_width(font, text, track)) + 2 * pad
    h = int(font.size * 1.6) + 2 * pad
    img = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(img)
    # ponytail: per-char draw keeps pair kerning only via getlength(prefix); no raqm shaping.
    xs = [pad + font.getlength(text[:i]) + track * i for i in range(len(text))]
    y = pad + font.size // 3
    layers = []  # all shadows, then all strokes, then all fills
    if dx or dy:
        layers.append(((dx, dy), hs.get("shadow_color", "#000000"), emb + stroke))
    if stroke:
        layers.append(((0, 0), hs.get("stroke_color", "#FFFFFF"), emb + stroke))
    layers.append(((0, 0), hs.get("fill", "#000000"), emb))
    for (ox, oy), color, sw in layers:
        for x, ch in zip(xs, text):
            d.text((x + ox, y + oy), ch, font=font, fill=color, stroke_width=sw, stroke_fill=color)
    shear = hs.get("shear", 0)
    if shear:
        # Pillow AFFINE maps output→input: x_in = x + shear*y + c.
        extra = int(abs(shear) * h) + 1
        c = -shear * h if shear > 0 else 0
        img = img.transform((w + extra, h), Image.AFFINE, (1, shear, c, 0, 1, 0), Image.BICUBIC)
    if hs.get("line_rotate_deg"):
        img = img.rotate(hs["line_rotate_deg"], expand=True, resample=Image.BICUBIC)
    return img.crop(img.getbbox())


def split_headline(text, spec_h, path):
    """'|' forces the split; else one line at one_line_cap_px if it fits the zone, else best 2-line split."""
    zw = spec_h["zone"][2]
    track = spec_h.get("tracking_px", 0)
    if "|" in text:
        lines = [s.strip() for s in text.split("|")]
        return lines, font_for_cap(path, spec_h["one_line_cap_px" if len(lines) == 1 else "two_line_cap_px"])
    one = font_for_cap(path, spec_h["one_line_cap_px"])
    if line_width(one, text, track) <= zw:
        return [text], one
    two = font_for_cap(path, spec_h["two_line_cap_px"])
    words = text.split()
    splits = [(" ".join(words[:i]), " ".join(words[i:])) for i in range(1, len(words))] or [(text,)]
    best = min(splits, key=lambda ls: max(line_width(two, s, track) for s in ls))
    return list(best), two


def draw_headline(canvas, spec, text):
    hs = spec["headline"]
    x, y, w, h = hs["zone"]
    text = unicodedata.normalize("NFC", text)
    if hs.get("uppercase", True):
        text = text.upper()
    hdir = ASSETS / spec["files"].get("headline_dir", {}).get("path", "-")
    precut = [p for p in hdir.glob("*.png") if unicodedata.normalize("NFC", p.stem).upper() == text.replace("|", " ")] if hdir.is_dir() else []
    if precut:
        img = Image.open(precut[0]).convert("RGBA")
        k = min(1, w / img.width, h / img.height)  # uniform scale, down only
        img = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
        note("OK", "headline", f"dùng PNG cắt sẵn {precut[0].name}, scale {k:.3f}")
        return put(canvas, img, (x + (w - img.width) // 2, y + (h - img.height) // 2))

    path = str(ASSETS / spec["fonts"]["headline"])
    lines, font = split_headline(text, hs, path)
    if len(lines) > 2:
        note("FAIL", "headline", f"{len(lines)} dòng, SKILL.md cho tối đa 2")
    imgs = [render_line(s, font, hs) for s in lines]
    # ponytail: lines stacked ink-box to ink-box (white strokes touch); spec has no leading value.
    bw, bh = max(i.width for i in imgs), sum(i.height for i in imgs)
    note("OK", "headline", f"{len(lines)} dòng, cỡ font {font.size} ({'one' if len(lines) == 1 else 'two'}_line_cap_px, "
                             f"{'chiều cao chữ hoa' if CAP_AS_HEIGHT else 'cỡ font'}), khối {bw}×{bh}")
    if bw > w:
        note("WARN", "headline", f"rộng {bw} vượt zone {w} (không tự thu nhỏ)")
    if bh > h:
        note("INFO", "headline", f"cao {bh} > zone {h} (tính cả dấu, viền, bóng) — so với ref_approved")
    cy = y + (h - bh) // 2
    for img in imgs:
        canvas = put(canvas, img, (x + (w - img.width) // 2, cy))
        cy += img.height
    return canvas


def draw_text_box(canvas, box, text, font_path, fill, stroke=0, stroke_color=None, f=None):
    x, y, w, h = box
    f = f or fit_font(font_path, text, w, h, stroke)
    l, t, r, b = f.getbbox(text, stroke_width=stroke)
    ImageDraw.Draw(canvas).text((x + (w - (r - l)) / 2 - l, y + (h - (b - t)) / 2 - t), text, font=f,
                                fill=fill, stroke_width=stroke, stroke_fill=stroke_color)


def draw_logo(canvas, spec):
    lg = spec["logo"]
    img = asset(spec, "logo")
    if img is None:
        placeholder(canvas, lg["content_box"], "THIẾU logo")
        return canvas
    s = lg["scale"]
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    bbox = img.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    px, py = lg["paste_at"]
    if bbox:
        got = [px + bbox[0], py + bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
        diff = [g - e for g, e in zip(got, lg["content_box"])]
        st = "OK" if max(map(abs, diff)) <= 3 else "WARN"
        note(st, "logo", f"vùng nét thật {got} · content_box {lg['content_box']} · lệch {diff} (cho phép ±3)")
    else:
        note("WARN", "logo", "ảnh logo trong suốt hoàn toàn sau khi scale")
    return put(canvas, img, (px, py))


def draw_subject(canvas, spec, path):
    x, y, w, h = spec["subject_box"]
    if not path:
        placeholder(canvas, spec["subject_box"], "ẢNH CHỦ THỂ (--subject)")
        return canvas
    img = Image.open(path).convert("RGBA")
    cutout = img.getchannel("A").getextrema()[0] < 255
    pad = 0 if cutout else 16
    k = min((w - 2 * pad) / img.width, (h - 2 * pad) / img.height)
    img = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
    ix, iy = x + (w - img.width) // 2, y + (h - img.height) // 2
    if not cutout:  # SKILL.md §3B.3: no clean cutout → rounded white card with black outline
        ImageDraw.Draw(canvas).rounded_rectangle(
            [ix - pad, iy - pad, ix + img.width + pad, iy + img.height + pad], 24,
            fill="#FFFFFF", outline="#000000", width=4)
    note("OK", "subject", ("cutout" if cutout else "thẻ trắng viền đen") + f", scale {k:.3f}")
    return put(canvas, img, (ix, iy))


def draw_benefits(canvas, spec, items):
    bb = spec["benefit_bar"]
    x, y, w, h = bb["box"]
    if len(items) > bb["max_items"]:
        note("FAIL", "benefit_bar", f"{len(items)} mục, spec cho tối đa {bb['max_items']}")
    # ponytail: spec has no bar colours; white fill + black border assumed (DQH sticker style).
    ImageDraw.Draw(canvas).rounded_rectangle([x, y, x + w - 1, y + h - 1], bb["radius"],
                                             fill="#FFFFFF", outline="#000000", width=bb["border_px"])
    inner = bb["border_px"] + 10
    seg = (w - 2 * inner) / max(1, len(items))
    body = str(ASSETS / spec["fonts"]["body"])
    boxes = [(round(x + inner + i * seg), y + inner, round(seg) - 12, h - 2 * inner) for i in range(len(items))]
    # one size for all items: the largest that fits every segment
    f = min((fit_font(body, t, b[2], b[3]) for t, b in zip(items, boxes)), key=lambda f: f.size, default=None)
    for t, b in zip(items, boxes):
        draw_text_box(canvas, b, t, body, "#000000", f=f)


def draw_footer(canvas, spec):
    box = spec["footer"]["box"]
    img = asset(spec, "footer")
    if img is None:
        placeholder(canvas, box, "THIẾU cta-footer")
        return canvas
    if img.size != tuple(box[2:]):
        note("WARN", "footer", f"file {img.width}×{img.height} ≠ box {box[2]}×{box[3]}; dán nguyên, không scale")
    return put(canvas, img, box[:2])


def guides(img, spec):
    d = ImageDraw.Draw(img)
    boxes = {"logo": spec["logo"]["content_box"], "headline": spec["headline"]["zone"],
             "subline": spec["subline"]["box"], "subject": spec["subject_box"],
             "benefit": spec["benefit_bar"]["box"], "footer": spec["footer"]["box"]}
    for name, (x, y, w, h) in boxes.items():
        d.rectangle([x, y, x + w - 1, y + h - 1], outline=(255, 0, 120, 255), width=2)
        d.text((x + 4, y + 2), name, fill=(255, 0, 120, 255), font=ImageFont.truetype(str(LABEL_FONT), 16))
    return img


def main():
    ap = argparse.ArgumentParser(description="Xem trước poster route compose theo spec.json")
    ap.add_argument("code")
    ap.add_argument("--headline", default="GIẶT HẤP", help="dùng | để ép xuống dòng")
    ap.add_argument("--subline", default="Áo dài · vest · đầm dạ hội")
    ap.add_argument("--benefits", default="Hấp đúng chất liệu|Thơm sạch|Gấp gọn", help="các mục cách nhau bằng |")
    ap.add_argument("--subject", help="ảnh chủ thể (PNG trong suốt hoặc ảnh thường)")
    ap.add_argument("--cap-as-height", action="store_true",
                    help="hiểu *_cap_px là chiều cao chữ hoa thay vì cỡ font")
    args = ap.parse_args()
    global CAP_AS_HEIGHT
    CAP_AS_HEIGHT = args.cap_as_height

    spec_path = ASSETS / "stores" / args.code / "spec.json"
    if not spec_path.exists():
        sys.exit(f"Không có {spec_path.relative_to(ROOT)}")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if spec.get("route") != "compose":
        sys.exit(f"{args.code} route={spec.get('route')!r}: chỉ xem trước được route compose")
    if spec.get("status") != "active":
        note("WARN", "spec", f"status={spec.get('status')}: skill sẽ không làm poster cho cửa hàng này")
    if spec["headline"].get("font_status") == "provisional":
        note("WARN", "headline", "font tiêu đề chưa duyệt (provisional)")

    W, H = spec["canvas"]
    bg = asset(spec, "background")
    if bg is None:
        canvas = Image.new("RGBA", (W, H), spec.get("background", {}).get("top_color", "#FFFFFF"))
    else:
        if bg.size != (W, H):
            note("WARN", "background", f"{bg.width}×{bg.height} ≠ canvas {W}×{H}")
        canvas = Image.new("RGBA", (W, H))
        canvas = put(canvas, bg, (0, 0))

    canvas = draw_logo(canvas, spec)
    canvas = draw_headline(canvas, spec, args.headline)
    sl = spec["subline"]
    draw_text_box(canvas, sl["box"], args.subline, str(ASSETS / spec["fonts"]["secondary"]),
                  sl["fill"], sl.get("stroke_px", 0), sl.get("stroke_color"))
    canvas = draw_subject(canvas, spec, args.subject)
    draw_benefits(canvas, spec, [s.strip() for s in args.benefits.split("|") if s.strip()])
    canvas = draw_footer(canvas, spec)

    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    base = out / f"preview_{args.code}"
    poster = canvas.convert("RGB")
    poster.save(f"{base}.png")
    written = [f"{base}.png"]

    ref_rel = spec["files"].get("ref_approved", {}).get("path")
    ref = Image.open(ASSETS / ref_rel).convert("RGB") if ref_rel and (ASSETS / ref_rel).exists() else None
    if ref is not None and ref.size != (W, H):
        note("WARN", "ref_approved", f"{ref.width}×{ref.height} ≠ canvas, đã resize để so")
        ref = ref.resize((W, H), Image.LANCZOS)
    g = Image.blend(poster, ref, 0.5) if ref is not None else poster.copy()
    guides(g, spec).save(f"{base}_guides.png")
    written.append(f"{base}_guides.png")
    if ref is not None:
        side = Image.new("RGB", (W * 2 + 20, H), "white")
        side.paste(poster, (0, 0))
        side.paste(ref, (W + 20, 0))
        side.save(f"{base}_compare.png")
        written.append(f"{base}_compare.png")
    else:
        note("WARN", "ref_approved", "chưa có, không xuất ảnh so sánh")

    for st, item, detail in report:
        print(f"{st:4}  {item:<14} {detail}")
    print("\n" + "\n".join(str(Path(p).relative_to(ROOT)) for p in written))
    sys.exit(1 if any(r[0] == "FAIL" for r in report) else 0)


if __name__ == "__main__":
    main()
