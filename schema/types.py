from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import strawberry
from strawberry.types import Info


@strawberry.type(name="Author")
class AuthorType:
    id: int = strawberry.field(
        description="""
        The ID of the author.
        """
    )

    first_name: str = strawberry.field(
        description="""
        The first name of the author.
        """
    )

    last_name: str = strawberry.field(
        description="""
        The last name of the author.
        """
    )

    @strawberry.field(description="The books published by the author.")
    async def books_published(self, info: Info) -> List[BookType]:
        pass


@strawberry.type(name="Tag")
class TagType:
    id: int = strawberry.field(
        description="""
        The ID of the tag.
        """
    )

    name: Optional[str] = strawberry.field(
        description="""
        The name of the tag.
        """
    )


@strawberry.type(name="Book")
class BookType:
    id: int = strawberry.field(
        description="""
        The ID of the book.
        """
    )

    title: str = strawberry.field(
        description="""
        The title of the book.
        """
    )
    
    isbn: str = strawberry.field(
        description="""
        The ISBN (International Standard Book Number) of the book.
        """
    )

    published_at: datetime = strawberry.field(
        description="""
        When the book was published.
        """
    )

    @strawberry.field(description="The authors of the book.")
    async def authors(self, info: Info) -> List[AuthorType]:
        pass

    @strawberry.field(description="The tags of the book.")
    async def tags(self, info: Info) -> List[TagType]:
        pass


@strawberry.type(name="Store")
class StoreType:
    id: int = strawberry.field(
        description="""
        The ID of the store.
        """
    )

    @strawberry.field(description="The books in the store.")
    async def books(self, info: Info) -> List[BookType]:
        pass