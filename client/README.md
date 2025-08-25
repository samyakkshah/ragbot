# Frontend – RagBot

The frontend is a **React + TypeScript** application styled with **Tailwind CSS**.

---

### Features

- Chat bubbles (user vs finbot)
- Markdown rendering (with tables, lists, etc.)
- Streaming dots animation while waiting
- Bubble splitting using `[[NEW_BUBBLE]]` delimiter
- Chat history persistence and replay
- Theming via Tailwind config

## Running Locally

```bash
npm install
npm start
```

By default, frontend runs on `http://localhost:3000`.
Make sure the backend server is running on port `8000` (or update `.env`).

---

## Notes

- Bubble splitting: assistant responses use `[[NEW_BUBBLE]]` delimiter.
- Extendable to add login/auth, multi-session history, and custom themes.

---
