from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/catalogos/", response_model=schemas.Catalogos)
def create_catalogo(catalogo: schemas.CatalogosCreate, db: Session = Depends(get_db)):
    db_catalogo = models.Catalogos(**catalogo.model_dump())
    db.add(db_catalogo)
    db.commit()
    db.refresh(db_catalogo)
    return db_catalogo

@router.get("/catalogos/", response_model=List[schemas.Catalogos])
def read_catalogos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    catalogos = db.query(models.Catalogos).offset(skip).limit(limit).all()
    return catalogos

@router.get("/catalogos/{catalogo_id}", response_model=schemas.Catalogos)
def read_catalogo(catalogo_id: int, db: Session = Depends(get_db)):
    db_catalogo = db.query(models.Catalogos).filter(models.Catalogos.id == catalogo_id).first()
    if db_catalogo is None:
        raise HTTPException(status_code=404, detail="Catálogo não encontrado")
    return db_catalogo

@router.put("/catalogos/{catalogo_id}", response_model=schemas.Catalogos)
def update_catalogo(catalogo_id: int, catalogo: schemas.CatalogosCreate, db: Session = Depends(get_db)):
    db_catalogo = db.query(models.Catalogos).filter(models.Catalogos.id == catalogo_id).first()
    if db_catalogo is None:
        raise HTTPException(status_code=404, detail="Catálogo não encontrado")
    
    for key, value in catalogo.model_dump().items():
        setattr(db_catalogo, key, value)
    
    db.commit()
    db.refresh(db_catalogo)
    return db_catalogo

@router.delete("/catalogos/{catalogo_id}")
def delete_catalogo(catalogo_id: int, db: Session = Depends(get_db)):
    db_catalogo = db.query(models.Catalogos).filter(models.Catalogos.id == catalogo_id).first()
    if db_catalogo is None:
        raise HTTPException(status_code=404, detail="Catálogo não encontrado")
    
    db.delete(db_catalogo)
    db.commit()
    return {"message": "Catálogo deletado com sucesso"}