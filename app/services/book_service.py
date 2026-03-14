from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List
import uuid

from app.models.book import Book
from app.models.user_book import UserBook
from app.schemas.book import BookCreate
from app.schemas.user_book import UserBookCreate, UserBookUpdate
from app.core.exceptions import NotFoundError, BadRequestError


class BookService:
    # --- Global Book Catalog ---
    @staticmethod
    async def get_all_books(db: AsyncSession) -> List[Book]:
        stmt = select(Book)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def create_book(db: AsyncSession, book_data: BookCreate) -> Book:
        new_book = Book(**book_data.model_dump())
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book

    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: uuid.UUID) -> Book:
        stmt = select(Book).where(Book.id == book_id)
        result = await db.execute(stmt)
        book = result.scalar_one_or_none()
        if not book:
            raise NotFoundError(f"Book with id {book_id} not found in catalog")
        return book

    # --- User's Personal Book List (Entities for the assignment) ---
    @staticmethod
    async def get_user_books(db: AsyncSession, user_id: uuid.UUID) -> List[UserBook]:
        stmt = select(UserBook).where(UserBook.user_id ==
                                      user_id).options(selectinload(UserBook.book))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def add_book_to_user(db: AsyncSession, user_id: uuid.UUID, data: UserBookCreate) -> UserBook:
        # Check if book exists
        await BookService.get_book_by_id(db, data.book_id)

        # Check if already added
        stmt = select(UserBook).where(UserBook.user_id ==
                                      user_id, UserBook.book_id == data.book_id)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            # Using 404/400 as appropriate
            raise NotFoundError("Book already in your list")

        user_book = UserBook(
            user_id=user_id,
            book_id=data.book_id,
            status=data.status
        )
        db.add(user_book)
        await db.commit()

        # Load book details for response
        stmt = select(UserBook).options(selectinload(UserBook.book)).where(
            UserBook.id == user_book.id).execution_options(populate_existing=True)
        res = await db.execute(stmt)
        return res.scalar_one()

    @staticmethod
    async def update_user_book(
        db: AsyncSession,
        association_id: uuid.UUID,
        user_id: uuid.UUID,
        data: UserBookUpdate
    ) -> UserBook:
        stmt = select(UserBook).where(
            UserBook.id == association_id, UserBook.user_id == user_id)
        result = await db.execute(stmt)
        user_book = result.scalar_one_or_none()
        if not user_book:
            raise NotFoundError("Entry not found in your list")

        user_book.status = data.status
        await db.commit()

        stmt = select(UserBook).options(selectinload(UserBook.book)).where(
            UserBook.id == user_book.id).execution_options(populate_existing=True)
        res = await db.execute(stmt)
        return res.scalar_one()

    @staticmethod
    async def remove_user_book(db: AsyncSession, association_id: uuid.UUID, user_id: uuid.UUID) -> None:
        stmt = delete(UserBook).where(
            UserBook.id == association_id, UserBook.user_id == user_id)
        result = await db.execute(stmt)
        if result.rowcount == 0:
            raise NotFoundError("Entry not found in your list")
        await db.commit()
