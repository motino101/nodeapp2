#!/usr/bin/env python3
"""
Example showing how to use the automatic Google Docs detection
"""

import os
from auto_google_docs import process_sources_with_google_docs

def example_usage():
    """Example of how the automatic Google Docs detection works"""
    
    # Example sources that might contain Google Docs URLs
    example_sources = [
        {
            "type": "text",
            "contents": "Here are my research notes: https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit. This document contains important insights about digital gardening."
        },
        {
            "type": "text", 
            "contents": "Regular text content without any Google Docs URLs."
        },
        {
            "type": "text",
            "contents": "Another Google Doc with my thoughts: https://docs.google.com/document/d/example123/edit. This has more detailed analysis."
        }
    ]
    
    print("📝 Example sources:")
    for i, source in enumerate(example_sources):
        print(f"  {i+1}. {source['contents'][:50]}...")
    
    # Get API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("\n⚠️  GOOGLE_API_KEY not set. This is just a demonstration.")
        print("   In real usage, the system would extract the Google Docs content.")
        return
    
    print(f"\n🔍 Processing sources with Google Docs detection...")
    
    # Process the sources
    processed_sources = process_sources_with_google_docs(example_sources, api_key)
    
    print(f"\n✅ Processing complete!")
    print(f"📊 Original sources: {len(example_sources)}")
    print(f"📊 Processed sources: {len(processed_sources)}")
    
    print(f"\n📄 Final sources:")
    for i, source in enumerate(processed_sources):
        if source.get("source_url"):
            print(f"  {i+1}. [Google Docs] {source.get('source_title', 'Untitled')}")
        else:
            print(f"  {i+1}. [Regular] {source['contents'][:50]}...")

if __name__ == "__main__":
    example_usage()
