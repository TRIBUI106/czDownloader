# CZ Video Downloader - Hướng dẫn cài đặt chi tiết

## Bước 1: Cài đặt Python

### Windows:
1. Truy cập https://www.python.org/downloads/
2. Download bản Python mới nhất (3.11+ khuyên dùng)
3. Chạy file .exe và **QUAN TRỌNG**: Tick vào "Add Python to PATH"
4. Chọn "Install Now"
5. Khởi động lại Command Prompt/PowerShell

### Kiểm tra Python đã cài đặt:
```bash
python --version
# hoặc
py --version
```

## Bước 2: Cài đặt ứng dụng

### Cách 1: Tự động (khuyên dùng)
1. Double-click file `setup.bat` 
2. Chờ script tự động cài đặt dependencies

### Cách 2: Thủ công
```bash
# Mở Command Prompt/PowerShell trong thư mục project
cd "d:\Code\czDownloader"

# Cài đặt dependencies
pip install yt-dlp requests

# Hoặc cài từ file requirements
pip install -r requirements.txt
```

## Bước 3: Chạy ứng dụng

### Cách 1: Double-click
- Double-click file `run.bat`

### Cách 2: Command line
```bash
cd "d:\Code\czDownloader"
python main.py
```

## Troubleshooting phổ biến

### 1. "'python' is not recognized"
**Nguyên nhân**: Python chưa được thêm vào PATH
**Giải pháp**: 
- Cài đặt lại Python và tick "Add Python to PATH"
- Hoặc thử lệnh `py main.py` thay vì `python main.py`

### 2. "No module named 'yt_dlp'"
**Nguyên nhân**: Chưa cài đặt dependencies
**Giải pháp**:
```bash
pip install yt-dlp
```

### 3. "Permission denied"
**Nguyên nhân**: Thiếu quyền ghi file
**Giải pháp**:
- Chạy Command Prompt as Administrator
- Hoặc change download folder trong code

### 4. App không mở được
**Nguyên nhân**: Lỗi import hoặc missing dependencies
**Giải pháp**:
1. Mở Command Prompt
2. Chạy `python main.py` để xem lỗi cụ thể
3. Cài đặt missing packages

## Test URLs để thử nghiệm

### YouTube:
- https://www.youtube.com/watch?v=dQw4w9WgXcQ
- https://youtu.be/dQw4w9WgXcQ

### TikTok:
- https://www.tiktok.com/@username/video/1234567890

### Facebook:
- https://www.facebook.com/watch/?v=1234567890

### Instagram:
- https://www.instagram.com/p/ABC123def456/

## Các lệnh hữu ích

```bash
# Cập nhật yt-dlp (nên làm thường xuyên)
pip install yt-dlp --upgrade

# Kiểm tra version các packages
pip list

# Xem thông tin chi tiết về 1 package
pip show yt-dlp

# Gỡ cài đặt (nếu cần)
pip uninstall yt-dlp
```

## FAQ

**Q: App có virus không?**
A: Không, đây là mã nguồn mở hoàn toàn. Bạn có thể xem toàn bộ code trong file main.py

**Q: Có cần internet không?**
A: Có, cần internet để download video. Nhưng app chạy hoàn toàn local.

**Q: Download có bị giới hạn không?**
A: Không, nhưng tùy thuộc vào policy của từng platform và internet của bạn.

**Q: Có thể download playlist không?**
A: Hiện tại chỉ download 1 video/lần. Có thể paste nhiều URL và download lần lượt.

**Q: Video lưu ở đâu?**
A: Mặc định trong `C:\Users\[YourName]\Downloads\czDownloader\`