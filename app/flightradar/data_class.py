from logging import exception
from urllib.request import urlopen, Request
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

from .flight import flights_to_json

FLIGHTS_API_PATTERN = ('https://data-live.flightradar24.com/zones'
                       '/fcgi/feed.js?bounds={},{},{},{}'
                       '&faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1'
                       '&estimated=1&maxage=14400&gliders=1&stats=1')

HEADERS = {'Connection': 'keep-alive',
           'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; '
                          'x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome')}

API_STRING = ("https://data-live.flightradar24.com/clickhandler/?flight={flight_id}")

def flights_to_json(flights: List[BriefFlight]):
    data = {}
    for flight in flights:
        data[flight.id] = {'id': flight.id, 'lat': flight.lat,
                           'lon': flight.lon,
                           'track': flight.track, 'speed': flight.speed,
                           'pic': get_image_id(flight.track)}
    return json.dumps(data)


def get_image_id(track: int) -> int:
    return 0
class Data:
    """
    Class for getting FlightRadar24 API data.
    """
    def __init__(self) -> None:
        self.API_STRING = API_STRING
        self.api = API()
        self.parser = Parser()
        self.detailed = []  
        
        # RUSSIA?
        self.p1_coords = {"lat" : 59.06, "lon" : 50.00} 
        self.p2_coords = {"lat" : 30.97, "lon" : 36.46}
        
        # PTOWN
        # p1_coords = {"lat" : 37.8, "lon" : 37.6} 
        # p2_coords = {"lat" : -121.90, "lon" : -121.78}
        
    def get_area(self, area: Area):
        """Returns all available flights within the specified area."""
        req = Request(FLIGHTS_API_PATTERN.format(*area),
                      headers=HEADERS)
        return self.parse_flights(
            json.loads(urlopen(req).read().decode()))

    def parse_flights(self, data: dict):
        """Finds all flights in the response and builds their instances."""
        return [BriefFlightBase.create(key, data[key])
                  for key in data if isinstance(data[key], list)]
          
    def get_data(self):
        p1 = Point(**self.p1_coords)
        p2 = Point(**self.p2_coords)

        mapp = {"sw" : p1, "ne" : p2}
        area = Area(**mapp)
        
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
            "detailed" : self.detailed
        }

    def run(self):
        return asyncio.run(self.async_main()) 
       
    def __str__(self):
        return f"{len(self.detailed)}" 
  

