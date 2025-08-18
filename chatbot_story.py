from openai import OpenAI
from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1️⃣ Прочитај PDF документ
pdf_path = "story.pdf"
pdf_text = ""

with open(pdf_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text + "\n"

# 2️⃣ Чувај историја на разговор
messages = [
    {"role": "system", "content": (
        "Ти си асистент кој извлекува информации за ликови од книга/текст. "
        "Секој твој одговор мора да биде во JSON формат, со јасни key-value парови."
    )}
]

print("💬 Поставувај прашања за ликовите (напиши 'exit' за да прекинеш)")

while True:
    user_input = input("Prompt: ")
    if user_input.lower() in ["exit", "quit", "izlez"]:
        print("👋 Крај на разговорот.")
        break

    # Додај во разговорот, вклучи PDF текст
    messages.append({"role": "user", "content": f"{user_input}\n\nPDF текст:\n{pdf_text}"})

    # Прати до GPT
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = resp.choices[0].message.content
    print("AI JSON:", answer)

    # Додај го одговорот во разговорот
    messages.append({"role": "assistant", "content": answer})
