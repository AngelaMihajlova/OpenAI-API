from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Прочитај го документот локално
with open("example.txt", "r", encoding="utf-8") as f:
    document_text = f.read()

# System prompt
system_prompt = (
    "Ти си асистент кој извлекува структурирани информации од документ. "
    "Врати го резултатот исклучиво во JSON формат. "
    "Користи јасни key-value парови."
)

# User message со текстот на документот
user_message = (
    f"Прочитај го следниот текст и извлечи ги главните податоци во JSON:\n\n{document_text}"
)

# Chat completion
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
