import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient

# --- CONFIG ---
COLLECTION_NAME = "markdown_docs"
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

# --- API KEYS ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Qdrant Client ---
qdrant = QdrantClient(location="localhost", port=6333)

# --- System Prompts ---
REWRITE_SYSTEM_PROMPT = (
    "You help rewrite the user's question using the recent chat history so it can be answered with retrieval. "
    "Return only the rewritten question."
)

ANSWER_SYSTEM_PROMPT = (
    "You are a precise assistant. Use the provided context chunks to answer the user. "
    "If the answer is not in the context, say you don’t know. "
    "Always cite the sources by their 'source' metadata when provided."
)

# --- Functions ---
def rewrite_query_with_history(user_query: str, history: list, turns: int = 5) -> str:
    messages = [{"role": "system", "content": REWRITE_SYSTEM_PROMPT}]
    for m in history[-turns:]:
        messages.append(m)

    messages.append({
        "role": "user",
        "content": f"Rewrite this question for retrieval: {user_query}"
    })

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0
    )
    return resp.choices[0].message.content or user_query


def search_qdrant(query: str, top_k: int = 5):
    query_embedding = client.embeddings.create(
        input=query, model=EMBED_MODEL
    ).data[0].embedding

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )
    return results


def build_context_and_answer(final_query: str, chunks: list):
    context_text = "\n\n".join(f"[Chunk {i+1}]\n{c}" for i, c in enumerate(chunks)) if chunks else ""
    messages = [
        {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
        {"role": "user",
         "content": (
             "Answer the question using ONLY the context below.\n"
             "If the answer is not contained in the context, say you don't know.\n\n"
             "===CONTEXT===\n"
             f"{context_text}\n\n"
             "===QUESTION===\n"
             f"{final_query}"
         )
        }
    ]
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0
    )
    answer = resp.choices[0].message.content or ""
    if not chunks and not answer.strip():
        answer = "I don't have relevant context to answer that."
    return answer, context_text


# --- Streamlit App ---
st.set_page_config(page_title="AI RAG Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot со Qdrant + Rewrite + Context Answer")

# Reset chat
if st.button("🗑️ Избриши историја"):
    st.session_state["messages"] = [{"role": "system", "content": "Ти си асистент кој одговара кратко и јасно."}]
    st.rerun()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "Ти си асистент кој одговара кратко и јасно."}]

# Display chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Напиши порака..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 1️⃣ Rewrite query
    rewritten_prompt = rewrite_query_with_history(prompt, st.session_state["messages"])

    # 2️⃣ Search chunks
    results = search_qdrant(rewritten_prompt)
    chunks = [r.payload.get("text", "") for r in results]

    # 3️⃣ Build context and get answer
    answer, context_text = build_context_and_answer(rewritten_prompt, chunks)

    # 4️⃣ Append assistant response
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
