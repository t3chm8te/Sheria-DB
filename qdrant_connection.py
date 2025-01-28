import os
import uuid
import logging
import numpy as np
from dotenv import load_dotenv
from typing import List, Tuple
from qdrant_client import QdrantClient
from qdrant_client.http import models

load_dotenv('.env')
logging.basicConfig(level=logging.INFO)

class QdrantCollectionManager:
    def __init__(self, collection_name: str = "test", vector_size: int = 384, distance_metric: str = "Cosine", https=False):
        
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance_metric = distance_metric

        self.client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"), https=https)

        self._create_collection()

    #Creates qdrant_collection
    def _create_collection(self):
        
        try:
            if not self.client.collection_exists(self.collection_name):
                self.client.recreate_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=self.distance_metric
                    )
                )
                logging.info(f"Created collection {self.collection_name}")
        except Exception as e:
            logging.error(f"Collection creation failed: {str(e)}")
            raise
    
    #Stores embeddings in qdrant_collection
    def store_embeddings(self, embeddings: List[Tuple[np.ndarray, str, dict]]):

        if not embeddings:
            logging.warning("No embeddings to store")
            return

        #Create points to store in qdrant_collection
        try:    
            points = [
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.tolist(),
                    payload={"text": text, "metadata": metadata}
                )
                for embedding, text, metadata in embeddings
            ]

            #Store points in qdrant_collection
            self.client.upsert(
                collection_name=self.collection_name,
                wait=True,
                points=points                
            )
            logging.info(f"Stored {len(points)} vectors.")     
       
        except Exception as e:
            logging.error(f"Storage failed: {str(e)}")
            raise

    def vector_search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[dict]:
        
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding.tolist(),
                limit=top_k
            )
            return [
                {
                    "score": result.score,
                    "text": result.payload["text"],
                    "metadata": result.payload["metadata"]
                }
                for result in results
            ]
        except Exception as e:
            logging.error(f"Search failed: {str(e)}")
            raise




    