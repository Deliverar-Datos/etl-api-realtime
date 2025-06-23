# app/models/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()

def get_db():
    """
    Dependency that provides a database session for each request.
    Ensures the session is properly closed after use.
    """
    print(settings.DATABASE_URL)
    db = SessionLocal()
    try:
        yield db
        print("Session created")
    finally:
        db.close()

def create_tables():
    """Create all tables in the database (for development)"""
    # Import blockchain models
    from app.guilds.blockchain.schemas.star_schema import (
        DimUser, 
        DimStatus, 
        DimDate, 
        DimConcept, 
        FactTransaction
    )
    
    # Import marketplace models
    from app.guilds.marketplace.models.tables import (
        Tenant,
        Comercio,
        Categoria
    )
    
    Base.metadata.create_all(bind=engine)