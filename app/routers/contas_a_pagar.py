from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/contas-a-pagar/", response_model=schemas.ContasAPagar)
def create_conta_pagar(conta: schemas.ContasAPagarCreate, db: Session = Depends(get_db)):
    db_conta = models.ContasAPagar(**conta.model_dump())
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta

@router.get("/contas-a-pagar/", response_model=List[schemas.ContasAPagar])
def read_contas_pagar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contas_pagar = db.query(models.ContasAPagar).offset(skip).limit(limit).all()
    return contas_pagar

@router.get("/contas-a-pagar/{conta_id}", response_model=schemas.ContasAPagar)
def read_conta_pagar(conta_id: int, db: Session = Depends(get_db)):
    db_conta = db.query(models.ContasAPagar).filter(models.ContasAPagar.id == conta_id).first()
    if db_conta is None:
        raise HTTPException(status_code=404, detail="Conta a Pagar não encontrada")
    return db_conta

@router.put("/contas-a-pagar/{conta_id}", response_model=schemas.ContasAPagar)
def update_conta_pagar(conta_id: int, conta: schemas.ContasAPagarCreate, db: Session = Depends(get_db)):
    db_conta = db.query(models.ContasAPagar).filter(models.ContasAPagar.id == conta_id).first()
    if db_conta is None:
        raise HTTPException(status_code=404, detail="Conta a Pagar não encontrada")
    
    for key, value in conta.model_dump().items():
        setattr(db_conta, key, value)
    
    db.commit()
    db.refresh(db_conta)
    return db_conta

@router.delete("/contas-a-pagar/{conta_id}")
def delete_conta_pagar(conta_id: int, db: Session = Depends(get_db)):
    db_conta = db.query(models.ContasAPagar).filter(models.ContasAPagar.id == conta_id).first()
    if db_conta is None:
        raise HTTPException(status_code=404, detail="Conta a Pagar não encontrada")
    
    db.delete(db_conta)
    db.commit()
    return {"message": "Conta a Pagar deletada com sucesso"}