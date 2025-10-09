from sqlalchemy import Column, Integer, String, Float

from app.core.db import Base


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    author = Column(String(256), nullable=False)
    pages = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
