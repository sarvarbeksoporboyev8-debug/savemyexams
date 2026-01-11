@echo off
REM Setup script for SaveMyExams Scraper (Windows)

echo ==========================================
echo SaveMyExams Scraper - Setup
echo ==========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        echo Make sure Python 3.8+ is installed
        exit /b 1
    )
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo.
echo Installing Python packages...
venv\Scripts\pip.exe install -q --upgrade pip
venv\Scripts\pip.exe install -q -r requirements.txt

if errorlevel 1 (
    echo Failed to install Python packages
    exit /b 1
)
echo Python packages installed

echo.
echo Installing Playwright browsers...
venv\Scripts\playwright.exe install chromium

if errorlevel 1 (
    echo Failed to install Playwright browsers
    exit /b 1
)
echo Playwright browsers installed

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo To run the scraper:
echo   run.bat
echo.
echo Or manually:
echo   venv\Scripts\activate
echo   python savemyexams_scraper.py
echo.
