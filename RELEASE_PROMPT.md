# Prompt phát hành lên ChatGPT

1. `python3 tools/build_release.py` → lấy file `dist/ao-may-marketing_v<X.Y.Z>.zip`.
2. Mở **chat mới** trên ChatGPT, đính kèm file zip, dán prompt dưới (thay `<X.Y.Z>` và `<bản đang chạy>`).
3. Ghi `release_id` mới vào CHANGELOG.md, commit, tag `v<X.Y.Z>`.
4. Mở **chat mới** khác, dán prompt kiểm tra ở cuối file.

```text
Phát hành bản <X.Y.Z> của plugin chứa skill ao-may-marketing bằng file zip đính kèm. Làm theo quy trình update_plugin, không sửa thư mục cache.
1. Đọc bản hiện tại bằng get_plugin_files, ghi current_release_id. Xác nhận bản đang chạy là <bản đang chạy>; nếu khác thì dừng và báo tôi.
2. Zip là bản ĐẦY ĐỦ của skill. Thay toàn bộ nội dung skills/ao-may-marketing/ bằng thư mục ao-may-marketing/ trong zip. Không đụng các skill khác, không đụng App binding, không đụng file ở gốc plugin ngoài 2 manifest.
3. Đặt version <X.Y.Z> trong plugin.json và .codex-plugin/plugin.json. SKILL.md trong zip đã ghi <X.Y.Z>.
4. Nếu trong skills/ao-may-marketing/ hiện có file không còn trong zip, liệt kê cho tôi và chờ xác nhận trước khi dùng delete_paths.
5. Gọi update_plugin với archive và expected_release_id. Sau đó đọc lại và in: danh sách file trong skills/ao-may-marketing/ kèm kích thước và SHA-256 của file ảnh, version ở cả 3 chỗ, release_id mới.
```

## Kiểm tra sau phát hành

```text
Chạy preflight của skill ao-may-marketing cho từng mã cửa hàng trong assets/stores/. Không làm poster.
In: phiên bản skill, đường dẫn thư mục skill, và với mỗi cửa hàng một bảng (file · OK/FAIL · lý do) kèm status và route đọc từ spec.json.
Với cửa hàng route compose, dựng thử dòng tiêu đề mẫu ở cỡ thật bằng font tiêu đề trong spec.json và tự kiểm tra dấu theo SKILL.md.
```
