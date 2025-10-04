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

# 2️⃣ System prompt
system_prompt = (
    "Ти си асистент кој извлекува информации за ликовите од книга/текст. "
    "Врати одговор во JSON формат, со полиња што ќе ги каже корисникот. "
    "Секој лик треба да има свои key-value парови."
)

# 3️⃣ Постави user message со барање и полиња
fields = ["first_name", "last_name", "gender", "age"]  # полиња што сакаш да ги извлечеш
user_message = (
    f"Извади ми JSON за сите ликови кои се спомнуваат во текстот подолу. "
    f"Секој лик треба да има полиња: {', '.join(fields)}.\n\nТекст:\n{pdf_text}"
)

# 4️⃣ Прати до GPT
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
)

json_output = resp.choices[0].message.content
print("📄 Извлечени податоци (JSON):")
print(json_output)

# 5️⃣ Може да се зачува во фајл
with open("characters.json", "w", encoding="utf-8") as f:
    f.write(json_output)

print("✅ JSON зачуван како characters.json")
