from .api import API

from .my_models import *

class Parser:
    
    def build_number(self, data):
        return NumberCreate(**data["identification"]["number"])
    
    def build_identification(self, data, number: Number):
        return Identification(
                identification=data["identification"]["id"],
                callsign=data["identification"]["callsign"],
                number=number.dict()
                )
        
    def build_model(self, data):
        return Model(**data["aircraft"]["model"])
    
    def build_aircraft(self, data, model):
        return Aircraft(
            country_id=data["aircraft"]["countryId"],
            registration=data["aircraft"]["registration"],
            hex=data["aircraft"]["hex"],
            age=data["aircraft"]["msn"],
            model=model.dict()
        )   
        
    def build_code(self, data):
        return Code(**data["airline"]["code"])
        
    def build_airline(self, data):
        data = self._handle_missing_airline(data)
        code = self.build_code(data)
        if  data["airline"].get("short") is None:
            print("SHORT DOESNT EXIST")
            data["airline"].get("short", "short")
            data["airline"]["short"] = "no_short"      
        return Airline(
            name=data["airline"]["name"],
            short=data["airline"]["short"],
            code=code.dict()
        )
        
    def build_detailed(self, identification, airline, aircraft):
        return DetailedFlightCreate(
                identification=identification.dict(),
                airline=airline.dict(),
                aircraft=aircraft.dict()
        )
        
    def _handle_missing_airline(self, data):
        if data.get("airline") is None:
            print("AIRLINE DOESNT EXIST")
            data["airline"] = data.get("airline", "airline")
            data["airline"] = {"name" : "no_name", "short": "no_short"}
        # else:
        #     print("AIRLINE EXISTS")

        if data["airline"].get("code") is None:
            print("CODE DOESNT EXIST")
            data["airline"].get("code", "code")
            data["airline"]["code"] = {"iata" : "no_iata", "icao": "no_icao"}
        # else:
        #     print("CODE EXISTS")
        
        return data