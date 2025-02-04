from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/controle-processo/", response_model=schemas.ControleProcesso)
def create_controle_processo(controle: schemas.ControleProcessoCreate, db: Session = Depends(get_db)):
    db_controle = models.ControleProcesso(**controle.model_dump())
    db.add(db_controle)
    db.commit()
    db.refresh(db_controle)
    return db_controle

@router.get("/controle-processo/", response_model=List[schemas.ControleProcesso])
def read_controles_processo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    controles = db.query(models.ControleProcesso).offset(skip).limit(limit).all()
    return controles

@router.get("/controle-processo/{controle_id}", response_model=schemas.ControleProcesso)
def read_controle_processo(controle_id: int, db: Session = Depends(get_db)):
    db_controle = db.query(models.ControleProcesso).filter(models.ControleProcesso.id == controle_id).first()
    if db_controle is None:
        raise HTTPException(status_code=404, detail="Controle de Processo não encontrado")
    return db_controle

@router.put("/controle-processo/{controle_id}", response_model=schemas.ControleProcesso)
def update_controle_processo(controle_id: int, controle: schemas.ControleProcessoCreate, db: Session = Depends(get_db)):
    db_controle = db.query(models.ControleProcesso).filter(models.ControleProcesso.id == controle_id).first()
    if db_controle is None:
        raise HTTPException(status_code=404, detail="Controle de Processo não encontrado")
    
    for key, value in controle.model_dump().items():
        setattr(db_controle, key, value)
    
    db.commit()
    db.refresh(db_controle)
    return db_controle

@router.delete("/controle-processo/{controle_id}")
def delete_controle_processo(controle_id: int, db: Session = Depends(get_db)):
    db_controle = db.query(models.ControleProcesso).filter(models.ControleProcesso.id == controle_id).first()
    if db_controle is None:
        raise HTTPException(status_code=404, detail="Controle de Processo não encontrado")
    
    db.delete(db_controle)
    db.commit()
    return {"message": "Controle de processo deletado com sucesso"}