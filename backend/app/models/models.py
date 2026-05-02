from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    user_password: Mapped[str] = mapped_column(String)
    user_role: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)



