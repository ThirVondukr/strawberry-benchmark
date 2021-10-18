import strawberry
from strawberry.extensions.tracing import ApolloTracingExtension

from schema.queries import Query


schema = strawberry.Schema(
    query=Query,
     extensions=(
        ApolloTracingExtension,
    )
)