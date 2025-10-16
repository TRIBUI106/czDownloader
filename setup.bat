@echo off
echo ==========================================
echo    CZ Video Downloader - Setup Script
echo ==========================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/3] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo Try running as Administrator
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [3/3] Creating download folder...
if not exist "%USERPROFILE%\Downloads\czDownloader" (
    mkdir "%USERPROFILE%\Downloads\czDownloader"
)
echo ✓ Download folder created: %USERPROFILE%\Downloads\czDownloader

echo.
echo ==========================================
echo    Setup completed successfully!
echo ==========================================
echo.
echo To run the app: python main.py
echo Or double-click run.bat
echo.
pause