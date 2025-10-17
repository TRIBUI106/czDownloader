# 🎬 CZ Video Downloader v2.0

**Modern video downloader với giao diện đẹp, hỗ trợ nhiều nền tảng**

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Tính năng nổi bật

- 🌐 **Hỗ trợ đa nền tảng**: YouTube, Facebook, TikTok, Instagram, Twitter/X
- 🎨 **Giao diện hiện đại**: UI đẹp mắt với theme sáng/tối, mượt mà
- 📋 **Quản lý hàng đợi**: Thêm nhiều URL, theo dõi tiến độ từng video
- ⚡ **Download đồng thời**: Tải nhiều video cùng lúc
- 📊 **Theo dõi chi tiết**: Progress bar thời gian thực, tốc độ download
- 🛠️ **Xử lý lỗi thông minh**: Log chi tiết, hướng dẫn khắc phục tự động
- ⚙️ **Tùy chỉnh chất lượng**: Từ best đến worst
- 🔄 **Auto-retry**: Tự động thử lại khi lỗi
- 🆕 **Auto-update system**: Tự động kiểm tra và cập nhật phiên bản mới
- 🎯 **One-click setup**: Chỉ cần chạy run.bat, mọi thứ tự động!

## 🚀 Cách sử dụng (Cực kỳ đơn giản!)

### Bước 1: Tải về
```bash
git clone https://github.com/TRIBUI106/czDownloader.git
cd czDownloader
```

### Bước 2: Chạy ngay lập tức
```bash
# Chỉ cần double-click hoặc:
.\run.bat
```

**Thế thôi!** 🎉 File `run.bat` sẽ tự động:
- ✅ Kiểm tra Python 
- ✅ Kiểm tra updates từ GitHub
- ✅ Cài đặt tất cả dependencies cần thiết
- ✅ Setup FFmpeg
- ✅ Test giao diện 
- ✅ Khởi chạy ứng dụng

**Không cần cài đặt thủ công gì cả!**

## 📱 Hướng dẫn sử dụng

### Thêm video để tải
1. **URL đơn**: Dán link vào ô input → Click "Add to Queue"
2. **Nhiều URL**: Dán vào text area (mỗi URL một dòng) → "Add All URLs"
3. **Hỗ trợ**: YouTube, Facebook, TikTok, Instagram, Twitter/X

### Tùy chọn download
- **Chất lượng**: best, 1080p, 720p, 480p, 360p, worst
- **Đồng thời**: 1-5 video cùng lúc
- **Thư mục**: Mặc định `~/Downloads/czDownloader/`

### Quản lý hàng đợi
- **Điều khiển cá nhân**: Tạm dừng, hủy, thử lại từng video
- **Thao tác hàng loạt**: Download tất cả, xóa hết, retry failed
- **Theo dõi**: Progress bar thời gian thực + tốc độ
- **Hỗ trợ lỗi**: Hệ thống troubleshooting tích hợp

## 🎨 Giao diện

### Các tab chính
- **📥 Download**: Thêm URL và cấu hình
- **📋 Queue**: Theo dõi và quản lý downloads  
- **⚙️ Settings**: Tùy chỉnh thư mục và themes

### Header buttons
- **🌙/☀️**: Chuyển đổi theme Dark/Light
- **🔄**: Kiểm tra update từ GitHub
- **ℹ️**: Thông tin về ứng dụng

### Themes
- **☀️ Light Mode**: Giao diện sáng, sạch sẽ
- **🌙 Dark Mode**: Dễ nhìn trong môi trường tối
- Chuyển đổi bất cứ lúc nào với nút theme ở header

## 🔧 Khắc phục sự cố

### Các lỗi thường gặp

