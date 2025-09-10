# Content Maker

AI-powered content creation system that processes sources and synthesises them into focused thematic content.

## 🚀 How It Works

1. **Add Sources** to `backend/sources/` folder:
   - Images (`.jpg`, `.png`, `.gif`) - AI will analyze them
   - Text files with Google Docs links
   - Text files with webpage URLs
   - Any JSON/text files

2. **Run** `python main.py`

3. **Pipeline**:
   - Auto-detects and extracts Google Docs, scrapes webpages, analyzes images with AI vision
   - Draws thematic threads from sources, asks you to select a thread to make content about
   - Generates video scripts with hooks, context, and shotlists using Claude Sonnet

Built using TensorZero - see `toml` file for different variants, and use TensorZero UI to see inferences/results.

## 🛠️ Quick Setup

1. **Install & Start**:
   ```bash
   cd backend
   pip install -r requirements.txt
   docker compose up -d
   ```

2. **Set Google API Key**:
   ```bash
   export GOOGLE_API_KEY='your_key_here'
   ```

3. **Run**:
   ```bash
   python main.py
   ```

## 📖 Source Examples

**Google Docs** (must be public):
```json
{"content": "Research notes: https://docs.google.com/document/d/123/edit"}
```

**Webpages**:
```json
{"content": "Interesting article: https://example.com/article"}
```

**Images**: Drop `.jpg`, `.png`, `.gif` files directly

## 🔧 Google Docs Setup

1. **Get API Key**: [Google Cloud Console](https://console.cloud.google.com/) → Enable Google Docs API → Create API Key
2. **Make Docs Public**: Share → "Anyone with link" → "Viewer"
3. **Add URLs**: Include Google Docs URLs in your source files

## 🏗️ Models Used

- **Claude Sonnet**: Threading ideas and content synthesis
- **GPT-4o-mini**: Image analysis and Google Docs extraction

## 🎯 Example Output

```
Processing 9 sources...
Found threads:
1. Digital Gardens as Intentional Spaces
2. Community Building in AI Era  
3. Growth Over Perfection Philosophy

Which thread? (1-3): 1

Generated video script:
- Hook: "In an age of AI noise, why do some spaces feel alive?"
- Context: [3 detailed points]
- Takeaway: "Gardening is human curation, not endless generation"
- Shotlist: [8 specific shots]
```

## 📁 Project Structure

```
nodeapp2/
├── backend/                    # Main application
│   ├── main.py                # Entry point - run this
│   ├── src/content_maker/     # Main package
│   │   ├── core/              # Core functionality
│   │   │   ├── main.py        # Main application logic
│   │   │   └── retriever.py   # Source retrieval and chunking
│   │   └── processors/        # Source processing modules
│   │       ├── image_processor.py  # Multimodal image analysis
│   │       ├── source_detector.py  # Smart source type detection
│   │       └── web_scraper.py      # Web scraping functionality
│   ├── tests/                 # Test suite
│   ├── sources/               # Add your files here
│   ├── config/tensorzero.toml # Model config
│   └── tensorzero_storage/    # Auto-created
└── README.md                  # This file
```

## 📦 Package Architecture

### Core Modules

- **`core/main.py`**: Main application logic and workflow orchestration
- **`core/retriever.py`**: Source retrieval and text chunking functionality

### Processors

- **`processors/image_processor.py`**: Multimodal AI image analysis using GPT-4o-mini
- **`processors/source_detector.py`**: Smart detection and processing of different source types
- **`processors/web_scraper.py`**: Web scraping and content extraction


## 🧪 Testing

Run the test suite:

```bash
cd backend

# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_image_processing.py
python tests/test_web_scraping.py
```

## 🔧 Development


### Code Style

The project follows Python best practices:
- Clean package structure with minimal boilerplate
- Relative imports within the package
- Separation of concerns across modules
- Comprehensive test coverage

## 📁 Source Types Supported

- **Images**: `.jpg`, `.png`, `.gif` - Analyzed with AI vision
- **Google Docs**: Public documents with URLs
- **Webpages**: Any accessible web content
- **Text/JSON**: Plain text and structured data

## 🔄 Workflow

1. **Source Detection**: Automatically detects and categorizes source types
2. **Content Processing**: Extracts and processes content from each source
3. **Threading**: AI identifies thematic threads across sources
4. **Synthesis**: Generates focused content based on selected threads
5. **Output**: Produces structured video scripts with hooks, context, and shotlists

## 🎯 Features

- **Unified Episode Tracking**: All inferences in a workflow are grouped under a single episode ID for better observability
- **Smart Source Detection**: Automatically processes different file types and URLs
- **Multimodal AI**: Analyzes images with AI vision capabilities
- **Web Scraping**: Extracts content from webpages automatically
- **Google Docs Integration**: Processes public Google Docs documents
- **Interactive Threading**: AI identifies themes and lets you choose focus areas
- **Structured Output**: Generates complete video scripts with hooks, context, and shotlists

## 🚀 Getting Started

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies and start TensorZero
4. Add your sources to the `sources/` folder
5. Run `python main.py`
6. Follow the interactive prompts to generate content

## 📊 Observability

The system uses TensorZero for observability:
- All inferences are tracked with unified episode IDs
- View detailed logs and metrics in TensorZero UI
- Monitor performance and usage patterns
- Track user feedback and ratings