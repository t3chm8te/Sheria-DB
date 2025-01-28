from embedder import loader, splitter, generate_embeddings
from qdrant_connection import QdrantCollectionManager
from fastembed import TextEmbedding
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
        # Load and process documents
        from embedder import loader, splitter, generate_embeddings
        documents = loader(pdf_path)
        chunks = splitter(documents)
        embeddings = generate_embeddings(chunks)
        
        # Store in Qdrant
        vector_store = QdrantCollectionManager()
        vector_store.store_embeddings(embeddings)
        
        return vector_store

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

def search_documents(query: str, top_k: int = 5):
    """Search for similar documents"""
    try:
        # Generate query embedding
        model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        query_embedding = list(model.embed([query]))[0]
        
        # Perform search
        vector_store = QdrantCollectionManager()
        return vector_store.vector_search(query_embedding, top_k=top_k)
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Process documents (only need to run once)
    # process_pipeline()
    
    # Example search
    query = "When can access to information be withdrawn?"
    results = search_documents(query)
    
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Score: {result['score']:.4f}")
        print(f"Text: {result['text'][:200]}...")  # Show first 200 chars
        print(f"Metadata: {result['metadata']}")