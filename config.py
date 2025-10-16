# CZ Video Downloader - Configuration
# Cấu hình cho ứng dụng

import os
from pathlib import Path

# App Settings
APP_NAME = "CZ Video Downloader"
APP_VERSION = "1.0"
APP_AUTHOR = "CZ Team"

# Default Settings
DEFAULT_QUALITY = "best"
DEFAULT_DOWNLOAD_PATH = str(Path.home() / "Downloads" / "czDownloader")

# Supported Platforms
SUPPORTED_PLATFORMS = {
    'youtube.com': 'YouTube',
    'youtu.be': 'YouTube',
    'facebook.com': 'Facebook', 
    'fb.watch': 'Facebook',
    'tiktok.com': 'TikTok',
    'instagram.com': 'Instagram',
    'twitter.com': 'Twitter/X',
    'x.com': 'Twitter/X'
}

# Quality Options
QUALITY_OPTIONS = [
    ("Best Available", "best"),
    ("1080p (Full HD)", "best[height<=1080]"),
    ("720p (HD)", "best[height<=720]"),
    ("480p (SD)", "best[height<=480]"),
    ("360p (Low)", "best[height<=360]"),
    ("Worst Available", "worst")
]

# File Extensions
SUPPORTED_FORMATS = ['mp4', 'mkv', 'webm', 'avi', 'flv']

# Download Settings
MAX_CONCURRENT_DOWNLOADS = 3
TIMEOUT_SECONDS = 60
RETRY_ATTEMPTS = 3

# UI Settings
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
MIN_WIDTH = 600
MIN_HEIGHT = 400

# Colors
COLORS = {
    'primary': '#3498db',
    'success': '#27ae60', 
    'error': '#e74c3c',
    'warning': '#f39c12',
    'info': '#17a2b8',
    'dark': '#2c3e50',
    'light': '#ecf0f1'
}

# User Agent for requests
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'