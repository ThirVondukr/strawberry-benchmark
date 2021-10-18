from sqlalchemy import Column, Integer, String, DateTime, select, func, ForeignKey
from sqlalchemy.orm import column_property, relationship

from .base import Base


class StoreBooksRelationship(Base):
    __tablename__ = "book_store_relationship"

    book_id = Column(Integer, ForeignKey("book.id"), primary_key=True)
    store_id = Column(Integer, ForeignKey("store.id"), primary_key=True)

    book = relationship("Book")


class Store(Base):
    __tablename__ = "store"

    id = Column(Integer, primary_key=True)
    books = relationship("Book", secondary="book_store_relationship")


class AuthorBookRelationship(Base):
    __tablename__ = "book_author_relationship"

    book_id = Column(Integer, ForeignKey("book.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"), primary_key=True)

    book = relationship("Book")
    author = relationship("Author")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=60))


class BookTagRelationship(Base):
    __tablename__ = "book_tag_relationship"
    book_id = Column(Integer, ForeignKey("book.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)

    book = relationship("Book")
    tag = relationship("Tag")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=255), nullable=False)
    isbn = Column(String(length=32), nullable=False)
    published_at = Column(DateTime, nullable=False)

    authors = relationship("Author", secondary=AuthorBookRelationship.__table__)
    tags = relationship("Tag", secondary=BookTagRelationship.__table__)


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(length=60), nullable=False)
    last_name = Column(String(length=60), nullable=False)

    published_books_count = column_property(
        select(func.count(Book.id))
        .filter(AuthorBookRelationship.author_id == id)
        .scalar_subquery(),
        deferred=True,
    )
