#!/bin/bash
# Setup script for SaveMyExams Scraper

echo "=========================================="
echo "SaveMyExams Scraper - Setup"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "Install python3-venv: sudo apt-get install python3-venv"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "Installing Python packages..."
./venv/bin/pip install -q --upgrade pip
./venv/bin/pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python packages"
    exit 1
fi
echo "✅ Python packages installed"

echo ""
echo "Installing Playwright browsers..."
./venv/bin/playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Playwright browsers"
    exit 1
fi
echo "✅ Playwright browsers installed"

echo ""
echo "=========================================="
echo "Setup complete! ✅"
echo "=========================================="
echo ""
echo "To run the scraper:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python savemyexams_scraper.py"
echo ""
