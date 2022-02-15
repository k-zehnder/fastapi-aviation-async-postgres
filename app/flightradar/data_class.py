from logging import exception
import os
import datetime
from distutils.command.build import build
import json
import asyncio
from textwrap import indent 
import httpx

from .api import API

from .my_models import *

from .parser import Parser


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
        self.parser = Parser()
        self.detailed = []  
                    
    def get_data(self):
        # p1_coords = {"lat" : 37.8, "lon" : 37.6} # PTOWN
        # p2_coords = {"lat" : -121.90, "lon" : -121.78}
        
        p1_coords = {"lat" : 59.06, "lon" : 50.00} # RUSSIA?
        p2_coords = {"lat" : 30.97, "lon" : 36.46}

        p1 = Point(**p1_coords)
        p2 = Point(**p2_coords)

        mapp = {"sw" : p1, "ne" : p2}
        area = Area(**mapp)
        
        return self.parse_data(json.loads(self.api.get_area(area)))
            
    def parse_data(self, data):
        briefs = [BriefFlightCreate(**data[item]) for item in data]
        return [flight.id for flight in briefs]
    
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
            "detailed" : self.detailed
        }

    def run(self):
        return asyncio.run(self.async_main()) 
       
    def __str__(self):
        return f"{len(self.detailed)}" 
  

