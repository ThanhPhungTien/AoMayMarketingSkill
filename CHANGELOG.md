# Changelog

Mỗi bản: ngày · thay đổi · release_id trên ChatGPT (điền sau khi phát hành).

## 1.4.7 — 2026-10-30
- §3C thêm mục 8–9: khối cố định (logo, khối liên hệ, nút, thẻ vé) dựng bằng code; không lặp nhiều vòng sửa bằng model ảnh.
- Gộp file AK (references/AK-editorial-poster-system.md, AK/spec.json) lấy từ bản live 1.4.12 để không bị ghi đè. Manifest plugin 1.4.13. release_id: pluginrel_6ae446e151b081919474aaca18db6999 (đã phát hành, ChatGPT xác nhận)

## 1.4.6 — 2026-10-30
- Đồng bộ repo với bản đang chạy trên ChatGPT (plugin 1.4.11, SKILL.md 1.4.5), vốn đã đi trước repo: thêm mục "Mandatory final export" (DQH-01 phải xuất đúng 1080×1080), sửa bước 3 và 5 của §3A; DQH spec.json điền sha256 cho footer, nền, ref, đổi ref-headline sang .png, thêm footer.canvas_paste_at.
- Các mục 1.4.3 dưới đây gộp vào bản này (số 1.4.3 chỉ từng dùng nội bộ trong repo, chưa phát hành).

### Gộp từ 1.4.3 — 2026-10-30
- Thêm §3C: làm lại poster từ ảnh mẫu (giữ nguyên ảnh mẫu làm nền, một khối logo, đối chiếu từng chữ, icon vector, không thêm thương hiệu khác). Rút ra từ thử nghiệm trên ChatGPT.
- §3C còn quy định: bỏ tên thương hiệu cũ ở mọi nơi (tiêu đề, ảnh, thẻ vé), bỏ tuyên bố riêng của cửa hàng mẫu (since, tiêu chuẩn châu Âu, miễn phí giao nhận, số phần trăm), kiểm icon đúng hình, không tô màu lên vùng ảnh thật, logo cố định góc trên trái ~28% rộng, không nền phụ.
- Chưa phát hành: còn chờ ảnh trong assets (xem CLAUDE.md).
- release_id: (điền)

## 1.4.2 — 2026-10-27
- Kiểm tra dấu chỉ xét nét đen; viền trắng liền quanh dấu là kiểu sticker đã duyệt.
- release_id: (điền)

## 1.4.1 — 2026-10-27
- DQH: `embolden_px` 3 → 0, `tracking_px` −4 → 2 (dấu Ấ bị dính, lỗ chữ A bị bít).
- Tiêu đề phải dựng ở cỡ thật và qua bước kiểm tra dấu chồng.
- release_id: (điền)

## 1.4.0 — 2026-10-27
- Mô hình nhượng quyền: `assets/stores/<MÃ>/spec.json` cho TH, CH, DQH, TP, NX, AK; `route` = direct | compose.
- Preflight bắt buộc; tài sản do người dùng tự làm, model không tạo hay sửa.
- release_id: (điền)

## 1.2.1 → 1.2.3 — 2026-10-22
- Bản cũ: sinh cả poster một lần, cấm ghép bằng code.
