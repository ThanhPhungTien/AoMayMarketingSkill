# Áo Mây Marketing Skill

Skill `ao-may-marketing` cho ChatGPT: caption, kế hoạch bài và poster Facebook cho chuỗi nhượng quyền giặt sấy Áo Mây và từng cửa hàng.

**Repo này là bản gốc.** Thư mục cache trên ChatGPT và các file zip chỉ là bản sao. Mọi thay đổi sửa ở đây trước, rồi mới phát hành.

## Cấu trúc

```
skills/ao-may-marketing/
  SKILL.md                    cách làm (quy trình, kiểm tra)
  references/brand-context.md quy chuẩn chuỗi + bảng cửa hàng (bản chụp từ Notion 02)
  assets/chain/               logo chuỗi, font dùng chung (+ giấy phép OFL)
  scripts/restyle_poster.py   route restyle: kiểm đủ thông tin cửa hàng + dán CTA/logo thật (check | paste)
  assets/stores/<MÃ>/         spec.json + logo, CTA, nền, ảnh mẫu của từng cửa hàng
tools/preflight.py            kiểm tra offline: spec, file, SHA-256, RGBA, font, version
tools/build_release.py        đóng zip đầy đủ vào dist/
tools/compose_preview.py      xem trước poster route compose theo spec.json, ra dist/
RELEASE_PROMPT.md             prompt gửi ChatGPT để phát hành và kiểm tra
CHANGELOG.md                  lịch sử phiên bản + release_id
TEST_PLAN.md                  bài thử end-to-end trên ChatGPT sau mỗi bản phát hành
```

Nguồn sự thật: **cách làm** = SKILL.md · **thông tin cửa hàng, bài đăng** = Notion (Áo Mây | Marketing Hub) · **thông số kỹ thuật** = `spec.json`.

## Quy trình

```bash
pip install pillow fonttools
python3 tools/preflight.py            # kiểm tra nhanh (thiếu ảnh = WARN)
# sửa file, tăng version trong SKILL.md, thêm mục CHANGELOG.md
python3 tools/build_release.py        # preflight --strict rồi đóng zip
```

Sau đó làm theo `RELEASE_PROMPT.md`.

## Thêm cửa hàng

1. Tạo dòng trong Notion 02 Cửa hàng (mã 2–4 chữ in hoa, không dấu).
2. Tạo `skills/ao-may-marketing/assets/stores/<MÃ>/spec.json` (sao từ cửa hàng cùng route), để `status: draft` tới khi đủ thông tin.
3. Thêm cửa hàng vào bảng trong `brand-context.md` và vào `description` của SKILL.md.
4. Tăng version, phát hành.

## Lưu ý

- Repo **private**: chứa logo và thông tin liên hệ của các cửa hàng nhượng quyền.
- File ảnh phải là file gốc (không lấy qua chat/Zalo). Đổi file thì cập nhật `sha256` trong spec.
- Font từ Google Fonts, giấy phép OFL đi kèm trong `assets/chain/fonts/`.
