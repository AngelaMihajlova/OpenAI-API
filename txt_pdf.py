import os
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # избегни None
                    text += page_text + "\n"
        return text.strip()

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    else:
        raise ValueError("Unsupported file type. Only PDF and TXT are supported.")


def ask_chatgpt(file_path, prompt="Please summarize the following text:"):
    text = read_file(file_path)

    # Ограничение: ако текстот е многу долг, може да треба да се скрати
    max_length = 3000  # пример, може да прилагодиш
    if len(text) > max_length:
        text = text[:max_length] + "\n\n[Text truncated]"

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": f"{prompt}\n\n{text}"}
        ],
    )

    return response.choices[0].message.content


# Пример користење:
file_path = "story.pdf"  # или "story.txt"
result = ask_chatgpt(file_path)
print(result)
