from codecs import Codec
from tokenize import String
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from typing import List, Optional, Any, Type
from pydantic import BaseModel, validator
import datetime


class UserBase(SQLModel):
    name: str
    
    class Config:
        orm_mode = True
        
class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
    responses: List["Response"] = Relationship(back_populates="user")
    
class DetailedFlightResponseLink(SQLModel, table=True):
    response_id: Optional[int] = Field(
        default=None, foreign_key="response.id", primary_key=True
    )
    detailedflight_id: Optional[int] = Field(
        default=None, foreign_key="detailedflight.id", primary_key=True
    )
    
class Identification(BaseModel):
    identification: str = Field(default=None, primary_key=False, alias="id")
    callsign: str = Field(default=None, primary_key=False)
    
    class Config:
        orm_mode = True 
        allow_population_by_field_name=True
        
class ResponseBase(SQLModel):
    headquarters: str = Field(default=None, primary_key=False)
    time_created: datetime.datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
    ))   
    class Config:
        orm_mode = True
    
class Response(ResponseBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="responses")

    flights: List["DetailedFlight"] = Relationship(link_model=DetailedFlightResponseLink)
    
    class Config:
        orm_mode = True

class DetailedFlightBase(SQLModel):
    identification: str = Field(default=None, primary_key=False)
    
class DetailedFlight(DetailedFlightBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
    class Config:
        orm_mode = True

class ResponseRead(ResponseBase):
    db_data: List[DetailedFlight]
    
class UserCreate(UserBase):
    pass

class ResponseCreate(ResponseBase):
    pass

class Code(BaseModel):
    iata: str = None
    icao: str = None

    # @validator("iata")
    # def is_valid_icao(cls, icao):
    #     return icao == "valid"

class Airline(BaseModel):
    name: str = None
    short: str = None
    url: str = None
    code: Code = None

class Model(BaseModel):
    code: str = None
    text: str = None

class Aircraft(BaseModel):
    countryId: int = None
    registration: str = None
    hex: str = None
    age: str = None
    msn: str = None
    images: List[str] = None
    model: Model

# Properties to receive via API on creation      
#NOTE: AllFlightRead INHERIT FROM REGULAR NOT SQLMODEL!      
class DetailedFlightCreate(DetailedFlightBase):
    identification: Identification
    aircraft: Aircraft
    # airline: Airline
    
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
# FR models
class Point:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def __str__(self) -> str:
        return '({}, {})'.format(self.lat, self.lon)

class Area:
    def __init__(self, sw: Point, ne: Point):
        self.southwest_lat = sw.lat
        self.southwest_lon = sw.lon
        self.northeast_lat = ne.lat
        self.northeast_lon = ne.lon

    def __str__(self) -> str:
        """Allows to unpack data this way: *area"""
        return '{}, {}, {}, {}'.format(self.southwest_lat, self.southwest_lon,
                                       self.northeast_lat, self.northeast_lon)

    def __iter__(self):
        return (coord for coord in (self.southwest_lat, self.southwest_lon,
                                    self.northeast_lat, self.northeast_lon))