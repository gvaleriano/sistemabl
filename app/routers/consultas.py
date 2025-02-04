from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/consultas/", response_model=schemas.Consultas)
def create_consulta(consulta: schemas.ConsultasCreate, db: Session = Depends(get_db)):
    db_consulta = models.Consultas(**consulta.model_dump())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@router.get("/consultas/", response_model=List[schemas.Consultas])
def read_consultas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consultas = db.query(models.Consultas).offset(skip).limit(limit).all()
    return consultas

@router.get("/consultas/{consulta_id}", response_model=schemas.Consultas)
def read_consulta(consulta_id: int, db: Session = Depends(get_db)):
    db_consulta = db.query(models.Consultas).filter(models.Consultas.id == consulta_id).first()
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return db_consulta

@router.put("/consultas/{consulta_id}", response_model=schemas.Consultas)
def update_consulta(consulta_id: int, consulta: schemas.ConsultasCreate, db: Session = Depends(get_db)):
    db_consulta = db.query(models.Consultas).filter(models.Consultas.id == consulta_id).first()
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    for key, value in consulta.model_dump().items():
        setattr(db_consulta, key, value)
    
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@router.delete("/consultas/{consulta_id}")
def delete_consulta(consulta_id: int, db: Session = Depends(get_db)):
    db_consulta = db.query(models.Consultas).filter(models.Consultas.id == consulta_id).first()
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    db.delete(db_consulta)
    db.commit()
    return {"message": "Consulta deletada com sucesso"}
    
#Detalhes das consultas
@router.post("/consultas-detalhes/", response_model=schemas.ConsultasDetalhes)
def create_consulta_detalhe(detalhe: schemas.ConsultasDetalhesCreate, db: Session = Depends(get_db)):
    db_detalhe = models.ConsultasDetalhes(**detalhe.model_dump())
    db.add(db_detalhe)
    db.commit()
    db.refresh(db_detalhe)
    return db_detalhe

@router.get("/consultas-detalhes/", response_model=List[schemas.ConsultasDetalhes])
def read_consultas_detalhes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    detalhes = db.query(models.ConsultasDetalhes).offset(skip).limit(limit).all()
    return detalhes

@router.get("/consultas-detalhes/{detalhe_id}", response_model=schemas.ConsultasDetalhes)
def read_consulta_detalhe(detalhe_id: int, db: Session = Depends(get_db)):
    db_detalhe = db.query(models.ConsultasDetalhes).filter(models.ConsultasDetalhes.id == detalhe_id).first()
    if db_detalhe is None:
        raise HTTPException(status_code=404, detail="Detalhe de Consulta não encontrado")
    return db_detalhe

@router.put("/consultas-detalhes/{detalhe_id}", response_model=schemas.ConsultasDetalhes)
def update_consulta_detalhe(detalhe_id: int, detalhe: schemas.ConsultasDetalhesCreate, db: Session = Depends(get_db)):
    db_detalhe = db.query(models.ConsultasDetalhes).filter(models.ConsultasDetalhes.id == detalhe_id).first()
    if db_detalhe is None:
        raise HTTPException(status_code=404, detail="Detalhe de Consulta não encontrado")
    
    for key, value in detalhe.model_dump().items():
        setattr(db_detalhe, key, value)
    
    db.commit()
    db.refresh(db_detalhe)
    return db_detalhe

@router.delete("/consultas-detalhes/{detalhe_id}")
def delete_consulta_detalhe(detalhe_id: int, db: Session = Depends(get_db)):
    db_detalhe = db.query(models.ConsultasDetalhes).filter(models.ConsultasDetalhes.id == detalhe_id).first()
    if db_detalhe is None:
        raise HTTPException(status_code=404, detail="Detalhe de Consulta não encontrado")
    
    db.delete(db_detalhe)
    db.commit()
    return {"message": "Detalhe de Consulta deletado com sucesso"}