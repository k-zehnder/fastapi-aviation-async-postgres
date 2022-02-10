import json
from operator import ge
import httpx
import asyncio
from typing import List, Dict
import datetime

from flightradar.api import API

#TODO: #from dataclass import schemas
from schemas.brief_flight import BriefFlight, BriefFlightBase, BriefFlightCreate, BriefFlightUpdate
from schemas.detailed_flight import DetailedFlight, DetailedFlightBase, DetailedFlightCreate, DetailedFlightRead
from schemas.detailed_flight import Song, SongBase, SongCreate, SongRead
from schemas.coordinates import Point, Area

import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator

from sqlmodel import create_engine, SQLModel, Session, Field

HEADERS = {'Connection': 'keep-alive',
           'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; '
                          'x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome')}

API_STRING = ("https://data-live.flightradar24.com/clickhandler/?flight={flight_id}")

class Data:
    """
    Class for getting FlightRadar24 API data.
    """
    def __init__(self) -> None:
        self.API_STRING = API_STRING
        self.api = API()
        self.detailed = []        
                    
    def get_data(self):
        # area = Area(Point(37.8, 37.6), Point(-121.90, -121.78))
        area = Area(Point(59.06, 55.00), Point(30.97, 36.46))
        return self.parse_data(json.loads(self.api.get_area(area)))
            
    def parse_data(self, data):
        briefs = [BriefFlightCreate(**data[item]) for item in data]
        return [flight.id for flight in briefs]
    
    async def make_request_async(self, flight_id, client):
        r = await client.get(self.API_STRING.format(flight_id=flight_id))
        data = r.json()
        print(json.dumps(data, indent=4, sort_keys=False))
        
        detailed = DetailedFlightCreate(
            identification=data["identification"]["id"]
        )
        self.detailed.append(detailed)
        # DetailedFlight.from_orm(detailed)
        
        # self.detailed.append(DetailedFlightCreate(**r.json()))
           
    async def async_main(self):
        overhead_ids = self.get_data()
        async with httpx.AsyncClient() as client:
            await asyncio.gather(
                *[self.make_request_async(flight_id, client) for flight_id in overhead_ids]
            )
        return {
            "time" : datetime.datetime.utcnow(),
            "detailed" : self.detailed
        }

    def run(self):
        return asyncio.run(self.async_main()) 
       
    def __str__(self):
        return f"{len(self.detailed)}" 
  
if __name__ == "__main__":
    import time

    if os.path.exists("test.db"):
        os.remove("test.db")
        print("deleting..")
        time.sleep(5)


    # get data
    DATABASE_URL_TRY = "sqlite://///home/batman/Desktop/dataclass/test.db"
    engine = create_engine(DATABASE_URL_TRY, echo=True, connect_args={"check_same_thread":False})
    SQLModel.metadata.create_all(engine)
    
    obj = Data()
    print(obj)
    data = obj.run() # dictionary
    print(type(data))
    print(data)
    
    # with Session(engine) as session:
    #     for item in data["detailed"]:
    #         print(item)
    #         print(item.identification)
    #         print()
    #         time.sleep(10)
            # detailed = DetailedFlightCreate(
            #     identification=item.identification["id"]
            # )
            # print(detailed)
            # print(type(detailed))
            # session.add(detailed)
            # session.commit()
            # session.refresh(detailed)
            # print(DetailedFlight.from_orm(item))
        
        
"""    song = Song(
            name=song.name,
            artist=song.artist
            )
    # song.from_orm(song)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song"""