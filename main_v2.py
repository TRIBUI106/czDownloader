#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CZ Video Downloader v2.0 - Modern UI
Advanced video downloader with modern interface and multi-URL support
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import threading
import time
import subprocess
import json
import uuid
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
import queue
import webbrowser

# Try to import required libraries
try:
    import yt_dlp
    import requests
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available - thumbnails will be disabled")

class ModernStyle:
    """Modern UI styling configuration"""
    
    # Colors
    COLORS = {
        'primary': '#6366f1',      # Indigo
        'primary_dark': '#4f46e5',
        'secondary': '#8b5cf6',    # Purple
        'success': '#10b981',      # Emerald
        'warning': '#f59e0b',      # Amber
        'error': '#ef4444',        # Red
        'bg_primary': '#ffffff',   # White
        'bg_secondary': '#f8fafc', # Slate 50
        'bg_tertiary': '#f1f5f9',  # Slate 100
        'text_primary': '#1e293b', # Slate 800
        'text_secondary': '#64748b', # Slate 500
        'border': '#e2e8f0',       # Slate 200
        'accent': '#06b6d4',       # Cyan
    }
    
    # Dark theme colors
    DARK_COLORS = {
        'primary': '#6366f1',
        'primary_dark': '#4f46e5', 
        'secondary': '#8b5cf6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'bg_primary': '#0f172a',   # Slate 900
        'bg_secondary': '#1e293b', # Slate 800
        'bg_tertiary': '#334155',  # Slate 700
        'text_primary': '#f1f5f9', # Slate 100
        'text_secondary': '#94a3b8', # Slate 400
        'border': '#475569',       # Slate 600
        'accent': '#06b6d4',
    }
    
    # Fonts
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),
        'heading': ('Segoe UI', 16, 'bold'),
        'subheading': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'code': ('Consolas', 9),
    }

class VideoItem:
    """Represents a video in the download queue"""
    
    def __init__(self, url, quality="best"):
        self.id = str(uuid.uuid4())
        self.url = url
        self.quality = quality
        self.status = "pending"  # pending, analyzing, downloading, completed, error, paused, cancelled
        self.title = "Loading..."
        self.duration = 0
        self.uploader = ""
        self.thumbnail_url = ""
        self.file_size = 0
        self.downloaded_size = 0
        self.speed = 0
        self.eta = 0
        self.progress = 0
        self.error_message = ""
        self.filename = ""
        self.added_time = datetime.now()
        
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'quality': self.quality,
            'status': self.status,
            'title': self.title,
            'duration': self.duration,
            'uploader': self.uploader,
            'progress': self.progress,
            'filename': self.filename,
            'added_time': self.added_time.isoformat()
        }

