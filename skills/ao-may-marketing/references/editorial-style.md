# Phong cách editorial chung (mọi cửa hàng)

Nguồn: prompt An Khánh của người dùng (2026-10-30), người dùng chốt dùng chung cho cả chuỗi (2026-11-01). Bản đầy đủ: `AK-editorial-poster-system.md`. Đây là phong cách (bố cục, chữ, đồ họa, ảnh), không phải bảng màu.

## Cách dùng
- Phong cách này áp cho mọi poster, mọi route. Màu sắc, font và logo vẫn lấy từ nhận diện từng cửa hàng (`spec.json`, mục B của phiếu): cửa hàng theo trụ sở dùng màu aomay.vn; MM và AK dùng màu riêng. Vàng bơ #F6D64A chỉ là màu của AK, không áp cho cửa hàng khác.
- Prompt gửi model ảnh vẫn NGẮN (xem SKILL §3D bước 2). Chỉ chép khối dưới đây, không dán bản đầy đủ.
- Kích thước, ngôn ngữ, vị trí logo và CTA theo `spec.json`, không theo prompt gốc (1920 px và "tiếng Anh" của bản gốc không áp dụng).

## Khối phong cách (đưa vào prompt)
Editorial magazine, cảm giác "một làn gió trong lành", ấm và sáng. Bố cục kiểu Swiss: nhiều khoảng trắng, bất đối xứng, chữ là nhân vật chính, ảnh hỗ trợ. Tiêu đề cực đậm, cỡ lớn, ít chữ phụ; không font trang trí, không 3D, không bóng đậm. Chỉ 2–5 yếu tố đồ họa có mục đích (mảng màu, thẻ kiểu hóa đơn, đường kẻ, tem tròn, băng dính, hạt giấy); tối đa một hình vẽ tay nét marker. Ảnh thật phù hợp chủ đề, ánh sáng tự nhiên. Chữ chiếm tối đa 30% khung. Tránh: quảng cáo giặt ủi kiểu cũ, tờ rơi công ty, clip art, nhiều icon, gradient nặng, hoạt hình, bố cục chật.

## Thành phần bắt buộc vẫn phải đủ
Phong cách editorial chỉ là cách trình bày, không được làm mất thành phần. Mỗi cửa hàng có danh sách `restyle.components` (MM: nền, tiêu đề 2 dòng, dải phụ, ảnh, mục lợi ích có icon thật, logo, CTA) và font tiêu đề theo spec; prompt phải nêu tên các thành phần đó. Thiếu mục lợi ích có icon hoặc sai font là lỗi (bài MM giặt chăn ga, 2026-11-01).

## Điểm cần kiểm khi duyệt
- Mỗi poster một bố cục khác nhau, nhưng logo và CTA đúng chỗ cố định.
- Hình phải giải thích được tiêu đề (giày sạch cho bài giày, khăn trắng cho bài khăn); không dùng hình máy giặt chung chung.
- Quy tắc cũ vẫn giữ: không người, không bịa thông tin cửa hàng, không vẽ lại logo.
