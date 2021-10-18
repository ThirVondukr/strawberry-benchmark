from typing import Optional

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import selectinload, undefer

from database.base import get_session
from database.models import Store, Book, Author
from schema.types import StoreType
from schema.types_inline import StoreInlineType


@strawberry.type
class Query:
    @strawberry.field(description="Gets a store by ID (uses dataloaders).")
    async def store(self, store_id: int) -> Optional[StoreType]:
        query = select(Store).filter(Store.id == store_id).limit(1)
        async with get_session() as session:
            store = await session.scalar(query)
        return store

    @strawberry.field(description="Gets a store by ID (uses joins).")
    async def store_joined(self, store_id: int) -> Optional[StoreInlineType]:
        query = (
            select(Store)
            .filter(Store.id == store_id)
            .limit(1)
            .options(
                selectinload(Store.books)
                .options(
                    selectinload(Book.authors).options(undefer(Author.published_books_count)),
                    selectinload(Book.tags),
                )
            )
        )
        async with get_session() as session:
            store = await session.scalar(query)
        return store