class VideoListFrame(ttk.Frame):
    """Modern video list with individual progress bars"""
    
    def __init__(self, parent, app_instance):
        super().__init__(parent)
        self.app = app_instance
        self.video_widgets = {}
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = ttk.Label(header_frame, text="📋 Download Queue", 
                               font=ModernStyle.FONTS['heading'])
        title_label.pack(side=tk.LEFT)
        
        # Action buttons
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        self.clear_btn = ttk.Button(btn_frame, text="🗑️ Clear All", 
                                   command=self.clear_all, width=12)
        self.clear_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.download_all_btn = ttk.Button(btn_frame, text="⬇️ Download All", 
                                         command=self.download_all, width=15)
        self.download_all_btn.pack(side=tk.RIGHT)
        
        # Scrollable list
        self.setup_scrollable_list()
        
    def setup_scrollable_list(self):
        # Create canvas and scrollbar for custom scrolling
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Canvas
        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0, bg=ModernStyle.COLORS['bg_secondary'])
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Scrollable frame
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind events
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Mouse wheel scrolling
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame_id, width=canvas_width)
        
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def add_video(self, video_item):
        """Add a video item to the list"""
        video_widget = self.create_video_widget(video_item)
        self.video_widgets[video_item.id] = video_widget
        
    def create_video_widget(self, video_item):
        """Create a modern video widget"""
        # Main container with border and shadow effect
        container = ttk.Frame(self.scrollable_frame, style="VideoCard.TFrame")
        container.pack(fill=tk.X, padx=10, pady=5)
        
        # Configure custom style for video cards
        style = ttk.Style()
        style.configure("VideoCard.TFrame", relief="solid", borderwidth=1)
        
        # Inner frame with padding
        inner_frame = ttk.Frame(container)
        inner_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Top row: Title and controls
        top_row = ttk.Frame(inner_frame)
        top_row.pack(fill=tk.X, pady=(0, 10))
        
        # Video info
        info_frame = ttk.Frame(top_row)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Title
        title_label = ttk.Label(info_frame, text=video_item.title, 
                               font=ModernStyle.FONTS['subheading'],
                               foreground=ModernStyle.COLORS['text_primary'])
        title_label.pack(anchor=tk.W)
        
        # URL and details
        url_text = video_item.url[:60] + "..." if len(video_item.url) > 60 else video_item.url
        url_label = ttk.Label(info_frame, text=url_text,
                             font=ModernStyle.FONTS['small'],
                             foreground=ModernStyle.COLORS['text_secondary'])
        url_label.pack(anchor=tk.W)
        
        # Controls frame
        controls_frame = ttk.Frame(top_row)
        controls_frame.pack(side=tk.RIGHT)
        
        # Control buttons
        pause_btn = ttk.Button(controls_frame, text="⏸️", width=3,
                              command=lambda: self.pause_video(video_item.id))
        pause_btn.pack(side=tk.LEFT, padx=2)
        
        cancel_btn = ttk.Button(controls_frame, text="❌", width=3,
                               command=lambda: self.cancel_video(video_item.id))
        cancel_btn.pack(side=tk.LEFT, padx=2)
        
        retry_btn = ttk.Button(controls_frame, text="🔄", width=3,
                              command=lambda: self.retry_video(video_item.id))
        retry_btn.pack(side=tk.LEFT, padx=2)
        
        # Middle row: Progress bar
        progress_frame = ttk.Frame(inner_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Progress bar
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, 
                                     maximum=100, style="Custom.Horizontal.TProgressbar")
        progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Progress text
        progress_text = ttk.Label(progress_frame, text="Pending...",
                                 font=ModernStyle.FONTS['small'],
                                 foreground=ModernStyle.COLORS['text_secondary'])
        progress_text.pack(anchor=tk.W)
        
        # Bottom row: Status and metadata
        bottom_row = ttk.Frame(inner_frame)
        bottom_row.pack(fill=tk.X)
        
        # Status
        status_label = ttk.Label(bottom_row, text=f"Status: {video_item.status}",
                               font=ModernStyle.FONTS['small'])
        status_label.pack(side=tk.LEFT)
        
        # Quality and time
        meta_label = ttk.Label(bottom_row, text=f"Quality: {video_item.quality} • Added: {video_item.added_time.strftime('%H:%M')}",
                              font=ModernStyle.FONTS['small'],
                              foreground=ModernStyle.COLORS['text_secondary'])
        meta_label.pack(side=tk.RIGHT)
        
        # Store references for updates
        widget_data = {
            'container': container,
            'title_label': title_label,
            'url_label': url_label,
            'progress_var': progress_var,
            'progress_bar': progress_bar,
            'progress_text': progress_text,
            'status_label': status_label,
            'pause_btn': pause_btn,
            'cancel_btn': cancel_btn,
            'retry_btn': retry_btn,
            'video_item': video_item
        }
        
        return widget_data
        
    def update_video(self, video_id, **kwargs):
        """Update video widget with new data"""
        if video_id not in self.video_widgets:
            return
            
        widget = self.video_widgets[video_id]
        video_item = widget['video_item']
        
        # Update video item
        for key, value in kwargs.items():
            setattr(video_item, key, value)
            
        # Update UI elements
        if 'title' in kwargs:
            widget['title_label'].config(text=kwargs['title'])
            
        if 'progress' in kwargs:
            widget['progress_var'].set(kwargs['progress'])
            
        if 'status' in kwargs:
            widget['status_label'].config(text=f"Status: {kwargs['status']}")
            
            # Update button states based on status
            status = kwargs['status']
            if status == "downloading":
                widget['pause_btn'].config(state="normal", text="⏸️")
                widget['cancel_btn'].config(state="normal")
                widget['retry_btn'].config(state="disabled")
            elif status == "paused":
                widget['pause_btn'].config(state="normal", text="▶️")
                widget['cancel_btn'].config(state="normal")
                widget['retry_btn'].config(state="normal")
            elif status in ["completed", "error", "cancelled"]:
                widget['pause_btn'].config(state="disabled")
                widget['cancel_btn'].config(state="disabled") 
                widget['retry_btn'].config(state="normal" if status != "completed" else "disabled")
                
        # Update progress text
        if 'speed' in kwargs and 'eta' in kwargs:
            speed_mb = kwargs.get('speed', 0) / 1024 / 1024
            eta = kwargs.get('eta', 0)
            progress_text = f"{video_item.progress:.1f}% • {speed_mb:.1f} MB/s • ETA: {eta}s"
            widget['progress_text'].config(text=progress_text)
            
    def remove_video(self, video_id):
        """Remove video from list"""
        if video_id in self.video_widgets:
            widget = self.video_widgets[video_id]
            widget['container'].destroy()
            del self.video_widgets[video_id]
            
    def clear_all(self):
        """Clear all videos from list"""
        if messagebox.askyesno("Confirm", "Clear all videos from queue?"):
            for video_id in list(self.video_widgets.keys()):
                self.remove_video(video_id)
            self.app.video_queue.clear()
            
    def download_all(self):
        """Start downloading all pending videos"""
        self.app.start_batch_download()
        
    def pause_video(self, video_id):
        """Pause/resume video download"""
        self.app.toggle_video_download(video_id)
        
    def cancel_video(self, video_id):
        """Cancel video download"""
        self.app.cancel_video_download(video_id)
        
    def retry_video(self, video_id):
        """Retry failed video download"""
        self.app.retry_video_download(video_id)

