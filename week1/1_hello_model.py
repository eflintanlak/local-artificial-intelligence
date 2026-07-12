from foundry_local_sdk import FoundryLocalManager, Configuration

config = Configuration(app_name="yerel-yapay-zeka")
manager = FoundryLocalManager(config)
catalog = manager.catalog

model = catalog.get_model("qwen3-0.6b")
model.load()

client = model.get_chat_client()
response = client.complete_chat(
    messages=[{"role": "user", "content": "Merhaba! Kendini tanıt."}]
)

cevap = response.choices[0].message.content
if "</think>" in cevap:
    cevap = cevap.split("</think>")[-1].strip()

print(f"AI: {cevap}")