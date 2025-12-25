import streamlit as st
from rag_core import generate_answer

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="🌍",
    layout="centered"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 AI Travel Assistant")
st.sidebar.markdown("""
An intelligent travel assistant that answers
questions related to tourism, sustainability,
and travel safety.

**Use Cases**
- Responsible tourism
- Eco-friendly travel
- Adventure activities
- Travel safety tips

Built as an **end-to-end AI project**.
""")

st.sidebar.markdown("---")
st.sidebar.caption("Academic Mini / Major Project")

# ---------------- MAIN UI ----------------
st.markdown(
    "<h2 style='text-align: center;'>Ask Anything About Travel ✈️</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Get clear, helpful answers for tourists and travelers"
    "</p>",
    unsafe_allow_html=True
)

# Chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Chat input
query = st.chat_input("Ask your travel question here...")

if query:
    # Store user message
    st.session_state.chat.append(("user", query))

    with st.spinner("Thinking..."):
        answer = generate_answer(query)

    # Store assistant message
    st.session_state.chat.append(("assistant", answer))

# Display chat messages
for role, message in st.session_state.chat:
    with st.chat_message(role):
        st.write(message)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 12px; color: gray;'>"
    "AI Travel Assistant • RAG-based • Streamlit UI"
    "</p>",
    unsafe_allow_html=True
)
