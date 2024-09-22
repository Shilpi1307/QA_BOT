import cohere
import os

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)
def generate_embeddings(text_chunks):
    """Generates embeddings for text chunks using Cohere's embedding model."""
    embeddings = co.embed(texts=text_chunks).embeddings
    return embeddings

def generate_response(context, query):
    """Generates an answer based on the context and query using Cohere's generation API."""
    prompt = f"Using the following context, answer the question: {context}\nQuestion: {query}\nAnswer:"
    response = co.generate(
        model='command-xlarge-nightly',  
        prompt=prompt,
        max_tokens=100
    )
    return response.generations[0].text.strip()
