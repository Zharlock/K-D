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


# Pydantic Model for Checkout
class CheckoutCreate(BaseModel):
    id_checkin: int
    obs: str
    id_pay: int
    id_funcionario: int

class CheckoutUpdate(BaseModel):
    id_checkin: int
    obs: str
    id_pay: int
    id_funcionario: int

# Pydantic Model for Response
class CheckoutResponse(BaseModel):
    id_checkout: int
    id_checkin: int
    date_created: datetime
    obs: str
    id_pay: int
    id_funcionario: int

# Database Model for Checkout
class Checkout(Base):
    __tablename__ = "Checkout"

    id_checkout = Column(Integer, primary_key=True, index=True)
    id_checkin = Column(Integer, index=True)
    date_created = Column(DateTime, default=datetime.now())
    obs = Column(String)
    id_pay = Column(Integer)
    id_funcionario = Column(Integer)

# CRUD Operations for Checkout
@app.post("/checkouts/", response_model=CheckoutResponse)
def create_checkout(checkout: CheckoutCreate, db: Session = Depends(get_db)):
    db_checkout = Checkout(**checkout.dict())
    db.add(db_checkout)
    db.commit()
    db.refresh(db_checkout)
    return {"status": "success", "message": "Checkout created successfully"}

@app.get("/checkouts/{checkout_id}", response_model=CheckoutResponse)
def read_checkout(checkout_id: int, db: Session = Depends(get_db)):
    db_checkout = db.query(Checkout).filter(Checkout.id_checkout == checkout_id).first()
    if db_checkout:
        return db_checkout
    raise HTTPException(status_code=404, detail="Checkout not found")

@app.put("/checkouts/{checkout_id}", response_model=CheckoutResponse)
def update_checkout(
    checkout_id: int,
    checkout_update: CheckoutUpdate,
    db: Session = Depends(get_db)
):
    db_checkout = db.query(Checkout).filter(Checkout.id_checkout == checkout_id).first()
    if db_checkout:
        for field, value in checkout_update.dict().items():
            setattr(db_checkout, field, value)

        db.commit()
        db.refresh(db_checkout)
        return {"status": "success", "message": "Cheackout updated successfully"}
    raise HTTPException(status_code=404, detail="Checkout not found")

@app.delete("/checkouts/{checkout_id}", response_model=ResponseModel)
def delete_checkout(checkout_id: int, db: Session = Depends(get_db)):
    db_checkout = db.query(Checkout).filter(Checkout.id_checkout == checkout_id).first()
    if db_checkout:
        db.delete(db_checkout)
        db.commit()
        return {"status": "success", "message": "Checkout deleted successfully"}
    raise HTTPException(status_code=404, detail="Checkout not found")
