# AGENTS.md

Repo này là **bản gốc** của skill ChatGPT `ao-may-marketing` (chuỗi nhượng quyền giặt sấy Áo Mây). Bản trên ChatGPT và file zip chỉ là bản sao. Đọc trước: README.md, CHANGELOG.md, RELEASE_PROMPT.md, skills/ao-may-marketing/SKILL.md, references/brand-context.md.

## Nguyên tắc (không tự đổi)
- Mỗi cửa hàng có mã (TH, CH, DQH, TP, NX, AK) và `skills/ao-may-marketing/assets/stores/<MÃ>/spec.json`.
  - `route`: `direct` (model ảnh sinh cả poster) | `compose` (ghép logo/CTA/chữ bằng code — hiện chỉ DQH).
  - `status`: `active` | `draft`; draft thì không làm poster.
- Nguồn sự thật, mỗi thông tin chỉ ở một nơi: cách làm = SKILL.md · thông tin cửa hàng, bài đăng = Notion (Áo Mây | Marketing Hub) · thông số kỹ thuật = spec.json.
- File ảnh (logo, CTA, nền, ảnh mẫu) do người dùng tự làm. Không tạo, vẽ lại hay sửa file ảnh. Không bịa thông tin cửa hàng (giá, ưu đãi, giờ mở cửa, dịch vụ chưa xác nhận).
- Phát hành: tăng `version` trong SKILL.md → thêm mục CHANGELOG.md → `python3 tools/build_release.py` → làm theo RELEASE_PROMPT.md. Zip luôn là bản đầy đủ.
- Không commit hay push khi người dùng chưa đồng ý.

## Làm poster hàng loạt
Luồng vận hành (vai trò, hai cách làm với ChatGPT, bẫy đã gặp, trạng thái từng cửa hàng): đọc [WORKFLOW.md](WORKFLOW.md) trước khi làm. Người dùng thả thư mục mẫu thì chạy luôn luồng đó, không hỏi lại.

## Lệnh hay dùng
```bash
pip install pillow fonttools
python3 tools/preflight.py            # kiểm tra nhanh, thiếu ảnh = WARN
python3 tools/preflight.py --strict   # thiếu ảnh = FAIL (trước khi phát hành)
python3 tools/build_release.py        # preflight --strict rồi đóng zip vào dist/
python3 tools/compose_preview.py DQH  # xem trước poster compose ra dist/preview_DQH*.png
```
CI (`.github/workflows/check.yml`) chạy `preflight.py` không `--strict` trên mọi push/PR.

## Việc đang chờ
(Cập nhật 2026-11-15.)
- Trạng thái cửa hàng: `active` + route `restyle` = AK, CH, DN, DQH, MM, TH. `draft` = NX, TP (chưa có thông tin xác nhận, không làm poster).
- Chưa commit: spec AK/TH/DQH/MM, logo + CTA của AK/TH/DQH (`stores/*/logo.png`, `cta-bar.png`), `tools/cta-bar-AK.html`, `checklists/`, thay đổi `restyle_poster.py`. `stores/MM/spec.json` không thuộc đợt poster Latusa, commit riêng.
- Phát hành: CHANGELOG mới nhất là 1.4.16 (CH) chưa phát hành (`release_id` còn trống). Bản live trên ChatGPT mới biết đến 1.4.15, chưa biết AK, TH, DQH (restyle) và DN. Muốn dùng plugin cho các cửa hàng đó thì phải tăng version, thêm mục CHANGELOG, build zip và phát hành.
- `release_id` còn thiếu trong CHANGELOG: 1.4.0, 1.4.1, 1.4.2 và một mục trong 1.4.6; điền khi người dùng cung cấp.
- DQH: `bg-default.png` và `ref-approved.png` đánh dấu `optional` vì SHA-256 không khớp; chờ người dùng xác nhận file đúng. Font tiêu đề restyle là Montserrat; `font_status: provisional` chờ người dùng duyệt.
- Poster đã giao: CH 15 (4/11), DQH 30, TH 30, AK 30, DN 30 (14/11, đã duyệt). Thông tin Đà Nẵng đã nhờ ChatGPT ghi lên Notion, chưa xác minh được.
- Làm poster hàng loạt: đọc `WORKFLOW.md`. Nội dung phải đọc từ ảnh mẫu của chính đợt đó, đối chiếu bằng `tools/batch/check_names.py` sau khi gen.
