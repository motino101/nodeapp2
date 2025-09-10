# Google Docs Integration Setup

This guide explains how to set up and use the Google Docs extraction functionality using TensorZero's tool use feature.

## Prerequisites

1. **Google API Key**: You need a Google API key with access to the Google Docs API
2. **Google Doc Access**: The document must be either public or accessible with your API key

## Setup Google API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Docs API
4. Create credentials (API Key)
5. Restrict the API key to Google Docs API for security

## How It Works

The Google Docs extraction uses TensorZero's tool use functionality:
- **Tool**: `extract_google_doc_content` - Handles the actual API calls to Google Docs
- **Function**: `extract_google_doc` - Uses GPT-4o-mini to intelligently process the extraction
- **Automatic Detection**: The system automatically detects Google Docs URLs in your sources
- **Natural Language**: You can request extraction using natural language prompts

## Automatic Google Docs Detection

The system now automatically detects Google Docs URLs in your source files and extracts their content:

1. **Automatic Detection**: When you run `main.py`, it scans all sources for Google Docs URLs
2. **Content Extraction**: Any Google Docs URLs found are automatically extracted
3. **Source Integration**: The extracted content is added to your sources list
4. **Seamless Workflow**: The extracted content flows through the threading and synthesis process

### Setting Up Automatic Detection

1. **Set Environment Variable**:
   ```bash
   export GOOGLE_API_KEY='your_google_api_key_here'
   ```

2. **Add Google Docs URLs to Sources**: Simply include Google Docs URLs in your source files:
   ```json
   {
     "content": "Check out my research notes: https://docs.google.com/document/d/123/edit. This contains important insights."
   }
   ```

3. **Run Your Workflow**: The system will automatically detect and extract the Google Docs content:
   ```bash
   python main.py
   ```

## Usage Options

### Option 1: Command Line Extraction

Extract a Google Doc and save it as a source file:

```bash
python extract_google_doc.py "https://docs.google.com/document/d/YOUR_DOC_ID/edit" "YOUR_API_KEY" "my_document.json"
```

This will:
- Extract the content from the Google Doc
- Save it to `sources/my_document.json`
- Format it as a proper source file

### Option 2: Integration in Main Workflow

Add Google Doc extraction directly to your main.py:

```python
from google_docs_helper import extract_and_add_google_doc

# After building your sources list
google_doc_url = "https://docs.google.com/document/d/YOUR_DOC_ID/edit"
api_key = "YOUR_API_KEY"
sources = extract_and_add_google_doc(google_doc_url, api_key, sources)
```

### Option 3: Load from Previously Extracted File

If you've already extracted a Google Doc:

```python
from google_docs_helper import load_google_doc_from_file

google_doc_source = load_google_doc_from_file("sources/my_google_doc.json")
if google_doc_source:
    sources.append(google_doc_source)
```

## File Format

The extracted Google Doc content is saved in the same format as your other sources:

```json
{
  "content": "The full text content of your Google Doc..."
}
```

## Error Handling

The system handles various error cases:
- Invalid Google Doc URLs
- API key issues
- Permission problems
- Network connectivity issues

## Security Notes

- Keep your API key secure and don't commit it to version control
- Consider using environment variables for API keys
- Restrict your API key to only the necessary Google APIs

## Example Workflow

1. Extract Google Doc content:
   ```bash
   python extract_google_doc.py "https://docs.google.com/document/d/123/edit" "your_key" "research_notes.json"
   ```

2. Run your main workflow:
   ```bash
   python main.py
   ```

3. The Google Doc content will be included in the threading and synthesis process

## Troubleshooting

- **"Extraction failed"**: Check your API key and document permissions
- **"Invalid URL"**: Ensure the Google Doc URL is correct and accessible
- **"API quota exceeded"**: You may have hit Google API limits
