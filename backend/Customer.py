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

# CRUD Operations
@app.post("/customers/", response_model=ResponseModel)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return {"status": "success", "message": "Customer created successfully"}

 
@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id_customer == customer_id).first()
    if customer:
        # Convert the datetime field to string before returning the response
        customer_response = CustomerResponse(**customer.__dict__)
        customer_response.created_at = str(customer.created_at)
        return customer_response
    raise HTTPException(status_code=404, detail="Customer not found")

@app.put("/customers/{customer_id}", response_model=ResponseModel)
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



@app.delete("/customers/{customer_id}", response_model=ResponseModel)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id_customer == customer_id).first()
    if customer:
        db.delete(customer)
        db.commit()
        return {"status": "success", "message": "Customer deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer not found")

#****************************************************************************************************

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
@app.post("/customer-types/", response_model=CustomerTypeResponse)
def create_customer_type(customer_type: CustomerTypeCreate, db: Session = Depends(get_db)):
    db_customer_type = CustomerType(**customer_type.dict())
    db.add(db_customer_type)
    db.commit()
    db.refresh(db_customer_type)
    return db_customer_type

@app.get("/customer-types/{customer_type_id}", response_model=CustomerTypeResponse)
def read_customer_type(customer_type_id: int, db: Session = Depends(get_db)):
    customer_type = db.query(CustomerType).filter(CustomerType.id_type == customer_type_id).first()
    if customer_type:
        return customer_type
    raise HTTPException(status_code=404, detail="Customer type not found")
# Pydantic Model for Updating Customer_type
class CustomerTypeUpdate(BaseModel):
    type: str

# CRUD Operations for Customer_type
@app.put("/customer-types/{customer_type_id}", response_model=CustomerTypeResponse)
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
        return db_customer_type
    raise HTTPException(status_code=404, detail="Customer type not found")

@app.delete("/customer-types/{customer_type_id}", response_model=ResponseModel)
def delete_customer_type(customer_type_id: int, db: Session = Depends(get_db)):
    customer_type = db.query(CustomerType).filter(CustomerType.id_type == customer_type_id).first()
    if customer_type:
        db.delete(customer_type)
        db.commit()
        return {"status": "success", "message": "Customer type deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer type not found")

#****************************************************************************************************

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
    return db_agenda

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
        return db_agenda
    raise HTTPException(status_code=404, detail="Agenda not found")

@app.delete("/agendas/{agenda_id}", response_model=ResponseModel)
def delete_agenda(agenda_id: int, db: Session = Depends(get_db)):
    db_agenda = db.query(Agenda).filter(Agenda.id_agenda == agenda_id).first()
    if db_agenda:
        db.delete(db_agenda)
        db.commit()
        return {"status": "success", "message": "Agenda deleted successfully"}
    raise HTTPException(status_code=404, detail="Agenda not found")

#****************************************************************************************************

# Pydantic Model for Pet
class PetCreate(BaseModel):
    nome: str
    animal: str
    race: str
    idade: int
    id_customer: int
    id_enclosure: int

class PetUpdate(BaseModel):
    nome: str
    animal: str
    race: str
    idade: int
    id_customer: int
    id_enclosure: int

# Pydantic Model for Response
class PetResponse(BaseModel):
    id_pet: int
    nome: str
    animal: str
    race: str
    idade: int
    id_customer: int
    id_enclosure: int

# Database Model for Pet
class Pet(Base):
    __tablename__ = "Pet"

    id_pet = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    animal = Column(String)
    race = Column(String)
    idade = Column(Integer)
    id_customer = Column(Integer, index=True)
    id_enclosure = Column(Integer)

# CRUD Operations for Pet
@app.post("/pets/", response_model=PetResponse)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    db_pet = Pet(**pet.dict())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

@app.get("/pets/{pet_id}", response_model=PetResponse)
def read_pet(pet_id: int, db: Session = Depends(get_db)):
    db_pet = db.query(Pet).filter(Pet.id_pet == pet_id).first()
    if db_pet:
        return db_pet
    raise HTTPException(status_code=404, detail="Pet not found")

@app.put("/pets/{pet_id}", response_model=PetResponse)
def update_pet(
    pet_id: int,
    pet_update: PetUpdate,
    db: Session = Depends(get_db)
):
    db_pet = db.query(Pet).filter(Pet.id_pet == pet_id).first()
    if db_pet:
        for field, value in pet_update.dict().items():
            setattr(db_pet, field, value)

        db.commit()
        db.refresh(db_pet)
        return db_pet
    raise HTTPException(status_code=404, detail="Pet not found")

@app.delete("/pets/{pet_id}", response_model=ResponseModel)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    db_pet = db.query(Pet).filter(Pet.id_pet == pet_id).first()
    if db_pet:
        db.delete(db_pet)
        db.commit()
        return {"status": "success", "message": "Pet deleted successfully"}
    raise HTTPException(status_code=404, detail="Pet not found")

#****************************************************************************************************

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
    return db_checkout

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
        return db_checkout
    raise HTTPException(status_code=404, detail="Checkout not found")

@app.delete("/checkouts/{checkout_id}", response_model=ResponseModel)
def delete_checkout(checkout_id: int, db: Session = Depends(get_db)):
    db_checkout = db.query(Checkout).filter(Checkout.id_checkout == checkout_id).first()
    if db_checkout:
        db.delete(db_checkout)
        db.commit()
        return {"status": "success", "message": "Checkout deleted successfully"}
    raise HTTPException(status_code=404, detail="Checkout not found")

