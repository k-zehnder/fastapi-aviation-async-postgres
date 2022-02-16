import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from flightradar.models import *

from flightradar.data_class import Data


async def async_main(data):
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:password@localhost/foo",
        echo=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        print("NOT REMOVING DB")
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=True, class_=AsyncSession
    )
    async with async_session() as session:
        async with session.begin():
            # print(data["detailed"])
            r1 = Response(
                    name="controller1",
                    time_created=datetime.datetime.now(),
                    flights=[DetailedFlight(identification=flight.identification.identification, airline_name=flight.airline.name, airplane_code=flight.aircraft.model.code) for flight in data["detailed"]],
                    briefs=[BriefFlight(flight_id=flight.flight_id, radar=flight.radar, vertical_speed=flight.vertical_speed, lat=flight.lat, registration=flight.registration, icao=flight.icao, lon=flight.lon, track=flight.track, origin=flight.origin, airline=flight.airline, alt=flight.alt, destination=flight.destination, speed=flight.speed, iata=flight.iata, squawk=flight.squawk) for flight in data["briefs"]]
            )   
            session.add(r1)
        await session.commit()                
    await engine.dispose()
    
async def get_one_response_from_db():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:password@localhost/foo",
        echo=False,
    )

    async_session = sessionmaker(
        engine, expire_on_commit=True, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            statement = select(Response).where(Response.name=="controller1")
            result = await session.execute(statement)
            c1_response = result.scalars().first()
            print(c1_response)
            print(c1_response.time_created)    
    await engine.dispose()

async def get_all_briefs():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:password@localhost/foo",
        echo=False,
    )

    async_session = sessionmaker(
        engine, expire_on_commit=True, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            statement = select(BriefFlight)
            result = await session.execute(statement)
            all_briefs = result.scalars().first()
            print(all_briefs)
    await engine.dispose()
    
async def get_session_async() -> AsyncSession:
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:password@localhost/foo",
        echo=False,
    )
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

    