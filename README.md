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



## Day 4 Upgrade
- Added overlapping text chunking
- Added embeddings for document chunks
- Added cosine similarity retrieval
- Added local semantic search for PDF Q&A

## How Retrieval Works
1. Upload PDF
2. Extract text
3. Split into chunks
4. Create embeddings for each chunk
5. Embed the user question
6. Retrieve top matching chunks
7. Send retrieved context to the LLM

## Current Limitations
- Embeddings are regenerated on every new upload
- No persistent vector database yet
- Retrieval works only for one uploaded PDF at a time