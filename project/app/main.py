import sqlmodel
from sqlmodel import create_engine, SQLModel

from models import *
from db import build_uri
# from . import crud

from dataclass.flightradar.api import API
from dataclass.data_class import Data

if __name__ == "__main__":
    obj = Data()    
    print(obj)
    data = obj.run() # dictionary
    print(type(data))
    # print(data)

    print()
    DATABASE_URL = build_uri()
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    