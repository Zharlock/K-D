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

# Pydantic Model for Customer
class CustomerCreate(BaseModel):
    id_type: int
    nome: str
    username: str
    email: str
    phone_number: str
    morada: str
    nif: int
    localidade: str
    codigo_postal: str
    created_at: datetime = datetime.now()
    is_pet_owner: bool

class CustomerUpdate(BaseModel):
    id_type: int
    nome: str
    username: str
    email: str
    phone_number: str
    morada: str
    nif: int
    localidade: str
    codigo_postal: str
    created_at: datetime
    is_pet_owner: bool



# Pydantic Model for Response
class CustomerResponse(BaseModel):
    id_customer: int
    id_type: int
    nome: str
    username: str
    email: str
    phone_number: str
    morada: str
    nif: int
    localidade: str
    codigo_postal: str
    created_at: datetime
    is_pet_owner: bool

class ResponseModel(BaseModel):
    status: str
    message: str

# Database Model for Customer
class Customer(Base):
    __tablename__ = "Customer"

    id_customer = Column(Integer, primary_key=True, index=True)
    id_type = Column(Integer, index=True)
    nome = Column(String, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    phone_number = Column(String, index=True)
    morada = Column(String)
    nif = Column(Integer)
    localidade = Column(String)
    codigo_postal = Column(String)
    created_at = Column(DateTime)
    is_pet_owner = Column(Boolean)


# CRUD Operations

def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return {"status": "success", "message": "Customer created successfully"}

def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id_customer == customer_id).first()
    if customer:
        # Convert the datetime field to string before returning the response
        customer_response = CustomerResponse(**customer.__dict__)
        customer_response.created_at = str(customer.created_at)
        return customer_response
    raise HTTPException(status_code=404, detail="Customer not found")

def read_all_customer(db: Session = Depends(get_db)):
    customer = db.query(Customer).filter().all()
    if customer:
        # Convert the datetime field to string before returning the response
        customer_response = CustomerResponse(**customer.__dict__)
        customer_response.created_at = str(customer.created_at)
        return customer_response
    raise HTTPException(status_code=404, detail="Customer not found")

def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db)
):
    db_customer = db.query(Customer).filter(Customer.id_customer == customer_id).first()
    if db_customer:
        # Update the customer fields based on the data provided
        for field, value in customer_update.dict().items():
            setattr(db_customer, field, value)

        db.commit()
        db.refresh(db_customer)
        return {"status": "success", "message": "Customer updated successfully"}
    raise HTTPException(status_code=404, detail="Customer not found")

def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id_customer == customer_id).first()
    if customer:
        db.delete(customer)
        db.commit()
        return {"status": "success", "message": "Customer deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer not found")
