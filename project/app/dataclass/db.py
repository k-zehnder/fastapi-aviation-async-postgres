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
