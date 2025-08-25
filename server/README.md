# Backend – (RagBot)

The backend is built with **FastAPI** and implements:

- Chat APIs (RAG pipeline: retrieval + generation)
- Session persistence with Postgres
- Modular services for vector stores and LLMs
- Logging, error handling, and environment configuration

---

## Tech

- **FastAPI** for APIs
- **SQLAlchemy** + **Postgres** for persistence
- **Pinecone** for vector retrieval
- **OpenAI** for LLM generation
- **Pydantic** for schema validation

---

## ENV Variables required:

```env
APP_NAME
ENV
DEBUG
REACT_APP_URL

POSTGRES_DSN
HTTPS

SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_KEY

PINECONE_API_KEY
PINECONE_ENV
PINECONE_INDEX_HOST


OPEN_AI_API_KEY
EMBED_MODEL
CHAT_MODEL

HISTORY_LIMIT
EMBED_DIM
```

## Running Locally

```bash
uvicorn app.main:app --reload --port 8000
```

Use Swagger UI at `http://localhost:8000/docs`.

---
