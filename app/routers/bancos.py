from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/bancos/", response_model=schemas.Bancos)
def create_banco(banco: schemas.BancosCreate, db: Session = Depends(get_db)):
    db_banco = models.Bancos(**banco.model_dump())
    db.add(db_banco)
    db.commit()
    db.refresh(db_banco)
    return db_banco

@router.get("/bancos/", response_model=List[schemas.Bancos])
def read_bancos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bancos = db.query(models.Bancos).offset(skip).limit(limit).all()
    return bancos

@router.get("/bancos/{banco_id}", response_model=schemas.Bancos)
def read_banco(banco_id: int, db: Session = Depends(get_db)):
    db_banco = db.query(models.Bancos).filter(models.Bancos.id == banco_id).first()
    if db_banco is None:
        raise HTTPException(status_code=404, detail="Banco não encontrado")
    return db_banco

@router.put("/bancos/{banco_id}", response_model=schemas.Bancos)
def update_banco(banco_id: int, banco: schemas.BancosCreate, db: Session = Depends(get_db)):
    db_banco = db.query(models.Bancos).filter(models.Bancos.id == banco_id).first()
    if db_banco is None:
        raise HTTPException(status_code=404, detail="Banco não encontrado")
    
    for key, value in banco.model_dump().items():
        setattr(db_banco, key, value)
    
    db.commit()
    db.refresh(db_banco)
    return db_banco

@router.delete("/bancos/{banco_id}")
def delete_banco(banco_id: int, db: Session = Depends(get_db)):
    db_banco = db.query(models.Bancos).filter(models.Bancos.id == banco_id).first()
    if db_banco is None:
        raise HTTPException(status_code=404, detail="Banco não encontrado")
    
    db.delete(db_banco)
    db.commit()
    return {"message": "Banco deletado com sucesso"}