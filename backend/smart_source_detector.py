#!/usr/bin/env python3
"""
Smart Source Detection and Processing System
Automatically detects and processes different types of sources
"""

import re
import json
import os
import mimetypes
from pathlib import Path
from tensorzero import TensorZeroGateway

class SmartSourceDetector:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        
    def detect_source_type(self, source_path):
        """
        Detect the type of source based on file path or content
        
        Returns:
            dict: {
                'type': 'image'|'google_docs'|'webpage'|'text'|'unknown',
                'path': str,
                'content': str (if applicable),
                'metadata': dict
            }
        """
        source_path = Path(source_path)
        
        # Check if it's a file
        if source_path.is_file():
            # Get file extension
            ext = source_path.suffix.lower()
            
            # Image detection
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
                return {
                    'type': 'image',
                    'path': str(source_path),
                    'content': f"Image file: {source_path.name}",
                    'metadata': {
                        'file_type': 'image',
                        'extension': ext,
                        'filename': source_path.name
                    }
                }
            
            # JSON file detection
            elif ext == '.json':
                try:
                    with open(source_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Check if it contains a Google Docs URL
                    content = data.get('content', '')
                    google_docs_urls = self._find_google_docs_urls(content)
                    
                    if google_docs_urls:
                        return {
                            'type': 'google_docs',
                            'path': str(source_path),
                            'content': content,
                            'metadata': {
                                'file_type': 'json',
                                'google_docs_urls': google_docs_urls,
                                'filename': source_path.name
                            }
                        }
                    else:
                        return {
                            'type': 'text',
                            'path': str(source_path),
                            'content': content,
                            'metadata': {
                                'file_type': 'json',
                                'filename': source_path.name
                            }
                        }
                        
                except (json.JSONDecodeError, KeyError):
                    return {
                        'type': 'text',
                        'path': str(source_path),
                        'content': f"Text file: {source_path.name}",
                        'metadata': {
                            'file_type': 'text',
                            'filename': source_path.name
                        }
                    }
            
            # Text file detection
            elif ext in ['.txt', '.md', '.rst']:
                try:
                    with open(source_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for URLs in text
                    google_docs_urls = self._find_google_docs_urls(content)
                    webpage_urls = self._find_webpage_urls(content)
                    
                    if google_docs_urls:
                        return {
                            'type': 'google_docs',
                            'path': str(source_path),
                            'content': content,
                            'metadata': {
                                'file_type': 'text',
                                'google_docs_urls': google_docs_urls,
                                'filename': source_path.name
                            }
                        }
                    elif webpage_urls:
                        return {
                            'type': 'webpage',
                            'path': str(source_path),
                            'content': content,
                            'metadata': {
                                'file_type': 'text',
                                'webpage_urls': webpage_urls,
                                'filename': source_path.name
                            }
                        }
                    else:
                        return {
                            'type': 'text',
                            'path': str(source_path),
                            'content': content,
                            'metadata': {
                                'file_type': 'text',
                                'filename': source_path.name
                            }
                        }
                        
                except Exception:
                    return {
                        'type': 'text',
                        'path': str(source_path),
                        'content': f"Text file: {source_path.name}",
                        'metadata': {
                            'file_type': 'text',
                            'filename': source_path.name
                        }
                    }
            
            # Other file types
            else:
                return {
                    'type': 'unknown',
                    'path': str(source_path),
                    'content': f"Unknown file type: {source_path.name}",
                    'metadata': {
                        'file_type': 'unknown',
                        'extension': ext,
                        'filename': source_path.name
                    }
                }
        
        # If it's not a file, treat as text content
        else:
            return {
                'type': 'text',
                'path': str(source_path),
                'content': str(source_path),
                'metadata': {
                    'file_type': 'text',
                    'filename': str(source_path)
                }
            }
    
    def _find_google_docs_urls(self, text):
        """Find Google Docs URLs in text"""
        pattern = r'https://docs\.google\.com/document/d/[a-zA-Z0-9_-]+'
        return re.findall(pattern, text)
    
    def _find_webpage_urls(self, text):
        """Find general webpage URLs in text"""
        pattern = r'https?://[^\s]+'
        urls = re.findall(pattern, text)
        # Filter out Google Docs URLs
        return [url for url in urls if 'docs.google.com' not in url]
    
    def process_source(self, source_info):
        """
        Process a source based on its detected type
        
        Args:
            source_info (dict): Source information from detect_source_type
            
        Returns:
            list: List of processed source objects for the main workflow
        """
        source_type = source_info['type']
        processed_sources = []
        
        if source_type == 'google_docs':
            # Processing Google Docs source
            urls = source_info['metadata']['google_docs_urls']
            
            for url in urls:
                extracted_content = self._extract_google_doc_content(url)
                if extracted_content:
                    processed_sources.append(extracted_content)
            
            # Also keep the original source if it has other content
            if source_info['content'] and not all(url in source_info['content'] for url in urls):
                processed_sources.append({
                    "type": "text",
                    "contents": source_info['content']
                })
        
        elif source_type == 'image':
            # Processing image source
            # For now, just add a description of the image
            processed_sources.append({
                "type": "text",
                "contents": f"Image reference: {source_info['content']}"
            })
        
        elif source_type == 'webpage':
            # Processing webpage source
            # For now, just add the content as text
            processed_sources.append({
                "type": "text",
                "contents": source_info['content']
            })
        
        elif source_type == 'text':
            # Processing text source
            processed_sources.append({
                "type": "text",
                "contents": source_info['content']
            })
        
        else:
            # Processing unknown source
            processed_sources.append({
                "type": "text",
                "contents": source_info['content']
            })
        
        return processed_sources
    
    def _extract_google_doc_content(self, google_doc_url):
        """Extract content from a publicly accessible Google Doc"""
        # Extracting content from Google Doc
        
        try:
            # Extract document ID from URL
            doc_id = self._extract_doc_id(google_doc_url)
            if not doc_id:
                print(f"❌ Could not extract document ID from URL: {google_doc_url}")
                return None
            
            # Try to extract from public Google Doc
            import requests
            from bs4 import BeautifulSoup
            
            # Try different export formats
            export_urls = [
                f"https://docs.google.com/document/d/{doc_id}/export?format=txt",
                f"https://docs.google.com/document/d/{doc_id}/export?format=html",
            ]
            
            for export_url in export_urls:
                try:
                    print(f"🔗 Trying export: {export_url}")
                    response = requests.get(export_url, timeout=10)
                    
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '')
                        
                        if 'text/plain' in content_type:
                            content = response.text
                            # Successfully extracted text content
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
                            
                            # Successfully extracted HTML content
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
            
            # If all exports failed, provide helpful message
            print(f"❌ Could not extract content from Google Doc")
            print(f"💡 To make this Google Doc accessible:")
            print(f"   1. Open the Google Doc in your browser")
            print(f"   2. Click 'Share' button")
            print(f"   3. Change permissions to 'Anyone with the link can view'")
            print(f"   4. Save and try again")
            
            # Return a placeholder with instructions
            return {
                "type": "text",
                "contents": f"[Google Doc content not accessible - please make the document public: {google_doc_url}]",
                "source_url": google_doc_url,
                "source_title": f"Google Doc {doc_id} (Not Public)"
            }
                
        except Exception as e:
            print(f"❌ Failed to extract Google Docs content: {e}")
            return None
    
    def _extract_doc_id(self, google_doc_url):
        """Extract document ID from Google Docs URL"""
        import re
        pattern = r'/document/d/([a-zA-Z0-9_-]+)'
        match = re.search(pattern, google_doc_url)
        return match.group(1) if match else None
    
    def _extract_text_from_doc(self, doc_data):
        """Extract text content from Google Docs API response"""
        content_parts = []
        
        def extract_text_from_element(element):
            if 'textRun' in element:
                return element['textRun'].get('content', '')
            elif 'paragraph' in element:
                paragraph = element['paragraph']
                if 'elements' in paragraph:
                    return ''.join(extract_text_from_element(elem) for elem in paragraph['elements'])
            elif 'table' in element:
                table = element['table']
                if 'tableRows' in table:
                    table_text = []
                    for row in table['tableRows']:
                        if 'tableCells' in row:
                            row_text = []
                            for cell in row['tableCells']:
                                if 'content' in cell:
                                    cell_text = ''.join(extract_text_from_element(elem) for elem in cell['content'])
                                    row_text.append(cell_text.strip())
                            table_text.append(' | '.join(row_text))
                    return '\n'.join(table_text)
            return ''
        
        if 'body' in doc_data and 'content' in doc_data['body']:
            for element in doc_data['body']['content']:
                text = extract_text_from_element(element)
                if text.strip():
                    content_parts.append(text.strip())
        
        return '\n\n'.join(content_parts)
    
    def process_sources_directory(self, sources_dir="sources"):
        """
        Process all sources in a directory with smart detection
        
        Args:
            sources_dir (str): Path to sources directory
            
        Returns:
            list: List of all processed sources
        """
        sources_path = Path(sources_dir)
        if not sources_path.exists():
            print(f"⚠️  Sources directory '{sources_dir}' not found")
            return []
        
        all_processed_sources = []
        
        for file_path in sources_path.iterdir():
            if file_path.is_file():
                # Detect source type
                source_info = self.detect_source_type(file_path)
                
                # Process the source
                processed_sources = self.process_source(source_info)
                all_processed_sources.extend(processed_sources)
        return all_processed_sources

# Example usage and testing
if __name__ == "__main__":
    detector = SmartSourceDetector()
    
    # Test with individual files
    test_files = [
        "sources/article1.json",
        "sources/test_google_docs.json",
        "sources/1-3.jpg"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n🧪 Testing: {test_file}")
            source_info = detector.detect_source_type(test_file)
            print(f"   Type: {source_info['type']}")
            print(f"   Metadata: {source_info['metadata']}")
            
            processed = detector.process_source(source_info)
            print(f"   Processed sources: {len(processed)}")
    
    # Test with entire directory
    # Processing entire sources directory
    all_sources = detector.process_sources_directory()
    print(f"Total processed sources: {len(all_sources)}")
