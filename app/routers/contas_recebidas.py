from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/contas-recebidas/", response_model=schemas.ContasRecebidas)
def create_conta_recebida(conta: schemas.ContasRecebidasCreate, db: Session = Depends(get_db)):
    db_conta = models.ContasRecebidas(**conta.model_dump())
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta

@router.get("/contas-recebidas/", response_model=List[schemas.ContasRecebidas])
def read_contas_recebidas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contas_recebidas = db.query(models.ContasRecebidas).offset(skip).limit(limit).all()
    return contas_recebidas

@router.get("/contas-recebidas/{conta_id}", response_model=schemas.ContasRecebidas)
def read_conta_recebida(conta_id: int, db: Session = Depends(get_db)):
    db_conta = db.query(models.ContasRecebidas).filter(models.ContasRecebidas.id == conta_id).first()
    if db_conta is None:
        raise HTTPException(status_code=404, detail="Conta Recebida não encontrada")
    return db_conta

@router.put("/contas-recebidas/{conta_id}", response_model=schemas.ContasRecebidas)
def update_conta_recebida(conta_id: int, conta: schemas.ContasRecebidasCreate, db: Session = Depends(get_db)):
    db_conta = db.query(models.ContasRecebidas).filter(models.ContasRecebidas.id == conta_id).first()
    if db_conta is None:
        raise HTTPException(status_code=404, detail="Conta Recebida não encontrada")
    
    for key, value in conta.model_dump().items():
        setattr(db_conta, key, value)
    
    db.commit()
    db.refresh(db_conta)
    return db_conta

@router.delete("/contas-recebidas/{conta_id}")
def delete_conta_recebida(conta_id: int, db: Session = Depends(get_db)):
    db_conta = db.query(models.ContasRecebidas).filter(models.ContasRecebidas.id == conta_id).first()
    if db_conta is None:
        raise HTTPException(status_code=404, detail="Conta Recebida não encontrada")
    
    db.delete(db_conta)
    db.commit()
    return {"message": "Conta Recebida deletada com sucesso"}

  #Detalhes
@router.post("/contas-recebidas-detalhes/", response_model=schemas.ContasRecebidasDetalhes)
def create_conta_recebida_detalhe(detalhe: schemas.ContasRecebidasDetalhesCreate, db: Session = Depends(get_db)):
    db_detalhe = models.ContasRecebidasDetalhes(**detalhe.model_dump())
    db.add(db_detalhe)
    db.commit()
    db.refresh(db_detalhe)
    return db_detalhe

@router.get("/contas-recebidas-detalhes/", response_model=List[schemas.ContasRecebidasDetalhes])
def read_contas_recebidas_detalhes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    detalhes = db.query(models.ContasRecebidasDetalhes).offset(skip).limit(limit).all()
    return detalhes

@router.get("/contas-recebidas-detalhes/{detalhe_id}", response_model=schemas.ContasRecebidasDetalhes)
def read_conta_recebida_detalhe(detalhe_id: int, db: Session = Depends(get_db)):
    db_detalhe = db.query(models.ContasRecebidasDetalhes).filter(models.ContasRecebidasDetalhes.id == detalhe_id).first()
    if db_detalhe is None:
        raise HTTPException(status_code=404, detail="Detalhe de Conta Recebida não encontrado")
    return db_detalhe

@router.put("/contas-recebidas-detalhes/{detalhe_id}", response_model=schemas.ContasRecebidasDetalhes)
def update_conta_recebida_detalhe(detalhe_id: int, detalhe: schemas.ContasRecebidasDetalhesCreate, db: Session = Depends(get_db)):
    db_detalhe = db.query(models.ContasRecebidasDetalhes).filter(models.ContasRecebidasDetalhes.id == detalhe_id).first()
    if db_detalhe is None:
        raise HTTPException(status_code=404, detail="Detalhe de Conta Recebida não encontrado")
    
    for key, value in detalhe.model_dump().items():
        setattr(db_detalhe, key, value)
    
    db.commit()
    db.refresh(db_detalhe)
    return db_detalhe

@router.delete("/contas-recebidas-detalhes/{detalhe_id}")
def delete_conta_recebida_detalhe(detalhe_id: int, db: Session = Depends(get_db)):
    db_detalhe = db.query(models.ContasRecebidasDetalhes).filter(models.ContasRecebidasDetalhes.id == detalhe_id).first()
    if db_detalhe is None:
        raise HTTPException(status_code=404, detail="Detalhe de Conta Recebida não encontrado")
    
    db.delete(db_detalhe)
    db.commit()
    return {"message": "Detalhe de Conta Recebida deletado com sucesso"}