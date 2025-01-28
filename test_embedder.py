from embedder import loader, splitter, generate_embeddings
from qdrant_connection import QdrantCollectionManager
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_pipeline(pdf_path: str = "Dataset/sample"):
    """End-to-end processing pipeline"""
    try:
        # 1. Load documents
        logger.info("Loading documents")
        documents = loader(pdf_path)
        
        # 2. Split documents
        logger.info("Splitting documents")
        chunks = splitter(documents)
        
        # 3. Generate embeddings
        logger.info("Generating embeddings")
        embeddings = generate_embeddings(chunks)
        
        # 4. Store in Qdrant
        logger.info("Initializing vector store")
        vector_store = QdrantCollectionManager()
        vector_store.store_embeddings(embeddings)
        
        logger.info("Pipeline completed successfully")
        return vector_store.client

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    process_pipeline()
