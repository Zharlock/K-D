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

# Pydantic Model for Customer_type
class CustomerTypeCreate(BaseModel):
    type: str

class CustomerTypeResponse(BaseModel):
    id_type: int
    type: str

# Database Model for Customer_type
class CustomerType(Base):
    __tablename__ = "Customer_type"

    id_type = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True, unique=True)

# CRUD Operations for Customer_type

def create_customer_type(customer_type: CustomerTypeCreate, db: Session = Depends(get_db)):
    db_customer_type = CustomerType(**customer_type.dict())
    db.add(db_customer_type)
    db.commit()
    db.refresh(db_customer_type)
    return {"status": "success", "message": "Customer_type created successfully"}


def read_customer_type(customer_type_id: int, db: Session = Depends(get_db)):
    customer_type = db.query(CustomerType).filter(CustomerType.id_type == customer_type_id).first()
    if customer_type:
        return customer_type
    raise HTTPException(status_code=404, detail="Customer type not found")


def read_all_customer_type(db: Session = Depends(get_db)):
    customer_type = db.query(CustomerType).filter().all()
    if customer_type:
        return customer_type
    raise HTTPException(status_code=404, detail="Customer type not found")

# Pydantic Model for Updating Customer_type
class CustomerTypeUpdate(BaseModel):
    type: str

# CRUD Operations for Customer_type

def update_customer_type(
    customer_type_id: int,
    customer_type_update: CustomerTypeUpdate,
    db: Session = Depends(get_db)
):
    db_customer_type = db.query(CustomerType).filter(CustomerType.id_type == customer_type_id).first()
    if db_customer_type:
        db_customer_type.type = customer_type_update.type
        db.commit()
        db.refresh(db_customer_type)
        return {"status": "success", "message": "Customer_type updated successfully"}
    raise HTTPException(status_code=404, detail="Customer type not found")


def delete_customer_type(customer_type_id: int, db: Session = Depends(get_db)):
    customer_type = db.query(CustomerType).filter(CustomerType.id_type == customer_type_id).first()
    if customer_type:
        db.delete(customer_type)
        db.commit()
        return {"status": "success", "message": "Customer type deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer type not found")
