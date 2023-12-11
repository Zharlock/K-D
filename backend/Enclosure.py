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

#****************************************************************************************************

# Pydantic Model for Enclosure
class EnclosureCreate(BaseModel):
    type: str
    ocupado: bool

class EnclosureUpdate(BaseModel):
    type: str
    ocupado: bool

# Pydantic Model for Response
class EnclosureResponse(BaseModel):
    id_enclosure: int
    type: str
    ocupado: bool

# Database Model for Enclosure
class Enclosure(Base):
    __tablename__ = "Enclosure"

    id_enclosure = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    ocupado = Column(Boolean)

# CRUD Operations for Enclosure

def create_enclosure(enclosure: EnclosureCreate, db: Session = Depends(get_db)):
    db_enclosure = Enclosure(**enclosure.dict())
    db.add(db_enclosure)
    db.commit()
    db.refresh(db_enclosure)
    return {"status": "success", "message": "Enclosure created successfully"}


def read_enclosure(enclosure_id: int, db: Session = Depends(get_db)):
    db_enclosure = db.query(Enclosure).filter(Enclosure.id_enclosure == enclosure_id).first()
    if db_enclosure:
        return db_enclosure
    raise HTTPException(status_code=404, detail="Enclosure not found")

def read_all_enclosure(db: Session = Depends(get_db)):
    db_enclosure = db.query(Enclosure).filter().all()
    if db_enclosure:
        return db_enclosure
    raise HTTPException(status_code=404, detail="Enclosure not found")

def update_enclosure(
    enclosure_id: int,
    enclosure_update: EnclosureUpdate,
    db: Session = Depends(get_db)
):
    db_enclosure = db.query(Enclosure).filter(Enclosure.id_enclosure == enclosure_id).first()
    if db_enclosure:
        for field, value in enclosure_update.dict().items():
            setattr(db_enclosure, field, value)

        db.commit()
        db.refresh(db_enclosure)
        return {"status": "success", "message": "Enclosure updated successfully"}
    raise HTTPException(status_code=404, detail="Enclosure not found")


def delete_enclosure(enclosure_id: int, db: Session = Depends(get_db)):
    db_enclosure = db.query(Enclosure).filter(Enclosure.id_enclosure == enclosure_id).first()
    if db_enclosure:
        db.delete(db_enclosure)
        db.commit()
        return {"status": "success", "message": "Enclosure deleted successfully"}
    raise HTTPException(status_code=404, detail="Enclosure not found")