#****************************************************************************************************

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
    return db_checkin

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
        return db_checkin
    raise HTTPException(status_code=404, detail="Checkin not found")

@app.delete("/checkins/{checkin_id}", response_model=ResponseModel)
def delete_checkin(checkin_id: int, db: Session = Depends(get_db)):
    db_checkin = db.query(Checkin).filter(Checkin.id_checkin == checkin_id).first()
    if db_checkin:
        db.delete(db_checkin)
        db.commit()
        return {"status": "success", "message": "Checkin deleted successfully"}
    raise HTTPException(status_code=404, detail="Checkin not found")

#****************************************************************************************************

# Pydantic Model for Enclosure
class EnclosureCreate(BaseModel):
    type: str
    ocupado: bool

class EnclosureUpdate(BaseModel):
    type: str
    ocupado: bool

# Pydantic Model for Response
class EnclosureResponse(BaseModel):
    id_enclosure: int
    type: str
    ocupado: bool

# Database Model for Enclosure
class Enclosure(Base):
    __tablename__ = "Enclosure"

    id_enclosure = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    ocupado = Column(Boolean)

# CRUD Operations for Enclosure
@app.post("/enclosures/", response_model=EnclosureResponse)
def create_enclosure(enclosure: EnclosureCreate, db: Session = Depends(get_db)):
    db_enclosure = Enclosure(**enclosure.dict())
    db.add(db_enclosure)
    db.commit()
    db.refresh(db_enclosure)
    return db_enclosure

@app.get("/enclosures/{enclosure_id}", response_model=EnclosureResponse)
def read_enclosure(enclosure_id: int, db: Session = Depends(get_db)):
    db_enclosure = db.query(Enclosure).filter(Enclosure.id_enclosure == enclosure_id).first()
    if db_enclosure:
        return db_enclosure
    raise HTTPException(status_code=404, detail="Enclosure not found")

@app.put("/enclosures/{enclosure_id}", response_model=EnclosureResponse)
def update_enclosure(
    enclosure_id: int,
    enclosure_update: EnclosureUpdate,
    db: Session = Depends(get_db)
):
    db_enclosure = db.query(Enclosure).filter(Enclosure.id_enclosure == enclosure_id).first()
    if db_enclosure:
        for field, value in enclosure_update.dict().items():
            setattr(db_enclosure, field, value)

        db.commit()
        db.refresh(db_enclosure)
        return db_enclosure
    raise HTTPException(status_code=404, detail="Enclosure not found")

@app.delete("/enclosures/{enclosure_id}", response_model=ResponseModel)
def delete_enclosure(enclosure_id: int, db: Session = Depends(get_db)):
    db_enclosure = db.query(Enclosure).filter(Enclosure.id_enclosure == enclosure_id).first()
    if db_enclosure:
        db.delete(db_enclosure)
        db.commit()
        return {"status": "success", "message": "Enclosure deleted successfully"}
    raise HTTPException(status_code=404, detail="Enclosure not found")

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
    return db_funcionario

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
        return db_funcionario
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
@app.post("/ofertas/", response_model=OfertasResponse)
def create_ofertas(ofertas: OfertasCreate, db: Session = Depends(get_db)):
    db_ofertas = Ofertas(**ofertas.dict())
    db.add(db_ofertas)
    db.commit()
    db.refresh(db_ofertas)
    return db_ofertas

@app.get("/ofertas/{ofertas_id}", response_model=OfertasResponse)
def read_ofertas(ofertas_id: int, db: Session = Depends(get_db)):
    db_ofertas = db.query(Ofertas).filter(Ofertas.id_oferta == ofertas_id).first()
    if db_ofertas:
        return db_ofertas
    raise HTTPException(status_code=404, detail="Ofertas not found")

@app.put("/ofertas/{ofertas_id}", response_model=OfertasResponse)
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
        return db_ofertas
    raise HTTPException(status_code=404, detail="Ofertas not found")

@app.delete("/ofertas/{ofertas_id}", response_model=ResponseModel)
def delete_ofertas(ofertas_id: int, db: Session = Depends(get_db)):
    db_ofertas = db.query(Ofertas).filter(Ofertas.id_oferta == ofertas_id).first()
    if db_ofertas:
        db.delete(db_ofertas)
        db.commit()
        return {"status": "success", "message": "Ofertas deleted successfully"}
    raise HTTPException(status_code=404, detail="Ofertas not found")

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
@app.post("/pagamentos/", response_model=PagamentoResponse)
def create_pagamento(pagamento: PagamentoCreate, db: Session = Depends(get_db)):
    db_pagamento = Pagamento(**pagamento.dict())
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento

@app.get("/pagamentos/{pagamento_id}", response_model=PagamentoResponse)
def read_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    db_pagamento = db.query(Pagamento).filter(Pagamento.id_pay == pagamento_id).first()
    if db_pagamento:
        return db_pagamento
    raise HTTPException(status_code=404, detail="Pagamento not found")

@app.put("/pagamentos/{pagamento_id}", response_model=PagamentoResponse)
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
        return db_pagamento
    raise HTTPException(status_code=404, detail="Pagamento not found")

@app.delete("/pagamentos/{pagamento_id}", response_model=ResponseModel)
def delete_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    db_pagamento = db.query(Pagamento).filter(Pagamento.id_pay == pagamento_id).first()
    if db_pagamento:
        db.delete(db_pagamento)
        db.commit()
        return {"status": "success", "message": "Pagamento deleted successfully"}
    raise HTTPException(status_code=404, detail="Pagamento not found")

#****************************************************************************************************