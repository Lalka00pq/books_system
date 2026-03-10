from datetime import date, datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, max_length=20)
    genre: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    publisher: Optional[str] = Field(None, max_length=100)
    publish_date: Optional[date] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookPatch(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, max_length=20)
    genre: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    publisher: Optional[str] = Field(None, max_length=100)
    publish_date: Optional[date] = None

class BookResponse(BookBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
