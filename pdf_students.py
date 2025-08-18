from openai import OpenAI
from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1️⃣ Прочитај PDF документ
pdf_path = "students.pdf"
pdf_text = ""

with open(pdf_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"

# 2️⃣ System prompt за конверзија во CSV
system_prompt = (
    "Ти си асистент кој прима табеларни податоци и ги враќа во CSV формат со запирки. "
    "Земи ги податоците од PDF текстот и направи CSV: id,име,презиме,поени."
)

# 3️⃣ User message со текстот од PDF
user_message = f"Еве го текстот од PDF:\n{pdf_text}"

# 4️⃣ Прати до GPT
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
)

csv_output = resp.choices[0].message.content
print("📄 CSV излез:")
print(csv_output)

# 5️⃣ Ако сакаш, можеш да го зачуваш во фајл
with open("output.csv", "w", encoding="utf-8") as f:
    f.write(csv_output)

print("✅ CSV зачуван како output.csv")
