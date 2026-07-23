from foundry_local_sdk import FoundryLocalManager, Configuration
import sqlite3
import json

config = Configuration(app_name="local-ai-assistant")
manager = FoundryLocalManager(config)
catalog = manager.catalog

model = catalog.get_model("qwen3-embedding-0.6b")
model.load()
client = model.get_embedding_client()

def get_embedding(text):
    response = client.generate_embedding(text)
    return response.data[0].embedding

# Connect to database
conn = sqlite3.connect("knowledge.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY,
        content TEXT,
        embedding TEXT
    )
""")

# Documents to store
documents = [
    "The cat is sleeping",
    "The car is going fast",
    "The weather is nice today"
]

# Save each document with its embedding
for doc in documents:
    embedding = get_embedding(doc)
    embedding_json = json.dumps(embedding)  # convert list to text
    cursor.execute(
        "INSERT INTO documents (content, embedding) VALUES (?, ?)",
        (doc, embedding_json)
    )

conn.commit()
print("Documents saved!\n")

# Read them back
cursor.execute("SELECT id, content, embedding FROM documents")
rows = cursor.fetchall()

for row in rows:
    doc_id, content, embedding_json = row
    embedding = json.loads(embedding_json)  # convert text back to list
    print(f"ID: {doc_id} | Content: {content}")
    print(f"  Embedding length: {len(embedding)}")
    print(f"  First 3 values: {embedding[:3]}\n")

conn.close()