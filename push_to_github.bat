@echo off
title Push Project to GitHub (amiya2005)
color 0A
echo =====================================================================
echo           HealthPulse: 1-Click Push to GitHub
echo =====================================================================
echo.
echo [*] Target Repository:
echo     https://github.com/amiya2005/hospital-and-patient-analysis
echo.
echo [!] Note: Agar aapne abhi tak repo create nahi ki hai, toh pehle:
echo     https://github.com/new?name=hospital-and-patient-analysis
echo     par jakar green 'Create repository' button daba dijiye.
echo.
echo [*] Pushing files to GitHub...
echo =====================================================================
echo.

git branch -M main
git remote remove origin >nul 2>&1
git remote add origin https://github.com/amiya2005/hospital-and-patient-analysis.git

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo =====================================================================
    echo [SUCCESS] Mubarak ho! Pura project GitHub par live ho gaya hai!
    echo.
    echo Aapka GitHub Link:
    echo https://github.com/amiya2005/hospital-and-patient-analysis
    echo =====================================================================
) else (
    echo.
    echo =====================================================================
    echo [!] Push karne ke liye:
    echo 1. Ensure karein: https://github.com/new?name=hospital-and-patient-analysis par repo bani hui hai.
    echo 2. Agar browser window khule, toh bas 'Authorize' / 'Sign in' par click karein.
    echo =====================================================================
)

echo.
pause
