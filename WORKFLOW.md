# WORKFLOW.md — Làm poster hàng loạt cho cửa hàng

Tài liệu này ghi lại luồng làm việc đã chạy thật (An Khánh 30 ảnh, Chánh Hưng, Miu Miu) để khỏi hỏi lại. Nguồn sự thật vẫn là `SKILL.md` (cách làm), `stores/<MÃ>/spec.json` (thông số) và Notion (thông tin cửa hàng). File này chỉ là sổ tay vận hành cho Claude Code.

## 1. Phân vai
| Ai | Làm gì |
|---|---|
| ChatGPT (web) | Chỉ vẽ **ảnh nền** kèm chữ nội dung. Bố cục là việc của nó. |
| Claude Code | Điều khiển ChatGPT qua trình duyệt trong app, tải ảnh, chạy `restyle_poster.py paste`, soi lỗi, lưu file, gửi bạn xem. |
| Người dùng | Cung cấp mẫu, logo, thông tin cửa hàng; duyệt cuối. |
| Code | Dán logo và CTA thật (không bao giờ để ChatGPT vẽ logo, hotline, địa chỉ). |

## 2. Trạng thái các cửa hàng (cập nhật 2026-11-06)
| Mã | Route | Logo | CTA | Ghi chú |
|---|---|---|---|---|
| CH Chánh Hưng | restyle | `stores/CH/logo.png` | `stores/CH/cta-bar.png` | Đã có trên plugin ChatGPT (skill 1.4.15) |
| AK An Khánh | restyle | `stores/AK/logo.png` | `stores/AK/cta-bar.png` (kem-vàng, HTML ở `tools/cta-bar-AK.html`) | 30 poster đã duyệt. Chưa commit, chưa phát hành |
| TH Tân Hưng | restyle | `stores/TH/logo.png` | `stores/TH/cta-bar.png` | Mới thêm 2026-11-06, chưa phát hành |
| DQH Dương Quảng Hàm | restyle (trước là compose) | `stores/DQH/logo.png` | `stores/DQH/cta-bar.png` | Đổi route 2026-11-06 để làm mẫu Latusa; khoá compose DQH-01 giữ nguyên |
| MM Miu Miu | restyle | `stores/MM/logo.png`, `logo-white.png` | `cta-bar.png`, `ticket-block.png` | Thương hiệu riêng |

Kiểm điều kiện trước khi làm: `python3 skills/ao-may-marketing/scripts/restyle_poster.py check <MÃ>` phải in `CHECK: OK`, và `python3 tools/preflight.py` không có FAIL.

## 3. Hai cách làm với ChatGPT
### A. Chat có plugin Áo Mây (cửa hàng đã có trên bản live)
- Dùng chat đã gắn plugin, ví dụ chat Chánh Hưng "Báo cáo sẵn sàng poster": `https://chatgpt.com/g/g-p-6ad743463cdc8191abaa9b47dbd50b6e-a-chuyen/c/6ae6babd-f8a8-83ec-be4c-cecfbec4b92f`.
- Gửi **prompt chữ**, không cần đính kèm ảnh, mô tả mẫu bằng lời. Mẫu prompt đã chạy được:
  > Dùng skill ao-may-marketing làm 1 poster Áo Mây <cửa hàng> (<MÃ>), dạng <không so sánh | so sánh TRƯỚC/SAU>. Mẫu tham khảo (mô tả, không có ảnh): <tiêu đề, dải phụ, ảnh chính, mục lợi ích>. Khi làm lại: đổi sang nhận diện cửa hàng theo spec; bỏ logo, tên, hotline, địa chỉ của cửa hàng cũ; bỏ các cam kết chưa xác nhận; không người. Làm đúng quy trình trong SKILL.md.
- ChatGPT thường dừng sau khi vẽ ảnh. Claude tải ảnh nền về và chạy lệnh dán ở máy (mục 4).
- Cửa hàng mới (TH, DQH, AK) chỉ có trên plugin sau khi **phát hành** bản mới (`python3 tools/build_release.py`, làm theo `RELEASE_PROMPT.md`). Bước đưa file zip vào chat là việc của người dùng.

### B. Chat thường (chưa phát hành) — tự gửi toàn bộ chỉ dẫn bằng chữ
- Mở chat mới `https://chatgpt.com/`, gửi prompt đủ ý: phong cách cửa hàng (màu, font, bố cục), chữ nội dung nguyên văn, vùng chừa trống, điều cấm.
- Có thể đính kèm 1–2 poster đã duyệt làm mẫu phong cách, nhưng việc đính kèm đi qua hộp thoại Windows và hay lỗi (mục 6). Nếu không đính kèm được thì mô tả phong cách bằng chữ, kết quả vẫn dùng được.

