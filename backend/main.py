
from Customer import * #(create_customer, read_customer, update_customer, delete_customer, CustomerResponse, CustomerCreate, CustomerUpdate, ResponseModel,get_db)
from Customer import CustomerResponse 
from Image import *
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

app = FastAPI()

# CRUD Operations for Customer
@app.post("/customers/", response_model=ResponseModel)
def create_customer_route(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(customer, db)

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def read_customer_route(customer_id: int, db: Session = Depends(get_db)):
    return read_customer(customer_id, db)

@app.put("/customers/{customer_id}", response_model=ResponseModel)
def update_customer_route(
    customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    return update_customer(customer_id, customer_update, db)

@app.delete("/customers/{customer_id}", response_model=ResponseModel)
def delete_customer_route(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(customer_id, db)

#********************************************************************************************

# CRUD Operations for Agenda
@app.post("/agendas/", response_model=ResponseModel)
def create_agenda_route(agenda: AgendaCreate, db: Session = Depends(get_db)):
    return create_agenda(agenda, db)

@app.get("/agendas/{agenda_id}", response_model=AgendaResponse)
def read_agenda_route(agenda_id: int, db: Session = Depends(get_db)):
    return read_agenda(agenda_id, db)

@app.put("/agendas/{agenda_id}", response_model=ResponseModel)
def update_agenda_route(
    agenda_id: int, agenda_update: AgendaUpdate, db: Session = Depends(get_db)):
    return update_agenda(agenda_id, agenda_update, db)

@app.delete("/agendas/{agenda_id}", response_model=ResponseModel)
def delete_agenda_route(agenda_id: int, db: Session = Depends(get_db)):
    return delete_agenda(agenda_id, db)

#********************************************************************************************

# CRUD Operations for Checkin
@app.post("/checkins/", response_model=ResponseModel)
def create_checkin_route(checkin: CheckinCreate, db: Session = Depends(get_db)):
    return create_checkin(checkin, db)

@app.get("/checkins/{checkin_id}", response_model=CheckinResponse)
def read_checkin_route(checkin_id: int, db: Session = Depends(get_db)):
    return read_checkin(checkin_id, db)

@app.put("/checkins/{checkin_id}", response_model=ResponseModel)
def update_checkin_route(
    checkin_id: int, checkin_update: CheckinUpdate, db: Session = Depends(get_db)):
    return update_checkin(checkin_id, checkin_update, db)

@app.delete("/checkins/{checkin_id}", response_model=ResponseModel)
def delete_checkin_route(checkin_id: int, db: Session = Depends(get_db)):
    return delete_checkin(checkin_id, db)

#********************************************************************************************

# CRUD Operations for Checkout
@app.post("/checkouts/", response_model=ResponseModel)
def create_checkout_route(checkout: CheckoutCreate, db: Session = Depends(get_db)):
    return create_checkout(checkout, db)

@app.get("/checkouts/{checkout_id}", response_model=CheckoutResponse)
def read_checkout_route(checkout_id: int, db: Session = Depends(get_db)):
    return read_checkout(checkout_id, db)

@app.put("/checkouts/{checkout_id}", response_model=ResponseModel)
def update_checkout_route(
    checkout_id: int, checkout_update: CheckoutUpdate, db: Session = Depends(get_db)):
    return update_checkout(checkout_id, checkout_update, db)

@app.delete("/checkouts/{checkout_id}", response_model=ResponseModel)
def delete_checkout_route(checkout_id: int, db: Session = Depends(get_db)):
    return delete_checkout(checkout_id, db)


#********************************************************************************************


# CRUD Operations for Customer_type
@app.post("/customer_types/", response_model=ResponseModel)
def create_customer_type_route(
    customer_type: CustomerTypeCreate, db: Session = Depends(get_db)
):
    return create_customer_type(customer_type, db)

@app.get("/customer_types/{customer_type_id}", response_model=CustomerTypeResponse)
def read_customer_type_route(customer_type_id: int, db: Session = Depends(get_db)):
    return read_customer_type(customer_type_id, db)

@app.put("/customer_types/{customer_type_id}", response_model=ResponseModel)
def update_customer_type_route(
    customer_type_id: int,
    customer_type_update: CustomerTypeUpdate,
    db: Session = Depends(get_db),
):
    return update_customer_type(customer_type_id, customer_type_update, db)

@app.delete("/customer_types/{customer_type_id}", response_model=ResponseModel)
def delete_customer_type_route(customer_type_id: int, db: Session = Depends(get_db)):
    return delete_customer_type(customer_type_id, db)

#********************************************************************************************

# CRUD Operations for Enclosure
@app.post("/enclosures/", response_model=ResponseModel)
def create_enclosure_route(enclosure: EnclosureCreate, db: Session = Depends(get_db)):
    return create_enclosure(enclosure, db)

@app.get("/enclosures/{enclosure_id}", response_model=EnclosureResponse)
def read_enclosure_route(enclosure_id: int, db: Session = Depends(get_db)):
    return read_enclosure(enclosure_id, db)

@app.put("/enclosures/{enclosure_id}", response_model=ResponseModel)
def update_enclosure_route(
    enclosure_id: int, enclosure_update: EnclosureUpdate, db: Session = Depends(get_db)
):
    return update_enclosure(enclosure_id, enclosure_update, db)

@app.delete("/enclosures/{enclosure_id}", response_model=ResponseModel)
def delete_enclosure_route(enclosure_id: int, db: Session = Depends(get_db)):
    return delete_enclosure(enclosure_id, db)

#********************************************************************************************

# CRUD Operations for Funcionario
@app.post("/funcionarios/", response_model=ResponseModel)
def create_funcionario_route(
    funcionario: FuncionarioCreate, db: Session = Depends(get_db)
):
    return create_funcionario(funcionario, db)

@app.get("/funcionarios/{funcionario_id}", response_model=FuncionarioResponse)
def read_funcionario_route(funcionario_id: int, db: Session = Depends(get_db)):
    return read_funcionario(funcionario_id, db)

@app.put("/funcionarios/{funcionario_id}", response_model=ResponseModel)
def update_funcionario_route(
    funcionario_id: int, funcionario_update: FuncionarioUpdate, db: Session = Depends(get_db)
):
    return update_funcionario(funcionario_id, funcionario_update, db)

@app.delete("/funcionarios/{funcionario_id}", response_model=ResponseModel)
def delete_funcionario_route(funcionario_id: int, db: Session = Depends(get_db)):
    return delete_funcionario(funcionario_id, db)

#********************************************************************************************

# CRUD Operations for Ofertas
@app.post("/ofertas/", response_model=ResponseModel)
def create_ofertas_route(ofertas: OfertasCreate, db: Session = Depends(get_db)):
    return create_ofertas(ofertas, db)

@app.get("/ofertas/{ofertas_id}", response_model=OfertasResponse)
def read_ofertas_route(ofertas_id: int, db: Session = Depends(get_db)):
    return read_ofertas(ofertas_id, db)

@app.put("/ofertas/{ofertas_id}", response_model=ResponseModel)
def update_ofertas_route(
    ofertas_id: int, ofertas_update: OfertasUpdate, db: Session = Depends(get_db)
):
    return update_ofertas(ofertas_id, ofertas_update, db)

@app.delete("/ofertas/{ofertas_id}", response_model=ResponseModel)
def delete_ofertas_route(ofertas_id: int, db: Session = Depends(get_db)):
    return delete_ofertas(ofertas_id, db)

#********************************************************************************************

# CRUD Operations for Pagamento
@app.post("/pagamentos/", response_model=ResponseModel)
def create_pagamento_route(pagamento: PagamentoCreate, db: Session = Depends(get_db)):
    return create_pagamento(pagamento, db)

@app.get("/pagamentos/{pagamento_id}", response_model=PagamentoResponse)
def read_pagamento_route(pagamento_id: int, db: Session = Depends(get_db)):
    return read_pagamento(pagamento_id, db)

@app.put("/pagamentos/{pagamento_id}", response_model=ResponseModel)
def update_pagamento_route(
    pagamento_id: int, pagamento_update: PagamentoUpdate, db: Session = Depends(get_db)
):
    return update_pagamento(pagamento_id, pagamento_update, db)

@app.delete("/pagamentos/{pagamento_id}", response_model=ResponseModel)
def delete_pagamento_route(pagamento_id: int, db: Session = Depends(get_db)):
    return delete_pagamento(pagamento_id, db)

#********************************************************************************************

# CRUD Operations for Pet
@app.post("/pets/", response_model=ResponseModel)
def create_pet_route(pet: PetCreate, db: Session = Depends(get_db)):
    return create_pet(pet, db)

@app.get("/pets/{pet_id}", response_model=PetResponse)
def read_pet_route(pet_id: int, db: Session = Depends(get_db)):
    return read_pet(pet_id, db)

@app.put("/pets/{pet_id}", response_model=ResponseModel)
def update_pet_route(
    pet_id: int, pet_update: PetUpdate, db: Session = Depends(get_db)
):
    return update_pet(pet_id, pet_update, db)

@app.delete("/pets/{pet_id}", response_model=ResponseModel)
def delete_pet_route(pet_id: int, db: Session = Depends(get_db)):
    return delete_pet(pet_id, db)

#********************************************************************************************

# CRUD Operations for Image
@app.post("/images/", response_model=ImageResponse)
def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    return create_image(image, db)

@app.get("/images/{image_id}", response_model=ImageResponse)
def read_image(image_id: int, db: Session = Depends(get_db)):
    return read_image(image_id, db)

@app.put("/images/{image_id}", response_model=ImageResponse)
def update_image(image_id: int,image_update: ImageUpdate,db: Session = Depends(get_db)):
    return update_image(image_id, image_update, db)

@app.delete("/images/{image_id}", response_model=ResponseModel)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    return delete_image(image_id, db)