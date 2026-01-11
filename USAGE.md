# SaveMyExams Scraper - Usage Guide

## Installation (One Time Only)

### Linux/Mac
```bash
./setup.sh
```

### Windows
```cmd
setup.bat
```

This will:
1. Create a virtual environment
2. Install all Python dependencies (playwright, beautifulsoup4, etc.)
3. Download Chromium browser for Playwright

## Running the Scraper

### Easiest Way (All Platforms)
```bash
python scrape.py
```

This automatically uses the virtual environment - no activation needed!

### Alternative Ways

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

**Manual (if you prefer):**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run scraper
python savemyexams_scraper.py
```

## What You Get

After running, you'll have:

### 1. JSON File: `savemyexams_questions.json`

Contains all scraped questions with:
- Question text
- Question HTML
- Answer text
- Answer HTML
- Marks
- Topic
- **List of image filenames**

### 2. Images Folder: `images/`

Contains all figures/diagrams from questions:
- Named with question IDs for easy matching
- Formats: PNG, JPG, SVG
- Example: `gcse_biology_aqa_18_topic-questions_1-cell-biology_1-1-cell-structure_exam-questions_2_fig1.png`

## Viewing Results

### Show Statistics
```bash
python view_questions.py --stats
```

Output:
```
Total questions: 189
Questions with images: 57
Total images: 62
Images folder: images
```

### List Questions with Images
```bash
python view_questions.py --list-images
```

### View Specific Question
```bash
python view_questions.py --question-id "gcse_biology_aqa_18_topic-questions_1-cell-biology_1-1-cell-structure_exam-questions_2"
```

## Configuration

Edit `savemyexams_scraper.py` to change:

```python
# How much to scrape
DEFAULT_MAX_SUBJECTS = 1              # Increase to scrape more subjects
DEFAULT_MAX_TOPICS_PER_SUBJECT = 2    # Increase to scrape more topics
DEFAULT_MAX_QUESTIONS_PER_TOPIC = 2   # Increase to scrape more questions

# Browser visibility
HEADLESS_MODE = True                  # Set False to watch the browser

# Image downloads
DOWNLOAD_IMAGES = True                # Set False to skip images
```

## Matching Images to Questions

Images are named with the question ID:

**Question in JSON:**
```json
{
  "id": "gcse_biology_aqa_18_topic-questions_1-cell-biology_1-1-cell-structure_exam-questions_2",
  "question_text": "Figure 1 shows an image of a plant cell...",
  "images": ["gcse_biology_aqa_18_topic-questions_1-cell-biology_1-1-cell-structure_exam-questions_2_fig1.png"]
}
```

**Image file:**
```
images/gcse_biology_aqa_18_topic-questions_1-cell-biology_1-1-cell-structure_exam-questions_2_fig1.png
```

The filename starts with the question ID, making it easy to match!

## Example Workflow

```bash
# 1. Setup (first time only)
./setup.sh

# 2. Run scraper
python scrape.py

# 3. View results
python view_questions.py --stats

# 4. Check images folder
ls images/

# 5. View specific question with images
python view_questions.py --list-images --limit 5
```

## Troubleshooting

### "No module named playwright"

You're not using the virtual environment. Use one of these:
- `python scrape.py` (easiest)
- `./run.sh` (Linux/Mac)
- `run.bat` (Windows)

### Setup fails

Make sure you have:
- Python 3.8 or higher: `python3 --version`
- Internet connection
- ~300MB free disk space

### Want to scrape more?

Edit the configuration in `savemyexams_scraper.py`:
```python
DEFAULT_MAX_SUBJECTS = 5              # Scrape 5 subjects
DEFAULT_MAX_TOPICS_PER_SUBJECT = 10   # 10 topics per subject
DEFAULT_MAX_QUESTIONS_PER_TOPIC = 5   # 5 question pages per topic
```

This will scrape: 5 × 10 × 5 = up to 250 question pages!

## Files Overview

| File | Purpose |
|------|---------|
| `savemyexams_scraper.py` | Main scraper (373 lines) |
| `scrape.py` | Simple wrapper - just run it! |
| `view_questions.py` | View and analyze scraped data |
| `setup.sh` / `setup.bat` | One-time setup |
| `run.sh` / `run.bat` | Run scraper |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `USAGE.md` | This file - quick usage guide |

## Tips

1. **Start small**: Test with default settings first (1 subject, 2 topics)
2. **Check output**: Use `view_questions.py --stats` to verify
3. **Scale up**: Increase limits in configuration once you're happy
4. **Be patient**: Scraping takes time due to realistic delays
5. **Images**: Check the `images/` folder to see all downloaded figures

## Need Help?

1. Check `README.md` for detailed documentation
2. Run `python view_questions.py --help` for viewer options
3. Look at the JSON file structure in `savemyexams_questions.json`
4. Check that images match questions by comparing IDs
