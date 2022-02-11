import asyncio

from models import *
# from . import crud

from persist_to_database import async_main

from dataclass.flightradar.api import API
from dataclass.data_class import Data

if __name__ == "__main__":
    print()

    # LIVE DATA
    data = Data()
    data = data.run()
    print("\n=============")
    print(f"data {data}")
    print(f'# detailed returned: {len(data["detailed"])}')
    
    asyncio.run(async_main(data))