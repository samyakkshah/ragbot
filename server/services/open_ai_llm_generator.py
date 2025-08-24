from typing import List, AsyncGenerator, TYPE_CHECKING, Any
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from config import config
from local_logs.logger import logger
from interfaces.llm_generator import LLMGenerator
from prompts.fintech import build_messages

if TYPE_CHECKING:
    from models import Message as MessageModel  # only for type checkers
else:
    MessageModel = Any


class OpenAIChatGenerator(LLMGenerator):
    """
    OpenAI Chat Completions streaming generator.

    :param model: Model name from config.CHAT_MODEL.
    :param temperature: Sampling temperature.
    """

    def __init__(self) -> None:
        if not config.OPEN_AI_API_KEY:
            raise ValueError("OPEN_AI_API_KEY is not configured.")
        if not config.CHAT_MODEL:
            raise ValueError("CHAT_MODEL is not configured.")

        self._client = AsyncOpenAI(api_key=config.OPEN_AI_API_KEY)
        self._model = config.CHAT_MODEL
        self._temperature = 0.3

    def _messages_from(
        self, context_chunks: List[str], query: str, history: List[MessageModel]
    ) -> List[ChatCompletionMessageParam]:
        """
        Build a prompt message list for OpenAI.

        Args:
            context_chunks: Retrieved knowledge text snippets.
            query: Current user query.
            history: Prior conversation messages (optional).

        Returns:
            List of chat messages for the API.
        """
        return build_messages(query=query, chunks=context_chunks, history=history or [])

    async def stream(
        self, context_chunks: List[str], query: str, history: List[MessageModel]
    ) -> AsyncGenerator[str, None]:
        """Stream tokens from the OpenAI chat completion API.

        Args:
            messages: Ordered list of role/content pairs
                following OpenAI Chat format.

        Yields:
            str: Content deltas emitted by the model.

        Raises:
            RuntimeError: Wraps lower-level SDK/network errors for the caller.
        """
        try:
            messages = self._messages_from(context_chunks, query, history)
            stream = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                stream=True,
            )
            async for part in stream:
                try:
                    choice = (getattr(part, "choices", None) or [None])[0]
                    delta = getattr(choice, "delta", None)
                    content = getattr(delta, "content", None)
                    if content:
                        yield content
                except Exception as chunk_err:
                    logger.warning(
                        f"[OpenAIChatGenerator] Stream chunk parse error: {chunk_err}"
                    )
        except Exception as e:
            logger.error("[OpenAIChatGenerator] Streaming failed", exc=e)
            raise
