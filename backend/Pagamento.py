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

# Pydantic Model for Pagamento
class PagamentoCreate(BaseModel):
    payment: str

class PagamentoUpdate(BaseModel):
    payment: str

# Pydantic Model for Response
class PagamentoResponse(BaseModel):
    id_pay: int
    payment: str

# Database Model for Pagamento
class Pagamento(Base):
    __tablename__ = "Pagamento"

    id_pay = Column(Integer, primary_key=True, index=True)
    payment = Column(String)

# CRUD Operations for Pagamento

def create_pagamento(pagamento: PagamentoCreate, db: Session = Depends(get_db)):
    db_pagamento = Pagamento(**pagamento.dict())
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return {"status": "success", "message": "Pagamento created successfully"}


def read_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    db_pagamento = db.query(Pagamento).filter(Pagamento.id_pay == pagamento_id).first()
    if db_pagamento:
        return db_pagamento
    raise HTTPException(status_code=404, detail="Pagamento not found")

def read_all_pagamento(db: Session = Depends(get_db)):
    db_pagamento = db.query(Pagamento).filter().all()
    if db_pagamento:
        return db_pagamento
    raise HTTPException(status_code=404, detail="Pagamento not found")

def update_pagamento(
    pagamento_id: int,
    pagamento_update: PagamentoUpdate,
    db: Session = Depends(get_db)
):
    db_pagamento = db.query(Pagamento).filter(Pagamento.id_pay == pagamento_id).first()
    if db_pagamento:
        for field, value in pagamento_update.dict().items():
            setattr(db_pagamento, field, value)

        db.commit()
        db.refresh(db_pagamento)
        return {"status": "success", "message": "Pagamento updated successfully"}
    raise HTTPException(status_code=404, detail="Pagamento not found")


def delete_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    db_pagamento = db.query(Pagamento).filter(Pagamento.id_pay == pagamento_id).first()
    if db_pagamento:
        db.delete(db_pagamento)
        db.commit()
        return {"status": "success", "message": "Pagamento deleted successfully"}
    raise HTTPException(status_code=404, detail="Pagamento not found")

#****************************************************************************************************
