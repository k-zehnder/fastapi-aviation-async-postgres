from codecs import Codec
from tokenize import String
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from typing import List, Optional, Any, Type
from pydantic import BaseModel, validator, parse_obj_as
import datetime


        
class ResponseBase(SQLModel):
    name: str = Field(index=True)
    time_created: datetime.datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
    ))   
    class Config:
        orm_mode = True
        
class Response(ResponseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    flights: List["DetailedFlight"] = Relationship(back_populates="response")
    
    class Config:
        orm_mode = True

class DetailedFlightBase(SQLModel):
    identification: str = Field(default=None, primary_key=False)
    
    response_id: Optional[int]= Field(default=None, foreign_key="response.id")
    
class DetailedFlight(DetailedFlightBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
    response: Optional[Response] = Relationship(back_populates="flights")
    
    class Config:
        orm_mode = True

class ResponseRead(ResponseBase):
    id: int
  
# class ResponseRead(ResponseBase):
#     db_data: List[DetailedFlight]
    

class ResponseCreate(ResponseBase):
    pass

class Number(BaseModel):
    default: Optional[str] = Field(default="default_default", primary_key=False)
    alternative: Optional[str] = Field(default="alternative_default", primary_key=False)
    
    class Config:
        orm_mode = True         

class Identification(BaseModel):
    identification: str = Field(default=None, primary_key=False, alias="id")
    callsign: str = Field(default=None, primary_key=False)
    number: Optional[Number] = None

    class Config:
        orm_mode = True 
        allow_population_by_field_name=True
class Code(BaseModel):
    iata: Optional[str] = Field(default=None, primary_key=False)
    icao:Optional[str] = Field(default=None, primary_key=False)

    # @validator("iata")
    # def is_valid_icao(cls, icao):
    #     return icao == "valid"

class Airline(BaseModel):
    name: Optional[str] = Field(default=None, primary_key=False)
    short: Optional[str] = Field(default=None, primary_key=False)
    url: Optional[str] = Field(default=None, primary_key=False)
    code: Optional[Code] = Field(default=None, primary_key=False)

class Model(BaseModel):
    code: Optional[str] = Field(default=None, primary_key=False)
    text: Optional[str] = Field(default=None, primary_key=False)

class Aircraft(BaseModel):
    countryId: Optional[int] = Field(default=None, primary_key=False)
    registration: Optional[str] = Field(default=None, primary_key=False)
    hex: Optional[str] = Field(default=None, primary_key=False)
    age: Optional[str] = Field(default=None, primary_key=False)
    msn: Optional[str] = Field(default=None, primary_key=False)
    images: Optional[List[str]] = Field(default=None, primary_key=False)
    model: Optional[Model] = Field(default=None, primary_key=False)
    
class DetailedFlightCreate(DetailedFlightBase):
    identification: Identification
    aircraft: Aircraft
    airline: Airline
    
class ResponseCreate(ResponseBase):
    pass

#NOTE: AllFlightRead INHERIT FROM REGULAR NOT SQLMODEL!      
class AllFlightRead(BaseModel):
    time_read: datetime.datetime = Field(
    sa_column=Column(
        DateTime(timezone=True),
        nullable=False
    )) 
    db_data: List[DetailedFlight]

#NOTE: BriefFlight INHERIT FROM REGULAR NOT SQLMODEL!
class BriefFlightBase(BaseModel):
    # flight_id: Any = "23"
    lat: float = 23.4
    lon: float = 25.6
    track: int = 25
    speed: int = 250
    pic: str = "pic"
    id: Any = 1
    
    @validator("speed")
    def speed_sanity_check(cls, speed):
        if speed > 1000:
            raise ValueError("speed invalid.")
        return speed
    
    class Config:
        orm_mode = True
        
class BriefFlight(BriefFlightBase):
    pass

    class Config:
        orm_mode = True 

class BriefFlightCreate(BriefFlightBase):
    pass

class Point(BaseModel):
    lat: float = 0.0
    lon: float = 0.0
    
    def __str__(self) -> str:
        return '({}, {})'.format(self.lat, self.lon) 
    
class Area(BaseModel):
    sw: Point
    ne: Point

    def __str__(self) -> str:
        """Allows to unpack data this way: *area"""
        return '{}, {}, {}, {}'.format(self.sw.lat, self.sw.lon,
                                       self.ne.lat, self.ne.lon)
    def __iter__(self):
        return (coord for coord in (self.sw.lat, self.sw.lon,
                                       self.ne.lat, self.ne.lon))
    