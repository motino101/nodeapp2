#!/usr/bin/env python3
"""
Extract content from publicly accessible Google Docs
"""

import requests
import re
from bs4 import BeautifulSoup

def extract_public_google_doc(google_doc_url):
    """
    Extract content from a publicly accessible Google Doc
    """
    print(f"📄 Extracting content from public Google Doc: {google_doc_url}")
    
    try:
        # Convert edit URL to export URL
        doc_id = extract_doc_id(google_doc_url)
        if not doc_id:
            print(f"❌ Could not extract document ID from URL: {google_doc_url}")
            return None
        
        # Try different export formats
        export_urls = [
            f"https://docs.google.com/document/d/{doc_id}/export?format=txt",
            f"https://docs.google.com/document/d/{doc_id}/export?format=html",
        ]
        
        for export_url in export_urls:
            print(f"🔗 Trying export URL: {export_url}")
            
            try:
                response = requests.get(export_url, timeout=10)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    
                    if 'text/plain' in content_type:
                        content = response.text
                        print(f"✅ Successfully extracted text content ({len(content)} characters)")
                        return {
                            "type": "text",
                            "contents": content,
                            "source_url": google_doc_url,
                            "source_title": f"Google Doc {doc_id}"
                        }
                    
                    elif 'text/html' in content_type:
                        # Parse HTML content
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # Get text content
                        content = soup.get_text()
                        
                        # Clean up the text
                        lines = (line.strip() for line in content.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        content = '\n'.join(chunk for chunk in chunks if chunk)
                        
                        print(f"✅ Successfully extracted HTML content ({len(content)} characters)")
                        return {
                            "type": "text",
                            "contents": content,
                            "source_url": google_doc_url,
                            "source_title": f"Google Doc {doc_id}"
                        }
                
                else:
                    print(f"❌ Export failed with status {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Export error: {e}")
                continue
        
        print(f"❌ Could not extract content from any export format")
        return None
        
    except Exception as e:
        print(f"❌ Failed to extract Google Docs content: {e}")
        return None

def extract_doc_id(google_doc_url):
    """Extract document ID from Google Docs URL"""
    pattern = r'/document/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, google_doc_url)
    return match.group(1) if match else None

def test_public_google_doc():
    """Test extracting from a public Google Doc"""
    
    # Test URL from your output
    test_url = "https://docs.google.com/document/d/1Eg0xx2bItcFnPpaMbIALassoccZ726UF6-xH7vSC-80"
    
    print(f"🧪 Testing public Google Doc extraction")
    print(f"📄 URL: {test_url}")
    
    result = extract_public_google_doc(test_url)
    
    if result:
        print(f"\n✅ Success!")
        print(f"📝 Title: {result['source_title']}")
        print(f"📄 Content preview: {result['contents'][:200]}...")
        return result
    else:
        print(f"\n❌ Failed to extract content")
        print(f"💡 Make sure the Google Doc is publicly accessible (Anyone with the link can view)")
        return None

if __name__ == "__main__":
    test_public_google_doc()
