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


# Pydantic Model for Checkin
class CheckinCreate(BaseModel):
    id_agenda: int
    id_enclosure: int

class CheckinUpdate(BaseModel):
    id_agenda: int
    id_enclosure: int

# Pydantic Model for Response
class CheckinResponse(BaseModel):
    id_checkin: int
    id_agenda: int
    date_created: datetime
    id_enclosure: int

# Database Model for Checkin
class Checkin(Base):
    __tablename__ = "Checkin"

    id_checkin = Column(Integer, primary_key=True, index=True)
    id_agenda = Column(Integer, index=True)
    date_created = Column(DateTime, default=datetime.now())
    id_enclosure = Column(Integer)

# CRUD Operations for Checkin
@app.post("/checkins/", response_model=CheckinResponse)
def create_checkin(checkin: CheckinCreate, db: Session = Depends(get_db)):
    db_checkin = Checkin(**checkin.dict())
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return {"status": "success", "message": "Checkin created successfully"}

@app.get("/checkins/{checkin_id}", response_model=CheckinResponse)
def read_checkin(checkin_id: int, db: Session = Depends(get_db)):
    db_checkin = db.query(Checkin).filter(Checkin.id_checkin == checkin_id).first()
    if db_checkin:
        return db_checkin
    raise HTTPException(status_code=404, detail="Checkin not found")

@app.put("/checkins/{checkin_id}", response_model=CheckinResponse)
def update_checkin(
    checkin_id: int,
    checkin_update: CheckinUpdate,
    db: Session = Depends(get_db)
):
    db_checkin = db.query(Checkin).filter(Checkin.id_checkin == checkin_id).first()
    if db_checkin:
        for field, value in checkin_update.dict().items():
            setattr(db_checkin, field, value)

        db.commit()
        db.refresh(db_checkin)
        return {"status": "success", "message": "Checkin updated successfully"}
    raise HTTPException(status_code=404, detail="Checkin not found")

@app.delete("/checkins/{checkin_id}", response_model=ResponseModel)
def delete_checkin(checkin_id: int, db: Session = Depends(get_db)):
    db_checkin = db.query(Checkin).filter(Checkin.id_checkin == checkin_id).first()
    if db_checkin:
        db.delete(db_checkin)
        db.commit()
        return {"status": "success", "message": "Checkin deleted successfully"}
    raise HTTPException(status_code=404, detail="Checkin not found")