## 4. Quy trình một poster
1. **Chốt nội dung** từng poster: tiêu đề hai dòng, dòng phụ, 2–4 ý phụ, hình minh hoạ. Chỉ dùng thông tin đã xác nhận.
2. **Gửi prompt cho ChatGPT**, chờ ảnh (khoảng 2–3 phút), tải về.
3. **Tải ảnh** bằng JS canvas → file `*.tmp` trong `Downloads`, đổi cỡ 1080x1080 (LANCZOS).
4. **Dán logo + CTA bằng code:**
   `python3 skills/ao-may-marketing/scripts/restyle_poster.py paste <MÃ> nen.png ra.png --block cta`
   Phải in `PASTE: OK` (khối CTA lệch 0, logo ≤ 4). FAIL thì vẽ lại nền theo lý do nó báo, tối đa 2–3 lần.
5. **Soi bằng mắt** từng chữ và dấu tiếng Việt, đúng nguyên văn, không chữ thừa, không người, không logo/tên cửa hàng khác, không chấm lạ gần chữ (phóng to kiểm).
6. **Lưu** vào thư mục kết quả của cửa hàng và gửi người dùng xem **một lượt cho cả bộ**.

Nếu đáy ảnh còn chi tiết sát CTA: làm mờ dần về màu nền (script tạm `finish_ak.py --fade`), chỉ sửa ảnh nền do ChatGPT vẽ, không động vào logo hay CTA.

## 5. Quy tắc nội dung (không tự đổi)
- Mẫu Latusa: giữ ý, bỏ logo, tên, hotline, địa chỉ Latusa và mọi tên cửa hàng khác (`restyle.forbid_text`).
- Dịch vụ chưa xác nhận cho cửa hàng (topper, gấu bông, rèm, dán keo đế giày, phục hồi màu, tẩy lem) → đổi thành "giặt hấp / giặt sấy / vệ sinh" tương ứng. Không bịa dịch vụ.
- Bỏ cam kết thời gian ("24H", "4–5H", "lấy liền", "cấp tốc"), "2–4 tuần/lần", "since 2017", "tiêu chuẩn châu Âu", giá, ưu đãi, giao nhận chưa xác nhận.
- Không người (mặt, toàn thân); tay được. Không hình người trong ảnh nền.
- File ảnh (logo, CTA, ảnh mẫu) do người dùng làm hoặc duyệt. Không tự vẽ lại hay sửa file trong `assets/`. CTA mới dựng bằng HTML (`tools/make_cta_bar.py` hoặc `tools/cta-bar-AK.html`) và phải được duyệt trước khi vào repo.
- Không commit, push, phát hành khi chưa được đồng ý.

## 6. Bẫy đã gặp
- **Kiểm cửa sổ foreground trước khi bấm hay gõ bằng PowerShell.** Người dùng hay mở game (Garena Delta Force). Cửa sổ trên cùng không phải `Open` hoặc `Claude` thì dừng, không bấm.
- Đính kèm file vào ChatGPT: bấm `+` → "Add photos & files" → hộp thoại `Open`. Copy nguồn sang đường dẫn ASCII (`C:\Temp\...`), dán đường dẫn bằng clipboard, không gõ. Sau khi Open phải **thấy hình thu nhỏ trong ô soạn** mới tin là đã đính kèm.
- ChatGPT bỏ qua giới hạn px: nói theo **% chiều cao** (góc logo 30%x21% trống, nội dung dừng ở 80%, đáy từ 85% là nền trơn).
- Nút gửi hay không có trong DOM: gõ prompt bằng `execCommand('insertText')` trên `.ProseMirror` rồi bấm phím Return.
- Đường dẫn tiếng Việt đôi khi lỗi `OSError: Invalid argument` khi ghi: ghi ra thư mục tạm rồi `copy`, có thử lại.
- Cổng kiểm báo vùng logo không trống vì thanh giá treo, cành lá, vòng phóng to chạm góc: nhờ ChatGPT dời xuống dưới 27% chiều cao.
- ChatGPT từng vẽ một chấm lạ cạnh chữ (AK-05) và một ký tự Thái trong prompt do gõ nhầm: soi kỹ, vá bằng màu nền ở ảnh nền trước khi dán.
- Hạn mức ảnh gói Plus hết sau khoảng 20–25 ảnh/ngày.

