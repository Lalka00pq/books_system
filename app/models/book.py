from datetime import date
from sqlalchemy import String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import BaseModel

class Book(BaseModel):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    author: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    isbn: Mapped[str | None] = mapped_column(String(20), nullable=True)
    genre: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(100), nullable=True)
    publish_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    
    user_associations: Mapped[list["UserBook"]] = relationship("UserBook", back_populates="book", cascade="all, delete-orphan")
