"""
Database Connection
===================
This file creates the connection to PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found in .env file!")

# Create engine (connection to database)
engine = create_engine(DATABASE_URL)

# Create session factory (for making queries)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()


def get_db():
    """
    Get database session.
    Use this in API endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
