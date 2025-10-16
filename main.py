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
import logging
import traceback

class UIAnimations:
    """Smooth UI animations and transitions"""
    
    @staticmethod
    def fade_in_widget(widget, duration=300, steps=20):
        """Fade in a widget smoothly"""
        try:
            original_bg = widget.cget('bg')
            step_delay = duration // steps
            
            def animate_step(step):
                if step <= steps:
                    alpha = step / steps
                    # Simple alpha blending simulation with background
                    widget.after(step_delay, lambda: animate_step(step + 1))
                    
        except:
            pass  # Fallback: no animation
    
    @staticmethod
    def slide_in_progress(progress_bar, target_value, duration=500):
        """Smooth progress bar animation"""
        try:
            current_value = progress_bar['value']
            steps = 30
            step_delay = duration // steps
            step_size = (target_value - current_value) / steps
            
            def animate_step(step):
                if step <= steps:
                    new_value = current_value + (step_size * step)
                    progress_bar['value'] = new_value
                    progress_bar.after(step_delay, lambda: animate_step(step + 1))
                else:
                    progress_bar['value'] = target_value
                    
            animate_step(1)
        except:
            # Fallback: direct set
            progress_bar['value'] = target_value
    
    @staticmethod
    def pulse_button(button, color='#3b82f6', duration=1000):
        """Pulse effect for important buttons"""
        try:
            original_bg = button.cget('bg')
            
            def pulse_step(step, direction=1):
                if step < 20:
                    # Simple color alternation
                    if step % 4 == 0:
                        button.config(bg=color)
                    else:
                        button.config(bg=original_bg)
                    button.after(duration // 20, lambda: pulse_step(step + 1))
                else:
                    button.config(bg=original_bg)
                    
            pulse_step(0)
        except:
            pass

class ErrorLogger:
    """Enhanced error logging system for download failures"""
    
    def __init__(self, download_path):
        self.download_path = download_path
        self.log_file = os.path.join(download_path, "czdownloader_errors.log")
        self.setup_logger()
        
    def setup_logger(self):
        """Setup rotating file logger"""
        self.logger = logging.getLogger("CZDownloader")
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler with UTF-8 encoding
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Formatter with detailed info
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    def log_download_error(self, video_item, error_msg, detailed_traceback=None):
        """Log detailed download error"""
        try:
            # Basic error info
            error_entry = {
                'timestamp': datetime.now().isoformat(),
                'video_title': getattr(video_item, 'title', 'Unknown'),
                'video_url': getattr(video_item, 'url', 'Unknown'),
                'video_quality': getattr(video_item, 'quality', 'Unknown'),
                'error_message': str(error_msg),
                'video_id': getattr(video_item, 'id', 'Unknown')
            }
            
            # Log to file
            log_msg = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 VIDEO DOWNLOAD ERROR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📺 Title: {error_entry['video_title']}
🔗 URL: {error_entry['video_url']}
🎯 Quality: {error_entry['video_quality']}
🆔 Video ID: {error_entry['video_id']}
❌ Error: {error_entry['error_message']}"""
            
            if detailed_traceback:
                log_msg += f"\n\n🐛 DETAILED TRACEBACK:\n{detailed_traceback}"
                
            log_msg += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            
            self.logger.error(log_msg)
            
        except Exception as e:
            print(f"Failed to log error: {e}")
            
    def log_batch_summary(self, batch_summary):
        """Log batch download summary"""
        try:
            total = batch_summary.get('total', 0)
            completed = batch_summary.get('completed', 0)
            failed = batch_summary.get('failed', 0)
            start_time = batch_summary.get('start_time')
            
            if start_time:
                duration = datetime.now() - start_time
                duration_str = str(duration).split('.')[0]
            else:
                duration_str = "Unknown"
                
            summary_msg = f"""
🎯 BATCH DOWNLOAD SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Total Videos: {total}
✅ Completed: {completed}
❌ Failed: {failed}
📈 Success Rate: {(completed/total*100) if total > 0 else 0:.1f}%
⏱️ Duration: {duration_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
            
            self.logger.info(summary_msg)
            
        except Exception as e:
            print(f"Failed to log batch summary: {e}")
            
    def get_log_file_path(self):
        """Get the log file path"""
        return self.log_file

class TroubleshootingHelper:
    """Helper class for troubleshooting common download issues"""
    
    @staticmethod
    def get_error_suggestions(error_message, platform=""):
        """Get troubleshooting suggestions based on error message"""
        suggestions = []
        
        error_lower = error_message.lower()
        
        if "403" in error_message or "access denied" in error_lower:
            suggestions.extend([
                "🔒 Video may be private or region-blocked",
                "🌍 Try using a VPN to change your location",
                "⏰ Wait a few minutes and try again",
                "🔄 Try a different quality setting"
            ])
            
        elif "404" in error_message or "not found" in error_lower:
            suggestions.extend([
                "❌ Video may have been deleted",
                "🔗 Check if the URL is correct",
                "📱 Try getting a fresh link from the platform"
            ])
            
        elif "429" in error_message or "rate limit" in error_lower:
            suggestions.extend([
                "⏳ Too many requests - wait 10-15 minutes",
                "🔢 Reduce concurrent downloads",
                "🕐 Try downloading during off-peak hours"
            ])
            
        elif "age" in error_lower and "restricted" in error_lower:
            suggestions.extend([
                "🔞 Age-restricted content cannot be downloaded",
                "👤 Video requires sign-in to verify age",
                "❌ This is a platform limitation"
            ])
            
        elif "private" in error_lower:
            suggestions.extend([
                "🔐 Video is set to private",
                "👥 Only the uploader can access it",
                "📧 Contact the uploader for access"
            ])
            
        elif "tiktok" in platform.lower():
            suggestions.extend([
                "📱 TikTok has strict anti-bot measures",
                "🔄 Try copying the URL again from mobile app",
                "⏰ Wait a few minutes between downloads",
                "🌐 Use different network connection"
            ])
            
        elif "instagram" in platform.lower():
            suggestions.extend([
                "📸 Instagram blocks automated downloads",
                "👤 Video may require login to view",
                "🔄 Try different quality setting",
                "📱 Use the share link from Instagram app"
            ])
            
        # General suggestions
        if not suggestions:
            suggestions.extend([
                "🔄 Try a different quality setting",
                "⏰ Wait a few minutes and retry",
                "🌐 Check your internet connection",
                "🔗 Verify the URL is correct and accessible"
            ])
            
        return suggestions[:4]  # Limit to 4 suggestions
    
    @staticmethod
    def show_help_dialog(parent, error_message, platform=""):
        """Show detailed help dialog for troubleshooting"""
        help_window = tk.Toplevel(parent)
        help_window.title("🛠️ Troubleshooting Help")
        help_window.geometry("500x400")
        help_window.resizable(True, True)
        help_window.grab_set()
        
        # Center window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - 250
        y = (help_window.winfo_screenheight() // 2) - 200
        help_window.geometry(f"500x400+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(help_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🛠️ Troubleshooting Help", 
                               font=("Segoe UI", 14, "bold"))
        title_label.pack(pady=(0, 15))
        
        # Error details
        error_frame = ttk.LabelFrame(main_frame, text="❌ Error Details", padding="10")
        error_frame.pack(fill=tk.X, pady=(0, 15))
        
        error_text = tk.Text(error_frame, height=3, wrap=tk.WORD, font=("Consolas", 9))
        error_text.pack(fill=tk.X)
        error_text.insert(tk.END, error_message)
        error_text.config(state=tk.DISABLED)
        
        # Suggestions
        suggestions_frame = ttk.LabelFrame(main_frame, text="💡 Suggested Solutions", padding="10")
        suggestions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        suggestions = TroubleshootingHelper.get_error_suggestions(error_message, platform)
        
        for i, suggestion in enumerate(suggestions, 1):
            suggestion_label = ttk.Label(suggestions_frame, text=f"{i}. {suggestion}",
                                       font=("Segoe UI", 10), wraplength=450)
            suggestion_label.pack(anchor=tk.W, pady=2)
        
        # Additional resources
        resources_frame = ttk.LabelFrame(main_frame, text="📚 Additional Resources", padding="10")
        resources_frame.pack(fill=tk.X, pady=(0, 15))
        
        resources_text = """Common solutions:
• Check if video is publicly accessible in your browser
• Try downloading one video at a time
• Update yt-dlp: pip install yt-dlp --upgrade
• Some platforms block downloads during peak hours"""
        
        resources_label = ttk.Label(resources_frame, text=resources_text,
                                  font=("Segoe UI", 9), justify=tk.LEFT)
        resources_label.pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        close_btn = ttk.Button(button_frame, text="✅ Close", 
                             command=help_window.destroy)
        close_btn.pack(side=tk.RIGHT)
        
        update_btn = ttk.Button(button_frame, text="🔄 Update yt-dlp", 
                              command=lambda: TroubleshootingHelper.update_ytdlp(help_window))
        update_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
    @staticmethod
    def update_ytdlp(parent_window):
        """Update yt-dlp in background"""
        def update_worker():
            try:
                import subprocess
                import sys
                result = subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp", "--upgrade"], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    parent_window.after(0, lambda: messagebox.showinfo("Success", "yt-dlp updated successfully!"))
                else:
                    parent_window.after(0, lambda: messagebox.showerror("Error", f"Update failed:\n{result.stderr}"))
            except Exception as e:
                parent_window.after(0, lambda: messagebox.showerror("Error", f"Update failed:\n{str(e)}"))
        
        thread = threading.Thread(target=update_worker)
        thread.daemon = True
        thread.start()
        
        messagebox.showinfo("Updating", "Updating yt-dlp in background...\nThis may take a minute.")

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
    
    # Light theme colors - Clean và professional
    COLORS = {
        'primary': '#2563eb',      # Blue 600
        'primary_dark': '#1d4ed8', # Blue 700
        'secondary': '#7c3aed',    # Violet 600
        'success': '#059669',      # Emerald 600
        'warning': '#d97706',      # Amber 600
        'error': '#dc2626',        # Red 600
        'bg_primary': '#ffffff',   # White
        'bg_secondary': '#f8fafc', # Slate 50
        'bg_tertiary': '#f1f5f9',  # Slate 100
        'bg_card': '#ffffff',      # White
        'text_primary': '#0f172a', # Slate 900
        'text_secondary': '#64748b', # Slate 500
        'border': '#e2e8f0',       # Slate 200
        'border_light': '#f1f5f9', # Slate 100
        'accent': '#0ea5e9',       # Sky 500
        'hover': '#f1f5f9',        # Slate 100
    }
    
    # Dark theme colors - Elegant và eye-friendly
    DARK_COLORS = {
        'primary': '#3b82f6',      # Blue 500 (brighter for dark)
        'primary_dark': '#2563eb', # Blue 600
        'secondary': '#8b5cf6',    # Violet 500
        'success': '#10b981',      # Emerald 500
        'warning': '#f59e0b',      # Amber 500
        'error': '#ef4444',        # Red 500
        'bg_primary': '#0f172a',   # Slate 900
        'bg_secondary': '#1e293b', # Slate 800
        'bg_tertiary': '#334155',  # Slate 700
        'bg_card': '#1e293b',      # Slate 800 for cards
        'text_primary': '#f1f5f9', # Slate 100
        'text_secondary': '#94a3b8', # Slate 400
        'border': '#334155',       # Slate 700
        'border_light': '#475569', # Slate 600
        'accent': '#0ea5e9',       # Sky 500
        'hover': '#334155',        # Slate 700
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
    
    @classmethod
    def get_colors(cls, is_dark=False):
        """Get color scheme based on theme"""
        return cls.DARK_COLORS if is_dark else cls.COLORS

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
        self.progress_mode = "determinate"  # determinate, indeterminate
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
        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0, 
                               bg=self.app.current_colors['bg_secondary'])
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
        colors = self.app.current_colors
        
        # Main container with modern card styling
        container = tk.Frame(self.scrollable_frame, 
                           bg=colors['bg_card'],
                           relief="solid", 
                           bd=1,
                           highlightbackground=colors['border'],
                           highlightthickness=1)
        container.pack(fill=tk.X, padx=10, pady=5)
        
        # Inner frame with padding
        inner_frame = tk.Frame(container, bg=colors['bg_card'])
        inner_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Top row: Title and controls
        top_row = tk.Frame(inner_frame, bg=colors['bg_card'])
        top_row.pack(fill=tk.X, pady=(0, 10))
        
        # Video info
        info_frame = tk.Frame(top_row, bg=colors['bg_card'])
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Title
        title_label = tk.Label(info_frame, text=video_item.title, 
                              font=ModernStyle.FONTS['subheading'],
                              fg=colors['text_primary'],
                              bg=colors['bg_card'],
                              anchor="w")
        title_label.pack(anchor=tk.W, fill=tk.X)
        
        # URL and details
        url_text = video_item.url[:60] + "..." if len(video_item.url) > 60 else video_item.url
        url_label = tk.Label(info_frame, text=url_text,
                            font=ModernStyle.FONTS['small'],
                            fg=colors['text_secondary'],
                            bg=colors['bg_card'],
                            anchor="w")
        url_label.pack(anchor=tk.W, fill=tk.X)
        
        # Controls frame
        controls_frame = tk.Frame(top_row, bg=colors['bg_card'])
        controls_frame.pack(side=tk.RIGHT)
        
        # Control buttons with modern styling
        btn_style = {
            'font': ("Segoe UI", 10),
            'width': 3,
            'relief': 'flat',
            'bg': colors['bg_tertiary'],
            'fg': colors['text_primary'],
            'activebackground': colors['hover'],
            'bd': 0,
            'cursor': 'hand2'
        }
        
        pause_btn = tk.Button(controls_frame, text="⏸️", 
                             command=lambda: self.pause_video(video_item.id),
                             **btn_style)
        pause_btn.pack(side=tk.LEFT, padx=2)
        
        cancel_btn = tk.Button(controls_frame, text="❌",
                              command=lambda: self.cancel_video(video_item.id),
                              **btn_style)
        cancel_btn.pack(side=tk.LEFT, padx=2)
        
        retry_btn = tk.Button(controls_frame, text="🔄",
                             command=lambda: self.retry_video(video_item.id),
                             **btn_style)
        retry_btn.pack(side=tk.LEFT, padx=2)
        
        # Help button for errors
        help_btn = tk.Button(controls_frame, text="❓",
                            command=lambda: self.show_help(video_item.id),
                            **btn_style)
        help_btn.pack(side=tk.LEFT, padx=2)
        
        # Middle row: Progress bar
        progress_frame = tk.Frame(inner_frame, bg=colors['bg_card'])
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Progress bar (custom styling with indeterminate support)
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, 
                                     maximum=100, style="Custom.Horizontal.TProgressbar")
        progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Progress text with animation support
        progress_text = tk.Label(progress_frame, text="Pending...",
                                font=ModernStyle.FONTS['small'],
                                fg=colors['text_secondary'],
                                bg=colors['bg_card'],
                                anchor="w")
        progress_text.pack(anchor=tk.W, fill=tk.X)
        
        # Bottom row: Status and metadata
        bottom_row = tk.Frame(inner_frame, bg=colors['bg_card'])
        bottom_row.pack(fill=tk.X)
        
        # Status
        status_label = tk.Label(bottom_row, text=f"Status: {video_item.status}",
                               font=ModernStyle.FONTS['small'],
                               fg=colors['text_primary'],
                               bg=colors['bg_card'])
        status_label.pack(side=tk.LEFT)
        
        # Quality and time
        meta_label = tk.Label(bottom_row, text=f"Quality: {video_item.quality} • Added: {video_item.added_time.strftime('%H:%M')}",
                             font=ModernStyle.FONTS['small'],
                             fg=colors['text_secondary'],
                             bg=colors['bg_card'])
        meta_label.pack(side=tk.RIGHT)
        
        # Error message row (initially hidden)
        error_frame = tk.Frame(inner_frame, bg=colors['bg_card'])
        if video_item.status == "error" and video_item.error_message:
            error_frame.pack(fill=tk.X, pady=(5, 0))
            error_icon = tk.Label(error_frame, text="⚠️", font=("Segoe UI", 10),
                                 bg=colors['bg_card'])
            error_icon.pack(side=tk.LEFT, padx=(0, 5))
            error_label = tk.Label(error_frame, text=video_item.error_message,
                                  font=ModernStyle.FONTS['small'],
                                  fg=colors['error'], 
                                  bg=colors['bg_card'],
                                  wraplength=500,
                                  anchor="w", justify="left")
            error_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
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
            'help_btn': help_btn,
            'error_frame': error_frame,
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
            
        if 'progress' in kwargs or 'progress_mode' in kwargs:
            progress_mode = getattr(video_item, 'progress_mode', 'determinate')
            progress_value = kwargs.get('progress', video_item.progress)
            
            if progress_mode == 'indeterminate':
                # Switch to indeterminate mode for unknown total
                widget['progress_bar'].config(mode='indeterminate')
                widget['progress_bar'].start(10)  # Animate every 10ms
                widget['progress_text'].config(text="🔄 Downloading... (size unknown)")
            else:
                # Determinate mode with percentage
                widget['progress_bar'].config(mode='determinate')
                widget['progress_bar'].stop()
                
                # Smooth progress animation
                try:
                    current_progress = widget['progress_var'].get()
                    if abs(progress_value - current_progress) > 1:  # Only animate significant changes
                        UIAnimations.slide_in_progress(widget['progress_bar'], progress_value)
                    else:
                        widget['progress_var'].set(progress_value)
                except:
                    widget['progress_var'].set(progress_value)
                
                # Update progress text with details
                if 'speed' in kwargs and 'eta' in kwargs:
                    speed_mb = kwargs.get('speed', 0) / 1024 / 1024 if kwargs.get('speed') else 0
                    eta = kwargs.get('eta', 0) or 0
                    if speed_mb > 0 and eta > 0:
                        widget['progress_text'].config(text=f"📥 {progress_value:.1f}% • {speed_mb:.1f} MB/s • ETA: {eta}s")
                    elif progress_value > 0:
                        widget['progress_text'].config(text=f"📥 {progress_value:.1f}% • Processing...")
                    else:
                        widget['progress_text'].config(text="📥 Starting download...")
                elif progress_value > 0:
                    widget['progress_text'].config(text=f"📥 {progress_value:.1f}% complete")
            
        if 'status' in kwargs:
            widget['status_label'].config(text=f"Status: {kwargs['status']}")
            
            # Show/hide error message
            if kwargs['status'] == "error" and hasattr(video_item, 'error_message') and video_item.error_message:
                # Show error message
                for child in widget['error_frame'].winfo_children():
                    child.destroy()
                    
                error_icon = tk.Label(widget['error_frame'], text="⚠️", font=("Segoe UI", 10),
                                     bg=self.app.current_colors['bg_card'])
                error_icon.pack(side=tk.LEFT, padx=(0, 5))
                error_label = tk.Label(widget['error_frame'], text=video_item.error_message,
                                      font=ModernStyle.FONTS['small'],
                                      fg=self.app.current_colors['error'], 
                                      bg=self.app.current_colors['bg_card'],
                                      wraplength=500, anchor="w", justify="left")
                error_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
                widget['error_frame'].pack(fill=tk.X, pady=(5, 0))
            else:
                # Hide error message
                widget['error_frame'].pack_forget()
            
            # Update button states based on status
            status = kwargs['status']
            if status == "downloading":
                widget['pause_btn'].config(state="normal", text="⏸️")
                widget['cancel_btn'].config(state="normal")
                widget['retry_btn'].config(state="disabled")
                widget['help_btn'].config(state="disabled")
            elif status == "paused":
                widget['pause_btn'].config(state="normal", text="▶️")
                widget['cancel_btn'].config(state="normal")
                widget['retry_btn'].config(state="normal")
                widget['help_btn'].config(state="disabled")
            elif status == "error":
                widget['pause_btn'].config(state="disabled")
                widget['cancel_btn'].config(state="disabled") 
                widget['retry_btn'].config(state="normal")
                widget['help_btn'].config(state="normal")
            elif status in ["completed", "cancelled"]:
                widget['pause_btn'].config(state="disabled")
                widget['cancel_btn'].config(state="disabled") 
                widget['retry_btn'].config(state="disabled" if status == "completed" else "normal")
                widget['help_btn'].config(state="disabled")
            else:  # pending, analyzing
                widget['pause_btn'].config(state="disabled")
                widget['cancel_btn'].config(state="normal")
                widget['retry_btn'].config(state="disabled")
                widget['help_btn'].config(state="disabled")
                
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
        
    def show_help(self, video_id):
        """Show help for video error"""
        if video_id in self.video_widgets:
            video_item = self.video_widgets[video_id]['video_item']
            if video_item.status == "error" and video_item.error_message:
                # Detect platform from URL
                platform = ""
                if 'tiktok.com' in video_item.url:
                    platform = "tiktok"
                elif 'instagram.com' in video_item.url:
                    platform = "instagram"
                elif 'facebook.com' in video_item.url or 'fb.watch' in video_item.url:
                    platform = "facebook"
                elif 'youtube.com' in video_item.url or 'youtu.be' in video_item.url:
                    platform = "youtube"
                
                TroubleshootingHelper.show_help_dialog(self.app.root, video_item.error_message, platform)

class ModernVideoDownloader:
    """Modern video downloader with advanced UI"""
    
    def __init__(self, root):
        self.root = root
        self.video_queue = {}  # video_id -> VideoItem
        self.download_threads = {}  # video_id -> thread
        self.is_dark_theme = False
        self.current_colors = ModernStyle.get_colors(False)
        self.download_path = ""
        self.batch_summary = {
            'total': 0,
            'completed': 0,
            'failed': 0,
            'errors': []
        }
        
        self.setup_ui()
        self.setup_download_folder()
        self.apply_modern_styles()
        
        # Initialize error logger after download folder is set
        self.error_logger = ErrorLogger(self.download_path)
        
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
        self.header_frame = tk.Frame(self.main_container, height=80, 
                                    bg=self.current_colors['primary'])
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        # Header content
        self.header_content = tk.Frame(self.header_frame, bg=self.current_colors['primary'])
        self.header_content.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        # Title
        self.title_label = tk.Label(self.header_content, text="🎬 CZ Video Downloader", 
                              font=ModernStyle.FONTS['title'],
                              bg=self.current_colors['primary'],
                              fg="white")
        self.title_label.pack(side=tk.LEFT)
        
        # Header buttons
        self.btn_frame = tk.Frame(self.header_content, bg=self.current_colors['primary'])
        self.btn_frame.pack(side=tk.RIGHT)
        
        # Theme toggle
        self.theme_btn = tk.Button(self.btn_frame, text="🌙", font=("Segoe UI", 12),
                                  command=self.toggle_theme, width=3,
                                  bg=self.current_colors['primary_dark'],
                                  fg="white", border=0, cursor="hand2")
        self.theme_btn.pack(side=tk.RIGHT, padx=5)
        
        # About button
        self.about_btn = tk.Button(self.btn_frame, text="ℹ️", font=("Segoe UI", 12),
                             command=self.show_about, width=3,
                             bg=self.current_colors['primary_dark'],
                             fg="white", border=0, cursor="hand2")
        self.about_btn.pack(side=tk.RIGHT, padx=5)
        
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
        self.style = ttk.Style()
        
        # Set theme based on current mode
        if self.is_dark_theme:
            self.style.theme_use('clam')
        else:
            self.style.theme_use('clam')
        
        self.update_widget_styles()
        
    def update_widget_styles(self):
        """Update all widget styles with current theme"""
        colors = self.current_colors
        
        # Configure ttk styles
        self.style.configure("Custom.Horizontal.TProgressbar",
                           background=colors['primary'],
                           troughcolor=colors['bg_tertiary'],
                           borderwidth=0,
                           lightcolor=colors['primary'],
                           darkcolor=colors['primary'])
        
        # Configure notebook style
        self.style.configure("TNotebook",
                           background=colors['bg_secondary'],
                           borderwidth=0)
        
        self.style.configure("TNotebook.Tab",
                           padding=[20, 10],
                           font=ModernStyle.FONTS['body'],
                           background=colors['bg_tertiary'],
                           foreground=colors['text_primary'])
        
        self.style.map("TNotebook.Tab",
                      background=[('selected', colors['bg_primary']),
                                ('active', colors['hover'])])
        
        # Configure frame styles
        self.style.configure("TFrame",
                           background=colors['bg_primary'])
        
        self.style.configure("VideoCard.TFrame",
                           background=colors['bg_card'],
                           relief="solid",
                           borderwidth=1)
        
        # Configure label styles
        self.style.configure("TLabel",
                           background=colors['bg_primary'],
                           foreground=colors['text_primary'])
        
        self.style.configure("Title.TLabel",
                           font=ModernStyle.FONTS['heading'],
                           foreground=colors['text_primary'],
                           background=colors['bg_primary'])
        
        # Configure entry styles
        self.style.configure("TEntry",
                           fieldbackground=colors['bg_primary'],
                           foreground=colors['text_primary'],
                           insertcolor=colors['text_primary'])
        
        # Configure button styles
        self.style.configure("TButton",
                           background=colors['bg_tertiary'],
                           foreground=colors['text_primary'],
                           font=ModernStyle.FONTS['body'])
        
        self.style.map("TButton",
                      background=[('active', colors['hover']),
                                ('pressed', colors['border'])])
        
        # Configure combobox styles
        self.style.configure("TCombobox",
                           fieldbackground=colors['bg_primary'],
                           foreground=colors['text_primary'])
        
        # Configure labelframe styles
        self.style.configure("TLabelframe",
                           background=colors['bg_primary'],
                           foreground=colors['text_primary'])
        
        self.style.configure("TLabelframe.Label",
                           background=colors['bg_primary'],
                           foreground=colors['text_primary'],
                           font=ModernStyle.FONTS['body'])
        
        # Update main container background
        # Note: ttk.Frame doesn't support bg, handled by style configure above
                       
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
            
            # Special handling for TikTok
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            # Platform-specific configurations
            if 'tiktok.com' in video_item.url:
                ydl_opts.update({
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-us,en;q=0.5',
                        'Accept-Encoding': 'gzip,deflate',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                        'Keep-Alive': '300',
                        'Connection': 'keep-alive',
                    },
                    'cookiefile': None,
                    'cookiesfrombrowser': None,
                })
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
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
                                               
                except yt_dlp.DownloadError as e:
                    error_msg = str(e)
                    video_item.status = "error"
                    
                    # Provide specific error messages for common issues
                    if "Private video" in error_msg:
                        video_item.error_message = "Video is private or unavailable"
                    elif "Video unavailable" in error_msg:
                        video_item.error_message = "Video not found or region blocked"
                    elif "Sign in to confirm your age" in error_msg:
                        video_item.error_message = "Age-restricted video"
                    elif "This video is not available" in error_msg:
                        video_item.error_message = "Video removed or restricted"
                    elif "tiktok" in video_item.url.lower() and "403" in error_msg:
                        video_item.error_message = "TikTok access blocked - try different URL format"
                    else:
                        video_item.error_message = f"Analysis failed: {error_msg[:100]}"
                    
                    self.video_list.update_video(video_item.id, status="error")
                    
        except ImportError:
            video_item.status = "error"
            video_item.error_message = "yt-dlp not installed"
            self.video_list.update_video(video_item.id, status="error")
        except Exception as e:
            video_item.status = "error"
            video_item.error_message = f"Unexpected error: {str(e)[:100]}"
            self.video_list.update_video(video_item.id, status="error")
            
    def start_batch_download(self):
        """Start downloading all pending videos"""
        pending_videos = [v for v in self.video_queue.values() if v.status == "pending"]
        
        if not pending_videos:
            messagebox.showinfo("Info", "No videos to download!")
            return
            
        # Reset batch summary
        self.batch_summary = {
            'total': len(pending_videos),
            'completed': 0,
            'failed': 0,
            'errors': [],
            'start_time': datetime.now()
        }
            
        max_concurrent = int(self.concurrent_var.get())
        
        for i, video in enumerate(pending_videos[:max_concurrent]):
            self.start_video_download(video.id)
            
        # Start monitoring thread for batch completion
        monitor_thread = threading.Thread(target=self.monitor_batch_completion)
        monitor_thread.daemon = True
        monitor_thread.start()
            
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
                    # Guard against None values (some extractors return None for total_bytes)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                    downloaded = d.get('downloaded_bytes') or 0
                    speed = d.get('speed', 0) or 0
                    eta = d.get('eta', 0) or 0

                    # Determine progress mode and calculate progress
                    if isinstance(total, (int, float)) and total > 0 and isinstance(downloaded, (int, float)):
                        # Determinate mode - we know total size
                        progress = (downloaded / total) * 100
                        progress = max(0.0, min(100.0, progress))  # Clamp progress
                        video_item.progress = progress
                        video_item.progress_mode = "determinate"
                        
                        # Update UI with determinate progress
                        self.video_list.update_video(video_item.id,
                                                   progress=progress,
                                                   progress_mode="determinate",
                                                   speed=speed,
                                                   eta=eta)
                    else:
                        # Indeterminate mode - unknown total size
                        video_item.progress_mode = "indeterminate"
                        
                        # Update UI with indeterminate progress and speed info
                        self.video_list.update_video(video_item.id,
                                                   progress_mode="indeterminate",
                                                   speed=speed,
                                                   eta=eta)

                    video_item.speed = speed
                    video_item.eta = eta
                        
                elif d['status'] == 'finished':
                    video_item.status = "completed"
                    video_item.progress = 100
                    video_item.filename = os.path.basename(d['filename'])
                    
                    self.video_list.update_video(video_item.id,
                                               status="completed",
                                               progress=100)
                    
                    # Update batch summary
                    self.batch_summary['completed'] += 1
                    
            # Enhanced yt-dlp options
            ydl_opts = {
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'format': self.get_format_selector(video_item.quality),
                'noplaylist': True,
                'extract_flat': False,
                'writeinfojson': False,
                'writethumbnail': False,
                'ignoreerrors': False,
                'retries': 3,
                'fragment_retries': 3,
                'timeout': 30,
            }
            
            # Platform-specific configurations
            if 'tiktok.com' in video_item.url:
                ydl_opts.update({
                    'format': 'best[ext=mp4]/best',
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Referer': 'https://www.tiktok.com/',
                    },
                    'cookiefile': None,
                })
            elif 'instagram.com' in video_item.url:
                ydl_opts.update({
                    'format': 'best[ext=mp4]/best',
                })
            elif 'facebook.com' in video_item.url or 'fb.watch' in video_item.url:
                ydl_opts.update({
                    'format': 'best[ext=mp4]/best',
                })
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_item.url])
                
        except yt_dlp.DownloadError as e:
            error_msg = str(e)
            video_item.status = "error"
            detailed_traceback = traceback.format_exc()
            
            # Categorize errors for better user understanding
            if "HTTP Error 403" in error_msg:
                video_item.error_message = "Access denied - Video may be private or region-blocked"
            elif "HTTP Error 404" in error_msg:
                video_item.error_message = "Video not found - May have been deleted"
            elif "HTTP Error 429" in error_msg:
                video_item.error_message = "Rate limited - Too many requests, try again later"
            elif "Sign in to confirm your age" in error_msg:
                video_item.error_message = "Age-restricted content - Cannot download"
            elif "Private video" in error_msg:
                video_item.error_message = "Private video - Access denied"
            elif "Video unavailable" in error_msg:
                video_item.error_message = "Video unavailable - May be deleted or restricted"
            elif "tiktok" in video_item.url.lower():
                video_item.error_message = "TikTok download failed - Platform restrictions"
            else:
                video_item.error_message = f"Download failed: {error_msg[:100]}"
            
            # Log detailed error
            self.error_logger.log_download_error(video_item, error_msg, detailed_traceback)
            
            self.video_list.update_video(video_item.id, status="error")
            
            # Update batch summary
            self.batch_summary['failed'] += 1
            self.batch_summary['errors'].append({
                'title': video_item.title,
                'url': video_item.url[:50] + "...",
                'error': video_item.error_message
            })
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            video_item.status = "error"
            video_item.error_message = error_msg[:100]
            detailed_traceback = traceback.format_exc()
            
            # Log detailed error
            self.error_logger.log_download_error(video_item, error_msg, detailed_traceback)
            
            self.video_list.update_video(video_item.id, status="error")
            
            # Update batch summary
            self.batch_summary['failed'] += 1
            self.batch_summary['errors'].append({
                'title': video_item.title,
                'url': video_item.url[:50] + "...",
                'error': video_item.error_message
            })
            
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
        self.current_colors = ModernStyle.get_colors(self.is_dark_theme)
        self.theme_var.set("Dark" if self.is_dark_theme else "Light")
        self.apply_theme()
        
    def apply_theme(self):
        """Apply selected theme to entire UI"""
        self.is_dark_theme = (self.theme_var.get() == "Dark")
        self.current_colors = ModernStyle.get_colors(self.is_dark_theme)
        
        # Update theme button icon
        self.theme_btn.config(text="☀️" if self.is_dark_theme else "🌙")
        
        # Update header colors
        self.header_frame.config(bg=self.current_colors['primary'])
        self.header_content.config(bg=self.current_colors['primary'])
        self.title_label.config(bg=self.current_colors['primary'])
        self.btn_frame.config(bg=self.current_colors['primary'])
        self.theme_btn.config(bg=self.current_colors['primary_dark'])
        self.about_btn.config(bg=self.current_colors['primary_dark'])
        
        # Update main container
        # Note: ttk.Frame doesn't support bg, handled by style
        
        # Update widget styles
        self.update_widget_styles()
        
        # Update canvas in video list
        if hasattr(self.video_list, 'canvas'):
            self.video_list.canvas.config(bg=self.current_colors['bg_secondary'])
            
        # Force refresh all video widgets
        self.refresh_video_widgets()
        
        # Update root background
        self.root.config(bg=self.current_colors['bg_secondary'])
        
    def refresh_video_widgets(self):
        """Refresh all video widgets with new theme"""
        if hasattr(self, 'video_list') and hasattr(self.video_list, 'video_widgets'):
            for video_id, widget_data in self.video_list.video_widgets.items():
                # Update container background
                try:
                    container = widget_data['container']
                    # Force recreation of video widget with new theme
                    video_item = widget_data['video_item']
                    
                    # Remove old widget
                    container.destroy()
                    
                    # Create new widget with current theme
                    new_widget = self.video_list.create_video_widget(video_item)
                    self.video_list.video_widgets[video_id] = new_widget
                    
                except Exception as e:
                    print(f"Error refreshing widget {video_id}: {e}")
            
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
        
    def monitor_batch_completion(self):
        """Monitor batch download completion and show summary"""
        while True:
            time.sleep(2)  # Check every 2 seconds
            
            # Check if all downloads are completed
            active_statuses = ['analyzing', 'downloading', 'pending']
            active_videos = [v for v in self.video_queue.values() 
                           if v.status in active_statuses]
            
            if not active_videos and self.batch_summary['total'] > 0:
                # All downloads completed, show summary
                self.root.after(0, self.show_batch_summary)
                break
                
    def show_batch_summary(self):
        """Show batch download completion summary"""
        if self.batch_summary['total'] == 0:
            return
            
        # Calculate statistics
        total = self.batch_summary['total']
        completed = self.batch_summary['completed']
        failed = self.batch_summary['failed']
        success_rate = (completed / total * 100) if total > 0 else 0
        
        # Calculate duration
        if 'start_time' in self.batch_summary:
            duration = datetime.now() - self.batch_summary['start_time']
            duration_str = str(duration).split('.')[0]  # Remove microseconds
        else:
            duration_str = "Unknown"
        
        # Log batch summary to file
        self.error_logger.log_batch_summary(self.batch_summary)
        
        # Create summary window with enhanced styling
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Batch Download Summary")
        summary_window.geometry("600x500")
        summary_window.resizable(True, True)
        summary_window.grab_set()
        
        # Center window
        summary_window.update_idletasks()
        x = (summary_window.winfo_screenwidth() // 2) - 300
        y = (summary_window.winfo_screenheight() // 2) - 250
        summary_window.geometry(f"600x500+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(summary_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="📊 Batch Download Complete!", 
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="📈 Statistics", padding="15")
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Stats grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)
        
        # Total
        ttk.Label(stats_grid, text="Total Videos:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(stats_grid, text=str(total), font=("Segoe UI", 10)).grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        # Completed
        ttk.Label(stats_grid, text="✅ Completed:", font=("Segoe UI", 10, "bold"), foreground="green").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        ttk.Label(stats_grid, text=str(completed), font=("Segoe UI", 10), foreground="green").grid(row=0, column=3, sticky=tk.W, padx=(0, 30))
        
        # Failed
        ttk.Label(stats_grid, text="❌ Failed:", font=("Segoe UI", 10, "bold"), foreground="red").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        ttk.Label(stats_grid, text=str(failed), font=("Segoe UI", 10), foreground="red").grid(row=1, column=1, sticky=tk.W, padx=(0, 30), pady=(5, 0))
        
        # Success rate
        ttk.Label(stats_grid, text="📊 Success Rate:", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        ttk.Label(stats_grid, text=f"{success_rate:.1f}%", font=("Segoe UI", 10)).grid(row=1, column=3, sticky=tk.W, pady=(5, 0))
        
        # Duration
        ttk.Label(stats_grid, text="⏱️ Duration:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        ttk.Label(stats_grid, text=duration_str, font=("Segoe UI", 10)).grid(row=2, column=1, sticky=tk.W, columnspan=3, pady=(5, 0))
        
        # Errors section (if any)
        if failed > 0 and self.batch_summary['errors']:
            errors_frame = ttk.LabelFrame(main_frame, text="❌ Error Details", padding="15")
            errors_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            
            # Create text widget with scrollbar for errors
            text_frame = ttk.Frame(errors_frame)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            error_text = tk.Text(text_frame, height=8, wrap=tk.WORD, font=("Consolas", 9))
            error_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=error_text.yview)
            error_text.configure(yscrollcommand=error_scrollbar.set)
            
            error_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            error_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate errors
            for i, error in enumerate(self.batch_summary['errors'], 1):
                error_text.insert(tk.END, f"{i}. {error['title']}\n")
                error_text.insert(tk.END, f"   URL: {error['url']}\n")
                error_text.insert(tk.END, f"   Error: {error['error']}\n\n")
            
            error_text.config(state=tk.DISABLED)
            
            # Troubleshooting tips
            tips_label = ttk.Label(errors_frame, 
                                 text="💡 Tips: Try different quality settings, check if videos are private/age-restricted, or retry later",
                                 font=("Segoe UI", 9), foreground="gray", wraplength=550)
            tips_label.pack(pady=(10, 0))
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Open folder button
        if completed > 0:
            open_folder_btn = ttk.Button(button_frame, text="📁 Open Download Folder", 
                                       command=lambda: os.startfile(self.download_path))
            open_folder_btn.pack(side=tk.LEFT)
        
        # View log button
        log_btn = ttk.Button(button_frame, text="📋 View Error Log", 
                           command=lambda: os.startfile(self.error_logger.get_log_file_path()))
        log_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Retry failed button
        if failed > 0:
            retry_btn = ttk.Button(button_frame, text="🔄 Retry Failed Downloads", 
                                 command=lambda: [summary_window.destroy(), self.retry_failed_downloads()])
            retry_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Close button
        close_btn = ttk.Button(button_frame, text="✅ Close", 
                             command=summary_window.destroy)
        close_btn.pack(side=tk.RIGHT)
        
        # Reset batch summary
        self.batch_summary = {'total': 0, 'completed': 0, 'failed': 0, 'errors': []}
        
    def retry_failed_downloads(self):
        """Retry all failed downloads"""
        failed_videos = [v for v in self.video_queue.values() if v.status == "error"]
        
        if not failed_videos:
            messagebox.showinfo("Info", "No failed downloads to retry!")
            return
            
        for video in failed_videos:
            video.status = "pending"
            video.progress = 0
            video.error_message = ""
            self.video_list.update_video(video.id, status="pending", progress=0)
            
        # Switch to queue tab and start downloads
        self.notebook.select(1)
        self.start_batch_download()

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