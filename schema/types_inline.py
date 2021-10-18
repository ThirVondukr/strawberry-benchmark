from datetime import datetime
from typing import List

import strawberry

from schema.types import AuthorType, TagType


@strawberry.type(name="BookInline")
class BookInlineType:
    id: strawberry.ID
    title: str
    isbn: str
    published_at: datetime
    authors: List[AuthorType]
    tags: List[TagType]


@strawberry.type(name="StoreInline")
class StoreInlineType:
    id: strawberry.ID
    books: List[BookInlineType]
