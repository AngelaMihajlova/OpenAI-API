from openai import OpenAI
from dotenv import load_dotenv
import os

# 1) Вчитај .env за да го земеш OPENAI_API_KEY
load_dotenv()

# 2) Иницијализирај OpenAI клиент
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 3) Прати едноставно текст барање преку Responses API
resp = client.responses.create(
    model="gpt-4o-mini",
    input="Објасни ми накратко што е супернова."
)

# 4) Испечати го текстуалниот излез
print(resp.output_text)
