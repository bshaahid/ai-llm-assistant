import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

from utils.pdf_utils import extract_text_from_pdf, chunk_text

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()

client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI LLM Assistant", page_icon="🤖", layout="centered")

st.title("🤖 My AI Assistant")
st.caption("Day 3 upgrade: PDF upload + document-aware Q&A")

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

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = []

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

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        extracted_text = extract_text_from_pdf(uploaded_file)
        st.session_state.document_text = extracted_text
        st.session_state.document_chunks = chunk_text(extracted_text)

        st.success("PDF uploaded and processed successfully!")
        st.write(f"Extracted {len(st.session_state.document_chunks)} text chunks.")

    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Active Mode")
    st.write(st.session_state.selected_mode)

    st.markdown("### Document Status")
    if st.session_state.document_text:
        st.write("PDF loaded and ready for questions.")
    else:
        st.write("No PDF uploaded yet.")

if len(st.session_state.messages) == 0:
    welcome_message = f"Hi! I’m your **{st.session_state.selected_mode}**."
    if st.session_state.document_text:
        welcome_message += " I can also answer questions about your uploaded PDF."
    else:
        welcome_message += " Ask me anything."
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

            if st.session_state.document_text:
                context = "\n\n".join(st.session_state.document_chunks[:3])

                system_prompt += (
                    "\n\nUse the following document context to answer the user’s question. "
                    "If the answer is not in the document, say so clearly.\n\n"
                    f"Document Context:\n{context}"
                )

            api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages
            )

            answer = response.choices[0].message.content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})