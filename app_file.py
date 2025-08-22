import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader

# Вчитај API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Chatbot + Multi File Auto", page_icon="🤖")
st.title("🤖 AI Chatbot со повеќе фајлови (автоматски одговор)")

# --- Иницијализација на session_state ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Ти си асистент кој одговара кратко и јасно."}
    ]
if "uploaded_files_texts" not in st.session_state:
    st.session_state["uploaded_files_texts"] = []

# --- Копче за чистење на разговорот ---
if st.button("🗑️ Избриши историја"):
    st.session_state["messages"] = [
        {"role": "system", "content": "Ти си асистент кој одговара кратко и јасно."}
    ]
    st.session_state["uploaded_files_texts"] = []
    st.rerun()

# --- File uploader со повеќе фајлови ---
uploaded_files = st.file_uploader(
    "Прикачи PDF или TXT фајлови", type=["pdf", "txt"], accept_multiple_files=True
)

if uploaded_files:
    st.session_state["uploaded_files_texts"] = []  # reset пред нов upload
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            pdf = PdfReader(uploaded_file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            st.session_state["uploaded_files_texts"].append(text)
        else:
            st.session_state["uploaded_files_texts"].append(uploaded_file.read().decode("utf-8"))
    st.success(f"📄 Прикачени {len(uploaded_files)} фајлови успешно!")

# --- Прикажи историја на разговор ---
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# --- Поле за внесување порака ---
if prompt := st.chat_input("Напиши порака..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Подготви messages за OpenAI
    messages_to_send = st.session_state["messages"].copy()

    # Додај текст од сите прикачени фајлови како system context
    for i, file_text in enumerate(st.session_state["uploaded_files_texts"], start=1):
        messages_to_send.append({
            "role": "system",
            "content": f"Фајл {i} содржи:\n{file_text}"
        })

    # Повик до OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_to_send
    )
    answer = response.choices[0].message.content

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
