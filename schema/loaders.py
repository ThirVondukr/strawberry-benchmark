import enum
from collections import defaultdict
from typing import List, Dict, Iterable

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, load_only
from strawberry.dataloader import DataLoader
from strawberry.extensions import Extension

from database.base import get_session
from database.models import Author, AuthorBookRelationship, StoreBooksRelationship, Book, Tag, BookTagRelationship


class DataLoaders(enum.Enum):
    book_authors = enum.auto()
    book_tags = enum.auto()
    store_books = enum.auto()
    author_published_books_count = enum.auto()


async def load_book_authors(book_ids: List[int]) -> List[List[Author]]:
    query = (
        select(AuthorBookRelationship)
        .filter(AuthorBookRelationship.book_id.in_(book_ids))
        .options(joinedload(AuthorBookRelationship.author))
    )
    async with get_session() as session:
        relationships: Iterable[AuthorBookRelationship] = await session.scalars(query)

    authors_by_book_id: Dict[int, List[Author]] = defaultdict(list)
    for rel in relationships:
        authors_by_book_id[rel.book_id].append(rel.author)

    return [authors_by_book_id[book_id] for book_id in book_ids]


async def load_store_books(store_ids: List[int]) -> List[List[Author]]:
    query = (
        select(StoreBooksRelationship)
        .filter(StoreBooksRelationship.store_id.in_(store_ids))
        .options(selectinload(StoreBooksRelationship.book))
    )
    async with get_session() as session:
        relationships: Iterable[StoreBooksRelationship] = await session.scalars(query)

    books_by_store_id: Dict[int, List[Book]] = defaultdict(list)
    for rel in relationships:
        books_by_store_id[rel.store_id].append(rel.book)

    return [books_by_store_id[store_id] for store_id in store_ids]


async def load_book_tags(book_ids: List[int]) -> List[List[Tag]]:
    query = (
        select(BookTagRelationship)
        .filter(BookTagRelationship.book_id.in_(book_ids))
        .options(joinedload(BookTagRelationship.tag))
    )

    async with get_session() as session:
        relationships: Iterable[BookTagRelationship] = await session.scalars(query)

    tags_by_book_id: Dict[int, List[Tag]] = defaultdict(list)
    for rel in relationships:
        tags_by_book_id[rel.book_id].append(rel.tag)

    return [tags_by_book_id[book_id] for book_id in book_ids]


async def load_author_published_books_count(author_ids: List[int]) -> List[int]:
    query = (
        select(Author)
        .filter(Author.id.in_(author_ids))
        .options(load_only(Author.id, Author.published_books_count))
    )

    async with get_session() as session:
        authors: Iterable[Author] = await session.scalars(query)

    authors_books_count: Dict[int, int] = {author.id: author.published_books_count for author in authors}

    return [authors_books_count[author_id] for author_id in author_ids]

class DataLoadersExtension(Extension):
    def on_request_start(self):
        self.execution_context.context.update({
            DataLoaders.book_authors: DataLoader(load_book_authors),
            DataLoaders.book_tags: DataLoader(load_book_tags),
            DataLoaders.store_books: DataLoader(load_store_books),
            DataLoaders.author_published_books_count: DataLoader(load_author_published_books_count),
        })
