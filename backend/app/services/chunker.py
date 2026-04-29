def chunk_text(text, chunk_size=100):
    if not text:
        return []

    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks
