from typing import Text

from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine("postgresql://postgres:1@localhost:5432/bot")
Session = sessionmaker(bind=engine)
session = Session()


class Reklama_image(Base):
    __tablename__ = 'reklama_image'

    id = Column(Integer, primary_key=True)
    photo = Column(String(300))
    text = Column(Text)




Base.metadata.create_all(engine)
