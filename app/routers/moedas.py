from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/moedas/", response_model=schemas.Moedas)
def create_moeda(moedas: schemas.MoedasCreate, db: Session = Depends(get_db)):
    db_moedas = models.Moedas(**moedas.model_dump())
    db.add(db_moedas)
    db.commit()
    db.refresh(db_moedas)
    return db_moedas

@router.get("/moedas/", response_model=List[schemas.Moedas])
def read_moedas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    moedas = db.query(models.Moedas).offset(skip).limit(limit).all()
    return moedas

@router.get("/moedas/{mo_cod}", response_model=schemas.Moedas)
def read_moeda(mo_cod: int, db: Session = Depends(get_db)):
    db_moedas = db.query(models.Moedas).filter(models.Moedas.mo_cod == mo_cod).first()
    if db_moedas is None:
        raise HTTPException(status_code=404, detail="Moeda não encontrado")
    return db_moedas

@router.put("/moedas/{mo_cod}", response_model=schemas.Moedas)
def update_moeda(mo_cod: int, moedas: schemas.MoedasCreate, db: Session = Depends(get_db)):
    db_moedas = db.query(models.Moedas).filter(models.Moedas.mo_cod == mo_cod).first()
    if db_moedas is None:
        raise HTTPException(status_code=404, detail="Moeda não encontrado")
    
    for key, value in moedas.model_dump().items():
        setattr(db_moedas, key, value)
    
    db.commit()
    db.refresh(db_moedas)
    return db_moedas

@router.delete("/moedas/{mo_cod}")
def delete_moeda(mo_cod: int, db: Session = Depends(get_db)):
    db_moedas = db.query(models.Moedas).filter(models.Moedas.mo_cod == mo_cod).first()
    if db_moedas is None:
        raise HTTPException(status_code=404, detail="Moeda não encontrado")
    
    db.delete(db_moedas)
    db.commit()
    return {"message": "Moeda deletado com sucesso"}