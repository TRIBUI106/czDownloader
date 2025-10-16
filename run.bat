@echo off
echo ==========================================
echo      CZ Video Downloader - Launcher
echo ==========================================
echo.

REM Check if dependencies are installed
python -c "import yt_dlp, requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo Dependencies not found. Running setup first...
    echo.
    call setup.bat
    if %errorlevel% neq 0 (
        echo Setup failed! Please check the errors above.
        pause
        exit /b 1
    )
    echo.
)

echo Starting CZ Video Downloader...
python main.py

if %errorlevel% neq 0 (
    echo.
    echo Application encountered an error!
    pause
)