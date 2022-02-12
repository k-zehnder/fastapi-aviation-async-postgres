import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session, Field, select

from models import *
# from . import crud

from persist_to_database import async_main

from dataclass.flightradar.api import API
from dataclass.data_class import Data

        
async def get_data():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:password@localhost/foo",
        echo=False,
    )
    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(
        engine, expire_on_commit=True, class_=AsyncSession
    )
    async with async_session() as session:
        async with session.begin():
            statement = select(Response).where(Response.name=="controller1")
            result = await session.execute(statement)
            c1_responses = result.one()       
            print(c1_responses)
                
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()
    
if __name__ == "__main__":
    print()

    # LIVE DATA
    data = Data()
    data = data.run()
    print("\n=============")
    # print(f"data {data}")
    print(f'# detailed returned: {len(data["detailed"])}')
    
    # get data
    asyncio.run(async_main(data))
    
    # retrieve data
    asyncio.run(get_data())
        