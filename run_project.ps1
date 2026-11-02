# HealthPulse - Hospital & Patient Analysis Launcher for PowerShell
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "          HealthPulse: Hospital & Patient Analysis System            " -ForegroundColor White
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] ERROR: Python is not detected in your system PATH." -ForegroundColor Red
    Write-Host "[*] Please install Python 3.9+ from https://python.org and add it to PATH." -ForegroundColor Yellow
    Read-Host "Press Enter to exit..."
    exit
}

Write-Host "[*] Detected $pythonVersion" -ForegroundColor Green
Write-Host "[*] Launching Streamlit Clinical Dashboard at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "[*] Opening in your default web browser..." -ForegroundColor Yellow
Write-Host ""
Write-Host "[!] Press CTRL+C to stop the dashboard server." -ForegroundColor Gray
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

python -m streamlit run app.py --server.port=8501 --server.headless=false
