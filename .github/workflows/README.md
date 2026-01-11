# GitHub Actions Workflow

## Scrape SaveMyExams

This workflow automatically scrapes questions from SaveMyExams and makes them available for download.

### How to Run

1. Go to the **Actions** tab in your GitHub repository
2. Click on **"Scrape SaveMyExams"** workflow
3. Click **"Run workflow"** button
4. Select the branch (usually `main`)
5. Click **"Run workflow"**

### What It Does

1. Sets up Python and installs dependencies
2. Installs Playwright browser (Chromium)
3. Runs the scraper with these settings:
   - **25 subjects**
   - **100 topics per subject**
   - **20 question pages per topic**
4. Creates artifacts for download

### Download Results

After the workflow completes (may take several hours):

1. Scroll to the bottom of the workflow run page
2. Find the **Artifacts** section
3. Download any of these:
   - `savemyexams-json` - Just the JSON file
   - `savemyexams-images` - Just the images folder (as ZIP)
   - `savemyexams-complete` - Everything in one tar.gz archive

### Artifacts Retention

Artifacts are kept for **90 days** after the workflow run.

### Automatic Schedule

The workflow also runs automatically:
- **Every Sunday at midnight UTC** (optional, can be disabled)

To disable automatic runs, remove the `schedule` section from `scrape.yml`.

### Configuration

To change scraping limits, edit `savemyexams_scraper.py`:

```python
DEFAULT_MAX_SUBJECTS = 25
DEFAULT_MAX_TOPICS_PER_SUBJECT = 100
DEFAULT_MAX_QUESTIONS_PER_TOPIC = 20
```

### Timeout

The workflow has a 6-hour timeout. If scraping takes longer, it will be cancelled.

### Troubleshooting

**Workflow fails:**
- Check the logs in the Actions tab
- Look for error messages in the "Run scraper" step

**No artifacts:**
- Make sure the workflow completed successfully
- Check that the JSON file was created in the "Check output" step

**Timeout:**
- Reduce the scraping limits in the configuration
- Or increase the timeout in `scrape.yml`
