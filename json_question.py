from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Прочитај го документот локално
with open("example.txt", "r", encoding="utf-8") as f:
    document_text = f.read()

# Чувај ја историјата на разговор
messages = [
    {"role": "system", "content": (
        "Ти си асистент кој извлекува структурирани информации од документ. "
        "Секој твој одговор мора да биде во JSON формат, со јасни key-value парови."
    )}
]

print("💬 Започни разговор со AI (пиши 'exit' за да прекинеш)")

while True:
    user_input = input("Ти: ")
    if user_input.lower() in ["exit", "quit", "izlez"]:
        print("👋 Крај на разговорот.")
        break

    # Додај во messages, вклучи текст од документот
    messages.append({"role": "user", "content": f"{user_input}\n\nДокумент:\n{document_text}"})

    # Прати барање до моделот
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = resp.choices[0].message.content
    print("AI:", answer)

    # Додај го одговорот во разговорот
    messages.append({"role": "assistant", "content": answer})
