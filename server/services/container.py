from typing import Optional
from interfaces import LLMGenerator, Embedder, VectorStore
from services.open_ai_embedder import OpenAIEmbedder
from services.pinecone_vector_store import PineconeVectorStore
from services.open_ai_llm_generator import OpenAIChatGenerator
from services.rag_pipeline import RAGPipeline

# Singleton-ish provider with lazy construction; replace with real DI anytime.
_embedder: Optional[Embedder] = None
_vector_store: Optional[VectorStore] = None
_llm: Optional[LLMGenerator] = None
_pipeline: Optional[RAGPipeline] = None


def get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        _embedder = OpenAIEmbedder()
    return _embedder


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = PineconeVectorStore(embedder=get_embedder(), namespace="")
    return _vector_store


def get_llm() -> LLMGenerator:
    global _llm
    if _llm is None:
        _llm = OpenAIChatGenerator()
    return _llm


def get_rag_pipeline() -> RAGPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipeline(get_vector_store(), get_llm(), top_k=5)
    return _pipeline
