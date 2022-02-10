import os
import datetime
from distutils.command.build import build
import json
import asyncio
from textwrap import indent 
import httpx

from flightradar.api import API
from models import *
from db import build_uri
# from . import crud

from sqlmodel import create_engine


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
        area = Area(Point(59.06, 50.00), Point(30.97, 36.46))
        return self.parse_data(json.loads(self.api.get_area(area)))
            
    def parse_data(self, data):
        briefs = [BriefFlightCreate(**data[item]) for item in data]
        return [flight.id for flight in briefs]
    
    def _debug(self, r):
        data = r.json()["airline"]
        print()
        # print(Identification(**data))
        return(json.dumps(data, indent=4, sort_keys=False))
    
    async def make_request_async(self, flight_id, client):
        r = await client.get(self.API_STRING.format(flight_id=flight_id))
        print(self._debug(r))
        
        data = r.json()        
        identification = Identification(**data["identification"])
        
        model = Model(**data["aircraft"]["model"])
        
        aircraft = Aircraft(
            country_id=data["aircraft"]["countryId"],
            registration=data["aircraft"]["registration"],
            hex=data["aircraft"]["hex"],
            age=data["aircraft"]["msn"],
            model=model.dict()
        )       
        
        print(json.dumps(data["aircraft"], indent=4, sort_keys=False))        
        # code = Code(**data["airline"]["code"])
        # airline = Airline(
        #     name=data["airline"]["name"],
        #     short=data["airline"]["short"],
        #     code=code.dict()
        # )

        detailed = DetailedFlightCreate(
                        identification=identification.dict(),
                        # airline=airline.dict(),
                        aircraft=aircraft.dict()
        )
        
        # print(f"detailed: {detailed}")
        
        self.detailed.append(detailed)      
        
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
    obj = Data()    
    print(obj)
    data = obj.run() # dictionary
    print(type(data))
    # print(data)

    print()
    DATABASE_URL = build_uri()
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)