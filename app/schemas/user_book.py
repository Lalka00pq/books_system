import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.user_book import BookStatus
from app.schemas.book import BookResponse

class UserBookBase(BaseModel):
    status: BookStatus = BookStatus.PLAN_TO_READ

class UserBookCreate(UserBookBase):
    book_id: uuid.UUID

class UserBookUpdate(UserBookBase):
    pass

class UserBookResponse(UserBookBase):
    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID
    added_at: datetime
    book: BookResponse

    model_config = {"from_attributes": True}
