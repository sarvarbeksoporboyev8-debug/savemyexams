# SaveMyExams Scraper

Scrapes exam questions and answers from savemyexams.co.uk using Playwright browser automation.

## Features

- ✅ **Playwright-based scraping** - Real browser automation with JavaScript rendering
- ✅ **Anti-bot measures** - Realistic user behavior, random delays, stealth scripts
- ✅ **Image extraction** - Downloads all question figures/diagrams automatically
- ✅ **Smart naming** - Images named with question IDs for easy matching
- ✅ **JSON output** - Structured data with metadata and image references
- ✅ **Configurable** - Easy-to-adjust scraping limits

## Quick Start

### Option 1: Simple (Works on all platforms)

```bash
# 1. Run setup (one time only)
./setup.sh        # Linux/Mac
setup.bat         # Windows

# 2. Run the scraper
python scrape.py  # Works on all platforms!
```

### Option 2: Shell scripts

**Linux/Mac:**
```bash
./setup.sh  # One time setup
./run.sh    # Run scraper
```

**Windows:**
```cmd
setup.bat   # One time setup
run.bat     # Run scraper
```

### Manual Setup

If the scripts don't work, you can set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run the scraper
python savemyexams_scraper.py
```

## Output

After running, you'll get:

1. **`savemyexams_questions.json`** - All scraped questions with metadata
2. **`images/`** - Folder containing all question figures/diagrams

### Image Naming

Images are named: `{question_id}_fig{N}.{ext}`

**Example:**
```
Question ID: gcse_biology_aqa_18_topic-questions_1-cell-biology_1-1-cell-structure_exam-questions_2
Image file:  gcse_biology_aqa_18_topic-questions_1-cell-biology_1-1-cell-structure_exam-questions_2_fig1.png
```

This makes it easy to match images to questions - the filename starts with the question ID.

## Configuration

Edit these constants in `savemyexams_scraper.py`:

```python
# Scraping scope
DEFAULT_MAX_SUBJECTS = 1              # Number of subjects to scrape
DEFAULT_MAX_TOPICS_PER_SUBJECT = 2    # Topics per subject
DEFAULT_MAX_QUESTIONS_PER_TOPIC = 2   # Question pages per topic

# Browser settings
HEADLESS_MODE = True                  # Set False to see browser in action

# Image settings
DOWNLOAD_IMAGES = True                # Set False to skip image downloads
```

## Helper Script

View and analyze scraped data:

```bash
# Show statistics
python view_questions.py --stats

# List questions with images
python view_questions.py --list-images

# View specific question
python view_questions.py --question-id "gcse_biology_..."

# Show all options
python view_questions.py --help
```

## JSON Structure

```json
{
  "metadata": {
    "source": "savemyexams.co.uk",
    "total_questions": 189,
    "questions_with_images": 57,
    "total_images": 62,
    "images_folder": "images",
    "scrape_date": "2026-01-11 05:24:21"
  },
  "questions": [
    {
      "id": "gcse_biology_..._2",
      "source_url": "https://www.savemyexams.co.uk/...",
      "question_number": 2,
      "question_text": "Figure 1 shows an image of a plant cell...",
      "question_html": "<div>...</div>",
      "answer": "P = Cell wall, Q = Nucleus, R = Chloroplast",
      "answer_html": "<div>...</div>",
      "marks": 3,
      "difficulty": null,
      "topic": "Cell Structure(AQA GCSE Biology)",
      "images": ["gcse_biology_..._2_fig1.png"]
    }
  ]
}
```

## Requirements

- Python 3.8 or higher
- Internet connection
- ~300MB disk space for Playwright browser

## Troubleshooting

### "No module named playwright"

Make sure you're using the virtual environment:

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# Then run
python savemyexams_scraper.py
```

Or use the run scripts:
- Linux/Mac: `./run.sh`
- Windows: `run.bat`

### "playwright: command not found"

Run the setup script again:
```bash
./setup.sh  # Linux/Mac
setup.bat   # Windows
```

### Virtual environment issues

Delete the `venv` folder and run setup again:
```bash
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

./setup.sh  # Linux/Mac
setup.bat   # Windows
```

## Files

- `savemyexams_scraper.py` - Main scraper script
- `view_questions.py` - Helper script to view scraped data
- `requirements.txt` - Python dependencies
- `setup.sh` / `setup.bat` - Setup scripts
- `run.sh` / `run.bat` - Run scripts
- `README.md` - This file

## Notes

- The scraper uses realistic delays to avoid being blocked
- Images are downloaded asynchronously for better performance
- All data is saved locally - no external database required
- The scraper respects the website's structure and doesn't overload servers

## License

For educational purposes only. Respect the website's terms of service.
