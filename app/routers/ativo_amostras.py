from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/ativo-amostras/", response_model=schemas.AtivoEAmostras)
def create_ativo_amostra(ativo: schemas.AtivoEAmostrasCreate, db: Session = Depends(get_db)):
    db_ativo = models.AtivoEAmostras(**ativo.model_dump())
    db.add(db_ativo)
    db.commit()
    db.refresh(db_ativo)
    return db_ativo

@router.get("/ativo-amostras/", response_model=List[schemas.AtivoEAmostras])
def read_ativo_amostras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ativos = db.query(models.AtivoEAmostras).offset(skip).limit(limit).all()
    return ativos

@router.get("/ativo-amostras/{ativo_id}", response_model=schemas.AtivoEAmostras)
def read_ativo_amostra(ativo_id: int, db: Session = Depends(get_db)):
    db_ativo = db.query(models.AtivoEAmostras).filter(models.AtivoEAmostras.id == ativo_id).first()
    if db_ativo is None:
        raise HTTPException(status_code=404, detail="Ativo/Amostra não encontrado")
    return db_ativo

@router.put("/ativo-amostras/{ativo_id}", response_model=schemas.AtivoEAmostras)
def update_ativo_amostra(ativo_id: int, ativo: schemas.AtivoEAmostrasCreate, db: Session = Depends(get_db)):
    db_ativo = db.query(models.AtivoEAmostras).filter(models.AtivoEAmostras.id == ativo_id).first()
    if db_ativo is None:
        raise HTTPException(status_code=404, detail="Ativo/Amostra não encontrado")
    
    for key, value in ativo.model_dump().items():
        setattr(db_ativo, key, value)
    
    db.commit()
    db.refresh(db_ativo)
    return db_ativo

@router.delete("/ativo-amostras/{ativo_id}")
def delete_ativo_amostra(ativo_id: int, db: Session = Depends(get_db)):
    db_ativo = db.query(models.AtivoEAmostras).filter(models.AtivoEAmostras.id == ativo_id).first()
    if db_ativo is None:
        raise HTTPException(status_code=404, detail="Ativo/Amostra não encontrado")
    
    db.delete(db_ativo)
    db.commit()
    return {"message": "Ativo/Amostra deletado com sucesso"}