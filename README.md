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

## 📁 Structure

```
backend/
├── main.py                    # Entry point - run this
├── src/content_maker/         # Main package
│   ├── core/                  # Core functionality
│   ├── processors/            # Source processing modules
│   └── utils/                 # Utilities
├── tests/                     # Test suite
├── sources/                   # Add your files here
├── config/tensorzero.toml     # Model config
└── tensorzero_storage/        # Auto-created
```