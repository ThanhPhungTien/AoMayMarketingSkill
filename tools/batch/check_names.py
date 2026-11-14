#!/usr/bin/env python3
"""Soi nhầm tên ảnh sau khi làm hàng loạt poster.

  python3 tools/batch/check_names.py <thư mục kết quả> [--checklist tieude.txt] [--out dist/batch/sheets]

Làm hai việc:
  1. Báo các cặp ảnh giống nhau bất thường (so phần giữa ảnh, bỏ logo và CTA vốn giống hệt).
     Hai ảnh trùng nội dung gần như chắc chắn là một ảnh bị gắn nhầm tên và một ảnh thật bị mất.
  2. Ghép bảng đối chiếu (6 ảnh/bảng, cắt vùng chữ) có ghi tên file và tiêu đề kỳ vọng,
     để soi bằng mắt xem tiêu đề trên ảnh có đúng với số thứ tự không.

--checklist: file văn bản, mỗi dòng một tiêu đề kỳ vọng, dòng thứ N ứng với ảnh _NN
(checklist của đợt, chép từ chính ảnh mẫu của đợt đó). Không có thì chỉ in tên file.
Tên ảnh dạng <MÃ>_NN.png. Cần Pillow.
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HASH = 16          # lưới băm 16x16
DUP_MAX = 12       # khoảng cách Hamming <= ngưỡng này thì coi là trùng (trên 256 bit)
MID = (0, 180, 1080, 900)   # vùng giữa ảnh 1080x1080 (bỏ logo trên và CTA dưới)


def ahash(im):
    g = im.convert("L").crop(MID).resize((HASH, HASH), Image.LANCZOS)
    px = list(g.tobytes())
    avg = sum(px) / len(px)
    return [1 if p > avg else 0 for p in px]


def ham(a, b):
    return sum(x != y for x, y in zip(a, b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--checklist")
    ap.add_argument("--out", default="dist/batch/sheets")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    files = []
    for p in sorted(Path(a.folder).glob("*.png")):
        m = re.search(r"_(\d+)\.png$", p.name)
        if m:
            files.append((int(m.group(1)), p))
    if not files:
        print("Không thấy ảnh dạng <MÃ>_NN.png trong", a.folder)
        sys.exit(1)

    titles = []
    if a.checklist:
        titles = [l.strip() for l in Path(a.checklist).read_text(encoding="utf-8").splitlines()]

    ims = {n: Image.open(p).convert("RGB").resize((1080, 1080)) for n, p in files}
    hashes = {n: ahash(im) for n, im in ims.items()}
    nums = [n for n, _ in files]
    dups = []
    for i, x in enumerate(nums):
        for y in nums[i + 1:]:
            d = ham(hashes[x], hashes[y])
            if d <= DUP_MAX:
                dups.append((x, y, d))
    if titles:
        missing = [n for n in range(1, len(titles) + 1) if n not in ims]
        if missing:
            print("Thiếu ảnh:", ", ".join(f"{n:02d}" for n in missing))
    if dups:
        print("NGHI GẮN NHẦM (hai ảnh gần như trùng):")
        for x, y, d in dups:
            print(f"  _{x:02d} và _{y:02d} (khác biệt {d}/256)")
    else:
        print("Không có cặp ảnh trùng.")

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cols, per = 3, 6
    cw, ch = 600, 400
    for s in range(0, len(nums), per):
        group = nums[s:s + per]
        sheet = Image.new("RGB", (cols * cw, 2 * (ch + 40)), "white")
        d = ImageDraw.Draw(sheet)
        for k, n in enumerate(group):
            x0, y0 = (k % cols) * cw, (k // cols) * (ch + 40)
            sheet.paste(ims[n].crop(MID).resize((cw, ch), Image.LANCZOS), (x0, y0 + 20))
            want = titles[n - 1] if n - 1 < len(titles) else ""
            d.text((x0 + 4, y0 + 4), f"_{n:02d}  kỳ vọng: {want}", fill="red")
        path = out / f"doichieu_{s // per + 1}.png"
        sheet.save(path)
    print(f"Đã ghép {len(range(0, len(nums), per))} bảng đối chiếu vào {out}")


if __name__ == "__main__":
    main()
