import os
from typing import Literal, List
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator


class Config(BaseModel):
    APP_NAME: str = "Eloquent AI"
    COMPANY_NAME: str = "Eloquent"
    ENV: Literal["dev", "prod", "test"] = "dev"
    REACT_APP_URL: str

    # API
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = []

    # Session
    HTTPS: bool = True

    # Database
    POSTGRES_DSN: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_ENV: str
    PINECONE_INDEX_HOST: str

    # Cookies
    SESSION_COOKIE_NAME: str = "sid"
    SESSION_COOKIE_EXP_MINUTES: int = 7 * 24 * 60  # 7 days

    # LLM
    OPEN_AI_API_KEY: str
    EMBED_MODEL: str
    CHAT_MODEL: str
    HISTORY_LIMIT: int

    # Embedding
    EMBED_DIM: int = 1024

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _split_csv(cls, v):
        if not v:
            return []
        if isinstance(v, list):
            return v
        return [s.strip() for s in str(v).split(",") if s.strip()]

    @classmethod
    def load_from_env(cls, env_file: str = ".env.local") -> "Config":
        load_dotenv(env_file)

        # Pick up declared fields only
        field_names = tuple(cls.model_fields.keys())
        data = {
            name: os.getenv(name) for name in field_names if os.getenv(name) is not None
        }

        if hasattr(cls, "model_validate"):
            return cls.model_validate(data)
        return cls.parse_obj(data)


config = Config.load_from_env()
