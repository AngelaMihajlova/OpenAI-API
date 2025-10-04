import streamlit as st
import os
from dotenv import load_dotenv

from history_tabs import create_tables
from dynamo_helpers import list_chats, create_chat, get_messages, add_message, CHAT_TABLE, delete_chat
from openai import OpenAI

# ---------- OpenAI иницијализација ----------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

create_tables()

st.set_page_config(page_title="Chat with Memory", layout="wide")

# ---------- init state ----------
if "current_chat_id" not in st.session_state or st.session_state["current_chat_id"] is None:
    st.session_state["current_chat_id"] = create_chat(title="")
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chat_title" not in st.session_state:
    st.session_state["chat_title"] = ""

# ---------- sidebar ----------
st.sidebar.title("Sessions")

# Нов chat
if st.sidebar.button("➕ New chat"):
    cid = create_chat(title="")
    st.session_state["current_chat_id"] = cid
    st.session_state["messages"] = []
    st.session_state["chat_title"] = ""

# Листа на chats со копче за бришење
chats = list_chats()
for chat in chats:
    chat_id = chat["chat_id"]
    title = chat.get("title", "(no title)")
    col1, col2 = st.sidebar.columns([0.8, 0.2])

    # селекција на chat
    if col1.button(title, key=f"chat_{chat_id}"):
        st.session_state["current_chat_id"] = chat_id
        msgs = get_messages(chat_id)
        st.session_state["messages"] = [{"role": m["role"], "content": m["content"]} for m in msgs]
        st.session_state["chat_title"] = title

    # бришење на chat
    if col2.button("✖", key=f"delete_{chat_id}"):
        delete_chat(chat_id)
        # ако е избришан тековниот chat, креирај нов празен chat
        if st.session_state["current_chat_id"] == chat_id:
            new_cid = create_chat(title="")
            st.session_state["current_chat_id"] = new_cid
            st.session_state["messages"] = []
            st.session_state["chat_title"] = ""

# ---------- главен chat прозорец ----------
st.title("💬 Chatbot with History")

# рендерирај историја
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# input поле
if prompt := st.chat_input("Type your message..."):
    # ако нема валиден chat_id
    if st.session_state["current_chat_id"] is None:
        st.session_state["current_chat_id"] = create_chat(title="")

    # ако chat title е празен, првата порака станува title
    if not st.session_state.get("chat_title"):
        st.session_state["chat_title"] = prompt
        CHAT_TABLE.update_item(
            Key={"chat_id": st.session_state["current_chat_id"]},
            UpdateExpression="SET title = :t",
            ExpressionAttributeValues={":t": prompt}
        )

    # додај user порака
    st.session_state["messages"].append({"role": "user", "content": prompt})
    add_message(st.session_state["current_chat_id"], "user", prompt)
    st.chat_message("user").write(prompt)

    # OpenAI повик
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )
    reply = response.choices[0].message.content

    # зачувај одговор
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    add_message(st.session_state["current_chat_id"], "assistant", reply)
    st.chat_message("assistant").write(reply)
