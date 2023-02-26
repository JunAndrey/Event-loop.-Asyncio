from sqlalchemy import Column, JSON, Integer, String, Text, VARCHAR, tuple_
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PG_DSN = 'postgresql+asyncpg://andrey:990414@127.0.0.1:5431/mybase'
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class SwapiPeople(Base):
    __tablename__ = 'swapi_people'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    height = Column(Text)
    mass = Column(Text)
    hair_color = Column(Text)
    skin_color = Column(Text)
    eye_color = Column(Text)
    birth_year = Column(Text)
    gender = Column(Text)
    homeworld = Column(Text)
    vehicles = Column(Text)
    species = Column(Text)
    starships = Column(Text)
    films = Column(Text)





