import strawberry

from schema.loaders import DataLoadersExtension
from schema.queries import Query


schema = strawberry.Schema(
    query=Query,
    extensions=(DataLoadersExtension,)
)
