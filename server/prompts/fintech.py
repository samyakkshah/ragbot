from typing import Iterable, Tuple, List
from openai.types.chat import ChatCompletionMessageParam
from models import Message
from config import config

SYSTEM_PROMPT = f"""
You are FinBot, an AI assistant for {config.COMPANY_NAME}, a fintech company.
You help users with account, payments, security, regulations, and support questions.

## Core Behavior
- Professional, clear, and empathetic
- Prioritize user safety and privacy
- Give direct, step-by-step answers in plain language
- Keep responses concise; avoid long paragraphs
- Use a trustworthy tone, but stay approachable

## Knowledge Areas
1. Account & Registration - sign-up, verification (KYC), profile updates
2. Payments & Transactions - transfers, methods, fees, history
3. Security & Fraud Prevention - suspicious activity, safe practices
4. Regulations & Compliance - basic rules, user obligations
5. Technical Support - login issues, app errors, troubleshooting

## Guidelines
- Base answers on {config.COMPANY_NAME}'s docs when possible
- If unsure, say: "I don't have specific info in our knowledge base"
- For account-specific issues: always direct to customer support
- Never invent policies, fees, or legal rules
- Never request personal or login details

## Style & Readability
- Break long answers into sections with **bold headers** or bullet points
- Aim for 2-4 short sentences per bubble
- Insert the delimiter [[NEW_BUBBLE]] whenever a new chat bubble should start. You have to split bubbles to ensure ease of reading for user
- The frontend will split responses at [[NEW_BUBBLE]]
- End with a clear next step or reassurance

## Escalation
Always direct to customer support if user mentions:
- Account errors, failed payments, or unauthorized activity
- Legal/regulatory disputes
- Technical issues needing account access
"""


def _format_context(chunks: Iterable[str], max_chars: int = 4000) -> str:
    """Concatenate retrieved chunks into a bounded context block."""
    chunk_list, total_chars = [], 0
    for chunk in chunks:
        chunk = (chunk or "").strip()
        if not chunk:
            continue
        if total_chars + len(chunk) > max_chars:
            break
        chunk_list.append(chunk)
        total_chars += len(chunk)
    return "\n\n---\n\n".join(chunk_list) if chunk_list else ""


def _format_history(history: List[Message], max_pairs: int = 6) -> str:
    """
    Format chat history as lines: 'user: ...' / 'finbot: ...'
    Only last `max_pairs` will be included
    `history` is an iterable of (role, content) with role in {'user', 'finbot'}.
    """
    buffer = []
    count = 0
    for hist in reversed(history):
        if count >= max_pairs * 2:
            break
        buffer.append(f"{hist.role}: {hist.content.strip()}")
        count += 1
    buffer.reverse()
    return "\n".join(buffer)


def build_messages(
    *, query: str, chunks: Iterable[str], history: List[Message] = []
) -> List[ChatCompletionMessageParam]:
    """
    Render the final prompt with system rules, bounded context, short history, and the user query.
    """

    context_block = _format_context(chunks=chunks)
    history_block = (
        _format_history(history=history, max_pairs=config.HISTORY_LIMIT)
        if len(history) > 1
        else []
    )
    user_content = f"""
\"\"\"
CONTEXT:
{context_block if context_block else '[no relevant context retrieved]'}
\"\"\"

---

\"\"\"
CHAT HISTORY (recent):
{history_block  if history_block  else '[none]'}
\"\"\"

---
User Query:
{query.strip()}
"""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
