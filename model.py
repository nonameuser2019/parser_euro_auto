from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String, Float


Base = declarative_base()
class EuroAuto(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    article = Column(String)
    brand = Column(String)
    weight = Column(String)
    url = Column(String)

    def __init__(self, name, article, brand, weight, url):
        self.name = name
        self.article = article
        self.brand = brand
        self.weight = weight
        self.url = url

    def __repr__(self):
        return "CData '%s'" % (self.url)


db_engine = create_engine("sqlite:///euroauto.db", echo=True)
Base.metadata.create_all(db_engine)