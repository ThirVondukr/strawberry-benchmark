from typing import Optional

import strawberry
from strawberry.types import Info

from schema.types import StoreType

@strawberry.type
class Query:
    @strawberry.field(description="Gets a store by ID.")
    async def store(self, info: Info, id: strawberry.ID) -> Optional[StoreType]:
        pass