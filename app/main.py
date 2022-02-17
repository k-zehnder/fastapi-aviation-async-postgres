#!/usr/bin/env python

import asyncio

from flightradar.models import *

from persist_to_database import async_main, get_one_response_from_db, get_all_briefs

from flightradar.data_class import Data


if __name__ == "__main__":
    print()

    # LIVE DATA FROM FLIGHT RADAR
    data = Data()
    data = data.run()
    
    # UNCOMMENT FOR VERBOSE DATA OUTPUT
    # print(f"data {data}")
    
    # SANITY CHECK
    print(f'# brief returned: {len(data["briefs"])}')
    print(f'# detailed returned: {len(data["detailed"])}')

    # PERSIST DATA TO POSTGRES
    asyncio.run(async_main(data)) 
    
    # ACCESS DB AND SHOW FIRST RESPONSE
    asyncio.run(get_one_response_from_db())

    # ACCESS DB AND GET ALL BRIEF FLIGHTS
    asyncio.run(get_all_briefs())
 