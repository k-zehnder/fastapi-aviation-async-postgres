import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator

from sqlmodel import create_engine, SQLModel, Session, Field

# Base models
###############################################################################
class SongBase(SQLModel):
    name: str
    artist: str
    
    class Config:
        orm_mode = True
        

class DetailedFlightBase(SQLModel):
    identification: Optional[str]
    
    class Config:
        orm_mode = True
                

# class DetailedFlightBase(SQLModel):
#     identification: Any
#     # status: Dict = None
#     # level: str = None
#     # promote: bool = None
#     # aircraft: Dict = None
#     # airline: Any = None
#     # owner: Any = None
#     # airspace: Any = None
#     # airport: Dict = None
#     # flightHistory: Any = None
#     # ems: Any = None
#     # availability: Any = None
#     # trail: List[Dict] = None
#     # s: Any = None
    
#     class Config:
#         orm_mode = True
        
# GET models
###############################################################################
class Song(SongBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
    class Config:
        orm_mode = True
        

class DetailedFlight(DetailedFlightBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
    class Config:
        orm_mode = True
        

# CREATE/UPDATE models
###############################################################################
class SongCreate(SongBase):
    pass

class SongRead(SongBase):
    pass

class DetailedFlightCreate(DetailedFlightBase):
    # datetime
    pass

class DetailedFlightRead(DetailedFlightBase):
    # datetime
    pass
