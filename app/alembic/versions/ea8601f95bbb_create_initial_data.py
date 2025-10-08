"""Create initial data

Revision ID: ea8601f95bbb
Revises: 0c27ed846584
Create Date: 2025-10-07 19:01:03.349228

"""

from alembic import op
from sqlalchemy.orm import Session

from app.models.book import Book

# revision identifiers, used by Alembic.
revision = "ea8601f95bbb"
down_revision = "0c27ed846584"
branch_labels = None
depends_on = None


def upgrade():
    session = Session(op.get_bind())

    data = {
        1: {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "pages": 324,
            "rating": 4.8,
            "price": 14.99,
        },
        2: {
            "title": "1984",
            "author": "George Orwell",
            "pages": 328,
            "rating": 4.7,
            "price": 12.95,
        },
        3: {
            "title": "Animal Farm",
            "author": "George Orwell",
            "pages": 112,
            "rating": 4.6,
            "price": 8.99,
        },
        4: {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "pages": 279,
            "rating": 4.6,
            "price": 9.99,
        },
        5: {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "pages": 180,
            "rating": 4.4,
            "price": 10.99,
        },
    }

    books = [Book(id=id, **values) for id, values in data.items()]
    for book in books:
        session.add(book)
    session.commit()


def downgrade():
    pass
