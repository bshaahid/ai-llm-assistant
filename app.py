import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

from utils.pdf_utils import extract_text_from_pdf, chunk_text
from utils.rag_utils import get_top_k_chunks

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()

client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI LLM Assistant", page_icon="🤖", layout="centered")

st.title("🤖 My AI Assistant")
st.caption("Day 4 upgrade: local RAG with embeddings-based retrieval")

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

if "chunk_embeddings" not in st.session_state:
    st.session_state.chunk_embeddings = []

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
        with st.spinner("Reading and indexing PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            chunks = chunk_text(extracted_text)

            chunk_embeddings = []
            for chunk in chunks:
                embedding_response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=chunk
                )
                chunk_embeddings.append(embedding_response.data[0].embedding)

            st.session_state.document_text = extracted_text
            st.session_state.document_chunks = chunks
            st.session_state.chunk_embeddings = chunk_embeddings

        st.success("PDF uploaded, chunked, and indexed successfully!")
        st.write(f"Created {len(chunks)} chunks and embeddings.")

    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Active Mode")
    st.write(st.session_state.selected_mode)

    st.markdown("### Document Status")
    if st.session_state.document_text:
        st.write("PDF loaded and retrieval is ready.")
    else:
        st.write("No PDF uploaded yet.")

if len(st.session_state.messages) == 0:
    welcome_message = f"Hi! I’m your **{st.session_state.selected_mode}**."
    if st.session_state.document_text:
        welcome_message += " I can answer questions using semantic retrieval from your PDF."
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

            if st.session_state.document_chunks and st.session_state.chunk_embeddings:
                question_embedding_response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=user_input
                )
                question_embedding = question_embedding_response.data[0].embedding

                top_chunks = get_top_k_chunks(
                    question_embedding,
                    st.session_state.chunk_embeddings,
                    st.session_state.document_chunks,
                    k=3
                )

                context = "\n\n".join(top_chunks)

                system_prompt += (
                    "\n\nUse the following retrieved document context to answer the user’s question. "
                    "If the answer is not in the document, say so clearly.\n\n"
                    f"Retrieved Context:\n{context}"
                )

            api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages
            )

            answer = response.choices[0].message.content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})