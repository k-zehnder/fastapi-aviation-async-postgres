from typing import List, Optional
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator


class Task(BaseModel):
    time: int
