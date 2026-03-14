import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete

from app.schemas.book import BookResponse, BookCreate, BookUpdate, BookPatch
from app.schemas.user_book import UserBookResponse, UserBookCreate, UserBookUpdate
from app.services.book_service import BookService
from app.dependencies import get_db, get_current_user
from app.models.user import User, UserRole
from app.models.book import Book
from app.core.exceptions import AppException

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


def role_required(role: UserRole):
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role != role:
            raise AppException(
                403, "FORBIDDEN", f"Operation requires {role.value} role")
        return current_user
    return dependency


@router.get("/catalog", response_model=List[BookResponse])
async def get_catalog(db: AsyncSession = Depends(get_db), admin: User = Depends(role_required(UserRole.ADMIN))):
    """Get all books in the global catalog."""
    return await BookService.get_all_books(db)


@router.post("/catalog", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_catalog_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(role_required(UserRole.ADMIN))
) -> BookResponse:
    """Add a new book to the global catalog (Admin only)."""
    return await BookService.create_book(db, book_data)


@router.put("/catalog/{id}", response_model=BookResponse)
async def update_catalog_book(
    id: uuid.UUID,
    book_data: BookUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(role_required(UserRole.ADMIN))
) -> BookResponse:
    await BookService.get_book_by_id(db, id)
    stmt = update(Book).where(Book.id == id).values(
        **book_data.model_dump()).returning(Book)
    res = await db.execute(stmt)
    await db.commit()
    return res.scalar_one()


@router.patch("/catalog/{id}", response_model=BookResponse)
async def patch_catalog_book(
    id: uuid.UUID,
    book_data: BookPatch,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(role_required(UserRole.ADMIN))
) -> BookResponse:
    await BookService.get_book_by_id(db, id)
    update_data = book_data.model_dump(exclude_unset=True)
    if not update_data:
        return await BookService.get_book_by_id(db, id)
    stmt = update(Book).where(Book.id == id).values(
        **update_data).returning(Book)
    res = await db.execute(stmt)
    await db.commit()
    return res.scalar_one()


@router.delete("/catalog/{id}", status_code=status.HTTP_200_OK)
async def delete_catalog_book(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(role_required(UserRole.ADMIN))
) -> dict:
    await BookService.get_book_by_id(db, id)
    await db.execute(delete(Book).where(Book.id == id))
    await db.commit()
    return {"message": "Success"}