## 5b. Thư mục
- Mẫu Latusa: `D:\Quyên\A Chuyên\Áo Mây\An Khánh\Mẫu Latusa` và `...\mẫu latusa 4 thang 11` (15 + 15 mẫu); cũng có `Chánh Hưng\Mẫu Latusa`.
- Kết quả: `D:\Quyên\A Chuyên\Áo Mây\<Cửa hàng>\Kết quả ...` (AK: `Kết quả An Khánh`, `Kết quả An Khánh 4-11`; CH: `Kết quả Chánh Hưng v2`).
- Checklist theo ảnh: `checklists/<MÃ>/` (`content.json` + `<MÃ>-NN.md`).
- Script tạm của phiên (tải ảnh, dán, làm mờ đáy) nằm trong scratchpad của Claude; chưa vào repo. Có thể đưa thành lệnh của skill nếu cần.

## 7. Việc đang chờ
- Làm mẫu 1 poster cho mỗi cửa hàng (CH, DQH, TH) rồi người dùng duyệt, sau đó mới làm hàng loạt: CH 15 ảnh (mẫu Latusa 4/11), DQH 30 ảnh, TH 30 ảnh.
- Commit phần AK, TH, DQH và `WORKFLOW.md` (tách riêng `stores/MM/spec.json`), phát hành 1.4.17 nếu muốn dùng plugin cho AK/TH/DQH.
- DQH: `bg-default.png` và `ref-approved.png` còn lệch SHA-256, chờ người dùng xác nhận.
- TH: dịch vụ thực sự có chưa xác nhận trên Notion.

## 8. Kinh nghiệm làm hàng loạt (rút ra 2026-11-07, đợt CH/DQH/TH 75 ảnh)
- **Nội dung chép nguyên văn từ mẫu Latusa**, không tự nghĩ. Chỉ bỏ nhận diện Latusa (logo, tên, hotline, địa chỉ, SINCE 2017, LIÊN HỆ NGAY). Chữ tiếng Anh trong mẫu đổi sang tiếng Việt.
- **Prompt:** có sẵn danh sách từ hay sai dấu (CHÂU ÂU, VỆ SINH, GIỮ, HỎNG, HỒI, ĐÚNG, BỊ, MƯA). Bố cục theo % chiều cao, ghi ngay từ lần gen đầu (cập nhật 2026-11-15, sau đợt Đà Nẵng): 23% trên cùng là nền trơn đồng màu (không cây, cửa sổ, mảng tối); tiêu đề bắt đầu khoảng 25%; nội dung kết thúc ≤70%; từ 72% xuống đáy là nền trơn (không ảnh nhỏ, mặt bàn, bóng). Bản cũ (tiêu đề 21-22%, nội dung đến 74-76%) làm nhiều ảnh trượt cổng "cạnh vùng logo" và "dải trên CTA", mỗi ảnh phải gen lại 2-4 lần.
- **Soi nhầm tên ảnh:** sau mỗi đợt chạy `python3 tools/batch/check_names.py <thư mục kết quả> --checklist <file tiêu đề của đợt>`. Nó báo cặp ảnh gần như trùng nhau và ghép bảng đối chiếu có ghi tiêu đề kỳ vọng cạnh từng ảnh. Giới hạn: chỉ bắt được ảnh trùng gần như y hệt; hai lần gen khác nhau của cùng một chủ đề vẫn lọt, nên vẫn phải nhìn bảng đối chiếu đối với tiêu đề.
- **Nội dung đọc từ chính ảnh mẫu của từng đợt:** không dùng lại danh sách của đợt trước và không giả định hai thư mục mẫu giống nhau, dù nhìn thumbnail thấy giống. Chép chữ từng ảnh mẫu thành checklist riêng của đợt rồi mới dựng prompt; sau khi gen đối chiếu tiêu đề từng poster với checklist (3/30 ảnh Đà Nẵng từng bị gắn nhầm tên dù tải cách nhau vài giây).
- **Tải ảnh:** ChatGPT tải về dạng `<guid>.tmp`, tên bị bỏ. Mỗi tab tải một ảnh, chờ khoảng 9 giây, rồi gán tên theo chỉ số của đúng tab đó. Không gán theo thứ tự giữa nhiều tab; kiểm số file mới đúng bằng số cần gán rồi mới đặt tên.
- **Cổng kiểm báo FAIL:** vẽ lại kèm một dòng "LẦN SỬA" riêng cho ảnh đó, không dùng `--heal` khi vật thể sát góc logo (để lại mảng tối).
- **Song song:** 5 tab ChatGPT chạy được, mỗi ảnh khoảng 3 phút. Hạn mức ảnh trong ngày hết sau khoảng 100 ảnh.
- **Soi chữ:** người dùng soi từng dấu bằng mắt; soi lại phóng to trước khi gửi, không chỉ nhìn bản thu nhỏ.

