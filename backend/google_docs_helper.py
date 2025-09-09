#!/usr/bin/env python3
"""
Helper functions for integrating Google Docs extraction into the main workflow
"""

from tensorzero import TensorZeroGateway
import json
import os

def extract_and_add_google_doc(google_doc_url, api_key, sources_list):
    """
    Extract content from a Google Doc and add it to the sources list
    
    Args:
        google_doc_url (str): The Google Docs URL
        api_key (str): Google API key
        sources_list (list): List of sources to append to
        
    Returns:
        list: Updated sources list with the Google Doc content
    """
    
    with TensorZeroGateway.build_embedded(
        clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
        config_file="config/tensorzero.toml",
    ) as client:
        
        print(f"Extracting Google Doc content...")
        
        # Call the extract_google_doc function with natural language
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
        import re
        title_match = re.search(r'Title:\s*(.+)', content)
        content_match = re.search(r'Content:\s*(.+)', content, re.DOTALL)
        
        if title_match and content_match:
            title = title_match.group(1).strip()
            extracted_content = content_match.group(1).strip()
            
            print(f"✅ Added Google Doc: {title}")
            
            # Add to sources list
            sources_list.append({
                "type": "text",
                "contents": extracted_content
            })
            
            return sources_list
            
        else:
            print(f"❌ Failed to extract Google Doc. Response: {content}")
            return sources_list

def load_google_doc_from_file(filepath):
    """
    Load a previously extracted Google Doc from a JSON file
    
    Args:
        filepath (str): Path to the JSON file containing the Google Doc content
        
    Returns:
        dict: Source object ready to be added to sources list
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return {
            "type": "text",
            "contents": data["content"]
        }
        
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in file: {filepath}")
        return None
    except KeyError:
        print(f"❌ Missing 'content' field in file: {filepath}")
        return None

# Example usage in main.py:
"""
# Option 1: Extract Google Doc directly
google_doc_url = "https://docs.google.com/document/d/YOUR_DOC_ID/edit"
api_key = "YOUR_API_KEY"
sources = extract_and_add_google_doc(google_doc_url, api_key, sources)

# Option 2: Load from previously extracted file
google_doc_source = load_google_doc_from_file("sources/my_google_doc.json")
if google_doc_source:
    sources.append(google_doc_source)
"""
