from typing import List, Optional
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator

from .item import Item

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True