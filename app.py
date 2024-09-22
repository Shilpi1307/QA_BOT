import os
import re
import streamlit as st
from dotenv import load_dotenv
from app.pdf_processing import process_pdf
from app.embedding import split_text_into_chunks
from app.cohere_manager import generate_embeddings, generate_response
from app.pinecone_manager import get_or_create_index, upsert_embeddings, query_index

# Load environment variables
load_dotenv()

# Streamlit app interface
st.title("Document-Based QA Bot")

# Step 1: Upload a PDF document
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

# Step 2: Process the PDF and generate embeddings
if uploaded_file is not None:
    with st.spinner("Processing PDF..."):
        # Extract text from the PDF
        document_text = process_pdf(uploaded_file)

        # Split the text into chunks
        document_chunks = split_text_into_chunks(document_text)

        # Generate embeddings for each chunk
        embeddings = generate_embeddings(document_chunks)

        # Create a unique index based on the document name
        base_name = uploaded_file.name.split(".")[0]
        index = get_or_create_index(embeddings, base_name)

        # Store embeddings in Pinecone index
        upsert_embeddings(index, document_chunks, embeddings)

        st.success("PDF processed and embeddings generated!")

# Step 3: Ask a question
query = st.text_input("Ask a question based on the document")

if query and uploaded_file:
    with st.spinner("Retrieving and generating answer..."):
        # Generate the embedding for the query
        query_embedding = generate_embeddings([query])[0]

        # Perform retrieval from Pinecone index
        results = query_index(index, query_embedding)

        # Combine the retrieved document chunks
        retrieved_docs = [match['id'] for match in results['matches']]
        context = ' '.join(retrieved_docs)

        # Generate an answer using the Cohere API
        answer = generate_response(context, query)

        # Display the retrieved context and the generated answer
        st.subheader("Retrieved Document Context:")
        st.write(context)

        st.subheader("Generated Answer:")
        st.write(answer)
