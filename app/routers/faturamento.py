from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Faturamento
from app.schemas import Faturamento as FaturamentoSchema, FaturamentoCreate
from app.database import get_db

router = APIRouter()

@router.post("/faturamento/", response_model=FaturamentoSchema)
def create_faturamento(faturamento: FaturamentoCreate, db: Session = Depends(get_db)):
    db_faturamento = Faturamento(**faturamento.dict())
    db.add(db_faturamento)
    db.commit()
    db.refresh(db_faturamento)
    return db_faturamento

@router.get("/faturamento/", response_model=List[FaturamentoSchema])
def read_faturamento(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    faturamentos = db.query(Faturamento).offset(skip).limit(limit).all()
    return faturamentos

@router.get("/faturamento/{faturamento_id}", response_model=FaturamentoSchema)
def read_faturamento(faturamento_id: int, db: Session = Depends(get_db)):
    db_faturamento = db.query(Faturamento).filter(Faturamento.id == faturamento_id).first()
    if db_faturamento is None:
        raise HTTPException(status_code=404, detail="Faturamento não encontrado")
    return db_faturamento

@router.put("/faturamento/{faturamento_id}", response_model=FaturamentoSchema)
def update_faturamento(faturamento_id: int, faturamento: FaturamentoCreate, db: Session = Depends(get_db)):
    db_faturamento = db.query(Faturamento).filter(Faturamento.id == faturamento_id).first()
    if db_faturamento is None:
        raise HTTPException(status_code=404, detail="Faturamento não encontrado")
    
    for key, value in faturamento.dict().items():
        setattr(db_faturamento, key, value)
    
    db.commit()
    db.refresh(db_faturamento)
    return db_faturamento

@router.delete("/faturamento/{faturamento_id}")
def delete_faturamento(faturamento_id: int, db: Session = Depends(get_db)):
    db_faturamento = db.query(Faturamento).filter(Faturamento.id == faturamento_id).first()
    if db_faturamento is None:
        raise HTTPException(status_code=404, detail="Faturamento não encontrado")
    
    db.delete(db_faturamento)
    db.commit()
    return {"message": "Faturamento deletado com sucesso"}