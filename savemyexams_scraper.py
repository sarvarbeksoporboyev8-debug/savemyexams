#!/usr/bin/env python3
"""
SaveMyExams Scraper
===================

Scrapes exam questions and answers from savemyexams.co.uk using Playwright browser automation.

Features:
- Playwright-based scraping with anti-bot measures
- Extracts questions, answers, marks, and topics
- Downloads all question images (figures, diagrams) to separate folder
- Images are named with question IDs for easy matching
- Saves to JSON format with image references
- Configurable scraping limits

Requirements:
- Python 3.8+
- playwright
- beautifulsoup4
- lxml

Installation:
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    pip install playwright beautifulsoup4 lxml
    playwright install chromium

Usage:
    python savemyexams_scraper.py

Configuration:
    Edit the main() function to adjust:
    - max_subjects: Number of subjects to scrape
    - max_topics_per_subject: Number of topics per subject
    - max_questions_per_topic: Number of question pages per topic

Output:
    savemyexams_questions.json - Contains all scraped questions with metadata
    images/ - Folder containing all downloaded question images
    
Image Naming:
    Images are named: {question_id}_fig{N}.{ext}
    Example: gcse_biology_aqa_18_topic-questions_1-cell-biology_1-1-cell-structure_exam-questions_2_fig1.png
    
    This makes it easy to match images to questions:
    - Question ID is in the JSON
    - Image filename starts with the same question ID
    
Helper Script:
    python view_questions.py --stats              # Show statistics
    python view_questions.py --list-images        # List questions with images
    python view_questions.py --question-id ID     # View specific question
"""

import asyncio
import json
import time
import re
import os
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright, Page, Browser
import random
import aiohttp
from pathlib import Path


# ============================================================================
# CONFIGURATION
# ============================================================================

# Adjust these values to control scraping scope
DEFAULT_MAX_SUBJECTS = 25
DEFAULT_MAX_TOPICS_PER_SUBJECT = 100
DEFAULT_MAX_QUESTIONS_PER_TOPIC = 20

# Browser settings
HEADLESS_MODE = True  # Set to False to see browser in action
PAGE_TIMEOUT = 30000  # milliseconds

# Delays (milliseconds) - to simulate human behavior
MIN_DELAY = 500
MAX_DELAY = 2000
MIN_PAGE_DELAY = 1000
MAX_PAGE_DELAY = 3000

# Image settings
IMAGES_FOLDER = "images"  # Folder to save question images
DOWNLOAD_IMAGES = True  # Set to False to skip image downloads


