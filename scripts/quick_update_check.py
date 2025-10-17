#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Update Check for CZ Video Downloader
"""

def check_updates():
    """Quick check for updates - notification only"""
    try:
        import requests
        try:
            from scripts.version import VERSION
        except ImportError:
            VERSION = "2.0.0"

        print("🔍 Checking for updates...")
        response = requests.get(
            "https://api.github.com/repos/TRIBUI106/czDownloader/releases/latest",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            latest = data.get("tag_name", "").replace("v", "")

            if latest and latest != VERSION:
                print(f"🆕 New version v{latest} available! (current: v{VERSION})")
                print("💡 Use the 🔄 button in the app to update")
            else:
                print("✅ You have the latest version!")
        else:
            print("⚠️  Could not check for updates")

    except ImportError:
        print("⚠️  Requests module not available - skipping update check")
    except Exception as e:
        print(f"⚠️  Update check failed: {e}")

if __name__ == "__main__":
    check_updates()