class ModernVideoDownloader:
    """Modern video downloader with advanced UI"""
    
    def __init__(self, root):
        self.root = root
        self.video_queue = {}  # video_id -> VideoItem
        self.download_threads = {}  # video_id -> thread
        self.is_dark_theme = False
        self.download_path = ""
        
        self.setup_ui()
        self.setup_download_folder()
        self.apply_modern_styles()
        
    def setup_ui(self):
        """Setup modern UI"""
        self.root.title("🎬 CZ Video Downloader v2.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Download tab
        self.download_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.download_tab, text="📥 Download")
        
        # Queue tab
        self.queue_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.queue_tab, text="📋 Queue")
        
        # Settings tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="⚙️ Settings")
        
        # Setup tab contents
        self.setup_download_tab()
        self.setup_queue_tab()
        self.setup_settings_tab()
        
    def create_header(self):
        """Create modern header with gradient effect"""
        header_frame = tk.Frame(self.main_container, height=80, 
                               bg=ModernStyle.COLORS['primary'])
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=ModernStyle.COLORS['primary'])
        header_content.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        # Title
        title_label = tk.Label(header_content, text="🎬 CZ Video Downloader", 
                              font=ModernStyle.FONTS['title'],
                              bg=ModernStyle.COLORS['primary'],
                              fg="white")
        title_label.pack(side=tk.LEFT)
        
        # Header buttons
        btn_frame = tk.Frame(header_content, bg=ModernStyle.COLORS['primary'])
        btn_frame.pack(side=tk.RIGHT)
        
        # Theme toggle
        self.theme_btn = tk.Button(btn_frame, text="🌙", font=("Segoe UI", 12),
                                  command=self.toggle_theme, width=3,
                                  bg=ModernStyle.COLORS['primary_dark'],
                                  fg="white", border=0)
        self.theme_btn.pack(side=tk.RIGHT, padx=5)
        
        # About button
        about_btn = tk.Button(btn_frame, text="ℹ️", font=("Segoe UI", 12),
                             command=self.show_about, width=3,
                             bg=ModernStyle.COLORS['primary_dark'],
                             fg="white", border=0)
        about_btn.pack(side=tk.RIGHT, padx=5)
        
    def setup_download_tab(self):
        """Setup download tab with URL input"""
        # URL input section
        url_section = ttk.LabelFrame(self.download_tab, text="📎 Add Videos", padding="20")
        url_section.pack(fill=tk.X, padx=20, pady=20)
        
        # URL input
        url_frame = ttk.Frame(url_section)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.url_var = tk.StringVar()
        self.url_var.trace_add("write", self.on_url_change)
        
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, 
                             font=ModernStyle.FONTS['body'], width=60)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        add_btn = ttk.Button(url_frame, text="➕ Add to Queue", 
                            command=self.add_url_to_queue, width=15)
        add_btn.pack(side=tk.RIGHT)
        
        # URL validation indicator
        self.url_status_var = tk.StringVar(value="Paste video URLs here...")
        url_status = ttk.Label(url_section, textvariable=self.url_status_var,
                              font=ModernStyle.FONTS['small'])
        url_status.pack(anchor=tk.W)
        
        # Bulk input
        bulk_frame = ttk.Frame(url_section)
        bulk_frame.pack(fill=tk.X, pady=(15, 0))
        
        bulk_label = ttk.Label(bulk_frame, text="📝 Bulk Add (one URL per line):",
                              font=ModernStyle.FONTS['body'])
        bulk_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Text area for multiple URLs
        text_frame = ttk.Frame(bulk_frame)
        text_frame.pack(fill=tk.X)
        
        self.bulk_text = tk.Text(text_frame, height=4, font=ModernStyle.FONTS['body'])
        bulk_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.bulk_text.yview)
        self.bulk_text.configure(yscrollcommand=bulk_scroll.set)
        
        self.bulk_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        bulk_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bulk actions
        bulk_actions = ttk.Frame(url_section)
        bulk_actions.pack(fill=tk.X, pady=(10, 0))
        
        bulk_add_btn = ttk.Button(bulk_actions, text="📥 Add All URLs", 
                                 command=self.add_bulk_urls)
        bulk_add_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        bulk_clear_btn = ttk.Button(bulk_actions, text="🗑️ Clear", 
                                   command=lambda: self.bulk_text.delete(1.0, tk.END))
        bulk_clear_btn.pack(side=tk.RIGHT)
        
        # Settings section
        settings_section = ttk.LabelFrame(self.download_tab, text="⚙️ Download Settings", padding="20")
        settings_section.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        settings_grid = ttk.Frame(settings_section)
        settings_grid.pack(fill=tk.X)
        
        # Quality selection
        ttk.Label(settings_grid, text="Quality:", font=ModernStyle.FONTS['body']).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(settings_grid, textvariable=self.quality_var,
                                   values=["best", "1080p", "720p", "480p", "360p", "worst"],
                                   state="readonly", width=15)
        quality_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Concurrent downloads
        ttk.Label(settings_grid, text="Concurrent:", font=ModernStyle.FONTS['body']).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        
        self.concurrent_var = tk.StringVar(value="2")
        concurrent_spin = ttk.Spinbox(settings_grid, from_=1, to=5, textvariable=self.concurrent_var, width=8)
        concurrent_spin.grid(row=0, column=3, sticky=tk.W)
        
    def setup_queue_tab(self):
        """Setup queue tab with video list"""
        self.video_list = VideoListFrame(self.queue_tab, self)
        self.video_list.pack(fill=tk.BOTH, expand=True)
        
    def setup_settings_tab(self):
        """Setup settings tab"""
        # Download folder
        folder_section = ttk.LabelFrame(self.settings_tab, text="📁 Download Location", padding="20")
        folder_section.pack(fill=tk.X, padx=20, pady=20)
        
        folder_frame = ttk.Frame(folder_section)
        folder_frame.pack(fill=tk.X)
        
        self.folder_var = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, 
                                state="readonly", font=ModernStyle.FONTS['body'])
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(folder_frame, text="📂 Browse", 
                               command=self.browse_folder)
        browse_btn.pack(side=tk.RIGHT)
        
        # Theme settings
        theme_section = ttk.LabelFrame(self.settings_tab, text="🎨 Appearance", padding="20")
        theme_section.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        theme_frame = ttk.Frame(theme_section)
        theme_frame.pack(fill=tk.X)
        
        self.theme_var = tk.StringVar(value="Light")
        light_radio = ttk.Radiobutton(theme_frame, text="☀️ Light", variable=self.theme_var, 
                                     value="Light", command=self.apply_theme)
        light_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        dark_radio = ttk.Radiobutton(theme_frame, text="🌙 Dark", variable=self.theme_var,
                                    value="Dark", command=self.apply_theme)
        dark_radio.pack(side=tk.LEFT)
        
        # About section
        about_section = ttk.LabelFrame(self.settings_tab, text="ℹ️ About", padding="20")
        about_section.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        about_text = """CZ Video Downloader v2.0
        
Modern video downloader supporting:
• YouTube, Facebook, TikTok, Instagram
• Multi-URL queue system  
• Individual progress tracking
• Dark/Light themes
• Batch downloads

Powered by yt-dlp"""
        
        about_label = ttk.Label(about_section, text=about_text, 
                               font=ModernStyle.FONTS['small'],
                               justify=tk.LEFT)
        about_label.pack(anchor=tk.W)
        
    def apply_modern_styles(self):
        """Apply modern styling to ttk widgets"""
        style = ttk.Style()
        
        # Configure styles for modern look
        style.configure("Custom.Horizontal.TProgressbar",
                       background=ModernStyle.COLORS['primary'],
                       troughcolor=ModernStyle.COLORS['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=ModernStyle.COLORS['primary'],
                       darkcolor=ModernStyle.COLORS['primary'])
                       
        # Configure notebook style
        style.configure("TNotebook.Tab",
                       padding=[20, 10],
                       font=ModernStyle.FONTS['body'])
                       
    def setup_download_folder(self):
        """Setup download folder"""
        downloads_path = Path.home() / "Downloads" / "czDownloader"
        downloads_path.mkdir(parents=True, exist_ok=True)
        self.download_path = str(downloads_path)
        self.folder_var.set(self.download_path)
        
    def on_url_change(self, *args):
        """Handle URL input changes"""
        url = self.url_var.get().strip()
        if not url:
            self.url_status_var.set("Paste video URLs here...")
            return
            
        if self.validate_url(url):
            self.url_status_var.set("✅ Valid URL detected")
        else:
            self.url_status_var.set("❌ URL not supported")
            
    def validate_url(self, url):
        """Validate if URL is supported"""
        supported_domains = [
            'youtube.com', 'youtu.be', 'facebook.com', 'fb.watch',
            'tiktok.com', 'instagram.com', 'twitter.com', 'x.com'
        ]
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            return any(supported in domain for supported in supported_domains)
        except:
            return False
            
    def add_url_to_queue(self):
        """Add single URL to queue"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL!")
            return
            
        if not self.validate_url(url):
            messagebox.showerror("Error", "URL not supported!")
            return
            
        self.add_video_to_queue(url)
        self.url_var.set("")
        
    def add_bulk_urls(self):
        """Add multiple URLs from text area"""
        text_content = self.bulk_text.get(1.0, tk.END).strip()
        if not text_content:
            messagebox.showerror("Error", "Please enter URLs in the text area!")
            return
            
        urls = [url.strip() for url in text_content.split('\n') if url.strip()]
        
        valid_count = 0
        for url in urls:
            if self.validate_url(url):
                self.add_video_to_queue(url)
                valid_count += 1
                
        self.bulk_text.delete(1.0, tk.END)
        messagebox.showinfo("Success", f"Added {valid_count} valid URLs to queue!")
        
        # Switch to queue tab
        self.notebook.select(1)
        
    def add_video_to_queue(self, url):
        """Add video to download queue"""
        quality = self.quality_var.get()
        video_item = VideoItem(url, quality)
        
        self.video_queue[video_item.id] = video_item
        self.video_list.add_video(video_item)
        
        # Analyze video info in background
        thread = threading.Thread(target=self.analyze_video, args=(video_item,))
        thread.daemon = True
        thread.start()
        
    def analyze_video(self, video_item):
        """Analyze video to get metadata"""
        try:
            import yt_dlp
            
            video_item.status = "analyzing"
            self.video_list.update_video(video_item.id, status="analyzing")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_item.url, download=False)
                
                video_item.title = info.get('title', 'Unknown')[:80]
                video_item.duration = info.get('duration', 0)
                video_item.uploader = info.get('uploader', 'Unknown')
                video_item.thumbnail_url = info.get('thumbnail', '')
                video_item.status = "pending"
                
                # Update UI
                self.video_list.update_video(video_item.id, 
                                           title=video_item.title,
                                           status="pending")
                
        except Exception as e:
            video_item.status = "error"
            video_item.error_message = str(e)
            self.video_list.update_video(video_item.id, status="error")
            
    def start_batch_download(self):
        """Start downloading all pending videos"""
        pending_videos = [v for v in self.video_queue.values() if v.status == "pending"]
        
        if not pending_videos:
            messagebox.showinfo("Info", "No videos to download!")
            return
            
        max_concurrent = int(self.concurrent_var.get())
        
        for i, video in enumerate(pending_videos[:max_concurrent]):
            self.start_video_download(video.id)
            
    def start_video_download(self, video_id):
        """Start downloading a specific video"""
        if video_id not in self.video_queue:
            return
            
        video_item = self.video_queue[video_id]
        
        if video_item.status in ["downloading", "completed"]:
            return
            
        # Create download thread
        thread = threading.Thread(target=self.download_video_worker, args=(video_item,))
        thread.daemon = True
        self.download_threads[video_id] = thread
        thread.start()
        
    def download_video_worker(self, video_item):
        """Worker function for downloading video"""
        try:
            import yt_dlp
            
            video_item.status = "downloading"
            self.video_list.update_video(video_item.id, status="downloading")
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if 'total_bytes' in d and d['total_bytes']:
                        progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                        video_item.progress = progress
                        video_item.speed = d.get('speed', 0)
                        video_item.eta = d.get('eta', 0)
                        
                        self.video_list.update_video(video_item.id,
                                                   progress=progress,
                                                   speed=video_item.speed,
                                                   eta=video_item.eta)
                        
                elif d['status'] == 'finished':
                    video_item.status = "completed"
                    video_item.progress = 100
                    video_item.filename = os.path.basename(d['filename'])
                    
                    self.video_list.update_video(video_item.id,
                                               status="completed",
                                               progress=100)
                    
            ydl_opts = {
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'format': self.get_format_selector(video_item.quality),
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_item.url])
                
        except Exception as e:
            video_item.status = "error"
            video_item.error_message = str(e)
            self.video_list.update_video(video_item.id, status="error")
            
    def get_format_selector(self, quality):
        """Get format selector for yt-dlp"""
        quality_map = {
            "best": "best[ext=mp4]/best",
            "1080p": "best[height<=1080][ext=mp4]/best[height<=1080]",
            "720p": "best[height<=720][ext=mp4]/best[height<=720]",
            "480p": "best[height<=480][ext=mp4]/best[height<=480]",
            "360p": "best[height<=360][ext=mp4]/best[height<=360]",
            "worst": "worst[ext=mp4]/worst"
        }
        return quality_map.get(quality, "best[ext=mp4]/best")
        
    def toggle_video_download(self, video_id):
        """Toggle pause/resume for video"""
        # This would require more advanced implementation with yt-dlp
        pass
        
    def cancel_video_download(self, video_id):
        """Cancel video download"""
        if video_id in self.video_queue:
            video_item = self.video_queue[video_id]
            video_item.status = "cancelled"
            self.video_list.update_video(video_id, status="cancelled")
            
    def retry_video_download(self, video_id):
        """Retry failed video download"""
        if video_id in self.video_queue:
            video_item = self.video_queue[video_id]
            video_item.status = "pending"
            video_item.progress = 0
            self.video_list.update_video(video_id, status="pending", progress=0)
            self.start_video_download(video_id)
            
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.folder_var.set(folder)
            
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.is_dark_theme = not self.is_dark_theme
        self.theme_var.set("Dark" if self.is_dark_theme else "Light")
        self.apply_theme()
        
    def apply_theme(self):
        """Apply selected theme"""
        self.is_dark_theme = (self.theme_var.get() == "Dark")
        
        colors = ModernStyle.DARK_COLORS if self.is_dark_theme else ModernStyle.COLORS
        
        # Update theme button
        self.theme_btn.config(text="☀️" if self.is_dark_theme else "🌙")
        
        # Apply theme to widgets (simplified - full implementation would be more extensive)
        style = ttk.Style()
        if self.is_dark_theme:
            style.theme_use('clam')
            # Configure dark theme styles
        else:
            style.theme_use('clam')
            # Configure light theme styles
            
    def show_about(self):
        """Show about dialog"""
        about_text = """🎬 CZ Video Downloader v2.0

Advanced video downloader with modern interface

Features:
• Multi-platform support (YouTube, Facebook, TikTok, Instagram)
• Multi-URL queue system
• Individual progress tracking  
• Dark/Light themes
• Batch downloads
• Modern UI with Material Design

Powered by yt-dlp
Created with ❤️ by CZ Team"""

        messagebox.showinfo("About CZ Video Downloader", about_text)

def main():
    """Main application entry point"""
    # Check dependencies
    try:
        import yt_dlp
        import requests
    except ImportError as e:
        result = tk.messagebox.askyesno("Missing Dependencies", 
                                       f"Required libraries not found: {e}\n\n" +
                                       "Would you like to install them automatically?")
        if result:
            import subprocess
            import sys
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "requests", "pillow"])
                tk.messagebox.showinfo("Success", "Dependencies installed successfully!\nPlease restart the application.")
            except Exception as install_error:
                tk.messagebox.showerror("Installation Failed", f"Failed to install dependencies:\n{install_error}")
        return
    
    # Create and run application
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
        
    app = ModernVideoDownloader(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()