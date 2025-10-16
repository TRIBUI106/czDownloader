#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CZ Video Downloader
Ứng dụng download video từ YouTube, Facebook, TikTok, Instagram
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import threading
import time
import subprocess
from pathlib import Path
import yt_dlp
import json
import requests
from urllib.parse import urlparse

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_download_folder()
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.root.title("CZ Video Downloader v1.0")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.minsize(600, 400)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom styles
        style.configure("Title.TLabel", font=("Arial", 18, "bold"), foreground="#2c3e50")
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))
        style.configure("Success.TLabel", foreground="#27ae60")
        style.configure("Error.TLabel", foreground="#e74c3c")
        style.configure("Info.TLabel", foreground="#3498db")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title with banner
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(title_frame, text="🎬 CZ Video Downloader", 
                               style="Title.TLabel")
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Download from YouTube • Facebook • TikTok • Instagram", 
                                 font=("Arial", 9), foreground="gray")
        subtitle_label.pack(pady=(5, 0))
        
        # URL input with validation
        url_frame = ttk.LabelFrame(main_frame, text="📎 Video URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.url_var = tk.StringVar()
        self.url_var.trace_add("write", self.on_url_change)
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=60, font=("Arial", 10))
        url_entry.pack(fill=tk.X, pady=(0, 5))
        
        # URL validation indicator
        self.url_status_var = tk.StringVar(value="Paste video URL here...")
        url_status_label = ttk.Label(url_frame, textvariable=self.url_status_var, 
                                   font=("Arial", 8), foreground="gray")
        url_status_label.pack(anchor=tk.W)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Quality selection
        quality_frame = ttk.Frame(settings_frame)
        quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        quality_label = ttk.Label(quality_frame, text="Quality:")
        quality_label.pack(side=tk.LEFT)
        
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                                   values=["best", "720p", "480p", "360p", "worst"], 
                                   state="readonly", width=15)
        quality_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Download button
        self.download_btn = ttk.Button(quality_frame, text="📥 Download Video", 
                                     command=self.start_download, style="Accent.TButton")
        self.download_btn.pack(side=tk.RIGHT)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Download Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, style="Accent.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Status text
        self.status_var = tk.StringVar(value="Ready to download...")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var, 
                               style="Info.TLabel", font=("Arial", 9))
        status_label.pack(anchor=tk.W)
        
        # Download folder info
        self.folder_var = tk.StringVar()
        folder_label = ttk.Label(progress_frame, textvariable=self.folder_var, 
                               foreground="gray", font=("Arial", 8))
        folder_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="📋 Activity Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        log_container = ttk.Frame(log_frame)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_container, height=8, wrap=tk.WORD, font=("Consolas", 9))
        log_scrollbar = ttk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_container.columnconfigure(0, weight=1)
        log_container.rowconfigure(0, weight=1)
        
    def on_url_change(self, *args):
        """Callback khi URL thay đổi"""
        url = self.url_var.get().strip()
        if not url:
            self.url_status_var.set("Paste video URL here...")
            return
            
        if self.validate_url(url):
            self.url_status_var.set("✅ Valid URL detected")
        else:
            self.url_status_var.set("❌ URL not supported or invalid")
        
    def setup_download_folder(self):
        """Thiết lập thư mục download"""
        downloads_path = Path.home() / "Downloads" / "czDownloader"
        downloads_path.mkdir(parents=True, exist_ok=True)
        self.download_path = str(downloads_path)
        self.folder_var.set(f"📁 Save to: {self.download_path}")
        self.log(f"📁 Download folder ready: {self.download_path}")
        
    def log(self, message):
        """Ghi log vào text area"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message, color="blue"):
        """Cập nhật status"""
        self.status_var.set(message)
        self.log(message)
        
    def progress_hook(self, d):
        """Hook để cập nhật progress bar"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                
                # Format speed
                speed = d.get('speed', 0)
                if speed:
                    if speed > 1024*1024:
                        speed_str = f"{speed/1024/1024:.1f} MB/s"
                    else:
                        speed_str = f"{speed/1024:.1f} KB/s"
                else:
                    speed_str = "Calculating..."
                
                # Format ETA
                eta = d.get('eta')
                if eta:
                    if eta > 60:
                        eta_str = f"{eta//60}m {eta%60}s"
                    else:
                        eta_str = f"{eta}s"
                else:
                    eta_str = "Calculating..."
                
                # Format file size
                if 'total_bytes' in d:
                    total_mb = d['total_bytes'] / 1024 / 1024
                    downloaded_mb = d['downloaded_bytes'] / 1024 / 1024
                    size_str = f"{downloaded_mb:.1f}/{total_mb:.1f} MB"
                else:
                    size_str = f"{d['downloaded_bytes']/1024/1024:.1f} MB"
                
                self.update_status(f"📥 Downloading... {percent:.1f}% • {speed_str} • ETA: {eta_str} • {size_str}")
            else:
                # Fallback when total bytes unknown
                downloaded_mb = d.get('downloaded_bytes', 0) / 1024 / 1024
                speed = d.get('speed', 0)
                speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "Calculating..."
                self.update_status(f"📥 Downloading... {downloaded_mb:.1f} MB • {speed_str}")
                
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            filename = os.path.basename(d['filename'])
            # Truncate long filenames
            if len(filename) > 50:
                filename = filename[:47] + "..."
            self.update_status(f"✅ Download completed: {filename}", "green")
            
            # Show success notification
            self.root.after(100, lambda: messagebox.showinfo(
                "Download Complete", 
                f"Video saved successfully!\n\nFile: {filename}\nLocation: {self.download_path}"
            ))
            
        elif d['status'] == 'error':
            self.update_status("❌ Download failed", "red")
            self.progress_var.set(0)
            
    def validate_url(self, url):
        """Kiểm tra URL hợp lệ"""
        supported_domains = [
            'youtube.com', 'youtu.be', 'facebook.com', 'fb.watch',
            'tiktok.com', 'instagram.com', 'twitter.com', 'x.com'
        ]
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            for supported in supported_domains:
                if supported in domain:
                    return True
            return False
        except:
            return False
            
    def download_video(self, url, quality):
        """Download video với yt-dlp"""
        try:
            # Kiểm tra yt-dlp
            try:
                import yt_dlp
            except ImportError:
                raise Exception("yt-dlp not installed. Run: pip install yt-dlp")
            
            # Cấu hình yt-dlp
            ydl_opts = {
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'format': self.get_format_selector(quality),
                'noplaylist': True,
                'extractaudio': False,
                'writeinfojson': False,
                'writethumbnail': False,
                'ignoreerrors': False,
                'no_warnings': False,
            }
            
            # Cấu hình thêm cho các platform
            if 'tiktok.com' in url:
                ydl_opts['format'] = 'best[ext=mp4]'
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            elif 'instagram.com' in url:
                ydl_opts['format'] = 'best[ext=mp4]'
            elif 'facebook.com' in url or 'fb.watch' in url:
                ydl_opts['format'] = 'best[ext=mp4]'
                
            self.update_status("🔍 Analyzing video...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Lấy thông tin video
                try:
                    info = ydl.extract_info(url, download=False)
                except Exception as e:
                    if "Private video" in str(e):
                        raise Exception("❌ Video is private or unavailable")
                    elif "Video unavailable" in str(e):
                        raise Exception("❌ Video not found or region blocked")
                    else:
                        raise Exception(f"❌ Cannot access video: {str(e)}")
                
                title = info.get('title', 'Unknown')[:50] + "..." if len(info.get('title', '')) > 50 else info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Unknown')
                view_count = info.get('view_count', 0)
                
                self.log(f"🎬 Title: {title}")
                self.log(f"👤 Channel: {uploader}")
                if duration:
                    minutes, seconds = divmod(duration, 60)
                    self.log(f"⏱️ Duration: {minutes:02d}:{seconds:02d}")
                if view_count:
                    self.log(f"👁️ Views: {view_count:,}")
                
                self.update_status("📥 Starting download...")
                
                # Download video
                ydl.download([url])
                
        except yt_dlp.DownloadError as e:
            error_msg = str(e)
            if "HTTP Error 403" in error_msg:
                self.update_status("❌ Access denied - try different quality", "red")
            elif "HTTP Error 404" in error_msg:
                self.update_status("❌ Video not found", "red") 
            else:
                self.update_status(f"❌ Download error: {error_msg}", "red")
            self.progress_var.set(0)
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", "red")
            self.progress_var.set(0)
            
    def get_format_selector(self, quality):
        """Chọn format dựa trên quality"""
        if quality == "best":
            return "best[ext=mp4]/best"
        elif quality == "720p":
            return "best[height<=720][ext=mp4]/best[height<=720]"
        elif quality == "480p":
            return "best[height<=480][ext=mp4]/best[height<=480]"
        elif quality == "360p":
            return "best[height<=360][ext=mp4]/best[height<=360]"
        elif quality == "worst":
            return "worst[ext=mp4]/worst"
        else:
            return "best[ext=mp4]/best"
            
    def start_download(self):
        """Bắt đầu quá trình download"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("❌ Error", "Please enter a video URL!")
            return
            
        if not self.validate_url(url):
            messagebox.showerror("❌ Unsupported URL", 
                               "This URL is not supported!\n\n" +
                               "Supported platforms:\n" +
                               "• YouTube (youtube.com, youtu.be)\n" +
                               "• Facebook (facebook.com, fb.watch)\n" +
                               "• TikTok (tiktok.com)\n" +
                               "• Instagram (instagram.com)\n" +
                               "• Twitter/X (twitter.com, x.com)")
            return
        
        # Check if yt-dlp is installed
        try:
            import yt_dlp
        except ImportError:
            result = messagebox.askyesno("❌ Missing Dependency", 
                                       "yt-dlp is required but not installed.\n\n" +
                                       "Would you like to install it automatically?\n" +
                                       "(This may take a few minutes)")
            if result:
                self.install_ytdlp()
            return
            
        # Disable button
        self.download_btn.config(state="disabled", text="📥 Downloading...")
        self.progress_var.set(0)
        
        # Chạy download trong thread riêng
        quality = self.quality_var.get()
        thread = threading.Thread(target=self.download_thread, args=(url, quality))
        thread.daemon = True
        thread.start()
        
    def install_ytdlp(self):
        """Cài đặt yt-dlp tự động"""
        self.update_status("📦 Installing yt-dlp...")
        self.download_btn.config(state="disabled", text="Installing...")
        
        def install_thread():
            try:
                import subprocess
                result = subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.root.after(0, lambda: [
                        self.update_status("✅ yt-dlp installed successfully!", "green"),
                        self.download_btn.config(state="normal", text="📥 Download Video"),
                        messagebox.showinfo("✅ Success", "yt-dlp installed successfully!\nYou can now download videos.")
                    ])
                else:
                    self.root.after(0, lambda: [
                        self.update_status("❌ Failed to install yt-dlp", "red"),
                        self.download_btn.config(state="normal", text="📥 Download Video"),
                        messagebox.showerror("❌ Installation Failed", 
                                           f"Failed to install yt-dlp:\n{result.stderr}")
                    ])
            except Exception as e:
                self.root.after(0, lambda: [
                    self.update_status(f"❌ Installation error: {str(e)}", "red"),
                    self.download_btn.config(state="normal", text="📥 Download Video")
                ])
        
        thread = threading.Thread(target=install_thread)
        thread.daemon = True
        thread.start()
        
    def download_thread(self, url, quality):
        """Thread để download video"""
        try:
            self.download_video(url, quality)
        finally:
            # Re-enable button
            self.root.after(0, lambda: [
                self.download_btn.config(state="normal", text="📥 Download Video"),
                self.update_status("Ready for next download...", "blue")
            ])

def main():
    # Tạo window
    root = tk.Tk()
    
    # Thiết lập icon (optional)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # Khởi tạo app
    app = VideoDownloader(root)
    
    # Chạy app
    root.mainloop()

if __name__ == "__main__":
    main()