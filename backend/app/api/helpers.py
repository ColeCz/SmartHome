from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from fastapi import FastAPI, Request, Cookie
import redis


redis = redis.Redis(host="redis", port=6379, decode_responses=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_signed_in(request: Request) -> bool:
    session_id = request.cookies.get("session_id")
    session = redis.hgetall(session_id)
    return session != None
