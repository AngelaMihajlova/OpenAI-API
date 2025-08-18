from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Претворање на локална слика во base64
with open("images.jfif", "rb") as f:
    image_bytes = f.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

# Правење data URL (битно!)
image_data_url = f"data:image/jpeg;base64,{image_b64}"

# Прати ја сликата до моделот
resp = client.responses.create(
    model="gpt-4o-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Што има на оваа слика? Опиши со краток текст."},
            {"type": "input_image", "image_url": image_data_url}
        ]
    }]
)

print(resp.output_text)
