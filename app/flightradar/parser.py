from .models import *


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
        if data["aircraft"].get("model") is None:
            data["aircraft"]["model"] = data["model"].get("model", "model")
            data["aircraft"]["model"] = {"name" : "no_name", "short": "no_short"}
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
            data["airline"] = data.get("airline", "airline")
            data["airline"] = {"name" : "no_name", "short": "no_short"}

        if data["airline"].get("code") is None:
            data["airline"].get("code", "code")
            data["airline"]["code"] = {"iata" : "no_iata", "icao": "no_icao"}
        
        if  data["airline"].get("short") is None:
            data["airline"].get("short", "short")
            data["airline"]["short"] = "no_short"   
        
        return data