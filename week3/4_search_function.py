from foundry_local_sdk import FoundryLocalManager, Configuration
import sqlite3
import json
import math

config = Configuration(app_name="local-ai-assistant")
manager = FoundryLocalManager(config)
catalog = manager.catalog

model = catalog.get_model("qwen3-embedding-0.6b")
model.load()
client = model.get_embedding_client()

def get_embedding(text):
    response = client.generate_embedding(text)
    return response.data[0].embedding

def cosine_similarity(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(a * a for a in vector1))
    magnitude2 = math.sqrt(sum(b * b for b in vector2))
    return dot_product / (magnitude1 * magnitude2)

def get_top_chunks(query, top_k=2):
    # Get embedding for the user's question
    query_embedding = get_embedding(query)
    
    # Load all chunks from database
    conn = sqlite3.connect("knowledge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT source, content, embedding FROM chunks")
    rows = cursor.fetchall()
    conn.close()
    
    # Calculate similarity for each chunk
    results = []
    for source, content, embedding_json in rows:
        chunk_embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, chunk_embedding)
        results.append({
            "source": source,
            "content": content,
            "score": score
        })
    
    # Sort by score, highest first
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Return only the top K results
    return results[:top_k]

# Test the search function
query = "How does the pitot tube measure airspeed?"
top_chunks = get_top_chunks(query)

print(f"Query: {query}\n")
print("Top matching chunks:\n")
for chunk in top_chunks:
    print(f"Score: {chunk['score']:.4f} | Source: {chunk['source']}")
    print(f"  {chunk['content']}\n")