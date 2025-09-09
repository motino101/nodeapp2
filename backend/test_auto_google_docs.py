#!/usr/bin/env python3
"""
Test script for automatic Google Docs detection and extraction
"""

import os
from auto_google_docs import process_sources_with_google_docs, load_sources_from_directory

def test_auto_google_docs():
    """Test the automatic Google Docs detection"""
    
    # Check if API key is set
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set")
        print("Set it with: export GOOGLE_API_KEY='your_api_key_here'")
        return
    
    print("🧪 Testing automatic Google Docs detection...")
    
    # Load sources from directory
    sources = load_sources_from_directory()
    print(f"📁 Loaded {len(sources)} sources from directory")
    
    # Process sources with Google Docs extraction
    processed_sources = process_sources_with_google_docs(sources, api_key)
    
    print(f"✅ Processing complete!")
    print(f"📊 Original sources: {len(sources)}")
    print(f"📊 Processed sources: {len(processed_sources)}")
    
    # Show what was processed
    for i, source in enumerate(processed_sources):
        if source.get("source_url"):
            print(f"📄 Source {i+1}: {source.get('source_title', 'Untitled')} (from Google Docs)")
        else:
            print(f"📄 Source {i+1}: Regular source")

if __name__ == "__main__":
    test_auto_google_docs()
