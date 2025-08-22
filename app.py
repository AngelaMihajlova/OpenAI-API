import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Вчитај API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot со OpenAI API")

# Копче за чистење на разговорот
if st.button("🗑️ Избриши историја"):
    st.session_state["messages"] = [
        {"role": "system", "content": "Ти си асистент кој одговара кратко и јасно."}
    ]
    st.rerun()  # ✅ новата функција

# Чувај историја во session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Ти си асистент кој одговара кратко и јасно."}
    ]

# Прикажи ја историјата
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Поле за внесување порака
if prompt := st.chat_input("Напиши порака..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Повик до OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )
    answer = response.choices[0].message.content

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
