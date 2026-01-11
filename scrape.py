#!/usr/bin/env python3
"""
Simple wrapper script that automatically uses the virtual environment.
This way you can just run: python scrape.py
"""

import sys
import os
from pathlib import Path
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Check if venv exists
    venv_dir = script_dir / "venv"
    if not venv_dir.exists():
        print("❌ Virtual environment not found!")
        print("\nPlease run setup first:")
        print("  Linux/Mac: ./setup.sh")
        print("  Windows:   setup.bat")
        sys.exit(1)
    
    # Determine the Python executable in venv
    if os.name == 'nt':  # Windows
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:  # Linux/Mac
        python_exe = venv_dir / "bin" / "python"
    
    if not python_exe.exists():
        print("❌ Virtual environment Python not found!")
        print("\nPlease run setup first:")
        print("  Linux/Mac: ./setup.sh")
        print("  Windows:   setup.bat")
        sys.exit(1)
    
    # Run the scraper using the venv Python
    scraper_script = script_dir / "savemyexams_scraper.py"
    
    print("Starting SaveMyExams Scraper...")
    print(f"Using Python: {python_exe}")
    print("")
    
    try:
        result = subprocess.run(
            [str(python_exe), str(scraper_script)],
            cwd=str(script_dir)
        )
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
