import uuid
import enum
from sqlalchemy import ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import BaseModel


class BookStatus(str, enum.Enum):
    READING = "reading"
    COMPLETED = "completed"
    PLAN_TO_READ = "plan_to_read"
    DROPPED = "dropped"


class UserBook(BaseModel):
    __tablename__ = "user_books"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[BookStatus] = mapped_column(
        Enum(BookStatus), default=BookStatus.PLAN_TO_READ, nullable=False)
    added_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="books")
    book: Mapped["Book"] = relationship(
        "Book", back_populates="user_associations")
