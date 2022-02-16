#!/usr/bin/env python

import asyncio

from flightradar.models import *

from persist_to_database import async_main, get_data

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

