from pickle import BYTEARRAY8
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.openapi.models import Response, Info, ExternalDocumentation
from pymysql import Binary
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import LargeBinary

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

#****************************************************************************************************

# Pydantic Model for Image
class ImageCreate(BaseModel):
    image: bytes
    image_type: str

class ImageUpdate(BaseModel):
    image: bytes
    image_type: str

# Pydantic Model for Response
class ImageResponse(BaseModel):
    id_image: int
    image_type: str

# Database Model for Image
class Image(Base):
    __tablename__ = "image"

    id_image = Column(Integer, primary_key=True, index=True)
    image = Column(LargeBinary)  # Assuming you store binary data for the image
    image_type = Column(String)

# CRUD Operations for Image
@app.post("/images/", response_model=ImageResponse)
def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    db_image = Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return {"status": "success", "message": "Image created successfully"}

@app.get("/images/{image_id}", response_model=ImageResponse)
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(Image).filter(Image.id_image == image_id).first()
    if db_image:
        return db_image
    raise HTTPException(status_code=404, detail="Image not found")

@app.put("/images/{image_id}", response_model=ImageResponse)
def update_image(
    image_id: int,
    image_update: ImageUpdate,
    db: Session = Depends(get_db)
):
    db_image = db.query(Image).filter(Image.id_image == image_id).first()
    if db_image:
        for field, value in image_update.dict().items():
            setattr(db_image, field, value)

        db.commit()
        db.refresh(db_image)
        return {"status": "success", "message": "Image updated successfully"}
    raise HTTPException(status_code=404, detail="Image not found")

@app.delete("/images/{image_id}", response_model=ResponseModel)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(Image).filter(Image.id_image == image_id).first()
    if db_image:
        db.delete(db_image)
        db.commit()
        return {"status": "success", "message": "Image deleted successfully"}
    raise HTTPException(status_code=404, detail="Image not found")