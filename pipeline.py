import logging
from Backend.embedder import loader, splitter, generate_embeddings
from Backend.qdrant_connection import QdrantCollectionManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline(pdf_path: str, collection_name: str = "sheria db"):
    logging.info(f"Starting pipeline for PDF directory: {pdf_path}")
    
    # Load documents from the specified PDF directory
    documents = loader(pdf_path)
    logging.info(f"Loaded {len(documents)} documents from {pdf_path}")
    
    # Log each document loaded
    for doc in documents:
        logging.info(f"Loaded document: {doc.metadata.get('title', 'Untitled')}")

    # Split the loaded documents into chunks
    chunks = splitter(documents)
    logging.info(f"Split documents into {len(chunks)} chunks.")
    
    # Log each chunk created
    for i, chunk in enumerate(chunks):
        logging.info(f"Created chunk {i + 1}: {chunk.page_content[:50]}...")  # Log first 50 characters of the chunk

    # Generate embeddings for the chunks
    embeddings = generate_embeddings(chunks)
    logging.info(f"Generated embeddings for {len(embeddings)} chunks.")
    
    # Log each embedding generated
    for i, embedding in enumerate(embeddings):
        logging.info(f"Generated embedding {i + 1} for chunk: {embedding[1][:50]}...")  # Log first 50 characters of the chunk text

    # Initialize QdrantCollectionManager and store embeddings
    qdrant_manager = QdrantCollectionManager(collection_name=collection_name)
    qdrant_manager.store_embeddings(embeddings)
    logging.info(f"Stored embeddings in collection: {collection_name}")


if __name__ == "__main__":
    pdf_directory = r"C:\Users\TBC-TRM\Desktop\Python-Projects\sheria-db\Dataset\Kenyan Legislation and Policy"
    run_pipeline(pdf_directory)