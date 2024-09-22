import os
import streamlit as st
import cohere
import pinecone
import fitz  
import pickle
from dotenv import load_dotenv
from pinecone import ServerlessSpec,Pinecone

# Load environment variables from .env
load_dotenv()

# Initialize API keys
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

if PINECONE_API_KEY:
    print("API Key loaded successfully!")
else:
    print("API Key not found. Please check your .env file.")

# Initialize Cohere and Pinecone
co = cohere.Client(COHERE_API_KEY)

pc = Pinecone(
    api_key='84816fb8-2e89-408a-b2e4-8396999a56c4'  # Replace with your Pinecone API key
)

# # Initialize Pinecone
# pc = pinecone(api_key=PINECONE_API_KEY)
# # Check if the index exists, otherwise create it
# if PINECONE_INDEX_NAME not in pc.list_indexes().names():
#     pc.create_index(
#         name=PINECONE_INDEX_NAME, 
#         dimension=4096,  # Cohere embedding size is 4096
#         metric='euclidean',
#         spec=ServerlessSpec(cloud='aws', region='us-east-1')
#     )

# # Connect to the index
index = pc.Index(PINECONE_INDEX_NAME)

# Function to load embeddings and chunks from pickle files
def load_embeddings_and_chunks():
    with open('embeddings.pkl', 'rb') as f_emb, open('chunks.pkl', 'rb') as f_chunks:
        embeddings = pickle.load(f_emb)
        chunks = pickle.load(f_chunks)
    return embeddings, chunks

# Function to process the uploaded PDF and extract text
def process_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to split text into smaller chunks for embedding generation
def split_text_into_chunks(text, chunk_size=500):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

# Function to generate embeddings for the document chunks
def generate_embeddings(chunks):
    embeddings = co.embed(texts=chunks).embeddings
    return embeddings

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

        # Save embeddings and chunks to pickle files
        with open('embeddings.pkl', 'wb') as f_emb, open('chunks.pkl', 'wb') as f_chunks:
            pickle.dump(embeddings, f_emb)
            pickle.dump(document_chunks, f_chunks)

        st.success("PDF processed and embeddings generated!")

# Step 3: Ask a question
query = st.text_input("Ask a question based on the document")

if query:
    with st.spinner("Retrieving and generating answer..."):
        # Generate embedding for the query
        query_embedding = co.embed(texts=[query]).embeddings[0]

        # Perform retrieval from Pinecone index
        results = index.query(vector=query_embedding, top_k=5, include_metadata=True)

        # Combine the retrieved document chunks
        retrieved_docs = [match['metadata']['text'] for match in results['matches']]
        context = ' '.join(retrieved_docs)

        # Generate an answer using the Cohere API
        response = co.generate(
            model='command',
            prompt=f"Using the following context, answer the question: {context}\nQuestion: {query}\nAnswer:",
            max_tokens=100
        )

        # Display the retrieved context and the generated answer
        st.subheader("Retrieved Document Context:")
        st.write(context)

        st.subheader("Generated Answer:")
        st.write(response.generations[0].text.strip())
