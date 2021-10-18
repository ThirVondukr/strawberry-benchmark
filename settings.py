from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "db_"

    database_url: str
    echo: bool


class SeedingSettings(BaseSettings):
    class Config:
        env_prefix = "seeding_"

    tags_count: int
    authors_count: int

    books_count: int
    tags_per_book: int
    authors_per_book: int

    stores_count: int
    books_per_store: int

database = DatabaseSettings(_env_file=".env")
seeding = SeedingSettings(_env_file=".env")
