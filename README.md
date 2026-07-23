# Aircraft Electrical & Electronics RAG Assistant

A local, offline AI assistant that answers questions about aircraft electrical and electronics systems using Retrieval-Augmented Generation (RAG) and Microsoft Foundry Local.

## What It Does

This assistant answers questions based on a small knowledge base of aircraft electrical and avionics topics. It runs entirely offline on your computer — no internet connection or cloud API required.

## How It Works

1. **Retrieve**: When you ask a question, the system converts it into an embedding (numeric vector) and searches a local SQLite database for the most relevant document chunks using cosine similarity.
2. **Augment**: The retrieved chunks are inserted into the prompt as context.
3. **Generate**: A local LLM (via Foundry Local) generates an answer based only on the provided context.

## System Architecture

Question
    ↓
Embedding Model (qwen3-embedding-0.6b)
    ↓
Cosine Similarity Search
    ↓
SQLite Database (10 chunks from 5 documents)
    ↓
Top-K Relevant Chunks
    ↓
Chat Model (qwen3-0.6b) + Context
    ↓
Answer

## Technologies Used

- **Microsoft Foundry Local** — on-device LLM runtime
- **qwen3-0.6b** — chat model for generating answers
- **qwen3-embedding-0.6b** — embedding model for semantic search
- **SQLite** — local storage for document chunks and embeddings
- **Python** — core language

## Project Structure

week1/ - Foundry Local setup and basic model tests
week2/ - Cosine similarity, embedding storage, prompt engineering
week3/ - Document chunking, ingestion pipeline, search function
week4/ - Full RAG pipeline and interactive assistant
week5/ - Testing and evaluation
documents/ - Knowledge base source files (aircraft electrical/electronics topics)

## How to Run

1. Install dependencies:
   pip install foundry-local-sdk

2. Run the ingestion script to build the knowledge base:
   python week3/3_ingest_to_database.py

3. Start the interactive assistant:
   python week4/2_interactive_assistant.py

4. Ask questions like:
   - "What is fly-by-wire?"
   - "How does the pitot tube measure airspeed?"
   - "How do circuit breakers work in aircraft?"

## Test Results

The assistant was tested with 5 questions — 3 that should be answerable from the knowledge base, and 2 that should not be.

| # | Question | Expected | Result | Time |
|---|----------|----------|--------|------|
| 1 | What is fly-by-wire? | Should answer | Pass | 11.7s |
| 2 | How does GPS work in aircraft? | Should answer | Pass | 13.8s |
| 3 | What is the APU? | Should answer | Pass | 12.7s |
| 4 | What is the price of a Boeing 747? | Should say "I don't know" | Pass | 12.1s |
| 5 | Who invented the airplane? | Should say "I don't know" | Pass | 13.4s |

**Result: 5/5 tests passed (100%)**

### Key Finding

Initial testing showed the model would sometimes use outside knowledge instead of admitting it didn't have the answer (Test 5 initially answered "The Wright brothers invented the airplane in 1903" — factually correct, but not sourced from the knowledge base). This was fixed by strengthening the system prompt to strictly forbid outside knowledge, after which all 5 tests passed.

## Known Limitations

- Small model (0.6B parameters) may occasionally produce imperfect answers
- Knowledge base is limited to 5 short documents on aircraft electrical/electronics topics
- Response time is approximately 12-15 seconds per query on CPU

## Author

Built by Eflin Tanlak as a learning project on local RAG systems using Microsoft Foundry Local.