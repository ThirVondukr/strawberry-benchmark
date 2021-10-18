import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from schema import schema


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(prefix="/graphql", router=GraphQLRouter(schema=schema, graphiql=True))
    return app


if __name__ == '__main__':
    uvicorn.run("main:create_application", factory=True, reload=True)

