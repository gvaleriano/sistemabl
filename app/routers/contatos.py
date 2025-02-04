from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Contatos, Clientes
from app.schemas import Contatos as ContatosSchema, ContatosCreate
from app.database import get_db

router = APIRouter()

@router.post("/contatos/", response_model=ContatosSchema)
def create_contato(contato: ContatosCreate, db: Session = Depends(get_db)):
    db_contato = Contatos(**contato.dict())
    db.add(db_contato)
    db.commit()
    db.refresh(db_contato)
    return db_contato

@router.get("/contatos/", response_model=List[ContatosSchema])
def read_contatos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contatos = db.query(Contatos).offset(skip).limit(limit).all()
    return contatos

@router.get("/contatos/{contato_id}", response_model=ContatosSchema)
def read_contato(contato_id: int, db: Session = Depends(get_db)):
    db_contato = db.query(Contatos).filter(Contatos.id == contato_id).first()
    if db_contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return db_contato

@router.put("/contatos/{contato_id}", response_model=ContatosSchema)
def update_contato(contato_id: int, contato: ContatosCreate, db: Session = Depends(get_db)):
    db_contato = db.query(Contatos).filter(Contatos.id == contato_id).first()
    if db_contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    
    for key, value in contato.dict().items():
        setattr(db_contato, key, value)
    
    db.commit()
    db.refresh(db_contato)
    return db_contato

@router.delete("/contatos/{contato_id}")
def delete_contato(contato_id: int, db: Session = Depends(get_db)):
    db_contato = db.query(Contatos).filter(Contatos.id == contato_id).first()
    if db_contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    
    db.delete(db_contato)
    db.commit()
    return {"message": "Contato deletado com sucesso"}