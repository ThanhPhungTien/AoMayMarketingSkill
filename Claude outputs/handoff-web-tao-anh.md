# Handoff — Hệ thống web tạo ảnh cửa hàng (đang bàn, chưa thiết kế)

Ngày: 2026-11-20. Trạng thái: **brainstorm, chưa chốt cách làm, chưa viết code.**
Hệ thống này **độc lập** với repo AoMayMarketingSkill; repo chỉ dùng để tham khảo cách đang làm ảnh.

## Người dùng muốn gì
- Một **website** để tạo ảnh cho các cửa hàng.
- Bước 1: chọn loại thiết kế:
  - **Redesign**: chọn một mẫu trong **link Google Drive** → làm lại theo mẫu đó. Chi tiết cách làm bàn sau.
  - **New design**: thiết kế mới. Chi tiết bàn sau.
- Làm xong → **lưu kết quả vào Google Drive**.

## Hiện trạng
- Ảnh đang tạo bằng **ChatGPT** (tài khoản dùng chung, khoảng **120.000đ/tháng**, không giới hạn số ảnh).
- Người dùng đang dùng **Claude Code điều khiển ChatGPT qua trình duyệt có sẵn của Claude** (browser pane).
- Repo AoMayMarketingSkill: AI chỉ vẽ **nền**, còn logo, CTA và chữ được **ghép bằng code** (`skills/ao-may-marketing/scripts/restyle_poster.py`). Mỗi cửa hàng có `spec.json`.

## Đã tìm hiểu
### Giá tạo ảnh qua API (ảnh 1K, tháng 10–11/2026, cần xem lại trang giá chính thức)
| Model | USD/ảnh |
|---|---|
| Seedream 5.0 Flash / Lite / Pro | 0,018 / 0,035 / 0,045 |
| Nano Banana 2.1 (Google) | 0,034 (1K) / 0,050 (2K) |
| GPT Image 2 (OpenAI) low / medium / high | 0,006 / 0,053 / 0,211 |
| Nano Banana Pro | 0,134 |
| FLUX.2 klein / pro | 0,014 / 0,03 |

- Với 120.000đ (khoảng 4,6 USD) thì tạo được khoảng 250 ảnh Seedream Flash, 135 ảnh Nano Banana 2.1, hoặc 85 ảnh GPT Image medium.
- API tính tiền theo từng ảnh, ChatGPT thì trả cố định hằng tháng. **Chưa biết số ảnh thực tế mỗi tháng**, nên chưa so được bên nào rẻ hơn.

### Cho website và ChatGPT làm việc với nhau
1. **Website gửi lệnh vào khung chat ChatGPT:** không có cách chính thức. Chỉ có thể cho máy tự điều khiển giao diện. Cách này trái điều khoản và dễ hỏng.
2. **ChatGPT gọi ra plugin riêng (MCP / Apps SDK):** làm được, nhưng cần bật developer mode. Với gói Plus/Pro các nguồn nói khác nhau, có thể chỉ đọc được. Việc chuyển ảnh ChatGPT vừa vẽ sang plugin (`openai/fileParams`) mới do cộng đồng tìm ra, chưa có tài liệu chính thức.
3. **Chỉ dùng ChatGPT kèm kết nối Google Drive:** đọc Drive được. Ghi Drive chủ yếu có ở gói Business/Enterprise.
- **Chưa biết** tài khoản dùng chung là gói gì, và người dùng có quyền bật developer mode không.

## Hướng đang nghiêng (CHƯA CHỐT)
Dùng **Claude Code làm cầu nối**, website không nói chuyện trực tiếp với ChatGPT:

```
Trang web (Artifact claude.ai có chỗ lưu dữ liệu: chọn loại, chọn mẫu) ──► hàng chờ yêu cầu
Claude Code đọc yêu cầu
  ├─ mở ChatGPT trong trình duyệt của Claude: đưa mẫu + prompt, tải ảnh về
  ├─ ghép logo/CTA bằng code nếu cần
  └─ lưu vào Drive (kết nối Google Drive sẵn có trong Claude Code) → ghi link kết quả lên trang web
```
- Ưu điểm: không cần máy chủ, không tốn tiền API, tận dụng gói ChatGPT đang trả.
- Giới hạn: máy phải bật và Claude Code phải đang chạy. Cách điều khiển giao diện ChatGPT sẽ hỏng khi ChatGPT đổi giao diện. Tự động hoá và dùng chung tài khoản đều trái điều khoản của OpenAI, có thể bị khoá.
- Phương án dự phòng: website chạy trên Google Apps Script (miễn phí, Drive có sẵn), tạo ảnh qua API rẻ (Seedream hoặc Nano Banana 2.1).

## Câu hỏi còn mở (hỏi theo thứ tự)
1. **Ai bấm yêu cầu trên web, và lúc đó người dùng có đang ngồi trước Claude Code không?** Nếu chỉ người dùng và đang ngồi máy thì làm ngay, gọn nhất. Nếu có người khác gửi lúc người dùng vắng mặt thì cần hàng chờ và Claude Code phải tự kiểm tra định kỳ.
2. ~~Vì sao muốn có web?~~ **Đã trả lời:** để tự động hoá, web dễ thao tác, giao việc (handoff) được. Còn cần làm rõ: tự động tới mức nào (bấm một lần là xong, hay có bước duyệt trước khi lưu Drive)?
3. Mỗi tháng tạo khoảng bao nhiêu ảnh, tính cả lần làm lại? Chi phí có bắt buộc phải dưới khoảng 120k/tháng không?
4. Tài khoản ChatGPT dùng chung là gói gì? Có bật được developer mode không?
5. Chi tiết quy trình redesign và new design (người dùng nói bàn sau).
6. Thư mục Drive chứa mẫu và thư mục lưu kết quả được tổ chức thế nào (theo cửa hàng? theo tháng?).

## Bước tiếp theo
Tiếp tục brainstorm từ câu hỏi 1 → bày các phương án → viết design doc → duyệt → lên plan.
Làm ở một thư mục hoặc repo **riêng**, không làm trong AoMayMarketingSkill.
