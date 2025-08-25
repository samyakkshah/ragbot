# Architecture Overview

This project follows a **full-stack design** with a retrieval-augmented generative chatbot to answer `FAQs` a user would have.

---

## Components

### Frontend

- `React` + `TS` app with chat UI
- Shows assistant & user bubbles
- Splits assistant responses using `[[NEW_BUBBLE]]`
- Persists chat history per session

### Backend

- FastAPI APIs (`/chat`, `/health`, `/history`)
- RAG pipeline:
  - Retrieve relevant docs via Pinecone
  - Construct system prompt
  - Generate response via OpenAI
- Stores messages in Postgres
- Designed to be extendable: swap vector DB (FAISS, Weaviate) or LLM provider

### Database

- Postgres via SQLAlchemy ORM
- Stores users, sessions, messages
- Extensible for analytics/logging

### Deployment

- **AWS-ready design**:
  - Backend on ECS or Lambda + API Gateway
  - Postgres (RDS or Supabase)
  - Pinecone or other Vector Database
  - Frontend hosted on S3 and backend deployed on a Docker cluster (e.g., ECS).
- `.env` based configuration for dev vs prod

---

## Design Decisions

- **RAG first** → ensures accuracy by grounding model in company FAQs
- **Delimiter splitting** → improves UX readability
- **Separation of concerns** → backend handles RAG & persistence; frontend only renders

---
