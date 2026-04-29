import faiss
import numpy as np

# Global index (simple version)
dimension = 384
index = faiss.IndexFlatL2(dimension)

# Store mapping (important)
chunk_store = []

def add_embeddings(embeddings, chunks):
    global index, chunk_store

    vectors = np.array(embeddings).astype("float32")
    index.add(vectors)

    chunk_store.extend(chunks)

def search(query_embedding, k=3):
    if index.ntotal == 0:
        return []

    vector = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(vector, k)

    results = []
    for i in indices[0]:
        if 0 <= i < len(chunk_store):
            results.append(chunk_store[i])

    return results
