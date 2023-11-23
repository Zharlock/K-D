from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.openapi.models import Response, Info, ExternalDocumentation
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Database Configuration

DATABASE_URL = "postgresql://postgres:lola9123@localhost/postgres" #Rafael
#DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"  #Bagulho
#DATABASE_URL = "postgresql://postgres:1234@localhost/postgres" #Carlos
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

# Pydantic Model for Funcionario
class FuncionarioCreate(BaseModel):
    nome: str
    cargo: str

class FuncionarioUpdate(BaseModel):
    nome: str
    cargo: str

# Pydantic Model for Response
class FuncionarioResponse(BaseModel):
    id_funcionario: int
    nome: str
    cargo: str

# Database Model for Funcionario
class Funcionario(Base):
    __tablename__ = "Funcionario"

    id_funcionario = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cargo = Column(String)

# CRUD Operations for Funcionario
@app.post("/funcionarios/", response_model=FuncionarioResponse)
def create_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    db_funcionario = Funcionario(**funcionario.dict())
    db.add(db_funcionario)
    db.commit()
    db.refresh(db_funcionario)
    return {"status": "success", "message": "Funcionario created successfully"}

@app.get("/funcionarios/{funcionario_id}", response_model=FuncionarioResponse)
def read_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    db_funcionario = db.query(Funcionario).filter(Funcionario.id_funcionario == funcionario_id).first()
    if db_funcionario:
        return db_funcionario
    raise HTTPException(status_code=404, detail="Funcionario not found")

@app.put("/funcionarios/{funcionario_id}", response_model=FuncionarioResponse)
def update_funcionario(
    funcionario_id: int,
    funcionario_update: FuncionarioUpdate,
    db: Session = Depends(get_db)
):
    db_funcionario = db.query(Funcionario).filter(Funcionario.id_funcionario == funcionario_id).first()
    if db_funcionario:
        for field, value in funcionario_update.dict().items():
            setattr(db_funcionario, field, value)

        db.commit()
        db.refresh(db_funcionario)
        return {"status": "success", "message": "Funcionario updated successfully"}
    raise HTTPException(status_code=404, detail="Funcionario not found")

@app.delete("/funcionarios/{funcionario_id}", response_model=ResponseModel)
def delete_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    db_funcionario = db.query(Funcionario).filter(Funcionario.id_funcionario == funcionario_id).first()
    if db_funcionario:
        db.delete(db_funcionario)
        db.commit()
        return {"status": "success", "message": "Funcionario deleted successfully"}
    raise HTTPException(status_code=404, detail="Funcionario not found")

#****************************************************************************************************