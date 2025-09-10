#!/usr/bin/env python3
"""
Standalone script to extract Google Docs content and save it as a source file
"""

from tensorzero import TensorZeroGateway
import json
import sys
import os
import re

def extract_google_doc(google_doc_url, api_key, output_filename=None):
    """
    Extract content from a Google Doc and save it as a source file
    
    Args:
        google_doc_url (str): The Google Docs URL
        api_key (str): Google API key
        output_filename (str, optional): Output filename. Defaults to auto-generated name
    """
    
    with TensorZeroGateway.build_embedded(
        clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
        config_file="config/tensorzero.toml",
    ) as client:
        
        print(f"Extracting content from Google Doc...")
        print(f"URL: {google_doc_url}")
        
        # Call the extract_google_doc function with a natural language request
        response = client.inference(
            function_name="extract_google_doc",
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": f"Extract content from {google_doc_url} using API key {api_key}"
                    }
                ]
            },
        )
        
        # Extract content from the response
        content = response.content
        
        # Try to extract title and content from the response
        # Look for patterns like "Title: ..." and "Content: ..."
        title_match = re.search(r'Title:\s*(.+)', content)
        content_match = re.search(r'Content:\s*(.+)', content, re.DOTALL)
        
        if title_match and content_match:
            title = title_match.group(1).strip()
            extracted_content = content_match.group(1).strip()
            
            print(f"✅ Successfully extracted content from: {title}")
            print(f"Content length: {len(extracted_content)} characters")
            
            # Generate output filename if not provided
            if not output_filename:
                # Extract a safe filename from the title
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
                output_filename = f"sources/{safe_title}.json"
            
            # Ensure sources directory exists
            os.makedirs("sources", exist_ok=True)
            
            # Save to file
            source_file = {
                "content": extracted_content
            }
            
            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(source_file, f, indent=2, ensure_ascii=False)
            
            print(f"📁 Content saved to {output_filename}")
            return output_filename
            
        else:
            print(f"❌ Extraction failed. Response: {content}")
            return None

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 3:
        print("Usage: python extract_google_doc.py <google_doc_url> <api_key> [output_filename]")
        print("Example: python extract_google_doc.py 'https://docs.google.com/document/d/123/edit' 'your_api_key' 'my_doc.json'")
        sys.exit(1)
    
    google_doc_url = sys.argv[1]
    api_key = sys.argv[2]
    output_filename = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = extract_google_doc(google_doc_url, api_key, output_filename)
    
    if result:
        print(f"\n🎉 Success! You can now use {result} as a source in your main.py workflow.")
    else:
        print("\n💥 Extraction failed. Please check your URL and API key.")
        sys.exit(1)

if __name__ == "__main__":
    main()
