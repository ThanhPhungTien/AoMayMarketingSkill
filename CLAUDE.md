# CLAUDE.md

Repo này là **bản gốc** của skill ChatGPT `ao-may-marketing` (chuỗi nhượng quyền giặt sấy Áo Mây). Bản trên ChatGPT và file zip chỉ là bản sao. Đọc trước: README.md, CHANGELOG.md, RELEASE_PROMPT.md, skills/ao-may-marketing/SKILL.md, references/brand-context.md.

## Nguyên tắc (không tự đổi)
- Mỗi cửa hàng có mã (TH, CH, DQH, TP, NX, AK) và `skills/ao-may-marketing/assets/stores/<MÃ>/spec.json`.
  - `route`: `direct` (model ảnh sinh cả poster) | `compose` (ghép logo/CTA/chữ bằng code — hiện chỉ DQH).
  - `status`: `active` | `draft`; draft thì không làm poster.
- Nguồn sự thật, mỗi thông tin chỉ ở một nơi: cách làm = SKILL.md · thông tin cửa hàng, bài đăng = Notion (Áo Mây | Marketing Hub) · thông số kỹ thuật = spec.json.
- File ảnh (logo, CTA, nền, ảnh mẫu) do người dùng tự làm. Không tạo, vẽ lại hay sửa file ảnh. Không bịa thông tin cửa hàng (giá, ưu đãi, giờ mở cửa, dịch vụ chưa xác nhận).
- Phát hành: tăng `version` trong SKILL.md → thêm mục CHANGELOG.md → `python3 tools/build_release.py` → làm theo RELEASE_PROMPT.md. Zip luôn là bản đầy đủ.
- Không commit hay push khi người dùng chưa đồng ý.

## Lệnh hay dùng
```bash
pip install pillow fonttools
python3 tools/preflight.py            # kiểm tra nhanh, thiếu ảnh = WARN
python3 tools/preflight.py --strict   # thiếu ảnh = FAIL (trước khi phát hành)
python3 tools/build_release.py        # preflight --strict rồi đóng zip vào dist/
```
CI (`.github/workflows/check.yml`) chạy `preflight.py` không `--strict` trên mọi push/PR.

## Việc đang chờ
- Thêm ảnh: `assets/chain/logo-ao-may.png`; `assets/stores/DQH/` gồm `logo.png` (SHA-256 phải khớp spec), `cta-footer.png` (hotline 0942 146 606), `bg-default.png`, `ref-approved.png`, `ref-headline.jpg` → phát hành 1.4.3.
- Font tiêu đề DQH đang là Paytone One, `font_status: provisional`; đổi thành `approved` khi người dùng duyệt.
- CH, TP, NX, AK đang `draft`; bật `active` khi Notion 02 có đủ địa chỉ, hotline, fanpage.
- Điền `release_id` của 1.4.0, 1.4.1, 1.4.2 vào CHANGELOG.md khi người dùng cung cấp.
