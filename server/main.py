from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import Base, engine, SessionLocal
from datetime import date
from typing import List


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weight Manager")

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
    return crud.create_person(db, person)


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
# Add a person weight
#----------------------------------------
@app.post("/persons/{person_id}/weights/", response_model=schemas.WeightEntryRead)
def add_weight(person_id: int, weight: schemas.WeightEntryCreate, db: Session = Depends(get_db)):
    entry = crud.add_weight_entry(db, person_id, weight)
    if not entry:
        raise HTTPException(status_code=404, detail="Person not found")
    return entry


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
    weight = db.query(models.WeightEntry).filter(models.WeightEntry.person_id == person_id).order_by(models.WeightEntry.date)
    return weight


#----------------------------------------
# Update a weight
#----------------------------------------
@app.put("/persons/{weight_id}/weight", response_model=schemas.WeightRead)
def update_weight(weight_id: int, weight_data: schemas.WeightUpdate, db: Session = Depends(get_db)):
    weight = crud.update_weight(db, weight_id, weight_data)
    if not weight:
        raise HTTPException(status_code=404, detail="Weight not found")
    return weight


#----------------------------------------
# Delete a weight
#----------------------------------------
@app.delete("/persons/{weight_id}/weights/")
def delete_weight(weight_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_weight(db, weight_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Weight not found")
    return {"message": "Weight deleted"}

