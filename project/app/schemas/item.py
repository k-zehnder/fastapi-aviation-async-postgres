from typing import List, Optional
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True