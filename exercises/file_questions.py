import pdfplumber
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Читање на PDF
text = ""
with pdfplumber.open("story.pdf") as pdf:
    for page in pdf.pages:
        text += page.extract_text() + "\n"

# Прати го текстот во ChatGPT
completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
    ],
)

# Испечатете го резултатот
print(completion.choices[0].message.content)
