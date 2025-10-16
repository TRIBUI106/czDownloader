@echo off
echo ==========================================
echo     CZ Video Downloader v2.0 - Fixed Theme
echo ==========================================
echo.

echo [Theme Test] Testing theme system first...
C:/Users/chez1s/AppData/Local/Programs/Python/Python314/python.exe theme_test.py

if %errorlevel% neq 0 (
    echo Theme test failed - checking main app...
)

echo.
echo [Main App] Launching CZ Video Downloader v2.0...
echo.

REM Try to run main.py
C:/Users/chez1s/AppData/Local/Programs/Python/Python314/python.exe main.py

if %errorlevel% neq 0 (
    echo.
    echo Main app failed, trying fallback launcher...
    C:/Users/chez1s/AppData/Local/Programs/Python/Python314/python.exe launcher.py
    
    if %errorlevel% neq 0 (
        echo.
        echo All attempts failed. Checking Python...
        C:/Users/chez1s/AppData/Local/Programs/Python/Python314/python.exe --version
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