from mimetypes import init
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session, Field
import urllib
import os


def build_uri() -> str:
    USER = "postgres"
    PASS = "password"
    HOST = "127.0.0.1"
    PORT = 5432
    DB = "foo"

    host_server = os.environ.get('host_server', 'localhost')
    db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
    database_name = os.environ.get('database_name', 'foo')
    db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
    db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'password')))
    DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(db_username, db_password, host_server, db_server_port, database_name)
    return DATABASE_URL


def get_session():
    with Session(engine) as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session_async() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

def create_db_and_tables(remove_existing_db=False):
    if remove_existing_db:
        print("[x] removing existing tables.")
        SQLModel.metadata.drop_all(engine)
    print("[x] creating tables.")
    SQLModel.metadata.create_all(engine)
    
# if __name__ == "__main__":
#     print()
    # DATABASE_URL = build_uri()
    # engine = create_engine(DATABASE_URL, echo=False, future=True)
    # create_db_and_tables(remove_existing_db=True)
    