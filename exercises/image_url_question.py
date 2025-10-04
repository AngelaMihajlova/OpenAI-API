from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resp = client.responses.create(
    model="gpt-4o-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Што има на сликата? Опиши во 1-2 реченици."},
            {"type": "input_image", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0MoViUbDiTA-BiT1AIcTMYXqfARDx57gAcA&s"}
        ]
    }]
)

print(resp.output_text)
