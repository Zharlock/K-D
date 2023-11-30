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

#ATÉ AQUI É GERAL    

# Pydantic Model for Agenda
class AgendaCreate(BaseModel):
    id_pet: int
    id_customer: int
    data_begin: datetime = datetime.now()
    date_end: Optional[datetime]
    id_oferta: Optional[int]
    date_mark: Optional[datetime]

class AgendaUpdate(BaseModel):
    id_pet: int
    id_customer: int
    data_begin: datetime
    date_end: Optional[datetime]
    id_oferta: Optional[int]
    date_mark: Optional[datetime]

# Pydantic Model for Response
class AgendaResponse(BaseModel):
    id_agenda: int
    id_pet: int
    id_customer: int
    data_begin: datetime
    date_end: Optional[datetime]
    id_oferta: Optional[int]
    date_mark: Optional[datetime]

# Database Model for Agenda
class Agenda(Base):
    __tablename__ = "Agenda"

    id_agenda = Column(Integer, primary_key=True, index=True)
    id_pet = Column(Integer)
    id_customer = Column(Integer, index=True)
    data_begin = Column(DateTime, default=datetime.now())
    date_end = Column(DateTime)
    id_oferta = Column(Integer)
    date_mark = Column(DateTime)

# CRUD Operations for Agenda
@app.post("/agendas/", response_model=AgendaResponse)
def create_agenda(agenda: AgendaCreate, db: Session = Depends(get_db)):
    db_agenda = Agenda(**agenda.dict())
    db.add(db_agenda)
    db.commit()
    db.refresh(db_agenda)
    return {"status": "success", "message": "Agenda created successfully"}

@app.get("/agendas/{agenda_id}", response_model=AgendaResponse)
def read_agenda(agenda_id: int, db: Session = Depends(get_db)):
    db_agenda = db.query(Agenda).filter(Agenda.id_agenda == agenda_id).first()
    if db_agenda:
        return db_agenda
    raise HTTPException(status_code=404, detail="Agenda not found")

@app.put("/agendas/{agenda_id}", response_model=AgendaResponse)
def update_agenda(
    agenda_id: int,
    agenda_update: AgendaUpdate,
    db: Session = Depends(get_db)
):
    db_agenda = db.query(Agenda).filter(Agenda.id_agenda == agenda_id).first()
    if db_agenda:
        for field, value in agenda_update.dict().items():
            setattr(db_agenda, field, value)

        db.commit()
        db.refresh(db_agenda)
        return {"status": "success", "message": "Agenda updated successfully"}
    raise HTTPException(status_code=404, detail="Agenda not found")

@app.delete("/agendas/{agenda_id}", response_model=ResponseModel)
def delete_agenda(agenda_id: int, db: Session = Depends(get_db)):
    db_agenda = db.query(Agenda).filter(Agenda.id_agenda == agenda_id).first()
    if db_agenda:
        db.delete(db_agenda)
        db.commit()
        return {"status": "success", "message": "Agenda deleted successfully"}
    raise HTTPException(status_code=404, detail="Agenda not found")