from fastapi import FastAPI, APIRouter, Cookie, Response, HTTPException, Depends, Form, Request
from sqlalchemy.orm import Session
import redis
import uuid
import json
from app.api.helpers import get_db, is_signed_in
from app.models.models import User


router = APIRouter()
redis = redis.Redis(host="redis", port=6379, decode_responses=True)


@router.post("/login")
def login(response: Response, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    user = db.query(User).filter_by(email=email).first()

    if user == None:
        return {"error" : "email not found, please try again"}

    elif password == user.user_password:
        session_id = str(uuid.uuid4())
        redis.hset(name=f"session:{session_id}", mapping={"first_name" : user.first_name, "last_name" : user.last_name, "role" : user.user_role, "phone_number" : user.phone_number}) # add pydantic later
        redis.expire(f"session:{session_id}", 3600)
        response.set_cookie(key="session_id", value=session_id, expires=3600)

        return {"success" : f"Hello {user.first_name}!"}

    else:
        return {"error" : "password is not valid, please try again"}

@router.post("/logout")
def logout(request: Request):
    if not is_signed_in(request):
        return {"error/success?" : "already logged out"}
    else:
        session_id = request.cookies.get("session_id")
        redis.delete(f"session:{session_id}")
        return {"success" : "user signed out"}

