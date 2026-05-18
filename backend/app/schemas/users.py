from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    owner = "owner"
    regular = "regular"

class UserRegistration(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    user_password: str
    user_role: UserRole
    phone_number: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
