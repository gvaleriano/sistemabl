from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/cambio/", response_model=schemas.Cambio)
def create_cambio(cambio: schemas.CambioCreate, db: Session = Depends(get_db)):
    db_cambio = models.Cambio(**cambio.model_dump())
    db.add(db_cambio)
    db.commit()
    db.refresh(db_cambio)
    return db_cambio

@router.get("/cambio/", response_model=List[schemas.Cambio])
def read_cambios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cambios = db.query(models.Cambio).offset(skip).limit(limit).all()
    return cambios

@router.get("/cambio/{cambio_id}", response_model=schemas.Cambio)
def read_cambio(cambio_id: int, db: Session = Depends(get_db)):
    db_cambio = db.query(models.Cambio).filter(models.Cambio.id == cambio_id).first()
    if db_cambio is None:
        raise HTTPException(status_code=404, detail="Câmbio não encontrado")
    return db_cambio

@router.put("/cambio/{cambio_id}", response_model=schemas.Cambio)
def update_cambio(cambio_id: int, cambio: schemas.CambioCreate, db: Session = Depends(get_db)):
    db_cambio = db.query(models.Cambio).filter(models.Cambio.id == cambio_id).first()
    if db_cambio is None:
        raise HTTPException(status_code=404, detail="Câmbio não encontrado")
    
    for key, value in cambio.model_dump().items():
        setattr(db_cambio, key, value)
    
    db.commit()
    db.refresh(db_cambio)
    return db_cambio

@router.delete("/cambio/{cambio_id}")
def delete_cambio(cambio_id: int, db: Session = Depends(get_db)):
    db_cambio = db.query(models.Cambio).filter(models.Cambio.id == cambio_id).first()
    if db_cambio is None:
        raise HTTPException(status_code=404, detail="Câmbio não encontrado")
    
    db.delete(db_cambio)
    db.commit()
    return {"message": "Câmbio deletado com sucesso"}