import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()

client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI LLM Assistant", page_icon="🤖", layout="centered")

st.title("🤖 My AI Assistant")
st.caption("Day 2 upgrade: chat history, assistant modes, better UX")

ASSISTANT_MODES = {
    "General Assistant": (
        "You are a helpful, clear, and professional AI assistant. "
        "Give accurate, concise, and useful responses."
    ),
    "AI Tutor": (
        "You are an AI tutor. Explain concepts in simple language, "
        "break ideas into steps, give examples, and help the user learn clearly."
    ),
    "Product Advisor": (
        "You are a product and strategy advisor. Help the user think in terms of "
        "customer value, product design, trade-offs, prioritization, and execution."
    )
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "General Assistant"

with st.sidebar:
    st.header("Controls")

    selected_mode = st.selectbox(
        "Choose assistant style",
        list(ASSISTANT_MODES.keys()),
        index=list(ASSISTANT_MODES.keys()).index(st.session_state.selected_mode)
    )

    if selected_mode != st.session_state.selected_mode:
        st.session_state.selected_mode = selected_mode
        st.session_state.messages = []
        st.success(f"Switched to {selected_mode}. Chat reset for clean context.")

    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Active Mode")
    st.write(st.session_state.selected_mode)

    st.markdown("### About")
    st.write("This assistant is built with Streamlit and OpenAI.")
    st.write("Modes change the assistant behavior using different system prompts.")

if len(st.session_state.messages) == 0:
    welcome_message = f"Hi! I’m your **{st.session_state.selected_mode}**. Ask me anything."
    with st.chat_message("assistant"):
        st.markdown(welcome_message)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            system_prompt = ASSISTANT_MODES[st.session_state.selected_mode]

            api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages
            )

            answer = response.choices[0].message.content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})