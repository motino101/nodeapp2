#!/usr/bin/env python3
"""
Test script for Google Docs extraction using TensorZero tool use
"""

from tensorzero import TensorZeroGateway
import json

def test_google_docs_tool():
    """Test the Google Docs extraction tool"""
    
    # Example Google Docs URL and API key (replace with actual values)
    google_doc_url = "https://docs.google.com/document/d/YOUR_DOCUMENT_ID/edit"
    api_key = "YOUR_GOOGLE_API_KEY"
    
    with TensorZeroGateway.build_embedded(
        clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
        config_file="config/tensorzero.toml",
    ) as client:
        
        print("Testing Google Docs extraction with tool use...")
        
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
        
        print("Response:")
        print(response.content)
        
        # Check if there were any tool calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"\nTool calls made: {len(response.tool_calls)}")
            for i, tool_call in enumerate(response.tool_calls):
                print(f"Tool call {i+1}: {tool_call.name}")
                print(f"Arguments: {tool_call.arguments}")

if __name__ == "__main__":
    test_google_docs_tool()
