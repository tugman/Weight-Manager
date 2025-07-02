from sqlalchemy.orm import Session
import models, schemas
from datetime import date

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_persons(db: Session):
    return db.query(models.Person)

def update_person(db: Session, person_id: int, update_data: schemas.PersonUpdate):
    db_person = get_person(db, person_id)
    if not db_person:
        return None
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(db_person, field, value)
    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int):
    person = get_person(db, person_id)
    if person:
        db.delete(person)
        db.commit()
    return person

def add_weight_entry(db: Session, person_id: int, weight_data: schemas.WeightEntryCreate):
    person = get_person(db, person_id)
    if not person:
        return None
    entry = models.WeightEntry(person_id=person_id, **weight_data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def calculate_bmi(person: models.Person, latest_weight: float) -> float:
    return round(latest_weight / (person.height ** 2), 2)


def get_weight(db: Session, weight_id: int):
    return db.query(models.WeightEntry).filter(models.WeightEntry.id == weight_id).first()


def update_weight(db: Session, weight_id: int, update_data: schemas.WeightUpdate):
    db_wight = get_weight(db, weight_id)
    if not db_wight:
        return None
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(db_wight, field, value)
    db.commit()
    db.refresh(db_wight)
    return db_wight


def delete_weight(db: Session, weight_id: int):
    weight = get_weight(db, weight_id)
    if weight:
        db.delete(weight)
        db.commit()
    return weight
