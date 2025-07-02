from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    birth_day = Column(Date)
    height = Column(Float, nullable=False)  # in meters

    weights = relationship("WeightEntry", back_populates="person", cascade="all, delete")

class WeightEntry(Base):
    __tablename__ = "weights"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    weight = Column(Float, nullable=False)  # in kg

    person_id = Column(Integer, ForeignKey("persons.id"))
    person = relationship("Person", back_populates="weights")
