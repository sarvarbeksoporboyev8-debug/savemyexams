#!/bin/bash
# Run script for SaveMyExams Scraper
# Automatically uses the virtual environment

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run setup first: ./setup.sh"
    exit 1
fi

# Check if playwright is installed
if [ ! -f "venv/bin/playwright" ]; then
    echo "❌ Playwright not installed!"
    echo "Run setup first: ./setup.sh"
    exit 1
fi

# Run the scraper using the virtual environment's Python
echo "Starting SaveMyExams Scraper..."
echo ""
./venv/bin/python savemyexams_scraper.py
