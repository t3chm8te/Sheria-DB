import embedder
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
    
    try:
        # 1. Load documents
        logger.info("Loading documents")
        documents = embedder.loader(pdf_path)
        
        # 2. Split documents
        logger.info("Splitting documents")
        chunks = embedder.splitter(documents)
        
        # 3. Generate embeddings
        logger.info("Generating embeddings")
        embeddings = embedder.generate_embeddings(chunks)
        
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
