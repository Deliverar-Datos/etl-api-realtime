import os
import sys

# Prevent __pycache__ creation
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True

from fastapi import FastAPI
from app.events.routers.callback import router as callback_router
from app.events.routers.role import router as role_router
from app.models.database import Base, engine
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Handles events from different guilds and transforms to star schema",
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

app.include_router(callback_router, prefix="/events")
app.include_router(role_router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Multi-Guild Event Processor API", "version": settings.APP_VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}