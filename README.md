# Sheria-DB

This is a project to create a vector database of Kenyan laws and regulations.

Instructions:

1. Install the requirements
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Set up the environment variables
```
export QDRANT_API_KEY=your_qdrant_api_key
```
3. Run the script to load the data into the vector database
```
python test_embedder.py
```
