from foundry_local_sdk import FoundryLocalManager, Configuration

config = Configuration(app_name="local-ai-assistant")
manager = FoundryLocalManager(config)
catalog = manager.catalog

model = catalog.get_model("qwen3-0.6b")
model.load()
client = model.get_chat_client()

def ask(system_message, user_message):
    response = client.complete_chat(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    answer = response.choices[0].message.content
    if "</think>" in answer:
        answer = answer.split("</think>")[-1].strip()
    return answer

# Test 1: No system message (no rules)
print("=== Without system message ===")
answer1 = ask(
    system_message="",
    user_message="What is the capital of Mars?"
)
print(f"AI: {answer1}\n")

# Test 2: With system message (strict rules)
print("=== With system message ===")
answer2 = ask(
    system_message="You only answer based on the context provided. If you don't know, say 'I don't have that information.' Never make up facts.",
    user_message="What is the capital of Mars?"
)
print(f"AI: {answer2}\n")