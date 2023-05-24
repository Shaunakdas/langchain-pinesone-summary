import os
import tempfile
import streamlit as st
import pinecone
from langchain.llms.openai import OpenAI
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader

# Streamlit app
st.subheader('Summarize Documents with LangChain & Pinecone')

# Get OpenAI API key, Pinecone API key, environment, index, and the source document input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API key", type="password")
    pinecone_api_key = st.text_input("Pinecone API key", type="password")
    pinecone_env = st.text_input("Pinecone environment")
    pinecone_index = st.text_input("Pinecone index name")
source_doc = st.file_uploader("Upload source document", type="pdf", label_visibility="collapsed")

if st.button("Summarize"):
    # Validate inputs
    if not openai_api_key or not pinecone_api_key or not pinecone_env or not pinecone_index or not source_doc:
        st.warning("Please upload the document and provide the missing fields.")
    else:
        try:
            # Save uploaded file temporarily to disk, load and split the file into pages, delete temp file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(source_doc.read())
            document_loader = PyPDFLoader(temp_file.name)
            pages = document_loader.load_and_split()
            os.remove(temp_file.name)

            # Create embeddings for the pages and insert into Pinecone vector database
            pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
            openai_embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            vector_store = Pinecone.from_documents(pages, openai_embeddings, index_name=pinecone_index)

            # Initialize the OpenAI module, load and run the summarize chain
            openai_llm = OpenAI(temperature=0, openai

