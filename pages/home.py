import base64
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from test_embedder import process_pipeline, search_documents

class StreamlitApp:

    def __init__(self):
        self.vector_store = process_pipeline()

    def run(self):
        st.title("Sheria PDF Viewer and Search Similarity")

        tab1, tab2 = st.tabs(["View Documents", "Similarity Search"])

        with tab1:
            st.header("View PDF Documents")
            # Display PDF documents from Dataset/sample directory
            st.info("PDF documents are loaded from Dataset/sample directory")
            
            # Add file uploader for viewing PDFs
            uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
            if uploaded_file is not None:
                # Display uploaded PDF
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(uploaded_file.read()).decode()}" width="700" height="500"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

        with tab2:
            st.header("Search Documents")
            query = st.text_input("Enter your search query:")
            
            if query:
                results = search_documents(query, top_k=5)
                
                for i, result in enumerate(results, 1):
                    with st.expander(f"Result {i} (Score: {result['score']:.4f})"):
                        st.markdown("**Relevant Text:**")
                        st.write(result['text'])
                        
                        st.markdown("**Source:**")
                        if 'metadata' in result:
                            st.write(f"Document: {result['metadata'].get('source', 'Unknown')}")
                            st.write(f"Page: {result['metadata'].get('page', 'Unknown')}")

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
