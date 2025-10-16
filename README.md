# 🎬 CZ Video Downloader v2.0

**Modern video downloader with beautiful interface and advanced features**

Ứng dụng download video hiện đại từ YouTube, Facebook, TikTok, Instagram với giao diện đẹp mắt và nhiều tính năng nâng cao.

## ✨ Tính năng mới v2.0

### 🎨 **Giao diện hiện đại**
- ✅ Material Design inspired UI
- ✅ Dark/Light theme toggle  
- ✅ Gradient colors và rounded corners
- ✅ Professional progress indicators
- ✅ Tabbed interface với settings panel

### 🔥 **Multi-URL Queue System**
- ✅ Add nhiều URL cùng một lúc
- ✅ Bulk input từ text area
- ✅ Individual progress bar cho từng video
- ✅ Queue management với pause/resume/cancel
- ✅ Batch download capabilities

### 📊 **Advanced Download Management**
- ✅ Real-time progress tracking per video
- ✅ Download speed và ETA display
- ✅ File size information
- ✅ Concurrent download settings
- ✅ Retry failed downloads

### 🛠️ **Smart Features**
- ✅ Auto dependency installer
- ✅ URL validation với real-time feedback
- ✅ Download folder customization
- ✅ Settings persistence
- ✅ Error handling với user-friendly messages

## 🚀 Quick Start

### Option 1: One-Click Launch (Recommended)
```bash
# Just double-click this file:
demo.bat         # Launch v2.0 with demo
run.bat          # Launch production version
```

### Option 2: Manual Launch
```bash
python launcher_v2.py    # Smart launcher với auto-install
python main_v2.py        # Direct launch (cần dependencies)
```

## 📸 Giao diện mới

### 🎯 **Download Tab**
- Modern URL input với validation
- Bulk URL text area  
- Advanced settings (quality, concurrent downloads)
- Smart dependency detection

### 📋 **Queue Tab**  
- Beautiful video cards với metadata
- Individual progress bars
- Download controls (pause/resume/cancel/retry)
- Real-time status updates

### ⚙️ **Settings Tab**
- Download folder selection
- Theme selection (Light/Dark)
- Application information
- Advanced configurations

## 🎨 Screenshots

```
┌─────────────────────────────────────────────────────┐
│  🎬 CZ Video Downloader v2.0                    🌙 ℹ️│
├─────────────────────────────────────────────────────┤
│  📥 Download  │  📋 Queue  │  ⚙️ Settings         │
├─────────────────────────────────────────────────────┤
│  📎 Add Videos                                      │
│  ┌─────────────────────────────────────────────┐     │
│  │ https://youtube.com/watch?v=...           │ ➕  │
│  └─────────────────────────────────────────────┘     │
│  ✅ Valid URL detected                              │
│                                                     │
│  📝 Bulk Add (one URL per line):                   │
│  ┌─────────────────────────────────────────────┐     │
│  │ https://youtube.com/watch?v=video1        │     │
│  │ https://tiktok.com/@user/video/123        │     │
│  │ https://instagram.com/p/ABC123/           │ 📥  │
│  └─────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

## 📦 Platform Support

| Platform | URL Format | Status |
|----------|------------|--------|
| **YouTube** | `youtube.com`, `youtu.be` | ✅ Full Support |
| **Facebook** | `facebook.com`, `fb.watch` | ✅ Full Support |
| **TikTok** | `tiktok.com` | ✅ Full Support |
| **Instagram** | `instagram.com` | ✅ Full Support |
| **Twitter/X** | `twitter.com`, `x.com` | ✅ Full Support |

## 🔧 Installation

### Auto Installation (Recommended)
```bash
# The launcher will auto-install everything needed
python launcher_v2.py
```

### Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Launch application  
python main_v2.py
```

### Required Dependencies
- `yt-dlp` - Video downloader engine
- `requests` - HTTP requests
- `Pillow` - Image processing (optional, for thumbnails)
- `tkinter` - GUI framework (built-in)

## 📁 Project Structure

```
czDownloader/
├── 🆕 main_v2.py          # Modern UI application
├── 🆕 launcher_v2.py      # Smart launcher với auto-install
├── 🆕 config.py           # Configuration management
├── 📜 main.py             # Original version (fallback)
├── 📦 requirements.txt    # Dependencies
├── 🖱️ run.bat             # Windows launcher
├── 🖱️ demo.bat            # Demo launcher
├── 🛠️ setup.bat           # Manual setup script
├── 📖 README.md           # Documentation
└── 📋 INSTALL.md          # Detailed installation guide
```

## 🎯 Usage Guide

### 1. **Single URL Download**
1. Paste URL vào input field
2. Chọn quality mong muốn  
3. Click "➕ Add to Queue"
4. Switch sang Queue tab
5. Click "⬇️ Download All"

### 2. **Bulk URL Download**  
1. Paste multiple URLs vào text area (1 URL/line)
2. Click "📥 Add All URLs"
3. Configure concurrent downloads
4. Start batch download

### 3. **Advanced Features**
- **Theme Toggle**: Click 🌙/☀️ button in header
- **Settings**: Use Settings tab for customization
- **Progress Control**: Individual pause/resume/cancel per video
- **Retry**: Auto-retry failed downloads

## 🎨 Themes

### ☀️ Light Theme
- Clean white background
- Blue accent colors
- Professional appearance
- Easy on the eyes

### 🌙 Dark Theme  
- Dark slate background
- Purple accent colors
- Modern cyberpunk feel
- Reduced eye strain

## ⚡ Performance

- **Multi-threading**: Non-blocking UI
- **Concurrent Downloads**: Up to 5 simultaneous downloads
- **Smart Queue**: Efficient resource management
- **Progress Tracking**: Real-time updates
- **Error Recovery**: Auto-retry mechanisms

## 🆚 Version Comparison

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Single URL | ✅ | ✅ |
| Multi URL | ❌ | ✅ |
| Progress per video | ❌ | ✅ |
| Themes | ❌ | ✅ |
| Modern UI | ❌ | ✅ |
| Batch download | ❌ | ✅ |
| Auto installer | ❌ | ✅ |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

## 👨‍💻 Author

**[TRIBUI106](https://github.com/TRIBUI106)**

---

> 💡 **Tip**: Sử dụng `demo.bat` để trải nghiệm nhanh tất cả tính năng mới!