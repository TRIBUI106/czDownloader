@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo     🎬 CZ Video Downloader v2.0
echo ==========================================
echo.

REM Check Python installation first
echo [1/4] 🐍 Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo.
    echo 📋 Please install Python from https://python.org
    echo 💡 Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo ✅ Python %PYTHON_VERSION% found

echo.
echo [2/4] 📦 Checking dependencies...

REM Create temp Python script for dependency check
echo import sys > temp_setup.py
echo import subprocess >> temp_setup.py
echo import importlib.util >> temp_setup.py
echo. >> temp_setup.py
echo def check_module(module_name): >> temp_setup.py
echo     try: >> temp_setup.py
echo         spec = importlib.util.find_spec(module_name) >> temp_setup.py
echo         return spec is not None >> temp_setup.py
echo     except: >> temp_setup.py
echo         return False >> temp_setup.py
echo. >> temp_setup.py
echo def install_package(package_name): >> temp_setup.py
echo     try: >> temp_setup.py
echo         cmd = [sys.executable, '-m', 'pip', 'install', package_name, '--upgrade', '--quiet'] >> temp_setup.py
echo         result = subprocess.run(cmd, capture_output=True, text=True, timeout=120) >> temp_setup.py
echo         return result.returncode == 0 >> temp_setup.py
echo     except: >> temp_setup.py
echo         return False >> temp_setup.py
echo. >> temp_setup.py
echo def check_ffmpeg(): >> temp_setup.py
echo     try: >> temp_setup.py
echo         result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5) >> temp_setup.py
echo         return result.returncode == 0 >> temp_setup.py
echo     except: >> temp_setup.py
echo         return False >> temp_setup.py
echo. >> temp_setup.py
echo packages = {'yt_dlp': 'yt-dlp', 'requests': 'requests', 'PIL': 'pillow'} >> temp_setup.py
echo missing = [] >> temp_setup.py
echo for module_name, package_name in packages.items(): >> temp_setup.py
echo     if check_module(module_name): >> temp_setup.py
echo         print(f'✅ {package_name} - OK') >> temp_setup.py
echo     else: >> temp_setup.py
echo         print(f'❌ {package_name} - Missing') >> temp_setup.py
echo         missing.append(package_name) >> temp_setup.py
echo. >> temp_setup.py
echo if missing: >> temp_setup.py
echo     print(f'📦 Installing {len(missing)} packages...') >> temp_setup.py
echo     all_success = True >> temp_setup.py
echo     for pkg in missing: >> temp_setup.py
echo         print(f'  Installing {pkg}...', end='') >> temp_setup.py
echo         if install_package(pkg): >> temp_setup.py
echo             print(' ✅') >> temp_setup.py
echo         else: >> temp_setup.py
echo             print(' ❌') >> temp_setup.py
echo             all_success = False >> temp_setup.py
echo     if not all_success: >> temp_setup.py
echo         print('❌ Some packages failed to install') >> temp_setup.py
echo         sys.exit(1) >> temp_setup.py
echo     else: >> temp_setup.py
echo         print('✅ All packages installed!') >> temp_setup.py
echo. >> temp_setup.py
echo print('🎬 Checking FFmpeg...') >> temp_setup.py
echo if check_ffmpeg(): >> temp_setup.py
echo     print('✅ FFmpeg - Available') >> temp_setup.py
echo else: >> temp_setup.py
echo     print('⚠️  FFmpeg - Not in PATH') >> temp_setup.py
echo     print('  Installing ffmpeg-python package...') >> temp_setup.py
echo     if install_package('ffmpeg-python'): >> temp_setup.py
echo         print('✅ ffmpeg-python installed') >> temp_setup.py
echo     else: >> temp_setup.py
echo         print('⚠️  FFmpeg setup incomplete') >> temp_setup.py
echo print('🎯 Setup check completed!') >> temp_setup.py

REM Run the setup check
python temp_setup.py
set SETUP_ERROR=%errorlevel%

REM Clean up temp file
del temp_setup.py >nul 2>&1

