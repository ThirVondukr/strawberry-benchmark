import strawberry

from schema.queries import Query


schema = strawberry.Schema(
    query=Query,
)
