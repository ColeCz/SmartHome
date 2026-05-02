from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv("../../.env")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=0,
    pool_timeout=30,
    pool_pre_ping=True # handles stale connections
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)