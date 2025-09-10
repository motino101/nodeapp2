# Content Maker Backend

AI-powered content creation system that processes sources and synthesises them into focused thematic content.

## 🏗️ Architecture

The backend is organized into a clean package structure:

```
backend/
├── src/
│   └── content_maker/
│       ├── core/                    # Core functionality
│       │   ├── main.py             # Main application logic
│       │   └── retriever.py        # Source retrieval and chunking
│       ├── processors/             # Source processing modules
│       │   ├── image_processor.py  # Multimodal image analysis
│       │   ├── source_detector.py  # Smart source type detection
│       │   └── web_scraper.py      # Web scraping functionality
│       └── utils/                  # Utility functions
├── tests/                          # Test suite
├── config/                         # TensorZero configuration
├── sources/                        # Input sources directory
└── main.py                         # Entry point
```

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start TensorZero**:
   ```bash
   docker compose up -d
   ```

3. **Set environment variables**:
   ```bash
   export GOOGLE_API_KEY='your_key_here'
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## 📦 Package Structure

### Core Modules

- **`core/main.py`**: Main application logic and workflow orchestration
- **`core/retriever.py`**: Source retrieval and text chunking functionality

### Processors

- **`processors/image_processor.py`**: Multimodal AI image analysis using GPT-4o-mini
- **`processors/source_detector.py`**: Smart detection and processing of different source types
- **`processors/web_scraper.py`**: Web scraping and content extraction

### Utils

- **`utils/`**: Common utility functions and helpers

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_image_processing.py
python tests/test_web_scraping.py
```

## 🔧 Development

### Installing in Development Mode

```bash
pip install -e .
```

### Code Style

The project follows Python best practices:
- Clean package structure with proper `__init__.py` files
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