**"Python not found"**
- Cài Python từ [python.org](https://python.org)
- Nhớ tick "Add Python to PATH"

**"Dependencies missing"**  
- Chạy `run.bat` - tự động cài đặt
- Hoặc thủ công: `pip install yt-dlp requests pillow`

**"FFmpeg not found"**
- App tự cài `ffmpeg-python`
- FFmpeg đầy đủ: [ffmpeg.org](https://ffmpeg.org)

**Download thất bại**
- Dùng hệ thống help tích hợp (nút ❓)
- Thử chất lượng khác
- Video có thể private/bị khóa vùng

## 📋 Cấu trúc project

```
czDownloader/
├── run.bat                 # 🎯 File duy nhất cần chạy!
├── main.py                # Ứng dụng chính với UI
├── version.py             # Quản lý version và thông tin app
├── quick_update_check.py  # Script kiểm tra update nhanh
├── README.md             # Hướng dẫn này
├── requirements.txt      # Dependencies (auto-install)
└── config.py            # Cấu hình (tùy chọn)
```

## ⚡ Tại sao chọn run.bat?

**Trước đây** (phức tạp): 
- setup.bat → demo.bat → setup_check.py → launcher.py → main.py
- Nhiều file, dễ nhầm lẫn

**Bây giờ** (đơn giản):
- `run.bat` làm tất cả!
- 1 file, 1 cú double-click → Xong!

## 🛠️ Chi tiết kỹ thuật

### Dependencies tự động
- **yt-dlp**: Engine download chính
- **requests**: HTTP requests  
- **Pillow**: Xử lý ảnh
- **tkinter**: GUI (có sẵn trong Python)
- **ffmpeg-python**: Hỗ trợ video processing

### Platform support
| Platform | URL Format | Status |
|----------|------------|--------|
| **YouTube** | `youtube.com`, `youtu.be` | ✅ Full Support |
| **Facebook** | `facebook.com`, `fb.watch` | ✅ Full Support |
| **TikTok** | `tiktok.com` | ✅ Full Support |
| **Instagram** | `instagram.com` | ✅ Full Support |
| **Twitter/X** | `twitter.com`, `x.com` | ✅ Full Support |

### Hiệu suất
- **Concurrent**: 1-5 downloads đồng thời
- **Memory**: Tối ưu cho batch lớn
- **Network**: Auto-retry, timeout handling
- **Storage**: Tên file thông minh, tổ chức tốt

## 🎯 Demo nhanh

```bash
# Clone project
git clone https://github.com/TRIBUI106/czDownloader.git
cd czDownloader

# Chạy ngay (tất cả đều tự động!)
.\run.bat
```

**Video demo**: Từ 0 đến chạy app chỉ trong 30 giây! 

## 🤝 Đóng góp

1. Fork repo này
2. Tạo branch: `git checkout -b feature-moi`
3. Commit: `git commit -am 'Thêm tính năng mới'`
4. Push: `git push origin feature-moi`  
5. Tạo Pull Request

## 📞 Hỗ trợ

- **Báo lỗi**: Tạo Issue trên GitHub
- **Góp ý**: Request features qua Issues
- **Help**: Dùng hệ thống troubleshooting tích hợp

## 🌟 Tính năng độc quyền

- ✅ **All-in-one**: 1 file run.bat làm tất cả
- ✅ **Zero-config**: Không cần setup thủ công  
- ✅ **Auto-install**: Dependencies tự cài
- ✅ **Auto-update**: Tự động kiểm tra và cập nhật từ GitHub
- ✅ **Smart-retry**: Thông minh xử lý lỗi
- ✅ **Beautiful UI**: Giao diện hiện đại mượt mà với nút update
- ✅ **Version management**: Hệ thống quản lý version chuyên nghiệp
- ✅ **Vietnamese-friendly**: Tài liệu và UI tiếng Việt

### 🆕 Hệ thống Auto-Update

**Tự động kiểm tra:**
- Mỗi lần khởi động qua `run.bat`
- Khi click nút 🔄 trong app
- Sau 3 giây khi mở app

**Tự động cập nhật:**
- Download từ GitHub Releases
- Backup phiên bản cũ
- Cài đặt phiên bản mới
- Khởi động lại app tự động

**An toàn:**
- Backup trước khi update
- Rollback nếu có lỗi
- Không làm mất dữ liệu

## 📄 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

---

**Made with ❤️ by CZ Team**

*Happy downloading! 🎬✨*