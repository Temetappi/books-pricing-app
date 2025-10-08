import pytest
from httpx import AsyncClient
from sqlmodel import Session

from app.models.book import Book


@pytest.mark.asyncio
async def test_create_book(client: AsyncClient) -> None:
    data = {
        "id": 1,
        "title": "title1",
        "author": "author1",
        "pages": 100,
        "rating": 2.5,
        "price": 10,
    }
    async with client:
        response = await client.post(
            "/books/",
            json=data,
        )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["author"] == data["author"]
    assert content["pages"] == data["pages"]
    assert content["rating"] == data["rating"]
    assert content["price"] == data["price"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {
            "id": -1,
            "title": "title1",
            "author": "author1",
            "pages": 100,
            "rating": 2.5,
            "price": 10,
        },
        {
            "id": 1,
            "title": None,
            "author": "author2",
            "pages": 100,
            "rating": 2.5,
            "price": 10,
        },
        {
            "id": 1,
            "title": "title1",
            "author": None,
            "pages": 100,
            "rating": 2.5,
            "price": 10,
        },
        {
            "id": 1,
            "title": "title2",
            "author": "author2",
            "pages": -400,
            "rating": 2.5,
            "price": 10,
        },
        {
            "id": 1,
            "title": "title1",
            "author": "author1",
            "pages": 100,
            "rating": -1,
            "price": 10,
        },
        {
            "id": 1,
            "title": "title1",
            "author": "author1",
            "pages": 100,
            "rating": -1,
            "price": -1,
        },
    ],
)
@pytest.mark.asyncio
async def test_create_book_invalid(client: AsyncClient, data) -> None:
    async with client:
        response = await client.post(
            "/books/",
            json=data,
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_book(session: Session, client: AsyncClient) -> None:
    book = Book(id=1, title="title1", author="author1", pages=100, rating=2.5, price=10)
    session.add(book)
    await session.flush()
    async with client:
        response = await client.get(f"/books/{book.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == book.title
    assert content["author"] == book.author
    assert content["pages"] == book.pages
    assert content["rating"] == book.rating
    assert content["price"] == book.price


@pytest.mark.asyncio
async def test_read_book_not_found(client: AsyncClient) -> None:
    id = 8
    async with client:
        response = await client.get(
            f"/books/{id}",
        )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == f"Book not found with id {id}"


@pytest.mark.asyncio
async def test_read_books(
    session: Session,
    client: AsyncClient,
) -> None:
    book_1 = Book(
        id=1, title="title1", author="author1", pages=100, rating=2.5, price=10
    )
    book_2 = Book(
        id=2, title="title2", author="author2", pages=200, rating=4.5, price=10
    )
    session.add(book_1)
    session.add(book_2)
    session.add(book_1)
    session.add(book_2)
    await session.flush()
    async with client:
        response = await client.get(
            "/books/",
        )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2


@pytest.mark.asyncio
async def test_read_books_filter_by_title(
    session: Session,
    client: AsyncClient,
) -> None:
    book_1 = Book(
        id=1, title="title1", author="author1", pages=100, rating=2.5, price=10
    )
    book_2 = Book(
        id=2, title="title2", author="author2", pages=200, rating=4.5, price=10
    )
    session.add(book_1)
    session.add(book_2)
    await session.flush()
    async with client:
        response = await client.get(
            "/books/",
            params={"title": "title1"},
        )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["id"] == book_1.id
    assert content[0]["title"] == book_1.title
    assert content[0]["author"] == book_1.author
    assert content[0]["pages"] == book_1.pages
    assert content[0]["rating"] == book_1.rating


@pytest.mark.asyncio
async def test_update_book(session: Session, client: AsyncClient) -> None:
    book = Book(id=1, title="title1", author="author1", pages=100, rating=2.5, price=10)
    session.add(book)
    await session.flush()

    data = {"title": "Updated title"}
    async with client:
        response = await client.put(
            f"/books/{book.id}",
            json=data,
        )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == book.id
    assert content["title"] == data["title"]


@pytest.mark.asyncio
async def test_update_book_not_found(client: AsyncClient) -> None:
    id = 8
    data = {"title": "Updated title", "description": "Updated description"}
    async with client:
        response = await client.put(
            f"/books/{8}",
            json=data,
        )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == f"Book not found with id {id}"


@pytest.mark.asyncio
async def test_delete_book(session: Session, client: AsyncClient) -> None:
    book = Book(id=1, title="title1", author="author1", pages=100, rating=2.5, price=10)
    session.add(book)
    await session.flush()
    async with client:
        response = await client.delete(
            f"/books/{book.id}",
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_book_not_found(client: AsyncClient) -> None:
    id = 8
    async with client:
        response = await client.delete(
            f"/books/{8}",
        )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == f"Book not found with id {id}"
