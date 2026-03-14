import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_book import UserBookResponse, UserBookCreate, UserBookUpdate
from app.services.book_service import BookService
from app.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=List[UserBookResponse])
async def get_my_books(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[UserBookResponse]:
    """Get list of books in user's personal collection."""
    return await BookService.get_user_books(db, current_user.id)


@router.get("/{association_id}", response_model=UserBookResponse)
async def get_my_book(
    association_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserBookResponse:
    """Get details of a specific book in user's collection."""
    return await BookService.get_book_by_id(db, association_id)


@router.post("", response_model=UserBookResponse, status_code=status.HTTP_201_CREATED)
async def add_book_to_my_list(
    data: UserBookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserBookResponse:
    """Associate a book from catalog with user's collection."""
    return await BookService.add_book_to_user(db, current_user.id, data)


@router.put("/{association_id}", response_model=UserBookResponse)
async def update_my_book_status(
    association_id: uuid.UUID,
    data: UserBookUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserBookResponse:
    """Update status of a book in user's collection."""
    return await BookService.update_user_book(db, association_id, current_user.id, data)


@router.delete("/{association_id}", status_code=status.HTTP_200_OK)
async def remove_from_my_list(
    association_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Remove a book from user's collection."""
    await BookService.remove_user_book(db, association_id, current_user.id)
    return {"message": "Success"}
