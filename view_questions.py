#!/usr/bin/env python3
"""
Question Viewer
===============

Helper script to view questions and their associated images.

Usage:
    python view_questions.py                    # View all questions with images
    python view_questions.py --question-id ID   # View specific question
    python view_questions.py --stats            # Show statistics
"""

import json
import argparse
from pathlib import Path


def load_data(json_file='savemyexams_questions.json'):
    """Load questions from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def show_stats(data):
    """Display statistics about scraped data"""
    metadata = data['metadata']
    questions = data['questions']
    
    print("="*70)
    print("SCRAPING STATISTICS")
    print("="*70)
    print(f"Source: {metadata['source']}")
    print(f"Scrape Date: {metadata['scrape_date']}")
    print(f"\nQuestions:")
    print(f"  Total: {metadata['total_questions']}")
    print(f"  With images: {metadata['questions_with_images']}")
    print(f"  Without images: {metadata['total_questions'] - metadata['questions_with_images']}")
    print(f"\nImages:")
    print(f"  Total images: {metadata['total_images']}")
    print(f"  Images folder: {metadata['images_folder']}")
    
    # Count questions by topic
    topics = {}
    for q in questions:
        topic = q.get('topic', 'Unknown')
        topics[topic] = topics.get(topic, 0) + 1
    
    print(f"\nQuestions by topic:")
    for topic, count in sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {topic}: {count}")
    
    print("="*70)


def show_question(question, show_html=False):
    """Display a single question with its details"""
    print("\n" + "="*70)
    print(f"QUESTION ID: {question['id']}")
    print("="*70)
    print(f"Topic: {question.get('topic', 'N/A')}")
    print(f"Marks: {question.get('marks', 'N/A')}")
    print(f"Source: {question['source_url']}")
    print(f"\nQuestion Text:")
    print("-" * 70)
    print(question['question_text'])
    print("-" * 70)
    
    if question.get('images'):
        print(f"\nImages ({len(question['images'])}):")
        for img in question['images']:
            img_path = Path(question.get('images_folder', 'images')) / img
            exists = "✅" if img_path.exists() else "❌"
            print(f"  {exists} {img}")
    else:
        print("\nImages: None")
    
    if question.get('answer'):
        print(f"\nAnswer:")
        print("-" * 70)
        print(question['answer'])
        print("-" * 70)
    
    if show_html:
        print(f"\nHTML (truncated):")
        print("-" * 70)
        print(question['question_html'][:500])
        print("-" * 70)


def list_questions_with_images(data, limit=10):
    """List questions that have images"""
    questions = [q for q in data['questions'] if q.get('images')]
    
    print("="*70)
    print(f"QUESTIONS WITH IMAGES (showing {min(limit, len(questions))} of {len(questions)})")
    print("="*70)
    
    for i, q in enumerate(questions[:limit], 1):
        print(f"\n{i}. ID: {q['id']}")
        print(f"   Topic: {q.get('topic', 'N/A')}")
        print(f"   Images: {len(q['images'])} - {', '.join(q['images'])}")
        print(f"   Text: {q['question_text'][:100]}...")


def main():
    parser = argparse.ArgumentParser(description='View scraped questions and images')
    parser.add_argument('--json', default='savemyexams_questions.json', help='JSON file to read')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--question-id', help='Show specific question by ID')
    parser.add_argument('--list-images', action='store_true', help='List questions with images')
    parser.add_argument('--limit', type=int, default=10, help='Limit number of results')
    parser.add_argument('--html', action='store_true', help='Show HTML content')
    
    args = parser.parse_args()
    
    # Load data
    try:
        data = load_data(args.json)
    except FileNotFoundError:
        print(f"❌ Error: File '{args.json}' not found")
        print("Run the scraper first: python savemyexams_scraper.py")
        return
    
    # Execute command
    if args.stats:
        show_stats(data)
    elif args.question_id:
        # Find question by ID
        question = next((q for q in data['questions'] if q['id'] == args.question_id), None)
        if question:
            show_question(question, show_html=args.html)
        else:
            print(f"❌ Question with ID '{args.question_id}' not found")
    elif args.list_images:
        list_questions_with_images(data, limit=args.limit)
    else:
        # Default: show stats and list some questions with images
        show_stats(data)
        print("\n")
        list_questions_with_images(data, limit=5)
        print("\n💡 Use --help to see all options")


if __name__ == "__main__":
    main()
