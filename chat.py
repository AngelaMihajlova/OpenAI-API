from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Низа на пораки која ќе ја чуваме како разговор
messages = [
    {"role": "system", "content": "Ти си асистент кој одговара кратко и јасно."},
    {"role": "user", "content": "Што е супернова?"}
]

# Прв одговор
resp1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)
answer1 = resp1.choices[0].message.content
print("AI:", answer1)

# Додај го одговорот во разговорот
messages.append({"role": "assistant", "content": answer1})

# Ново прашање од корисникот (ќе го земе во предвид целиот контекст погоре)
messages.append({"role": "user", "content": "А што се неутронски ѕвезди?"})

# Втор одговор
resp2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)
answer2 = resp2.choices[0].message.content
print("AI:", answer2)
