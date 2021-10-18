import asyncio
import random
from typing import List

import faker

import settings
from database.base import get_session, Base
from database.models import Tag, Author, Book, Store

_faker = faker.Faker()


def generate_tags(*, count: int = settings.seeding.tags_count) -> List[Tag]:
    return [Tag(name=_faker.word()) for _ in range(count)]


def generate_authors(*, count: int = settings.seeding.authors_count) -> List[Author]:
    return [
        Author(
            first_name=_faker.first_name(),
            last_name=_faker.last_name(),
        )
        for _ in range(count)
    ]


def generate_books(
    *,
    tags: List[Tag],
    authors: List[Author],
    count: int = settings.seeding.books_count,
    tags_per_book: int = settings.seeding.tags_per_book,
    authors_per_book: int = settings.seeding.authors_per_book,
):
    return [
        Book(
            title=" ".join(_faker.words()),
            isbn=_faker.isbn13(),
            published_at=_faker.past_datetime(start_date="-10y"),
            tags=random.sample(tags, k=tags_per_book),
            authors=random.sample(authors, k=authors_per_book),
        )
        for _ in range(count)
    ]


def generate_stores(
    *,
    books: List[Book],
    count: int = settings.seeding.stores_count,
    books_per_store: int = settings.seeding.books_per_store,
) -> List[Store]:
    return [
        Store(books=random.sample(books, k=books_per_store))
        for _ in range(count)
    ]


async def main():
    async with get_session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

    tags = generate_tags()
    authors = generate_authors()
    books = generate_books(tags=tags, authors=authors)
    stores = generate_stores(books=books)

    async with get_session() as session:
        session.add_all(tags)
        session.add_all(authors)
        session.add_all(books)
        session.add_all(stores)
        await session.commit()


if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
