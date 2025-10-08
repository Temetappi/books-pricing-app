from typing import Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseCRUD
from app.core.db import get_session
from app.models.book import Book, BookCreate, BookUpdate, GetBooksParams


class BookCRUD(BaseCRUD[Book, BookCreate, BookUpdate]):
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.db_session = db_session

    async def create(self, book_in: BookCreate) -> Book:
        book = Book(**book_in.model_dump())
        self.db_session.add(book)
        await self.db_session.commit()
        await self.db_session.refresh(book)
        return book

    async def get_by_id(self, book_id: int, raise_not_found: bool = True) -> Book:
        statement = select(Book).where(Book.id == book_id)
        results = await self.db_session.execute(statement)
        book = results.scalars().first()
        if not book and raise_not_found:
            raise HTTPException(
                status_code=404, detail=f"Book not found with id {book_id}"
            )
        return book

    async def get_by_criteria(self, params: GetBooksParams) -> Sequence[Book]:
        statement = select(Book)
        if params.title:
            statement = statement.where(Book.title == params.title)
        if params.min_pages:
            statement = statement.where(Book.pages >= params.min_pages)
        results = await self.db_session.execute(statement=statement)
        return results.scalars().all()

    async def update(self, book_id: int, book_data: BookUpdate) -> Book:
        book = await self.get_by_id(book_id=book_id)
        book_data_dict = book_data.model_dump(exclude_unset=True)
        for key, value in book_data_dict.items():
            setattr(book, key, value)

        self.db_session.add(book)
        await self.db_session.commit()
        await self.db_session.refresh(book)

        return book

    async def delete(self, book_id: int) -> None:
        book = await self.get_by_id(book_id=book_id)
        await self.db_session.delete(book)
        await self.db_session.commit()
