import streamlit as st
from foundry_local_sdk import FoundryLocalManager, Configuration
import sqlite3
import json
import math

# Page setup
st.set_page_config(page_title="Aircraft AI Assistant", page_icon="✈️")

st.title("✈️ Aircraft Electrical & Electronics Assistant")
st.write("Ask questions about aircraft electrical systems, avionics, and more — powered by a local AI running entirely on this computer.")

# Load models (cached so it only happens once)
@st.cache_resource
def load_models():
    config = Configuration(app_name="local-ai-assistant")
    manager = FoundryLocalManager(config)
    catalog = manager.catalog

    embedding_model = catalog.get_model("qwen3-embedding-0.6b")
    embedding_model.load()
    embedding_client = embedding_model.get_embedding_client()

    chat_model = catalog.get_model("qwen3-0.6b")
    chat_model.load()
    chat_client = chat_model.get_chat_client()

    return embedding_client, chat_client

with st.spinner("Loading AI models..."):
    embedding_client, chat_client = load_models()

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
    top_chunks = get_top_chunks(question)
    context = "\n\n".join([chunk["content"] for chunk in top_chunks])
    
    system_message = f"""You are a strict assistant that ONLY answers using the provided context below. 
You must NEVER use any outside knowledge, even if you know the answer.
If the context does not contain the answer, respond EXACTLY with: "I don't have that information."

Context:
{context}"""
    
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

# User input
question = st.text_input("Your question:", placeholder="e.g. What is fly-by-wire?")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        answer, sources = answer_query(question)
    
    st.subheader("Answer")
    st.write(answer)
    
    st.subheader("Sources")
    for source in set(s["source"] for s in sources):
        st.caption(f"📄 {source}")