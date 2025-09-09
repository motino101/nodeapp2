#!/usr/bin/env python3
"""
Test script for Google Docs extraction functionality
"""

from tensorzero import TensorZeroGateway
import json

def test_google_docs_extraction():
    """Test the Google Docs extraction function"""
    
    # Example Google Docs URL (you'll need to replace with actual URL and API key)
    google_doc_url = "https://docs.google.com/document/d/YOUR_DOCUMENT_ID/edit"
    api_key = "YOUR_GOOGLE_API_KEY"
    
    with TensorZeroGateway.build_embedded(
        clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
        config_file="config/tensorzero.toml",
    ) as client:
        
        print("Testing Google Docs extraction...")
        
        # Call the extract_google_doc function
        response = client.inference(
            function_name="extract_google_doc",
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "arguments": {
                                    "google_doc_url": google_doc_url,
                                    "api_key": api_key
                                }
                            }
                        ]
                    }
                ]
            },
        )
        
        result = response.output.parsed
        
        if result["success"]:
            print(f"✅ Successfully extracted content from: {result['title']}")
            print(f"Content preview: {result['content'][:200]}...")
            
            # Save to a file in the sources directory
            source_file = {
                "content": result["content"]
            }
            
            with open("sources/google_doc_content.json", "w", encoding="utf-8") as f:
                json.dump(source_file, f, indent=2, ensure_ascii=False)
            
            print("📁 Content saved to sources/google_doc_content.json")
            
        else:
            print(f"❌ Extraction failed: {result['error_message']}")

if __name__ == "__main__":
    test_google_docs_extraction()
