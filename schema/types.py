from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import strawberry
from strawberry.types import Info

from schema.loaders import DataLoaders


@strawberry.type(name="Author")
class AuthorType:
    id: strawberry.ID
    first_name: str
    last_name: str
    books_published: List[BookType]

    @strawberry.field(description="The books published by the author.")
    async def books_published(self, info: Info) -> List[BookType]:
        pass


@strawberry.type(name="Tag")
class TagType:
    id: strawberry.ID
    name: Optional[str]


@strawberry.type(name="Book")
class BookType:
    id: strawberry.ID
    title: str
    isbn: str
    published_at: datetime

    @strawberry.field(description="The authors of the book.")
    async def authors(self, info: Info) -> List[AuthorType]:
        return await info.context[DataLoaders.book_authors].load(self.id)

    @strawberry.field(description="The tags of the book.")
    async def tags(self, info: Info) -> List[TagType]:
        return await info.context[DataLoaders.book_tags].load(self.id)


@strawberry.type(name="Store")
class StoreType:
    id: strawberry.ID

    @strawberry.field(description="The books in the store.")
    async def books(self, info: Info) -> List[BookType]:
        return await info.context[DataLoaders.store_books].load(self.id)