class SaveMyExamsScraper:
    def __init__(self):
        self.base_url = "https://www.savemyexams.co.uk"
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.questions = []
        self.images_folder = Path(IMAGES_FOLDER)
        
        # Create images folder if it doesn't exist
        if DOWNLOAD_IMAGES:
            self.images_folder.mkdir(exist_ok=True)
    
    async def init_browser(self):
        """Initialize Playwright browser with anti-bot measures"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=HEADLESS_MODE,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )
        
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
        )
        
        # Add stealth scripts
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        """)
        
        self.page = await context.new_page()
    
    async def human_delay(self, min_ms: int = 500, max_ms: int = 2000):
        """Random delay to simulate human behavior"""
        await asyncio.sleep(random.uniform(min_ms / 1000, max_ms / 1000))
    
    async def get_page_content(self, url: str) -> Optional[str]:
        """Navigate to page and get content"""
        try:
            print(f"Fetching: {url}")
            await self.page.goto(url, wait_until='domcontentloaded', timeout=PAGE_TIMEOUT)
            await self.human_delay(MIN_PAGE_DELAY, MAX_PAGE_DELAY)
            
            # Scroll to load lazy content
            await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
            await self.human_delay(MIN_DELAY, MAX_DELAY)
            await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await self.human_delay(MIN_DELAY, MAX_DELAY)
            
            return await self.page.content()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    async def download_image(self, image_url: str, question_id: str, image_index: int) -> Optional[str]:
        """Download an image and save it with a meaningful filename"""
        try:
            # Create filename: questionid_imageN.ext
            ext = image_url.split('.')[-1].split('?')[0]  # Get extension, remove query params
            if ext not in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']:
                ext = 'png'  # Default extension
            
            filename = f"{question_id}_fig{image_index}.{ext}"
            filepath = self.images_folder / filename
            
            # Download image
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        content = await response.read()
                        with open(filepath, 'wb') as f:
                            f.write(content)
                        return filename
            return None
        except Exception as e:
            print(f"    Warning: Failed to download image {image_url}: {e}")
            return None
    
    async def close(self):
        """Close browser"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
    
    async def discover_subjects(self) -> List[Dict[str, str]]:
        """Discover available subjects"""
        from bs4 import BeautifulSoup
        
        html = await self.get_page_content(f"{self.base_url}/subjects/")
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        subjects = []
        
        # Look for subject links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/gcse/' in href or '/a-level/' in href or '/ib/' in href:
                full_url = urljoin(self.base_url, href)
                text = link.get_text(strip=True)
                if text and full_url not in [s['url'] for s in subjects]:
                    subjects.append({
                        'name': text,
                        'url': full_url
                    })
        
        return subjects[:10]  # Limit for testing
    
    async def find_topic_question_pages(self, subject_url: str) -> List[str]:
        """Find topic question pages for a subject"""
        from bs4 import BeautifulSoup
        
        html = await self.get_page_content(subject_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        pages = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'topic-questions' in href or 'questions' in href:
                full_url = urljoin(self.base_url, href)
                if full_url not in pages:
                    pages.append(full_url)
        
        return pages
    
    async def find_actual_question_links(self, topic_page_url: str) -> List[str]:
        """Find links to actual question pages from a topic overview page"""
        from bs4 import BeautifulSoup
        
        html = await self.get_page_content(topic_page_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        question_links = []
        
        # Look for links to exam-questions pages
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'exam-questions' in href and href not in question_links:
                full_url = urljoin(self.base_url, href)
                question_links.append(full_url)
        
        return question_links[:10]  # Limit per topic
    
    async def extract_question_from_page(self, url: str) -> List[Dict]:
        """Extract questions and answers from an actual question page"""
        from bs4 import BeautifulSoup
        
        html = await self.get_page_content(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        questions = []
        
        # Extract page title/topic
        topic = None
        title_elem = soup.find(['h1', 'h2'])
        if title_elem:
            topic = title_elem.get_text(strip=True)
        
        # Look for question cards or containers
        question_containers = soup.find_all(['div', 'article'], class_=re.compile(r'question|card', re.I))
        
        for idx, container in enumerate(question_containers, 1):
            # Extract question text
            question_text = container.get_text(strip=True)
            
            # Skip if too short or contains marketing text
            if len(question_text) < 30:
                continue
            if any(phrase in question_text.lower() for phrase in ['get better grades', 'boost exam confidence', 'learn from examiners', 'identify weak areas']):
                continue
            
            # Generate question ID
            question_id = f"{urlparse(url).path.replace('/', '_').strip('_')}_{idx}"
            
            question_data = {
                'id': question_id,
                'source_url': url,
                'question_number': idx,
                'question_text': question_text[:1000],  # Limit length
                'question_html': str(container)[:2000],
                'answer': '',
                'answer_html': '',
                'marks': None,
                'difficulty': None,
                'topic': topic,
                'images': []  # List of image filenames
            }
            
            # Extract images (figures, diagrams, etc.)
            if DOWNLOAD_IMAGES:
                images = container.find_all('img')
                for img_idx, img in enumerate(images, 1):
                    img_src = img.get('src') or img.get('data-src')
                    if img_src:
                        # Make absolute URL
                        img_url = urljoin(self.base_url, img_src)
                        
                        # Download image
                        filename = await self.download_image(img_url, question_id, img_idx)
                        if filename:
                            question_data['images'].append(filename)
            
            # Try to find answer/solution
            answer_elem = container.find(['div', 'section', 'p'], class_=re.compile(r'answer|solution|explanation', re.I))
            if answer_elem:
                question_data['answer'] = answer_elem.get_text(strip=True)[:1000]
                question_data['answer_html'] = str(answer_elem)[:2000]
            
            # Extract marks
            marks_match = re.search(r'(\d+)\s*marks?', question_text, re.I)
            if marks_match:
                question_data['marks'] = int(marks_match.group(1))
            
            questions.append(question_data)
        
        return questions
    
    async def scrape_all(self, max_subjects: int = 2, max_topics_per_subject: int = 2, max_questions_per_topic: int = 3) -> List[Dict]:
        """Scrape questions from multiple subjects"""
        await self.init_browser()
        
        try:
            print("Discovering subjects...")
            subjects = await self.discover_subjects()
            print(f"Found {len(subjects)} subjects")
            
            all_questions = []
            
            for subject in subjects[:max_subjects]:
                print(f"\n{'='*60}")
                print(f"Processing: {subject['name']}")
                print(f"{'='*60}")
                
                # Find topic overview pages
                topic_pages = await self.find_topic_question_pages(subject['url'])
                print(f"Found {len(topic_pages)} topic overview pages")
                
                for topic_url in topic_pages[:max_topics_per_subject]:
                    # Find actual question pages from topic overview
                    question_pages = await self.find_actual_question_links(topic_url)
                    print(f"  Found {len(question_pages)} question pages in topic")
                    
                    for question_url in question_pages[:max_questions_per_topic]:
                        questions = await self.extract_question_from_page(question_url)
                        print(f"    Extracted {len(questions)} questions from {question_url}")
                        all_questions.extend(questions)
                        
                        await self.human_delay(1000, 2000)
                    
                    await self.human_delay(1500, 2500)
                
                await self.human_delay(2000, 3000)
            
            return all_questions
        finally:
            await self.close()
    
    def save_to_json(self, questions: List[Dict], filename: str = "savemyexams_questions.json"):
        """Save questions to JSON file"""
        # Count images
        total_images = sum(len(q.get('images', [])) for q in questions)
        questions_with_images = sum(1 for q in questions if q.get('images'))
        
        output = {
            'metadata': {
                'source': 'savemyexams.co.uk',
                'total_questions': len(questions),
                'questions_with_images': questions_with_images,
                'total_images': total_images,
                'images_folder': IMAGES_FOLDER if DOWNLOAD_IMAGES else None,
                'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'questions': questions
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"Saved {len(questions)} questions to {filename}")
        if DOWNLOAD_IMAGES:
            print(f"  - {questions_with_images} questions with images")
            print(f"  - {total_images} total images downloaded to '{IMAGES_FOLDER}/' folder")
        print(f"{'='*60}")


async def main():
    """Main entry point"""
    print("SaveMyExams Scraper (Playwright)")
    print("="*60)
    print("\nConfiguration:")
    print(f"  - Subjects: {DEFAULT_MAX_SUBJECTS}")
    print(f"  - Topics per subject: {DEFAULT_MAX_TOPICS_PER_SUBJECT}")
    print(f"  - Question pages per topic: {DEFAULT_MAX_QUESTIONS_PER_TOPIC}")
    print(f"  - Headless mode: {HEADLESS_MODE}")
    print("="*60 + "\n")
    
    scraper = SaveMyExamsScraper()
    
    try:
        # Scrape questions
        questions = await scraper.scrape_all(
            max_subjects=DEFAULT_MAX_SUBJECTS,
            max_topics_per_subject=DEFAULT_MAX_TOPICS_PER_SUBJECT,
            max_questions_per_topic=DEFAULT_MAX_QUESTIONS_PER_TOPIC
        )
        
        # Save to JSON
        if questions:
            scraper.save_to_json(questions)
            print(f"\n✅ Successfully scraped {len(questions)} questions!")
            print(f"   Saved to: savemyexams_questions.json")
        else:
            print("\n⚠️  No questions found.")
            print("The site may have changed structure or requires authentication.")
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
