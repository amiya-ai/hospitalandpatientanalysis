@echo off
title HealthPulse - Hospital and Patient Analytics
color 0B
echo =====================================================================
echo           HealthPulse: Hospital & Patient Analysis System
echo =====================================================================
echo.
echo [*] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Python is not detected in your system PATH.
    echo [*] Please install Python 3.9+ from https://python.org and add it to PATH.
    echo.
    pause
    exit /b
)

echo [*] Python verified successfully.
echo [*] Launching Streamlit Clinical Dashboard at: http://localhost:8501
echo [*] Your default browser will open automatically...
echo.
echo [!] Press CTRL+C at any time in this window to stop the server.
echo =====================================================================
echo.

python -m streamlit run app.py --server.port=8501 --server.headless=false

pause
