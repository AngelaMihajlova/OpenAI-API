from openai import OpenAI
from dotenv import load_dotenv
import os

# 1) Вчитај .env за да го земеш OPENAI_API_KEY
load_dotenv()

# 2) Иницијализирај OpenAI клиент
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 3) Прати едноставно чат барање преку Chat Completions API
resp = client.chat.completions.create(
    model="gpt-4o-mini",   # можеш и gpt-4.1 или gpt-4o
    messages=[
        {"role": "system", "content": "Ти си асистент кој објаснува кратко и јасно."},
        {"role": "user", "content": "Објасни ми накратко што е супернова."}
    ]
)

# 4) Испечати го текстуалниот излез
print(resp.choices[0].message.content)
