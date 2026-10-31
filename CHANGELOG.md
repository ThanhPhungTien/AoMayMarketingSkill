# Changelog

Mỗi bản: ngày · thay đổi · release_id trên ChatGPT (điền sau khi phát hành).

## 1.4.10 — 2026-10-31
- §3D viết lại thành danh sách [A]–[D]: lệnh đầu tiên của lượt phải là check và dán bảng vào câu trả lời; ảnh trả về từ công cụ ảnh không phải điểm kết thúc, hành động kế tiếp bắt buộc là Python (lưu nen.png, đổi cỡ, paste). Lý do: 1.4.9 vẫn dừng sau bước nền khi thử lại bài giày. Chưa phát hành; release_id: (điền)
- Bổ sung (prompt ngắn): §3D bước 2 và spec `prompt_policy`: prompt gửi model ảnh chỉ nêu mẫu, chủ đề, nhận diện, vùng trống bắt buộc và điều cấm; bố cục để model tự sáng tạo. `components` chỉ là danh sách kiểm tra sau khi sinh, không đưa vào prompt.
- Bổ sung (dạng poster): spec restyle thêm `poster_types` (compare = so sánh trước/sau, single = không so sánh, một ảnh minh họa chính); component `before_after` đổi thành `visual` theo dạng. §3D bước 2 dặn chọn dạng theo ảnh mẫu.
- Bổ sung (vị trí logo): spec restyle thêm `logo_position` chỉ nhận `top-left`, `top-center`, `top-right` (kèm `logo_margin`, `logo_zone_height`), thay cho việc nhập toạ độ x,y. Script tự tính toạ độ dán và vùng chừa trống; spec cũ chỉ có `logo_paste_at` và `logo_zone` vẫn chạy. MM đặt `top-left`, kết quả dán giống hệt bản trước.
- Bổ sung (chuẩn hoá thành phần): spec MM thêm `components` (nền, tiêu đề, dải phụ, ảnh trước/sau, icon lợi ích, logo, CTA), `layout_mode: free` và `layout_constraints`. Chỉ logo và khối CTA/vé cố định vị trí, model tự bố cục phần còn lại; §3D bước 2 bỏ yêu cầu bắt chước bố cục ảnh mẫu.
- Bổ sung (lô v4 Miu Miu, nền sáng): cổng kiểm `paste` thêm (a) dải sát trên khối CTA/vé (`margin` theo từng khối: cta 15, ticket 3), (b) ngưỡng riêng cho vùng logo `logo_zone_detail_max` 0.009, (c) `logo_zone` thu còn [0,0,380,152] cho khớp chiều cao logo thật, (d) quét cạnh logo chỉ ở x 8–120 và y 122–157 để không nhầm với đầu tiêu đề; thêm cờ `--heal` (làm mượt góc logo, ít dùng, có thể kéo màu tiêu đề vào góc nên mặc định tắt). Spec MM: nền SÁNG vì logo đậm màu, `background_variants` V1–V4 để xoay vòng.
- Bổ sung (rà soát lô 14 poster Miu Miu): `paste` thêm kiểm cạnh vùng logo (`zone_edge_max`), từ chối nền có ô phẳng viền cứng sau logo vốn làm cụt đầu tiêu đề; spec MM thêm `headline_top_min` 210 và ghi rõ không dùng font condensed dù ảnh mẫu dùng; §3D bước 2 và 4 yêu cầu chuyển sắc mượt, tiêu đề dưới 210px, soát logo cũ và ô icon trống.

## 1.4.9 — 2026-10-31
- §3D: thứ tự cố định trong một lượt (check → đọc mẫu → sinh nền → paste → giao). Cấm sinh ảnh trước khi in bảng check; trả về mỗi ảnh nền không được tính là giao, phải tới dòng `PASTE: OK`. Lý do: bài thử giày trên ChatGPT với 1.4.8 dừng ngay sau bước nền, không in bảng check, không dán. Manifest plugin 1.4.15. 6 file ảnh cũ trên bản live giữ nguyên. release_id: pluginrel_6ae556ff28a08191b3fdff69a0257672 (ChatGPT báo updated)

## 1.4.8 — 2026-10-31
- Route mới `restyle` (§3D): gen poster từ ảnh mẫu theo từng cửa hàng. Bước 0 bắt buộc kiểm đủ thông tin (logo, CTA, khối vé, font, màu, hotline/địa chỉ, toạ độ) bằng `scripts/restyle_poster.py check <MÃ>`; thiếu thì dừng, không bịa. Bước dán dùng `restyle_poster.py paste`, tự đọc lại file và so pixel với asset (khối 0, logo ≤4), từ chối nền có vật ở vùng logo.
- Thêm cửa hàng/thương hiệu MM (Miu Miu Premium Laundry): `assets/stores/MM/` gồm logo F58B9F, thanh CTA, khối vé, spec.json (màu #F34F7B, #F58B9F; Be Vietnam Pro Black cho tiêu đề; quy tắc không mặt người).
- SKILL.md thêm dòng 8a của §3C (màu logo #F58B9F). preflight chấp nhận route restyle. Manifest plugin 1.4.14. Giữ nguyên 6 file ảnh đang có trên bản live (logo-ao-may.png và 5 file DQH), không dùng delete_paths. release_id: pluginrel_6ae4d64b36388191a900a7826cc25e2f (ChatGPT báo updated; chưa đọc lại danh sách file)

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
