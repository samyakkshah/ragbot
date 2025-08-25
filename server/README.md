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

## Running Locally

```bash
uvicorn app.main:app --reload --port 8000
```

Use Swagger UI at `http://localhost:8000/docs`.

---
