# backend/retriever.py
import glob
import json

def load_sources(path="sources/*.json"):
    """Load all JSON files from the sources folder."""
    sources = []
    for file in glob.glob(path):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            sources.append(data["content"])
    return sources

def chunk_text(text, chunk_size=500):
    """Split long text into word chunks of ~chunk_size words."""
    words = text.split()
    return [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

def build_chunks():
    """Load all sources and break them into chunks."""
    chunks = []
    for content in load_sources():
        chunks.extend(chunk_text(content))
    return chunks

def get_relevant_chunks(query, chunks, top_k=3):
    """Retrieve top_k chunks matching query words (naive keyword search)."""
    return [
        c for c in chunks
        if any(word in c.lower() for word in query.lower().split())
    ][:top_k]
