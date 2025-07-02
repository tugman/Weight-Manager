from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class WeightEntryBase(BaseModel):
    date: date
    weight: float

class WeightEntryCreate(WeightEntryBase):
    pass

class WeightEntryRead(WeightEntryBase):
    id: int
    class Config:
        orm_mode = True

class PersonBase(BaseModel):
    first_name: str
    last_name: str
    birth_day: date
    height: float = Field(..., gt=0)  # in meters

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_day: Optional[date] = None
    height: Optional[float] = Field(None, gt=0)

class PersonRead(PersonBase):
    id: int
    weights: List[WeightEntryRead] = []

    class Config:
        orm_mode = True

class PersonsRead(PersonBase):
    pass


class WeightRead(WeightEntryBase):
    id: int
    
    class Config:
        orm_mode = True

class WeightUpdate(BaseModel):
    date: Optional[date]
    weight: Optional[float] = None
 
 
