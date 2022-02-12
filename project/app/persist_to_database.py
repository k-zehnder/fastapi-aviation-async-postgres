import json
from os import remove
from typing import Dict, List

import sqlmodel
from sqlmodel import create_engine, SQLModel, Session, select
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from models import *
from db import build_uri
# from . import crud

from dataclass.flightradar.api import API
from dataclass.data_class import Data

from hero_models import Team, TeamCreate



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
        r1 = Response(
            name="controller1",
            time_created=datetime.datetime.now()
        )   

        for flight in data["detailed"]:
            f = DetailedFlight(
                identification=flight.identification,
                response_id=r1.id
            )
            print(f)
            print("----")
            session.add(f)
            
        await session.commit()
        await session.refresh(f)
            
        # for AsyncEngine created in function scope, close and
        # clean-up pooled connections
    await engine.dispose()
        
# statement = select(Response).where(Response.id==1)
# result = await session.execute(statement)
# response = result.one()
# print(response)