# Bài thử end-to-end trên ChatGPT

Chạy sau khi **1.4.3** đã phát hành và prompt "Kiểm tra sau phát hành" trong RELEASE_PROMPT.md cho kết quả OK.
Mỗi bài một **chat mới**. Kết quả dán lại theo bảng cuối file → sửa thành 1.4.4.

## Trước khi thử (trên máy)
```bash
python3 tools/preflight.py --strict
python3 tools/compose_preview.py DQH --headline "GIẶT HẤP" --subject <ảnh áo>
```
Mở `dist/preview_DQH_guides.png` và `_compare.png`: logo, tiêu đề, CTA nằm đúng ô so với `ref-approved.png`. Dùng cùng ảnh áo cho bài 1.

---

## 1. DQH — poster ghép (compose)
Đính kèm 1 ảnh áo, dán:
```text
Dương Quảng Hàm — theo mẫu DQH-01, giặt hấp, ảnh này.
```
Đạt khi:
- [ ] Trả đúng **1** ảnh PNG, tên theo mẫu `AO-MAY_DQH_<YYYYMMDD>_GIAT-HAP_DQH-01_V01.png`.
- [ ] Logo đúng vị trí và kích thước so với `ref-approved.png` (đặt cạnh `dist/preview_DQH.png` để so).
- [ ] Có dòng `Assets: preflight OK · logo SHA-256 khớp · pixel diff <số ≤ 2>`.
- [ ] Dấu tiêu đề rõ khi xem 100%: xét **nét đen**, từng dấu tách rời, không chạm chữ khác. Viền trắng dính nhau là đúng kiểu.
- [ ] CTA ở chân ảnh nguyên vẹn, không bị chủ thể hay thanh lợi ích đè; hotline 0942 146 606.
- [ ] Có một câu báo font tiêu đề chưa duyệt (vì `font_status: provisional`).
- [ ] Không có logo vẽ lại, chữ tiếng Việt do model ảnh sinh, nút hồng "LIÊN HỆ NGAY" hay bục đứng.

## 2. TH — poster sinh một lần (direct)
```text
Làm poster cho bài 06 Tân Hưng trong lịch đăng Áo Mây.
```
Đạt khi:
- [ ] Đúng bài 06 của **Tân Hưng** (không lẫn bài 06 của Chánh Hưng); nêu link trang Notion đã đọc.
- [ ] Chủ đề là bài giới thiệu cửa hàng tại khu vực, **không** phải bài giặt 24 giờ.
- [ ] Chữ "TÂN HƯNG" đặt riêng cạnh logo chuỗi, không nhập vào logo.
- [ ] Hotline 0908 982 393; không có ưu đãi 20% hay ưu đãi nào chưa xác nhận.
- [ ] Gọi tạo ảnh đúng 1 lần, ra 1 ảnh vuông; có kiểm tra chữ và dấu sau khi tạo.

## 3. CH — cửa hàng draft
```text
Làm poster giặt sấy cho Áo Mây Chánh Hưng.
```
Đạt khi:
- [ ] Từ chối làm poster vì `status: draft`.
- [ ] Nêu cụ thể còn thiếu gì (địa chỉ, hotline, fanpage… trong Notion 02).
- [ ] Không mượn thông tin hay ảnh của Tân Hưng.

## 4. Caption DQH có "miễn phí giao nhận"
```text
Viết caption Facebook cho Áo Mây Dương Quảng Hàm về giặt hấp, nhắc miễn phí giao nhận tận nơi.
```
Đạt khi:
- [ ] Nêu miễn phí giao nhận như thông tin đã xác nhận, **không** thêm điều kiện (bán kính, đơn tối thiểu).
- [ ] Hotline đúng định dạng 0942 146 606; hashtag lấy từ bộ đã lưu của DQH.
- [ ] Độ dài khoảng 120–170 từ trước phần liên hệ, 1 hook + 3 đoạn ngắn + 1 CTA.
- [ ] Không bịa giá, giờ mở cửa, giặt 24h.
- [ ] Nếu tool `check_marketing_copy` gắn cờ "miễn phí giao nhận": **ghi lại nguyên văn** cảnh báo (đây là lỗi của tool, không phải của caption).

## 5. Đọc quy tắc của `check_marketing_copy`
```text
Không sửa gì, không viết bài. In nguyên văn các quy tắc trong screenCopy của tool check_marketing_copy: danh sách từ hoặc cụm bị gắn cờ, mức cảnh báo và lý do. Nếu không đọc được mã nguồn tool, nói rõ là không đọc được, không đoán.
```
Đạt khi:
- [ ] Có danh sách nguyên văn, hoặc nói rõ không đọc được.
- [ ] Dán kết quả về repo để đối chiếu với SKILL.md (quy tắc nào chặn thông tin DQH đã xác nhận).

## 6. Tên cửa hàng mơ hồ
```text
Làm poster cho Áo Mây Hưng.
```
Đạt khi:
- [ ] Hỏi lại Tân Hưng hay Chánh Hưng, không tự chọn.

---

## Ghi kết quả
| Bài | Đạt / Không | Ghi chú (sai ở đâu, nguyên văn cảnh báo) | Ảnh / link chat |
|---|---|---|---|
| 1 DQH compose | | | |
| 2 TH direct | | | |
| 3 CH draft | | | |
| 4 Caption DQH | | | |
| 5 screenCopy | | | |
| 6 Tên mơ hồ | | | |
