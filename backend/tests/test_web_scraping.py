#!/usr/bin/env python3
"""
Test script for web scraping RAG functionality
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from content_maker.processors.source_detector import SmartSourceDetector
from content_maker.processors.web_scraper import WebScraper

def test_web_scraper():
    """Test the web scraper directly"""
    print("🧪 Testing Web Scraper")
    print("=" * 50)
    
    scraper = WebScraper()
    
    # Test URL extraction
    test_text = """
    Check out these resources:
    https://maggieappleton.com/garden-history
    https://www.technologyreview.com/2020/09/03/1007716/digital-gardens-let-you-cultivate-your-own-little-bit-of-the-internet/
    Also, here's a Google Doc: https://docs.google.com/document/d/123/edit
    """
    
    print("📋 Testing URL extraction:")
    urls = scraper.extract_webpage_urls(test_text)
    print(f"Found URLs: {urls}")
    
    # Test scraping a real webpage
    if urls:
        test_url = urls[0]  # Test first URL
        print(f"\n🔍 Testing scrape of: {test_url}")
        result = scraper.scrape_webpage(test_url)
        
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Title: {result['title']}")
            print(f"Content preview: {result['content'][:300]}...")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")

def test_smart_detection_with_webpages():
    """Test smart source detection with webpage URLs"""
    print("\n🧪 Testing Smart Source Detection with Webpages")
    print("=" * 50)
    
    detector = SmartSourceDetector()
    
    # Test with the webpage test file
    test_file = "sources/test_webpage.json"
    if os.path.exists(test_file):
        print(f"📁 Testing: {test_file}")
        source_info = detector.detect_source_type(test_file)
        print(f"   Type: {source_info['type']}")
        print(f"   Metadata: {source_info['metadata']}")
        
        # Process the source
        processed = detector.process_source(source_info)
        print(f"   Processed sources: {len(processed)}")
        for i, source in enumerate(processed):
            print(f"     {i+1}. {source.get('source_title', 'Regular source')}: {source['contents'][:100]}...")
    else:
        print(f"❌ Test file not found: {test_file}")

def test_full_directory_processing():
    """Test processing the entire sources directory"""
    print("\n🧪 Testing Full Directory Processing")
    print("=" * 50)
    
    detector = SmartSourceDetector()
    all_sources = detector.process_sources_directory("sources")
    
    print(f"📊 Total processed sources: {len(all_sources)}")
    
    # Categorize by type
    type_counts = {}
    for source in all_sources:
        if source.get('source_url'):
            if 'google' in source.get('source_url', '').lower():
                source_type = 'google_docs'
            else:
                source_type = 'webpage'
        else:
            source_type = 'text'
        
        type_counts[source_type] = type_counts.get(source_type, 0) + 1
    
    print(f"📊 Source types:")
    for source_type, count in type_counts.items():
        print(f"     {source_type}: {count}")

if __name__ == "__main__":
    test_web_scraper()
    test_smart_detection_with_webpages()
    test_full_directory_processing()
