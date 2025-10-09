from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.repository.base import BaseRepository
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, GetBooksParams


class BookRepository(BaseRepository[Book, BookCreate, BookUpdate]):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(Book, session)

    async def get_by_criteria(self, params: GetBooksParams) -> Sequence[Book]:
        statement = select(Book)
        if params.title:
            statement = statement.where(Book.title == params.title)
        if params.min_pages:
            statement = statement.where(Book.pages >= params.min_pages)
        results = await self.session.execute(statement=statement)
        return results.scalars().all()
