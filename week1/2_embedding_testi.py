from foundry_local_sdk import FoundryLocalManager, Configuration

config = Configuration(app_name="yerel-yapay-zeka")
manager = FoundryLocalManager(config)
catalog = manager.catalog

model = catalog.get_model("qwen3-embedding-0.6b")
model.load()
client = model.get_embedding_client()

cumleler = [
    "Kedi uyuyor",
    "Kedi uyukladı",
    "Araba hızlı gidiyor"
]

for cumle in cumleler:
    response = client.generate_embedding(cumle)
    embedding = response.data[0].embedding
    print(f"'{cumle}'")
    print(f"  İlk 3 sayı: {embedding[:3]}")
    print()