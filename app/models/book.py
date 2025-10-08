from sqlmodel import SQLModel, Field


class BookBase(SQLModel):
    id: int = Field(primary_key=True, gt=0, unique=True, index=True)
    title: str
    author: str
    pages: int = Field(gt=0)
    rating: float = Field(gt=0)
    price: float = Field(gt=0)


class Book(BookBase, table=True):
    __tablename__ = "book"


class BookCreate(BookBase):
    pass


class BookUpdate(SQLModel):
    title: str | None = None
    author: str | None = None
    pages: int | None = Field(default=None, gt=0)
    rating: float | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)


class GetBooksParams(SQLModel):
    model_config = {"extra": "forbid"}
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, gt=0, le=50)
    title: str | None = None
    min_pages: int | None = Field(default=None, gt=0)
