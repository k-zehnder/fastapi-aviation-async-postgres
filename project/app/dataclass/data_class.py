from logging import exception
import os
import datetime
from distutils.command.build import build
import json
import asyncio
from textwrap import indent 
import httpx

from .flightradar.api import API
from models import *
import db

from pydantic import parse_obj_as
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
        counts = 0
        r = await client.get(self.API_STRING.format(flight_id=flight_id))

        data = r.json()
        
        # if counts < 1:
        #     print(json.dumps(data, indent=4, sort_keys=False))
        # counts += 1
        
        number = NumberCreate(**data["identification"]["number"])
        print(f"number: {number}")
        
        identification = Identification(
                identification=data["identification"]["id"],
                callsign=data["identification"]["callsign"],
                number=number.dict()
                )
        print(f"identification: {identification}")
            
        model = Model(**data["aircraft"]["model"])
        print(f"model: {model}")
        
        aircraft = Aircraft(
            country_id=data["aircraft"]["countryId"],
            registration=data["aircraft"]["registration"],
            hex=data["aircraft"]["hex"],
            age=data["aircraft"]["msn"],
            model=model.dict()
        )   
        print(f"aircraft: {aircraft}")
        print()
        print()
        
        if data.get("airline") is None:
            print("AIRLINE DOESNT EXIST")
            data["airline"] = data.get("airline", "airline")
            data["airline"] = {"name" : "no_name", "short": "no_short"}
            # print(data["airline"])
        else:
            print("AIRLINE EXISTS")
            # print(data["airline"])
        
        if data["airline"].get("code") is None:
            print("CODE DOESNT EXIST")
            data["airline"].get("code", "code")
            data["airline"]["code"] = {"iata" : "no_iata", "icao": "no_icao"}
            # print(data["airline"]["code"])
        else:
            print("CODE EXISTS")
            # print(data["airline"]["code"])
              
        code = Code(**data["airline"]["code"])
        # print(code)

        if  data["airline"].get("short") is None:
            print("SHORT DOESNT EXIST")
            data["airline"].get("short", "short")
            data["airline"]["short"] = "no_short"      
        
        airline = Airline(
            name=data["airline"]["name"],
            short=data["airline"]["short"],
            code=code.dict()
        )
        # print(airline.short, airline.code, airline.code)
        
        detailed = DetailedFlightCreate(
                        identification=identification.dict(),
                        airline=airline.dict(),
                        aircraft=aircraft.dict()
        )
    
        print(f"detailed: {detailed}")
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
  

