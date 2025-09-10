#!/usr/bin/env python3
"""
Test script for smart source detection system
"""

import os
from smart_source_detector import SmartSourceDetector

def test_smart_detection():
    """Test the smart source detection system"""
    
    print("🧪 Testing Smart Source Detection System")
    print("=" * 50)
    
    # Initialize detector
    detector = SmartSourceDetector()
    
    # Test individual file detection
    test_files = [
        "sources/article1.json",
        "sources/article2.json", 
        "sources/article3.json",
        "sources/test_google_docs.json",
        "sources/input.json",
        "sources/1-3.jpg"
    ]
    
    print("\n📁 Testing individual file detection:")
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n🔍 Testing: {test_file}")
            source_info = detector.detect_source_type(test_file)
            print(f"   Type: {source_info['type']}")
            print(f"   Metadata: {source_info['metadata']}")
            
            # Process the source
            processed = detector.process_source(source_info)
            print(f"   Processed sources: {len(processed)}")
            for i, source in enumerate(processed):
                print(f"     {i+1}. {source['type']}: {source['contents'][:50]}...")
        else:
            print(f"❌ File not found: {test_file}")
    
    # Test directory processing
    print(f"\n🔍 Testing directory processing:")
    all_sources = detector.process_sources_directory("sources")
    
    print(f"\n📊 Summary:")
    print(f"   Total processed sources: {len(all_sources)}")
    
    # Categorize by type
    type_counts = {}
    for source in all_sources:
        source_type = source.get('source_url', 'regular')
        if 'google' in source_type.lower():
            source_type = 'google_docs'
        else:
            source_type = 'text'
        
        type_counts[source_type] = type_counts.get(source_type, 0) + 1
    
    print(f"   Source types:")
    for source_type, count in type_counts.items():
        print(f"     {source_type}: {count}")

if __name__ == "__main__":
    test_smart_detection()
