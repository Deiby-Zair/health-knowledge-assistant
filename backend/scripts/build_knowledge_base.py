from scripts.sources.fetch_faqs import main as fetch_faqs
from scripts.sources.fetch_glossary import main as fetch_glossary
from scripts.processing.process_pdfs import main as process_pdfs
from scripts.processing.clean_faqs import main as clean_faqs
from scripts.processing.clean_glossary import main as clean_glossary
from scripts.processing.create_chunks import main as create_chunks

from scripts.indexing.create_collection import main as create_collection
from scripts.indexing.ingest_qdrant import main as ingest

def main():
    fetch_faqs()
    fetch_glossary()
    process_pdfs()
    clean_faqs()
    clean_glossary()
    create_chunks()
    
    create_collection()
    ingest()
    print("Knowledge base loaded.")

if __name__ == "__main__":
    main()