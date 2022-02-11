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
    
    counts = 0

    async with async_session() as session:
        async with session.begin():
            """
            This is where you add data.
            """
            r1 = Response(
                name="controller1",
                time_created=datetime.datetime.now())
            
            print(data.keys()) # time, detailed
            print(data["detailed"])
            
            counts += 1
            
            if counts > 1:
                pass
            
            session.add(r1)
            await session.commit()
        # NOTE: this must go outside inner session.begin() block
        await session.refresh(r1)
            
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()
    
    
