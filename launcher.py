#!/usr/bin/env python3
"""
CZ Video Downloader Launcher
Simple launcher with dependency check
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python():
    """Kiểm tra Python version"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7+ is required")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def install_package(package):
    """Cài đặt package nếu chưa có"""
    try:
        __import__(package.replace('-', '_'))
        print(f"✅ {package} is available")
        return True
    except ImportError:
        print(f"📦 Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False

def check_dependencies():
    """Kiểm tra và cài đặt dependencies"""
    print("Checking dependencies...")
    
    required_packages = ["yt-dlp", "requests"]
    
    for package in required_packages:
        if not install_package(package):
            print(f"❌ Could not install {package}")
            print("Please install manually with: pip install " + package)
            input("Press Enter to exit...")
            return False
    
    return True

def create_download_folder():
    """Tạo thư mục download"""
    downloads_path = Path.home() / "Downloads" / "czDownloader"
    downloads_path.mkdir(parents=True, exist_ok=True)
    print(f"📁 Download folder: {downloads_path}")

def main():
    print("=" * 50)
    print("🎬 CZ Video Downloader")
    print("=" * 50)
    
    # Kiểm tra Python
    check_python()
    
    # Kiểm tra dependencies
    if not check_dependencies():
        return
    
    # Tạo thư mục download
    create_download_folder()
    
    print("\n🚀 Starting application...")
    print("-" * 50)
    
    # Import và chạy app
    try:
        import tkinter as tk
        from main import VideoDownloader
        
        root = tk.Tk()
        app = VideoDownloader(root)
        root.mainloop()
        
    except ImportError as e:
        if "tkinter" in str(e):
            print("❌ Error: tkinter is not available")
            print("On Ubuntu/Debian: sudo apt-get install python3-tk")
            print("On CentOS/RHEL: sudo yum install tkinter")
        else:
            print(f"❌ Import error: {e}")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()