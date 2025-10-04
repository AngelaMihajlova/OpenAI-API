from openai import OpenAI
from dotenv import load_dotenv
import os

# Вчитај API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Чувај ја историјата на разговор
messages = [
    {"role": "system", "content": "Ти си асистент кој одговара кратко и јасно."}
]

print("💬 Започни разговор со AI (пиши 'exit' за да прекинеш)")

while True:
    # Прашање од корисникот
    user_input = input("Ти: ")
    if user_input.lower() in ["exit", "quit", "izlez"]:
        print("👋 Крај на разговорот.")
        break

    # Додај во историјата
    messages.append({"role": "user", "content": user_input})

    # Побарај одговор
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    answer = resp.choices[0].message.content

    # Испечати го одговорот
    print("AI:", answer)

    # Додај одговорот во историјата
    messages.append({"role": "assistant", "content": answer})
