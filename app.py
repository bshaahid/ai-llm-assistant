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

st.title("My First AI Assistant")
st.write("Ask a question and get a response from the model.")

user_input = st.text_input("Enter your question:")

if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response.choices[0].message.content
        st.write("### Response")
        st.write(answer)
