@echo off
REM Run script for SaveMyExams Scraper (Windows)
REM Automatically uses the virtual environment

if not exist "venv\" (
    echo Virtual environment not found!
    echo Run setup first: setup.bat
    exit /b 1
)

if not exist "venv\Scripts\playwright.exe" (
    echo Playwright not installed!
    echo Run setup first: setup.bat
    exit /b 1
)

echo Starting SaveMyExams Scraper...
echo.
venv\Scripts\python.exe savemyexams_scraper.py
