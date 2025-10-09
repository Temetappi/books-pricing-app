from pydantic import BaseModel, Field


class BookBase(BaseModel):
    id: int = Field(gt=0)
    title: str
    author: str
    pages: int = Field(gt=0)
    rating: float = Field(gt=0)
    price: float = Field(gt=0)


class Book(BookBase):
    pass


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    pages: int | None = Field(default=None, gt=0)
    rating: float | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)


class GetBooksParams(BaseModel):
    model_config = {"extra": "forbid"}
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, gt=0, le=50)
    title: str | None = None
    min_pages: int | None = Field(default=None, gt=0)
