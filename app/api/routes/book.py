from typing import Annotated, Sequence

from fastapi import APIRouter, Query, Depends, HTTPException, Path

from app.repository.book import BookRepository
from app.schemas.book import GetBooksParams, BookCreate, BookUpdate, Book

router = APIRouter(tags=["books"])


@router.post("/", response_model=Book)
async def create_book(
    book_in: BookCreate,
    book_crud: BookRepository = Depends(BookRepository),
) -> Book:
    if await book_crud.get_by_id(book_in.id, raise_not_found=False):
        raise HTTPException(
            status_code=400, detail=f"A book with id {book_in.id} already exists!"
        )
    book = await book_crud.create(book_in)
    return book


@router.get("/{id}", response_model=Book)
async def get_book(
    id: Annotated[int, Path(title="The ID of the book to get", ge=1)],
    book_crud: BookRepository = Depends(BookRepository),
) -> Book:
    book = await book_crud.get_by_id(id)
    return book


@router.get("/")
async def get_books(
    filter_query: Annotated[GetBooksParams, Query()],
    book_crud: BookRepository = Depends(BookRepository),
) -> Sequence[Book]:
    books = await book_crud.get_by_criteria(filter_query)
    return books


@router.put("/{id}", response_model=Book)
async def update_book(
    id: int,
    book_data: BookUpdate,
    book_crud: BookRepository = Depends(BookRepository),
) -> Book:
    book = await book_crud.update(id, book_data)
    return book


@router.delete("/{id}")
async def delete_book(
    id: int, book_crud: BookRepository = Depends(BookRepository)
) -> None:
    await book_crud.delete(id)
