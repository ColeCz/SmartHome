from fastapi import APIRouter, Response, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
import redis
import uuid
from app.api.helpers import get_db, is_signed_in
from app.models.models import User
from app.schemas.users import UserRegistration, UserLogin
from passlib.context import CryptContext


router = APIRouter()
redis = redis.Redis(host="redis", port=6379, decode_responses=True)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login", status_code=status.HTTP_200_OK)
def login(response: Response, data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()

    if not user or not pwd_context.verify(data.password, user.user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="login failed, please check your credentials"
        )

    session_id = str(uuid.uuid4())
    redis.hset(name=session_id, mapping={"user_id": user.id, "role": user.user_role})
    redis.expire(f"{session_id}", 3600)
    response.set_cookie(key="session_id", value=session_id, expires=3600, httponly=True)

    return {"detail": f"Hello {user.first_name}!"}


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(request: Request, response: Response):
    if not is_signed_in(request):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no active session found")

    session_id = request.cookies.get("session_id")
    redis.delete(session_id)
    response.delete_cookie("session_id")

    return {"detail": "successfully signed out"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: Request, data: UserRegistration, db: Session = Depends(get_db)):

    if not is_signed_in(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="must be signed in to register new users"
        )

    session_id = request.cookies.get("session_id")

    role = redis.hget(session_id, "role")
    if role not in ("owner", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="must be owner or administrator to register new users"
        )

    hashed_password = pwd_context.hash(data.user_password)
    new_user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        user_password=hashed_password,
        user_role=data.user_role,
        phone_number=data.phone_number,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.post("/test-register", status_code=status.HTTP_201_CREATED)
def register(request: Request, data: UserRegistration, db: Session = Depends(get_db)):

    hashed_password = pwd_context.hash(data.user_password)
    new_user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        user_password=hashed_password,
        user_role=data.user_role,
        phone_number=data.phone_number,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user