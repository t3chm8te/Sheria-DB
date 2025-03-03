import os
import numpy as np
from typing import List, Dict
import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from embedder import get_embedding_function
from qdrant_connection import QdrantCollectionManager

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
qdrant_manager = QdrantCollectionManager()

embedding_model = get_embedding_function()

class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    score: float
    text: str
    metadata: Dict

class SearchResponse(BaseModel):
    results: List[SearchResult]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000"
    ],

    allow_methods=["GET", "POST"],

    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
    

@app.post("/search/", response_model=SearchResponse)
async def search_endpoint(search_query: SearchQuery):
    try:
        
        logging.info(f"Received search query: {search_query.query}")
        
        
        query_embedding = list(embedding_model.embed([search_query.query]))[0]
        query_embedding = np.array(query_embedding)
        
        
        logging.info(f"Query embedding shape: {query_embedding.shape}")
        
        
        search_result = qdrant_manager.vector_search(query_embedding, top_k=5)
        
        
        logging.info(f"Search results: {search_result}")
        
        
        api_results = []
        for result in search_result:
            result_dict = {
                "score": float(result["score"]),  
                "text": str(result["text"]),      
                "metadata": dict(result["metadata"])  
            }
            api_results.append(SearchResult(**result_dict))
        
        return SearchResponse(results=api_results)

    except ValueError as e:
        logging.error(f"ValueError in search endpoint: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error(f"Search endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during the search."
        )
    

@app.get("/documents/")
async def list_documents():
    files = [f for f in os.listdir('../Dataset/sample') if f.endswith('.pdf')]
    return files

@app.get("/documents/{document_name}")
async def get_document(document_name: str):
    return FileResponse(f"Dataset/sample/{document_name}")