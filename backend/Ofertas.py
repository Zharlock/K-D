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

#****************************************************************************************************

# Pydantic Model for Ofertas
class OfertasCreate(BaseModel):
    tipo: str
    valor_dia: int

class OfertasUpdate(BaseModel):
    tipo: str
    valor_dia: int

# Pydantic Model for Response
class OfertasResponse(BaseModel):
    id_oferta: int
    tipo: str
    valor_dia: int

# Database Model for Ofertas
class Ofertas(Base):
    __tablename__ = "Ofertas"

    id_oferta = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    valor_dia = Column(Integer)

# CRUD Operations for Ofertas

def create_ofertas(ofertas: OfertasCreate, db: Session = Depends(get_db)):
    db_ofertas = Ofertas(**ofertas.dict())
    db.add(db_ofertas)
    db.commit()
    db.refresh(db_ofertas)
    return {"status": "success", "message": "Ofertas created successfully"}


def read_ofertas(ofertas_id: int, db: Session = Depends(get_db)):
    db_ofertas = db.query(Ofertas).filter(Ofertas.id_oferta == ofertas_id).first()
    if db_ofertas:
        return db_ofertas
    raise HTTPException(status_code=404, detail="Ofertas not found")


def read_all_ofertas(db: Session = Depends(get_db)):
    db_ofertas = db.query(Ofertas).filter().all()
    if db_ofertas:
        return db_ofertas
    raise HTTPException(status_code=404, detail="Ofertas not found")


def update_ofertas(
    ofertas_id: int,
    ofertas_update: OfertasUpdate,
    db: Session = Depends(get_db)
):
    db_ofertas = db.query(Ofertas).filter(Ofertas.id_oferta == ofertas_id).first()
    if db_ofertas:
        for field, value in ofertas_update.dict().items():
            setattr(db_ofertas, field, value)

        db.commit()
        db.refresh(db_ofertas)
        return {"status": "success", "message": "Ofetas updated successfully"}
    raise HTTPException(status_code=404, detail="Ofertas not found")


def delete_ofertas(ofertas_id: int, db: Session = Depends(get_db)):
    db_ofertas = db.query(Ofertas).filter(Ofertas.id_oferta == ofertas_id).first()
    if db_ofertas:
        db.delete(db_ofertas)
        db.commit()
        return {"status": "success", "message": "Ofertas deleted successfully"}
    raise HTTPException(status_code=404, detail="Ofertas not found")

#****************************************************************************************************
