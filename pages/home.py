import streamlit as st

class StreamlitApp:

    def __init__(self):
        None

    def run(self):
        st.title("Sheria PDF Viewer and Search Similarity")

        tab1, tab2 = st.tabs(["View Documents", "Similarity Search"])

        with tab1:
            st.header("View PDF Documents")
            documents = fetch_documents_with_pdfs(collection, limit=10)
            if documents:
                for doc in documents:
                    st.subheader(f"Document ID: {doc['_id']}")
                    pdf_data = decode_pdf(doc["pdf"])
                    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_data}" width="700" height="500"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.warning("No PDF documents found in the collection.")