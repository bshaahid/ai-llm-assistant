# AI LLM Assistant

A conversational AI assistant built with Python, Streamlit, and OpenAI API.

## Features
- Chat-style interface
- Conversation memory using Streamlit session state
- Reset chat button
- Clean and simple UI

## Tech Stack
- Python
- Streamlit
- OpenAI API
- python-dotenv

## Project Structure

```text
ai-llm-assistant/
  app.py
  .env
  requirements.txt
  README.md
  utils/


  - Multiple assistant modes:
  - General Assistant
  - AI Tutor
  - Product Advisor

  ## Next Steps
  - Add document upload
  - Add PDF question answering
  - Add RAG pipeline


  ## New Features
- PDF upload
- Text extraction from PDF
- Document-aware Q&A
- Chat interface with assistant modes

## Current Limitations
- Only the first few chunks of the uploaded document are used as context
- No semantic retrieval yet

## Next Steps
- Add embeddings
- Add vector search
- Convert into a true RAG pipeline