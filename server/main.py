# MIT License

# Copyright (c) 2025 BERNIER Francois

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


#----------------------------------------
# Logs
#----------------------------------------
VERSION = "0.0.1"

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import Base, engine, SessionLocal
from datetime import date
from typing import List
from dotenv import load_dotenv
import os
import logging
from pydantic_collections import BaseCollectionModel


#----------------------------------------
# Logs
#----------------------------------------
load_dotenv()
LOGS_FILE = os.getenv("LOGS_FILE")
match os.getenv("LOGS_LEVEL"):
  case "DEBUG":
    LOGS_LEVEL=logging.DEBUG
  case "INFO":
    LOGS_LEVEL=logging.INFO
  case "WARNING":
    LOGS_LEVEL=logging.WARNING
  case "ERROR":
    LOGS_LEVEL=logging.ERROR
  case "CRITICAL":
    LOGS_LEVEL=logging.ERROR
  case _:
    LOGS_LEVEL=logging.DEBUG
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', filename=LOGS_FILE, encoding='utf-8', level=LOGS_LEVEL)
logger.critical("")
logger.critical("-------------------------------------")
logger.critical("- Starting Weight Manager Front End -")
logger.critical("-------------------------------------")
logger.critical("Weight Manager Front End version: %s", VERSION)
logger.critical('Log file: %s', os.getenv("LOGS_FILE"))
logger.critical('Debug level: %s', os.getenv("LOGS_LEVEL"))


#----------------------------------------
# Apllication
#----------------------------------------
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Weight Manager")


#----------------------------------------
# Database
#----------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#----------------------------------------
# Create a person
#----------------------------------------
@app.post("/persons/", response_model=schemas.PersonRead)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    person = crud.create_person(db, person)
    logger.debug("Person created")
    return person


#----------------------------------------
# List all persons
#----------------------------------------
@app.get("/persons/", response_model=List[schemas.PersonsRead])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = db.query(models.Person).order_by(models.Person.last_name, models.Person.first_name).offset(skip).limit(limit).all()
    return persons


#----------------------------------------
# Show person by Id
#----------------------------------------
@app.get("/persons/{person_id}", response_model=schemas.PersonRead)
def read_person(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


#----------------------------------------
# Update a person
#----------------------------------------
@app.put("/persons/{person_id}", response_model=schemas.PersonRead)
def update_person(person_id: int, person_data: schemas.PersonUpdate, db: Session = Depends(get_db)):
    person = crud.update_person(db, person_id, person_data)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


#----------------------------------------
# Delete a person
#----------------------------------------
@app.delete("/persons/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_person(db, person_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": "Person deleted"}


#----------------------------------------
# Add a person weight record
#----------------------------------------
@app.post("/persons/{person_id}/weights/", response_model=schemas.WeightEntryRead)
def add_weight(person_id: int, weight: schemas.WeightEntryCreate, db: Session = Depends(get_db)):
    entry = crud.add_weight_entry(db, person_id, weight)
    if not entry:
        raise HTTPException(status_code=404, detail="Person not found")
    return entry


#----------------------------------------
# Get a weight record
#----------------------------------------
@app.get("/persons/{weight_id}/weights", response_model=schemas.WeightRead)
def read_weight(weight_id: int, db: Session = Depends(get_db)):
    weight = crud.get_weight(db, weight_id)
    if not weight:
        raise HTTPException(status_code=404, detail="Weight not found")
    return weight


#----------------------------------------
# Update a weight record
#----------------------------------------
@app.put("/persons/{weight_id}/weights", response_model=schemas.WeightRead)
def update_weight(weight_id: int, weight_data: schemas.WeightUpdate, db: Session = Depends(get_db)):
    weight = crud.update_weight(db, weight_id, weight_data)
    if not weight:
        raise HTTPException(status_code=404, detail="Weight not found")
    return weight


#----------------------------------------
# Delete a weight record
#----------------------------------------
@app.delete("/persons/{weight_id}/weights/")
def delete_weight(weight_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_weight(db, weight_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Weight not found")
    return {"message": "Weight deleted"}


#----------------------------------------
# Get a person last BMI Body Mass Index
#----------------------------------------
@app.get("/persons/{person_id}/last_bmi/")
def get_bmi(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person or not person.weights:
        raise HTTPException(status_code=404, detail="Person or weight data not found")
    latest = sorted(person.weights, key=lambda w: w.date)[-1]
    bmi = crud.calculate_bmi(person, latest.weight)
    return {
        "first_name": person.first_name,
        "last_name": person.last_name,
        "height": person.height,
        "date": latest.date,
        "weight": latest.weight,
        "bmi": bmi
    }


#----------------------------------------
# List person all weight
#----------------------------------------
@app.get("/persons/{person_id}/all_weight/", response_model=List[schemas.WeightEntryRead])
def get_weight(person_id: int, db: Session = Depends(get_db)):
    weights = db.query(models.WeightEntry).filter(models.WeightEntry.person_id == person_id).order_by(models.WeightEntry.date)
    return weights


#----------------------------------------
# List person all weight and BMI
#----------------------------------------
class WeightCollection(BaseCollectionModel[schemas.WeightEntryBase]):
    pass

@app.get("/persons/{person_id}/all_weight_bmi/", response_model=List[schemas.WeightEntryRead])
def get_weight(person_id: int, db: Session = Depends(get_db)):



    weights = db.query(models.WeightEntry).filter(models.WeightEntry.person_id == person_id).order_by(models.WeightEntry.date)
    logger.debug("XX: %s", weights.first().weight)
    logger.debug("XX: %s", weights[0].weight)
    logger.debug("XX: %s", weights.count())
    for x in weights:
        logger.debug("YY: %s", x.weight)

    for i in range(0,weights.count()):
        logger.debug("ZZZ: %s %s", i, weights[i].weight)
        

#    weightsCollection = WeightCollection(weights)
#    logger.debug("Weight collection: %s", weightsCollection)




    person = crud.get_person(db, person_id)
    logger.debug("Size: %s", person.height)    



    return weights



logger.critical("Weight Manager Front End ready")
logger.critical("-------------------------------------")
