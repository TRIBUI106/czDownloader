# CZ Video Downloader

Ứng dụng download video từ YouTube, Facebook, TikTok, Instagram với giao diện đơn giản và chuyên nghiệp.

## Tính năng

- ✅ Download video từ YouTube, Facebook, TikTok, Instagram
- ✅ Chọn chất lượng video (best, 720p, 480p, 360p, worst)
- ✅ Progress bar hiển thị tiến trình download
- ✅ Tự động lưu vào thư mục `Downloads/czDownloader`
- ✅ Giao diện đẹp với tkinter
- ✅ Log chi tiết quá trình download
- ✅ Chạy local, không cần deploy

## Cài đặt

1. **Cài đặt Python** (nếu chưa có):
   - Download từ https://python.org (Python 3.7+)
   - Đảm bảo check "Add Python to PATH"

2. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy ứng dụng**:
   ```bash
   python main.py
   ```

## Hướng dẫn sử dụng

1. Mở ứng dụng bằng lệnh `python main.py`
2. Dán URL video vào ô "Video URL"
3. Chọn chất lượng video mong muốn
4. Nhấn nút "📥 Download"
5. Theo dõi tiến trình qua progress bar
6. Video sẽ được lưu vào `Downloads/czDownloader`

## Platform được hỗ trợ

- **YouTube**: youtube.com, youtu.be
- **Facebook**: facebook.com, fb.watch  
- **TikTok**: tiktok.com
- **Instagram**: instagram.com
- **Twitter/X**: twitter.com, x.com (bonus)

## Cấu trúc project

```
czDownloader/
├── main.py              # File chính của ứng dụng
├── requirements.txt     # Dependencies cần thiết
├── README.md           # Hướng dẫn này
├── setup.bat           # Script cài đặt tự động (Windows)
└── run.bat             # Script chạy nhanh (Windows)
```

## Yêu cầu hệ thống

- Windows 10/11 (hoặc macOS/Linux)
- Python 3.7 trở lên
- Internet connection
- Khoảng 100MB dung lượng ổ cứng

## Troubleshooting

### Lỗi "yt-dlp not found"
```bash
pip install yt-dlp --upgrade
```

### Lỗi "Permission denied" 
- Chạy command prompt với quyền Administrator
- Hoặc chọn thư mục khác để lưu video

### Video không download được
- Kiểm tra URL có chính xác không
- Một số video có thể bị hạn chế địa lý
- Thử với chất lượng thấp hơn

## Tác giả

[TRIBUI106](https://github.com/TRIBUI106)

## License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.