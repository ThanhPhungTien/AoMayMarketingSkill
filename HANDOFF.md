# Handoff — 27/10/2026

Trạng thái: skill **1.4.2** đang chạy trên ChatGPT (plugin chứa 8 skill, gồm cả miu-miu-marketing). Repo này là bản gốc. Preflight local: 0 FAIL, 10 WARN (chỉ thiếu ảnh).

## Rủi ro chưa kiểm chứng (chưa chạy thật lần nào)
1. Chưa có poster thật nào làm bằng 1.4.x: route `compose` (DQH) và route `direct` với `logo.mode = chain+label` (TH) mới chỉ có trên giấy.
2. `stores/DQH/spec.json` → `logo.paste_at [287,-133]`, `scale 0.467` được tính từ bản logo đã bị chat nén (RGB, nền trắng; vùng nét logo trong file 1080×1080 là x 173–908, y 341–670). Nếu file logo gốc RGBA có lề khác thì logo đặt lệch. Bước kiểm tra pixel trong SKILL.md chỉ xác nhận logo đúng file gốc, KHÔNG kiểm tra vị trí.
3. Toạ độ các box trong spec DQH đo từ ảnh mẫu đã nén, sai số ±3 px.
4. Tool `check_marketing_copy` nằm trong App (Sites, `lib/marketing-mcp.ts`), không nằm trong repo này và chưa được cập nhật theo 1.4.x. Có thể gắn cờ sai "miễn phí giao nhận" dù DQH đã xác nhận.

## Việc tiếp theo (theo thứ tự)
A. **Tool xem trước local**: viết `tools/compose_preview.py <MÃ> [--headline "GIẶT SẤY"] [--subject ảnh.jpg]` dựng poster route compose đúng theo spec.json (logo, tiêu đề với embolden/tracking/stroke/shadow/shear, dòng phụ, thanh lợi ích, CTA, nền) ra `dist/preview_<MÃ>.png`, và nếu có `ref_approved` thì xuất thêm ảnh chồng/cạnh nhau để so vị trí. Mục đích: phát hiện rủi ro 2–3 trên máy trước khi phát hành. Không sửa file ảnh trong assets.
B. **Khi tôi bỏ ảnh vào assets**: chạy `preflight.py --strict`; chạy `compose_preview.py DQH`, đối chiếu với `ref-approved.png`; nếu logo lệch thì tính lại `logo.scale`/`paste_at` từ vùng nét thật của file RGBA và đề xuất (chờ tôi duyệt) trước khi sửa spec. Điền `sha256` cho file mới. Sau đó tăng 1.4.3, CHANGELOG, `build_release.py`, đưa tôi zip + prompt từ RELEASE_PROMPT.md.
C. **Bài thử end-to-end trên ChatGPT sau 1.4.3** — viết sẵn vào `TEST_PLAN.md` (prompt để tôi copy + tiêu chí đạt):
   - DQH compose: "Dương Quảng Hàm — theo mẫu DQH-01, giặt hấp, ảnh này" + 1 ảnh áo. Đạt: logo đúng vị trí so với ref, có dòng `Assets: preflight OK…`, dấu tiêu đề rõ (xét nét đen), CTA không bị đè, đúng 1 ảnh.
   - TH direct: gọi 1 bài số trong Content Calendar. Đạt: đúng bài Tân Hưng (không lẫn bài cùng số của Chánh Hưng), tên "TÂN HƯNG" đặt riêng cạnh logo chuỗi, hotline 0908 982 393.
   - CH: yêu cầu poster. Đạt: từ chối vì status draft, nêu thiếu gì.
   - Caption DQH có "miễn phí giao nhận". Đạt: không bị coi là cam kết chưa xác nhận; nếu tool gắn cờ thì ghi lại.
   - Prompt nhờ ChatGPT in nguyên văn các quy tắc trong `screenCopy` của check_marketing_copy để đối chiếu với SKILL.md (chỉ đọc, không sửa).
D. Kết quả từng bài thử tôi sẽ dán lại → sửa thành 1.4.4.

## Việc đang chờ tôi
- Ảnh: `assets/chain/logo-ao-may.png` (logo chuỗi gốc, ChatGPT từng thấy bản 900×900 màu teal trong bộ Poster Generator cũ) và 5 file trong `assets/stores/DQH/`.
- Duyệt font tiêu đề DQH (Paytone One, `font_status: provisional`).
- Thông tin CH, TP, NX, AK để bật `active`.
- release_id của 1.4.0–1.4.2 cho CHANGELOG.
- Notion: chạy các đợt prompt 1–4 trong tài liệu hướng dẫn (database Cửa hàng, relation, Asset Library, Mẫu thiết kế, Lưu trữ).
