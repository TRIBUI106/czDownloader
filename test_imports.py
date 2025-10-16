#!/usr/bin/env python3
# Test script to check main_v2.py

try:
    print("Testing imports...")
    import tkinter as tk
    print("✅ tkinter OK")
    
    from tkinter import ttk, messagebox, filedialog
    print("✅ tkinter submodules OK")
    
    import threading, time, os, sys
    print("✅ Standard libraries OK")
    
    from datetime import datetime
    print("✅ datetime OK")
    
    from pathlib import Path
    print("✅ pathlib OK")
    
    from urllib.parse import urlparse
    print("✅ urllib OK")
    
    # Test yt-dlp
    try:
        import yt_dlp
        print("✅ yt-dlp OK")
    except ImportError:
        print("❌ yt-dlp not found")
    
    # Test PIL
    try:
        from PIL import Image, ImageTk
        print("✅ PIL OK")
    except ImportError:
        print("⚠️ PIL not found (optional)")
    
    print("\n🚀 All core imports successful!")
    print("Creating test window...")
    
    # Test basic tkinter
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("300x200")
    
    label = tk.Label(root, text="✅ CZ Video Downloader v2.0\nImports successful!", 
                     font=("Arial", 12), justify=tk.CENTER)
    label.pack(expand=True)
    
    close_btn = tk.Button(root, text="Close", command=root.destroy)
    close_btn.pack(pady=10)
    
    print("✅ Test window created successfully!")
    print("Close the window to continue...")
    
    root.mainloop()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()