REM Check if setup failed
if %SETUP_ERROR% neq 0 (
    echo.
    echo ❌ Setup check failed!
    echo 💡 Try running as Administrator or install packages manually:
    echo    pip install yt-dlp requests pillow ffmpeg-python
    echo.
    pause
    exit /b 1
)

if %errorlevel% neq 0 (
    echo.
    echo ❌ Setup check failed!
    echo 💡 Try running as Administrator or install packages manually:
    echo    pip install yt-dlp requests pillow ffmpeg-python
    echo.
    pause
    exit /b 1
)

echo.
echo [3/4] 🎨 Testing theme system...

REM Create temp theme test script
echo import tkinter as tk > temp_theme.py
echo import threading >> temp_theme.py
echo import time >> temp_theme.py
echo. >> temp_theme.py
echo def theme_test(): >> temp_theme.py
echo     try: >> temp_theme.py
echo         print('✅ Theme test window created!') >> temp_theme.py
echo         root = tk.Tk() >> temp_theme.py
echo         root.title('Theme Test') >> temp_theme.py
echo         root.geometry('300x200') >> temp_theme.py
echo         root.update_idletasks() >> temp_theme.py
echo         x = (root.winfo_screenwidth() // 2) - 150 >> temp_theme.py
echo         y = (root.winfo_screenheight() // 2) - 100 >> temp_theme.py
echo         root.geometry(f'300x200+{x}+{y}') >> temp_theme.py
echo         label = tk.Label(root, text='🎨 Testing Themes...', font=('Segoe UI', 12)) >> temp_theme.py
echo         label.pack(expand=True) >> temp_theme.py
echo         def test_themes(): >> temp_theme.py
echo             time.sleep(0.5) >> temp_theme.py
echo             root.after(0, lambda: root.config(bg='#1e293b')) >> temp_theme.py
echo             root.after(0, lambda: label.config(bg='#1e293b', fg='#f1f5f9', text='🌙 Dark Mode')) >> temp_theme.py
echo             print('🌙 Switched to dark mode') >> temp_theme.py
echo             time.sleep(1) >> temp_theme.py
echo             root.after(0, lambda: root.config(bg='white')) >> temp_theme.py
echo             root.after(0, lambda: label.config(bg='white', fg='black', text='☀️ Light Mode')) >> temp_theme.py
echo             print('☀️ Switched to light mode') >> temp_theme.py
echo             time.sleep(1) >> temp_theme.py
echo             root.after(0, lambda: label.config(text='✅ Theme Test OK!')) >> temp_theme.py
echo             print('✅ Theme test completed!') >> temp_theme.py
echo             time.sleep(0.5) >> temp_theme.py
echo             root.after(0, root.destroy) >> temp_theme.py
echo         thread = threading.Thread(target=test_themes) >> temp_theme.py
echo         thread.daemon = True >> temp_theme.py
echo         thread.start() >> temp_theme.py
echo         root.after(3000, root.destroy) >> temp_theme.py
echo         root.mainloop() >> temp_theme.py
echo     except Exception as e: >> temp_theme.py
echo         print(f'⚠️  Theme test failed: {e}') >> temp_theme.py
echo. >> temp_theme.py
echo print('🎨 Starting theme test...') >> temp_theme.py
echo theme_test() >> temp_theme.py
echo print('🎯 Theme test finished!') >> temp_theme.py

REM Run theme test
python temp_theme.py

REM Clean up
del temp_theme.py >nul 2>&1

echo.
echo [4/4] 🚀 Launching CZ Video Downloader...
echo.

REM Create download folder if not exists
if not exist "%USERPROFILE%\Downloads\czDownloader" (
    mkdir "%USERPROFILE%\Downloads\czDownloader" >nul 2>&1
)

REM Launch main application
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Main app failed to start!
    echo.
    echo 🔍 Troubleshooting:
    echo 1. Check if main.py exists in current directory
    echo 2. Try running: python main.py
    echo 3. Check error messages above
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Application launched successfully!
echo 🎯 Closing launcher in 2 seconds...
timeout /t 2 >nul
exit