## 9. Chuẩn logo (2026-11-15)
- **Cỡ dán theo khung, không theo chiều rộng:** spec khai `restyle.logo_box: [200, 135]` (rộng tối đa × cao tối đa, px trên canvas 1080). Script giữ tỉ lệ logo, logo cao bị giới hạn bởi chiều cao, logo ngang bị giới hạn bởi chiều rộng, nên mọi cửa hàng có diện tích hiển thị gần nhau. Cách tính: 135 lấy theo logo Chánh Hưng đã duyệt (160×135); logo cách mép trên `logo_margin` 30. Kết quả: CH 160×135, DN 154×135, TH 177×135, DQH 200×102.
- **File logo phải đạt** (`restyle_poster.py check <MÃ>` báo FAIL kèm lý do nếu không): PNG RGBA nền trong suốt; vùng nội dung sau khi cắt viền trong suốt ≥ 400×270 px (để thu về khung 200×135 vẫn nét khoảng 2 lần); tỉ lệ rộng/cao từ 1,0 đến 2,2. Viền trong suốt thừa không sao, script cắt lúc dán, không sửa file của người dùng.
- **Ngoại lệ:** spec chưa có `logo_box` vẫn dùng `logo_width` cũ (AK rộng 250 vì vùng trống 225; MM ở góc trái, tỉ lệ 3,3). Đổi sang `logo_box` khi cần đồng bộ.
- Đổi `logo_box` hay thêm cửa hàng mới: chạy `check`, rồi dán thử một nền (`paste`) để chắc vùng logo và cổng kiểm vẫn đạt.

## 10. Vị trí logo và cách thể hiện layout (2026-11-15)
**Luật chung (2026-11-15): mọi cửa hàng đặt logo ở góc trên trái.** Vị trí khác chỉ khi người dùng bảo cho một poster lẻ. Bảng theo cửa hàng (`restyle.logo_position` trong spec):
| Mã | Vị trí | Cỡ | Ghi chú |
|---|---|---|---|
| DN Đà Nẵng | top-left | khung 200×135, lề 30 | Quyết định 2026-11-15: logo luôn ở góc trái |
| MM Miu Miu | top-left | rộng 302, lề 54 | Thương hiệu riêng |
| AK An Khánh | top-left | rộng 250, lề 48 | Vùng chừa 225 |
| CH | top-left | khung 200×135, lề 30 | Đổi 2026-11-15 theo yêu cầu |
| TH, DQH | top-left | khung 200×135, lề 30 | Đổi 2026-11-15 theo luật chung |
Một poster lẻ cần vị trí khác: đổi tạm `logo_position` rồi `paste`, sau đó trả lại spec.

**Layout khi logo ở góc trái trên** (đã chạy được ở DN và DQH_10, tránh dải trống lớn phía trên):
- Nói theo % khung vuông trong prompt: hình chữ nhật 0-21% rộng × 0-19% cao (DQH: 0-24%) là nền mờ đồng màu, không chữ, vật thể, cây, cửa sổ hay mảng tối. Không được chừa cả dải ngang phía trên.
- Tiêu đề bắt đầu từ khoảng 4-5% chiều cao, nằm bên phải góc logo (từ 24-26% chiều rộng sang phải). Phần còn lại dùng hết khung.
- Nội dung phủ từ ~5% đến ~84% chiều cao, phải LỚN. Dặn thêm "lần sửa" nội dung kết thúc ≤78% khi cổng "dải trên CTA" báo trượt (ChatGPT thường vượt thêm ~5%). Từ ~86% xuống đáy là nền trơn cho thanh CTA.
- Poster có hàng thẻ dưới: thẻ cao 56-84%, chữ và icon to; tiêu đề cùng ảnh minh hoạ chiếm khoảng 4-52%.
- Nếu một poster lẻ để logo top-center thì tiêu đề phải bắt đầu ≥ ~25% (nếu không trượt cổng "cạnh vùng logo"), nên phía trên trống nhiều. Đây là lý do chuyển sang góc trái.

**Poster khai trương có ảnh thật** (DN, đã duyệt): khung ảnh dọc 5,5-49% rộng × 21-75,5% cao để trống hoàn toàn (`tools/batch/paste_photo.py` dán, rect mặc định 60,225,470,590); cột chữ bên phải 53-96%; trang trí dàn đều khắp ảnh nhưng dừng ở ~84% chiều cao.
