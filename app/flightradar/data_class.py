from urllib.request import urlopen, Request
import datetime
import json
import asyncio
import httpx

from .models import *
from .parser import Parser
from .utils import FLIGHTS_API_PATTERN, HEADERS, API_STRING


class Data:
    """
    Class for getting FlightRadar24 API data.
    """
    def __init__(self) -> None:
        self.API_STRING = API_STRING
        self.parser = Parser()
        self.briefs = []
        self.detailed = []  
        
        # RUSSIA?
        self.p1_coords = {"lat" : 59.06, "lon" : 50.00} 
        self.p2_coords = {"lat" : 30.97, "lon" : 36.46}
        
        # PTOWN
        # self.p1_coords = {"lat" : 37.8, "lon" : 37.6} 
        # self.p2_coords = {"lat" : -121.90, "lon" : -121.78}
        
    def get_area(self, area: Area) -> List[BriefFlightCreate]:
        """Returns all available flights within the specified area."""
        req = Request(FLIGHTS_API_PATTERN.format(*area),
                      headers=HEADERS)
        return self.parse_flights(
            json.loads(urlopen(req).read().decode()))

    def parse_flights(self, data: dict):
        """Finds all flights in the response and builds their instances."""
        briefs = [BriefFlightCreate.create(key, data[key])
                  for key in data if isinstance(data[key], list)]
        for b in briefs:
            self.briefs.append(b)
        return briefs
          
    def get_data(self):
        p1 = Point(**self.p1_coords)
        p2 = Point(**self.p2_coords)

        mapp = {"sw" : p1, "ne" : p2}
        area = Area(**mapp)
        
        # self.get_area(area) returns List[BriefFlightCreate]
        return self.get_ids(self.get_area(area)) 

    def get_ids(self, briefs):
            return [flight.flight_id for flight in briefs]            
    
    async def make_request_async(self, flight_id, client):
        r = await client.get(self.API_STRING.format(flight_id=flight_id))
        data = r.json()
        
        number = self.parser.build_number(data)
        identification = self.parser.build_identification(data, number)
        model = self.parser.build_model(data)
        aircraft = self.parser.build_aircraft(data, model) 
        airline = self.parser.build_airline(data)        
        detailed = self.parser.build_detailed(identification, airline, aircraft)                 
        self.detailed.append(detailed) 


    async def async_main(self):
        overhead_ids = self.get_data()
        async with httpx.AsyncClient() as client:
            await asyncio.gather(
                *[self.make_request_async(flight_id, client) for flight_id in overhead_ids]
            )
        return {
            "time" : datetime.datetime.utcnow(),
            "detailed" : self.detailed,
            "briefs" : self.briefs
        }

    def run(self):
        return asyncio.run(self.async_main()) 
       
    def __str__(self):
        return f"{len(self.detailed)}" 
  

