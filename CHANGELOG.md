# CZ Video Downloader - Changelog

## Version 2.1.0 (2025-10-21) - Major Feature Update

### 🔥 Critical Bug Fixes
- ✅ Fixed `AssertionError` with fixup policy (changed 'normal' → 'detect_or_warn')
- ✅ Fixed `AttributeError` in exception handler (corrected self.app.root → self.root)
- ✅ Added comprehensive try-catch blocks to prevent crashes

### 🚀 Performance & Stability (A)
- ✅ **Auto-retry logic with exponential backoff**
  - Automatically retries failed downloads up to 3 times
  - Smart detection of retryable errors (timeout, network, 429, 503)
  - Exponential backoff: 3s → 6s → 12s between retries
  - Displays retry count in error messages

- ✅ **Improved memory management**
  - Better thread cleanup and resource management
  - Proper error handling in all critical sections

- ✅ **Cancellation handling**
  - Added cancel_flag to VideoItem for graceful cancellation
  - Users can cancel downloads in progress
  - Proper thread state management

### 🎨 UI/UX Enhancements (B)
- ✅ **Real-time speed indicator**
  - Displays download speed in MB/s in queue items
  - Shows ETA (estimated time remaining)
  - Format: "📥 45.3% • 12.5 MB/s • ETA: 25s"

- ✅ **Drag-and-drop URL support**
  - Enhanced paste functionality with keyboard shortcuts
  - Visual feedback when pasting URLs
  - Tip messages for better UX

- 🎵 **Sound notifications** (Future)
  - Planned for v2.2.0

- 🖼️ **Thumbnail preview** (Future)
  - Would require image caching system
  - Planned for v2.2.0

### ⚡ Advanced Features (C)
- ✅ **Custom filename templates**
  - Configurable output format in Settings tab
  - Supports placeholders: %(title)s, %(uploader)s, %(upload_date)s, %(id)s
  - Default: `%(title)s.%(ext)s`
  - Example: `%(title)s-%(uploader)s-%(upload_date)s.%(ext)s`

- ✅ **Audio-only extraction**
  - New checkbox: "🎵 Extract audio only (MP3/M4A)"
  - Automatically extracts and converts to MP3 at 192kbps
  - Perfect for music videos and podcasts
  - Uses FFmpeg for conversion

- ✅ **Export/Import queue**
  - Save entire queue to JSON file for later
  - Import previously saved queues
  - Includes metadata: export date, video count, URLs, titles, quality
  - Perfect for batch processing across sessions
  - Location: Settings tab → Queue Management

- ⏱️ **Schedule downloads** (Future)
  - Planned for v2.2.0

### 💎 Quality of Life (D)
- ✅ **Enhanced settings UI**
  - New "⚙️ Download Options" section
  - Audio extraction toggle
  - Filename template editor with hints
  - Concurrent downloads spinner (1-5)

- ✅ **Queue management**
  - Export/Import buttons in Settings tab
  - Timestamped export files
  - Easy backup and restore

- 🔍 **Search/filter in queue** (Future)
  - Planned for v2.2.0

- 📈 **Download history with statistics** (Future)
  - Would require SQLite database
  - Planned for v2.3.0

- 🌐 **Proxy support** (Future)
  - Planned for v2.2.0

- 🔐 **Login support for private videos** (Future)
  - Planned for v2.3.0

### 📊 Technical Improvements
- Enhanced VideoItem class with new properties:
  - `retry_count` and `max_retries`
  - `cancel_flag` for cancellation
  - `extract_audio` for audio-only mode

- Better error categorization and user messages
- Improved progress tracking with determinate/indeterminate modes
- Smoother UI updates with `update_idletasks()`

### 🔧 Configuration
New settings available in Settings tab:
- 🎵 Extract audio only (checkbox)
- 📁 Filename template (text input with examples)
- ⚡ Max concurrent downloads (1-5 spinner)
- 💾 Export Queue button
- 📂 Import Queue button

### 📝 Usage Examples

#### Audio Extraction
1. Go to Settings tab
2. Check "🎵 Extract audio only (MP3/M4A)"
3. Add video URLs and download
4. Files will be saved as .mp3

#### Custom Filenames
1. Go to Settings tab
2. Edit filename template, e.g.:
   - `[%(uploader)s] %(title)s.%(ext)s`
   - `%(upload_date)s - %(title)s.%(ext)s`
   - `%(title)s [%(id)s].%(ext)s`
3. Downloads will use this format

#### Queue Backup
1. Add videos to queue
2. Go to Settings → Queue Management
3. Click "💾 Export Queue"
4. Save .json file
5. Later: Click "📂 Import Queue" to restore

### 🐛 Known Issues
- Pause/Resume not supported (yt-dlp limitation)
- Drag-drop from browser requires tkinterdnd2 package (not included)
  - Current workaround: Copy-paste URLs

### 🙏 Credits
- Powered by yt-dlp
- UI inspired by Modern Material Design
- Built with Python 3.x + tkinter
- Created by CZ Team

### 📦 Dependencies
- Python 3.8+
- yt-dlp (latest)
- requests
- PIL/Pillow
- FFmpeg (for audio extraction and some video formats)

---

## Version 2.0.0 (Previous)
- Initial modern UI release
- Multi-platform support
- Queue system
- Dark/Light themes
- Batch downloads
