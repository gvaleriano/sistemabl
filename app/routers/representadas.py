from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Representadas
from app.schemas import Representadas as RepresentadasSchema, RepresentadasCreate
from app.database import get_db

router = APIRouter()

@router.post("/representadas/", response_model=RepresentadasSchema)
def create_representada(representada: RepresentadasCreate, db: Session = Depends(get_db)):
    db_representada = Representadas(**representada.dict())
    db.add(db_representada)
    db.commit()
    db.refresh(db_representada)
    return db_representada

@router.get("/representadas/", response_model=List[RepresentadasSchema])
def read_representadas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    representadas = db.query(Representadas).offset(skip).limit(limit).all()
    return representadas

@router.get("/representadas/{representada_id}", response_model=RepresentadasSchema)
def read_representada(representada_id: int, db: Session = Depends(get_db)):
    db_representada = db.query(Representadas).filter(Representadas.id == representada_id).first()
    if db_representada is None:
        raise HTTPException(status_code=404, detail="Representada não encontrada")
    return db_representada

@router.put("/representadas/{representada_id}", response_model=RepresentadasSchema)
def update_representada(representada_id: int, representada: RepresentadasCreate, db: Session = Depends(get_db)):
    db_representada = db.query(Representadas).filter(Representadas.id == representada_id).first()
    if db_representada is None:
        raise HTTPException(status_code=404, detail="Representada não encontrada")
    
    for key, value in representada.dict().items():
        setattr(db_representada, key, value)
    
    db.commit()
    db.refresh(db_representada)
    return db_representada

@router.delete("/representadas/{representada_id}")
def delete_representada(representada_id: int, db: Session = Depends(get_db)):
    db_representada = db.query(Representadas).filter(Representadas.id == representada_id).first()
    if db_representada is None:
        raise HTTPException(status_code=404, detail="Representada não encontrada")
    
    db.delete(db_representada)
    db.commit()
    return {"message": "Representada deletada com sucesso"}