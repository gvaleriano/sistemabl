from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/clientes/", response_model=schemas.Clientes)
def create_cliente(cliente: schemas.ClientesCreate, db: Session = Depends(get_db)):
    db_cliente = models.Clientes(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/clientes/", response_model=List[schemas.Clientes])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(models.Clientes).offset(skip).limit(limit).all()
    return clientes

@router.get("/clientes/{cliente_id}", response_model=schemas.Clientes)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Clientes).filter(models.Clientes.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

@router.put("/clientes/{cliente_id}", response_model=schemas.Clientes)
def update_cliente(cliente_id: int, cliente: schemas.ClientesCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Clientes).filter(models.Clientes.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    for key, value in cliente.model_dump().items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/clientes/{cliente_id}")
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Clientes).filter(models.Clientes.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(db_cliente)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}