def split_text_into_chunks(text, chunk_size=500):
    """Splits the input text into smaller chunks for embedding generation."""
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks
