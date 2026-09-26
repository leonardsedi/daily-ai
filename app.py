import streamlit as st
from groq import Groq

st.set_page_config(page_title="Cortex Link", page_icon="🧠")
st.title("🧠 Cortex Link")
st.caption("Created by Leonard Sedi")

# --- PUT YOUR REAL KEY HERE ---
client = Groq(api_key="GROQ_API_KEY")

# Ask for user's name first time
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    st.write("### Welcome to Cortex Link! 👋")
    name = st.text_input("What should I call you?")
    if st.button("Start Chatting"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# Memory with dynamic name
user_name = st.session_state.user_name

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hey {user_name}! 👋 I'm Cortex Link, your daily AI. Ask me anything about your day, studies, business, or life. How can I help today?"}
    ]

# Sidebar with branding + name change
with st.sidebar:
    st.header("🧠 Cortex Link")
    st.write(f"User: **{user_name}**")
    st.write("Created by Leonard Sedi")
    if st.button("Change Name"):
        st.session_state.user_name = ""
        st.session_state.messages = []
        st.rerun()

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input(f"Ask me anything, {user_name}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                max_tokens=1000,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
