from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator


# Base models
###############################################################################
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

# CREATE/UPDATE models
###############################################################################
class BriefFlightUpdate(BriefFlightBase):
    # datetime: Optional[str]
    pass
class BriefFlightCreate(BriefFlightBase):
    pass

# GET models
###############################################################################
class BriefFlight(BriefFlightBase):
    pass

    class Config:
        orm_mode = True
    


       