from fastapi import FastAPI
from app.events.routers.callback import router as callback_router
from app.models.database import Base, engine
from app.core.config import settings
import sys
sys.dont_write_bytecode = True

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Handles events from different guilds and transforms to star schema",
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

app.include_router(callback_router, prefix="/events")

@app.get("/")
async def root():
    return {"message": "Multi-Guild Event Processor API", "version": settings.APP_VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}