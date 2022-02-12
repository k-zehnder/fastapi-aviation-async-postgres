#!/usr/bin/env python

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session, Field, select

from app.my_models import *

from app.persist_to_database import async_main, get_data

from app.flightradar import api
from app.data_class import Data


from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
async def pong():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}

if __name__ == "__main__":
    print()

    # LIVE DATA
    data = Data()
    data = data.run()
    # print(f"data {data}")
    print(f'# detailed returned: {len(data["detailed"])}')
    
    # get data
    asyncio.run(async_main(data))
    
    # retrieve data
    asyncio.run(get_data())
        