from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from fastembed import TextEmbedding
import numpy as np
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO)

def get_embedding_function():
    embedding = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return embedding

def loader(pdf_path: str) -> List[Document]:
    logging.info(f"Loading PDF files from {pdf_path}")
    directory_loader = PyPDFDirectoryLoader(pdf_path, glob="**/*.pdf")
    documents = directory_loader.load()
    logging.info(f"Loaded {len(documents)} documents from {pdf_path}")
    return documents

def splitter(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    logging.info(f"Splitting PDF files from {documents}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )

    chunks = text_splitter.split_documents(documents)
    logging.info(f"Split into {len(chunks)} chunks.")
    return chunks

def generate_embeddings(chunks: List[Document], batch_size: int = 100) -> List[Tuple[np.ndarray, str, dict]]:
    if not chunks:
        logging.warning("No chunks provided for embedding")
        return []
    
    logging.info(f"Generating embeddings for {len(chunks)} chunks")
    model = get_embedding_function()
    
    # Extract text and metadata from documents
    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]
    
    # Generate embeddings in batch
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_embeddings = list(model.embed(batch_texts))
        embeddings.extend(batch_embeddings)
    
    # Return tuples of (embedding, text, metadata)
    return list(zip(embeddings, texts, metadatas))

files = loader("Dataset\sample")

logging.info("Starting PDF loader")
print(loader("Dataset\sample"))
logging.info("PDF loader completed")

logging.info("Starting PDF splitter")
print(splitter(files))
logging.info("PDF splitter completed")

logging.info("Starting embedding generation")
print(generate_embeddings(splitter(files)))
logging.info("Embedding generation completed")