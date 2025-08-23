from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from db_manager import db_manager
from config import config
from routers import system

# routes
from routers.sessions import router as sessions_router

SESSION_COOKIE_NAME = "sid"

app = FastAPI(
    title=config.APP_NAME,
    version="0.1.0",
    debug=config.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.REACT_APP_URL] if config.REACT_APP_URL else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system.router, prefix=config.API_V1_PREFIX)
