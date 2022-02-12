import sqlmodel
from sqlmodel import create_engine, SQLModel, Session, select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from models import *
from db import build_uri
# from . import crud

from dataclass.flightradar.api import API
from dataclass.data_class import Data


async def async_main(data):
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:password@localhost/foo",
        echo=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(
        engine, expire_on_commit=True, class_=AsyncSession
    )
    async with async_session() as session:
        async with session.begin():
            # print(data["detailed"])
            r1 = Response(
                    name="controller1",
                    time_created=datetime.datetime.now(),
                    flights=[DetailedFlight(identification=flight.identification.identification, airline_name=flight.airline.name, airplane_code=flight.aircraft.model.code) for flight in data["detailed"]]
            )   
            session.add(r1)
            
        await session.commit()
                
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()
        
