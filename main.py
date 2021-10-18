from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from schema import schema


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(router=GraphQLRouter(schema=schema, graphiql=True))
    return app

app = create_application()