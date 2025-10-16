@echo off
echo ==========================================
echo      CZ Video Downloader v2.0 - Launcher
echo ==========================================
echo.

REM Check if dependencies are installed for v2
python -c "import yt_dlp, requests, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Dependencies not found. Running smart installer...
    echo.
    python launcher_v2.py
) else (
    echo Starting CZ Video Downloader v2.0...
    python main_v2.py
)

if %errorlevel% neq 0 (
    echo.
    echo Application encountered an error!
    echo Trying fallback to v1...
    python main.py
    if %errorlevel% neq 0 (
        echo.
        echo Both versions failed. Please check Python installation.
        echo Download Python from: https://python.org
    )
    pause
)