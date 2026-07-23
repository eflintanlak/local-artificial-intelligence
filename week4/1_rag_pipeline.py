from foundry_local_sdk import FoundryLocalManager, Configuration
import sqlite3
import json
import math

config = Configuration(app_name="local-ai-assistant")
manager = FoundryLocalManager(config)
catalog = manager.catalog

# Load both models
embedding_model = catalog.get_model("qwen3-embedding-0.6b")
embedding_model.load()
embedding_client = embedding_model.get_embedding_client()

chat_model = catalog.get_model("qwen3-0.6b")
chat_model.load()
chat_client = chat_model.get_chat_client()

def get_embedding(text):
    response = embedding_client.generate_embedding(text)
    return response.data[0].embedding

def cosine_similarity(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(a * a for a in vector1))
    magnitude2 = math.sqrt(sum(b * b for b in vector2))
    return dot_product / (magnitude1 * magnitude2)

def get_top_chunks(query, top_k=2):
    query_embedding = get_embedding(query)
    
    conn = sqlite3.connect("knowledge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT source, content, embedding FROM chunks")
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for source, content, embedding_json in rows:
        chunk_embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, chunk_embedding)
        results.append({
            "source": source,
            "content": content,
            "score": score
        })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

def answer_query(question):
    # Step 1: Retrieve relevant chunks
    top_chunks = get_top_chunks(question)
    
    # Step 2: Build context from retrieved chunks
    context = "\n\n".join([chunk["content"] for chunk in top_chunks])
    
    # Step 3: Build the prompt with system instructions
    system_message = f"""You are a helpful assistant that answers questions about aircraft electrical and electronics systems.
Answer ONLY using the following context. If the answer is not in the context, say "I don't have that information."

Context:
{context}"""
    
    # Step 4: Send to chat model
    response = chat_client.complete_chat(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
    )
    
    answer = response.choices[0].message.content
    if "</think>" in answer:
        answer = answer.split("</think>")[-1].strip()
    
    return answer, top_chunks

# Test it
question = "How does the pitot tube measure airspeed?"
answer, sources = answer_query(question)

print(f"Question: {question}\n")
print(f"Answer: {answer}\n")
print("Sources used:")
for source in sources:
    print(f"  - {source['source']} (score: {source['score']:.4f})")