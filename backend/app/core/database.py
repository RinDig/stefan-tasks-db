"""
Database configuration and connection
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Use the external URL for database connection
# IMPORTANT: Set DATABASE_URL as an environment variable in production
DATABASE_URL = settings.DATABASE_URL or "sqlite:///./test.db"  # Use SQLite for local dev

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()

def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()