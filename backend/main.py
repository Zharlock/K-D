
from Customer import * #(create_customer, read_customer, update_customer, delete_customer, CustomerResponse, CustomerCreate, CustomerUpdate, ResponseModel,get_db)
from Customer import CustomerResponse 
from Customer_type import *
from Pet import *
from Pagamento import *
from Agenda import *
from Ofertas import *
from Funcionario import *
from Enclosure import *
from Checkin import *
from Checkout import *
from typing import Union
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.openapi.models import Response, Info, ExternalDocumentation
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

#****************************************************************************************************
#C:\Users\torad\Documents\python311\python.exe -m uvicorn main:app --reload    computador Rafael
#C:\Users\torad\Documents\python311\python.exe -m uvicorn Customer:app --reload    computador Rafael
#E:\Programming\Python\Python312\python.exe -m uvicorn main:app --reload    computador Carlos
#E:\Programming\Python\Python312\python.exe -m uvicorn Customer:app --reload    computador Carlos
#C:\Python\python311\python.exe -m uvicorn main:app --reload    computador Rodrigo
#C:\Python\python311\Python312\python.exe -m uvicorn Customer:app --reload    computador Rodrigo
#****************************************************************************************************
'''
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/exemplo")
def exemplo()-> str:
    return "Hello World"

#if __name__ == "__name__":
 #   uvicorn.run(app, port=8000)
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def re_customer(customer_id: int, db: Session = Depends(get_db)):
    read_customer(customer_id , db )
    return HTTPException(status_code=404, detail="Customer not found")
'''
#*******************************************************


app = FastAPI()

@app.get("/exemplo")
def exemplo() -> str:
    return "Hello World"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# CRUD Operations for Customer
@app.post("/customers/", response_model=ResponseModel)
def create_customer_route(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(customer, db)

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def read_customer_route(customer_id: int, db: Session = Depends(get_db)):
    return read_customer(customer_id, db)

@app.put("/customers/{customer_id}", response_model=ResponseModel)
def update_customer_route(
    customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db)
):
    return update_customer(customer_id, customer_update, db)

@app.delete("/customers/{customer_id}", response_model=ResponseModel)
def delete_customer_route(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(customer_id, db)
