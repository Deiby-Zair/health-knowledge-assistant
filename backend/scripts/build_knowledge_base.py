from backend.src.ingest.fetch_faqs import main as fetch_faqs
from backend.src.ingest.fetch_glossary import main as fetch_glossary
from backend.src.ingest.process_pdfs import main as process_pdfs
from backend.src.ingest.clean_faqs import main as clean_faqs
from backend.src.ingest.clean_glossary import main as clean_glossary
from backend.src.ingest.create_chunks import main as create_chunks

from create_collection import main as create_collection
from ingest_qdrant import main as ingest

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