#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CZ Video Downloader - Version Information
"""

# Application version
VERSION = "2.0.0"
BUILD_NUMBER = "2024.10.17"

# GitHub repository information
GITHUB_OWNER = "TRIBUI106"
GITHUB_REPO = "czDownloader"
GITHUB_FULL = f"{GITHUB_OWNER}/{GITHUB_REPO}"

# API URLs
GITHUB_API_RELEASES = f"https://api.github.com/repos/{GITHUB_FULL}/releases/latest"
GITHUB_REPO_URL = f"https://github.com/{GITHUB_FULL}"

# Application information
APP_NAME = "CZ Video Downloader"
APP_DESCRIPTION = "Modern video downloader with beautiful interface"
APP_AUTHOR = "CZ Team"
APP_LICENSE = "MIT"

# Version helpers
def get_version_string():
    """Get formatted version string"""
    return f"v{VERSION}"

def get_full_version_string():
    """Get full version string with build"""
    return f"v{VERSION} (Build {BUILD_NUMBER})"

def get_about_text():
    """Get complete about text"""
    return f"""🎬 {APP_NAME} {get_version_string()}

{APP_DESCRIPTION}

✨ Features:
• Multi-platform support (YouTube, Facebook, TikTok, Instagram)
• Multi-URL queue system
• Individual progress tracking  
• Dark/Light themes
• Batch downloads
• Modern UI with Material Design
• Auto-update system 🆕

🔧 Technical:
• Powered by yt-dlp
• Auto-dependency management
• Smart error handling
• GitHub integration

💝 Created with ❤️ by {APP_AUTHOR}
📅 Version: {get_full_version_string()}
🔗 GitHub: {GITHUB_REPO_URL}
📄 License: {APP_LICENSE}"""