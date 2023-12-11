from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.openapi.models import Response, Info, ExternalDocumentation
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Database Configuration

#DATABASE_URL = "postgresql://postgres:lola9123@localhost/postgres" #Rafael
#DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"  #Bagulho
DATABASE_URL = "postgresql://postgres:1234@localhost/postgres" #Carlos
#DATABASE_URL = "postgresql://postgres:123@localhost/postgres" #Rodrigo

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ResponseModel(BaseModel):
    status: str
    message: str



# Pydantic Model for Pet
class PetCreate(BaseModel):
    nome: str
    animal: str
    race: str
    idade: int
    id_customer: int
    id_enclosure: int

class PetUpdate(BaseModel):
    nome: str
    animal: str
    race: str
    idade: int
    id_customer: int
    id_enclosure: int

# Pydantic Model for Response
class PetResponse(BaseModel):
    id_pet: int
    nome: str
    animal: str
    race: str
    idade: int
    id_customer: int
    id_enclosure: int

# Database Model for Pet
class Pet(Base):
    __tablename__ = "Pet"

    id_pet = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    animal = Column(String)
    race = Column(String)
    idade = Column(Integer)
    id_customer = Column(Integer, index=True)
    id_enclosure = Column(Integer)

# CRUD Operations for Pet

def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    db_pet = Pet(**pet.dict())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return {"status": "success", "message": "Pet created successfully"}


def read_pet(pet_id: int, db: Session = Depends(get_db)):
    db_pet = db.query(Pet).filter(Pet.id_pet == pet_id).first()
    if db_pet:
        return db_pet
    raise HTTPException(status_code=404, detail="Pet not found")


def read_all_pet(db: Session = Depends(get_db)):
    db_pet = db.query(Pet).filter().all()
    if db_pet:
        return db_pet
    raise HTTPException(status_code=404, detail="Pet not found")

def update_pet(
    pet_id: int,
    pet_update: PetUpdate,
    db: Session = Depends(get_db)
):
    db_pet = db.query(Pet).filter(Pet.id_pet == pet_id).first()
    if db_pet:
        for field, value in pet_update.dict().items():
            setattr(db_pet, field, value)

        db.commit()
        db.refresh(db_pet)
        return {"status": "success", "message": "Pet updated successfully"}
    raise HTTPException(status_code=404, detail="Pet not found")


def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    db_pet = db.query(Pet).filter(Pet.id_pet == pet_id).first()
    if db_pet:
        db.delete(db_pet)
        db.commit()
        return {"status": "success", "message": "Pet deleted successfully"}
    raise HTTPException(status_code=404, detail="Pet not found")
