#!/usr/bin/env python3
"""
Test script to extract real content from Google Docs
"""

import os
import requests
import re

def extract_doc_id(google_doc_url):
    """Extract document ID from Google Docs URL"""
    pattern = r'/document/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, google_doc_url)
    return match.group(1) if match else None

def test_google_docs_api():
    """Test Google Docs API with different authentication methods"""
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ No Google API key found")
        return
    
    # Test URL from your output
    test_url = "https://docs.google.com/document/d/1Eg0xx2bItcFnPpaMbIALassoccZ726UF6-xH7vSC-80"
    doc_id = extract_doc_id(test_url)
    
    if not doc_id:
        print(f"❌ Could not extract document ID from: {test_url}")
        return
    
    print(f"🔍 Testing Google Docs API")
    print(f"📄 Document ID: {doc_id}")
    print(f"🔑 API Key: {api_key[:10]}...")
    
    # Method 1: API Key authentication
    print(f"\n🔧 Method 1: API Key authentication")
    url = f"https://docs.googleapis.com/v1/documents/{doc_id}"
    params = {'key': api_key}
    
    try:
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            doc_data = response.json()
            title = doc_data.get('title', 'Untitled')
            print(f"✅ Success! Document title: {title}")
            
            # Extract some content
            if 'body' in doc_data and 'content' in doc_data['body']:
                content_elements = doc_data['body']['content'][:3]  # First 3 elements
                print(f"📝 First few content elements:")
                for i, element in enumerate(content_elements):
                    if 'paragraph' in element:
                        para = element['paragraph']
                        if 'elements' in para:
                            text = ''.join(elem.get('textRun', {}).get('content', '') for elem in para['elements'])
                            print(f"  {i+1}. {text[:100]}...")
            
            return doc_data
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Method 2: Bearer token authentication (if API key is actually a token)
    print(f"\n🔧 Method 2: Bearer token authentication")
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            doc_data = response.json()
            title = doc_data.get('title', 'Untitled')
            print(f"✅ Success! Document title: {title}")
            return doc_data
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print(f"\n💡 Note: Make sure your Google Doc is publicly accessible or shared with the API key's service account")

if __name__ == "__main__":
    test_google_docs_api()
