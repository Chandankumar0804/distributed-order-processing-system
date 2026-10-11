from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.config import settings


# Database connection
engine = create_engine(
    settings.DATABASE_URL
)

# Database session
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Base for database models
Base = declarative_base()


# Get database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()