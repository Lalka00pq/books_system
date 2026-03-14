import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import BaseModel


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.USER, nullable=False)

    books: Mapped[list["UserBook"]] = relationship(
        "UserBook", back_populates="user", cascade="all, delete-orphan")
