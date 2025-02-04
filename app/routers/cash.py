from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/cash/", response_model=schemas.Cash)
def create_cash(cash: schemas.CashCreate, db: Session = Depends(get_db)):
    db_cash = models.Cash(**cash.model_dump())
    db.add(db_cash)
    db.commit()
    db.refresh(db_cash)
    return db_cash

@router.get("/cash/", response_model=List[schemas.Cash])
def read_cash_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cash_entries = db.query(models.Cash).offset(skip).limit(limit).all()
    return cash_entries

@router.get("/cash/{cash_id}", response_model=schemas.Cash)
def read_cash(cash_id: int, db: Session = Depends(get_db)):
    db_cash = db.query(models.Cash).filter(models.Cash.id == cash_id).first()
    if db_cash is None:
        raise HTTPException(status_code=404, detail="Registro de Cash não encontrado")
    return db_cash

@router.put("/cash/{cash_id}", response_model=schemas.Cash)
def update_cash(cash_id: int, cash: schemas.CashCreate, db: Session = Depends(get_db)):
    db_cash = db.query(models.Cash).filter(models.Cash.id == cash_id).first()
    if db_cash is None:
        raise HTTPException(status_code=404, detail="Registro de Cash não encontrado")
    
    for key, value in cash.model_dump().items():
        setattr(db_cash, key, value)
    
    db.commit()
    db.refresh(db_cash)
    return db_cash

@router.delete("/cash/{cash_id}")
def delete_cash(cash_id: int, db: Session = Depends(get_db)):
    db_cash = db.query(models.Cash).filter(models.Cash.id == cash_id).first()
    if db_cash is None:
        raise HTTPException(status_code=404, detail="Registro de Cash não encontrado")
    
    db.delete(db_cash)
    db.commit()
    return {"message": "Registro de Cash deletado com sucesso"}