from foundry_local_sdk import FoundryLocalManager, Configuration

config = Configuration(app_name="local-ai-assistant")
manager = FoundryLocalManager(config)
catalog = manager.catalog

model = catalog.get_model("qwen3-0.6b")

print("Downloading model...")
model.download()
print(f"Cached: {model.is_cached}")

model.load()

client = model.get_chat_client()
response = client.complete_chat(
    messages=[{"role": "user", "content": "Hello! Introduce yourself."}]
)

answer = response.choices[0].message.content
if "</think>" in answer:
    answer = answer.split("</think>")[-1].strip()

print(f"AI: {answer}")