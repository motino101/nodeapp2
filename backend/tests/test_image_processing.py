#!/usr/bin/env python3
"""
Test script for multimodal image processing
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from content_maker.processors.image_processor import MultimodalImageProcessor

def test_multimodal_image_processing():
    """Test multimodal image processing with the existing image"""
    print("🧪 Testing Multimodal Image Processing")
    print("=" * 50)
    
    processor = MultimodalImageProcessor()
    
    # Test with the existing image in sources
    test_image = "sources/1-3.jpg"
    if os.path.exists(test_image):
        print(f"📁 Testing with: {test_image}")
        
        result = processor.process_image(test_image)
        
        print(f"\nResult: {result['status']}")
        if result['status'] == 'success':
            print(f"📝 Filename: {result['filename']}")
            print(f"📋 MIME type: {result['mime_type']}")
            print(f"🔍 Analysis preview: {result['analysis'][:300]}...")
            print(f"📄 Full content length: {len(result['content'])} characters")
        else:
            print(f"❌ Error: {result['error']}")
    else:
        print(f"❌ Test image not found: {test_image}")

def test_smart_detection_with_multimodal():
    """Test smart source detection with multimodal image processing"""
    print("\n🧪 Testing Smart Source Detection with Multimodal Images")
    print("=" * 50)
    
    from content_maker.processors.source_detector import SmartSourceDetector
    
    detector = SmartSourceDetector()
    
    # Test with the image file
    test_file = "sources/1-3.jpg"
    if os.path.exists(test_file):
        print(f"📁 Testing: {test_file}")
        source_info = detector.detect_source_type(test_file)
        print(f"   Type: {source_info['type']}")
        print(f"   Metadata: {source_info['metadata']}")
        
        # Process the source
        processed = detector.process_source(source_info)
        print(f"   Processed sources: {len(processed)}")
        for i, source in enumerate(processed):
            print(f"     {i+1}. Type: {source['type']}")
            print(f"        Title: {source.get('source_title', 'N/A')}")
            print(f"        Content preview: {source['contents'][:200]}...")
    else:
        print(f"❌ Test file not found: {test_file}")

if __name__ == "__main__":
    test_multimodal_image_processing()
    test_smart_detection_with_multimodal()
