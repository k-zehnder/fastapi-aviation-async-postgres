#!/usr/bin/env python

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session, Field, select

from flightradar.my_models import *
# from my_models import *

# from app.persist_to_database import async_main, get_data
from persist_to_database import async_main, get_data

# from app.data_class import Data
from flightradar.data_class import Data


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
        