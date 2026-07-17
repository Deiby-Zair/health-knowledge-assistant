# Health Knowledge Assistant

RAG-based assistant built with LangChain and ChromaDB using official information from the Colombian Ministry of Health (FAQs, glossary, and PDF documents).

## Features
- SharePoint FAQ extraction
- Glossary extraction
- HTML cleaning and normalization
- PDF text preprocessing
- Document chunking for embeddings
- ChromaDB vector store generation

## Structure
- `src/ingest`: data extraction and preprocessing
- `src/embeddings`: vector store creation
- `src/rag`: retrieval and generation logic
- `data/processed`: cleaned data
- `data/chunks`: chunked documents
