import pinecone
import os
import re
import uuid
from pinecone import ServerlessSpec, Pinecone

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# Initialize Pinecone
if PINECONE_API_KEY:
    pc = Pinecone(api_key=PINECONE_API_KEY)

# Function to create or connect to an index
def get_or_create_index(embeddings, base_name):
    """Creates or connects to a Pinecone index for storing embeddings."""
    embedding_dimension = len(embeddings[0])
    first_word = base_name.split()[0] 
    cleaned_name = re.sub(r'[^a-z0-9-]', '-', first_word.lower())  
    
    index_name = f'document-index-{cleaned_name}'
    existing_indexes = pc.list_indexes()

    # If the index exists, connect to it
    if index_name in existing_indexes:
        index = pc.Index(index_name)
    else:
        pc.create_index(
            name=index_name,
            dimension=embedding_dimension,
            metric='euclidean',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
        index = pc.Index(index_name)
    
    return index

# Function to upsert embeddings
def upsert_embeddings(index, document_chunks, embeddings):
    """Upserts document chunks and their embeddings to Pinecone index."""
    for i, chunk in enumerate(document_chunks):
        vector_id = str(uuid.uuid4())
        index.upsert(vectors=[(vector_id, embeddings[i])])

# Function to query the index
def query_index(index, query_embedding, top_k=5):
    """Queries the Pinecone index for the closest matches to the query embedding."""
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return results
