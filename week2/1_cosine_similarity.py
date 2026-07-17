from foundry_local_sdk import FoundryLocalManager, Configuration
import math

config = Configuration(app_name="local-ai-assistant")
manager = FoundryLocalManager(config)
catalog = manager.catalog

model = catalog.get_model("qwen3-embedding-0.6b")
model.load()
client = model.get_embedding_client()

def cosine_similarity(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(a * a for a in vector1))
    magnitude2 = math.sqrt(sum(b * b for b in vector2))
    return dot_product / (magnitude1 * magnitude2)

def get_embedding(text):
    response = client.generate_embedding(text)
    return response.data[0].embedding

question = "What is the cat doing?"

documents = [
    "The cat is sleeping",
    "The cat took a nap",
    "The car is going fast",
    "The weather is nice today"
]

question_embedding = get_embedding(question)

print(f"Question: {question}\n")
print("Similarity scores:")

for doc in documents:
    doc_embedding = get_embedding(doc)
    score = cosine_similarity(question_embedding, doc_embedding)
    print(f"  '{doc}' -> {score:.4f}")