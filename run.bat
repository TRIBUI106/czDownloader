@echo off
echo ==========================================
echo     CZ Video Downloader v2.0 - Fixed Theme
echo ==========================================
echo.

echo [Theme Test] Testing theme system first...
python theme_test.py

if %errorlevel% neq 0 (
    echo Theme test failed - checking main app...
)

echo.
echo [Main App] Launching CZ Video Downloader v2.0...
echo.

REM Try to run main.py
python main.py

if %errorlevel% neq 0 (
    echo.
    echo Main app failed, trying fallback launcher...
    python launcher.py
    
    if %errorlevel% neq 0 (
        echo.
        echo All attempts failed. Checking Python...
        python --version
        if %errorlevel% neq 0 (
            echo.
            echo Python not found or not in PATH!
            echo Please install Python from https://python.org
            echo Make sure to check "Add Python to PATH"
        )
    )
)

echo.
echo Press any key to exit...
pause >nul