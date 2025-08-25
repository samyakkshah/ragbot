# RagBot

This project is a full-stack web application featuring an **AI-powered chatbot** for a fictional fintech company.  
The chatbot uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers about account setup, payments, security, compliance, and technical issues.

---

## Features

- **Server (FastAPI, Python)**

  - REST APIs for chat interactions
  - RAG pipeline with vector search (Pinecone) and LLM generation
  - Support for session-based chat history
  - Modular design to extend vector DB or LLM provider

- **Client (React + TypeScript)**

  - Clean, minimal chat interface with bubble-based UI
  - Support for anonymous & known users
  - Chat history persistence and scrolling
  - Streaming responses with delimiter-based bubble splitting

- **Deployment**
  - Ready for AWS (ECS/EKS or Lambda + API Gateway)
  - Postgres for persistent storage
  - Extendable to Redis for caching or streaming improvements

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ & npm/yarn
- Docker (for containerized setup, optional)
- Accounts/keys for:
  - OpenAI (LLM)
  - Pinecone (Vector DB)
  - Postgres (local or Supabase)

### Setup

1.  Clone the repository:

    ```bash
    git clone https://github.com/samyakkshah/ragbot.git
    cd ragbot
    ```

2.  Backend setup:

    ```bash
    cd server
    cp .env.example .env   # add API keys and DB config
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```

3.  Frontend Setup:
    ```bash
    cd client
    cp .env.example .env # add API base URL
    npm install
    npm start
    ```

### Run end to end

- Start backend (FastAPI server)
- Start frontend (React dev server)
- Open `http://localhost:3000` to use the chatbot

### Documentation

- [Backend Readme](server/README.md)
- [Frontend Readme](client/README.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
