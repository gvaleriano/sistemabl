from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/condicoes/", response_model=schemas.Condicoes)
def create_condicao(condicao: schemas.CondicoesCreate, db: Session = Depends(get_db)):
    db_condicao = models.Condicoes(**condicao.model_dump())
    db.add(db_condicao)
    db.commit()
    db.refresh(db_condicao)
    return db_condicao

@router.get("/condicoes/", response_model=List[schemas.Condicoes])
def read_condicoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    condicoes = db.query(models.Condicoes).offset(skip).limit(limit).all()
    return condicoes

@router.get("/condicoes/{condicao_id}", response_model=schemas.Condicoes)
def read_condicao(condicao_id: int, db: Session = Depends(get_db)):
    db_condicao = db.query(models.Condicoes).filter(models.Condicoes.id == condicao_id).first()
    if db_condicao is None:
        raise HTTPException(status_code=404, detail="Condição não encontrada")
    return db_condicao

@router.put("/condicoes/{condicao_id}", response_model=schemas.Condicoes)
def update_condicao(condicao_id: int, condicao: schemas.CondicoesCreate, db: Session = Depends(get_db)):
    db_condicao = db.query(models.Condicoes).filter(models.Condicoes.id == condicao_id).first()
    if db_condicao is None:
        raise HTTPException(status_code=404, detail="Condição não encontrada")
    
    for key, value in condicao.model_dump().items():
        setattr(db_condicao, key, value)
    
    db.commit()
    db.refresh(db_condicao)
    return db_condicao

@router.delete("/condicoes/{condicao_id}")
def delete_condicao(condicao_id: int, db: Session = Depends(get_db)):
    db_condicao = db.query(models.Condicoes).filter(models.Condicoes.id == condicao_id).first()
    if db_condicao is None:
        raise HTTPException(status_code=404, detail="Condição não encontrada")
    
    db.delete(db_condicao)
    db.commit()
    return {"message": "Condição deletada com sucesso"}

#Condições de pagamento para clientes
@router.post("/condicoes-pag-clientes/", response_model=schemas.CondicoesPagClientes)
def create_condicao_pag_cliente(condicao: schemas.CondicoesPagClientesCreate, db: Session = Depends(get_db)):
    db_condicao = models.CondicoesPagClientes(**condicao.model_dump())
    db.add(db_condicao)
    db.commit()
    db.refresh(db_condicao)
    return db_condicao

@router.get("/condicoes-pag-clientes/", response_model=List[schemas.CondicoesPagClientes])
def read_condicoes_pag_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    condicoes = db.query(models.CondicoesPagClientes).offset(skip).limit(limit).all()
    return condicoes

@router.get("/condicoes-pag-clientes/{condicao_id}", response_model=schemas.CondicoesPagClientes)
def read_condicao_pag_cliente(condicao_id: int, db: Session = Depends(get_db)):
    db_condicao = db.query(models.CondicoesPagClientes).filter(models.CondicoesPagClientes.id == condicao_id).first()
    if db_condicao is None:
        raise HTTPException(status_code=404, detail="Condição de Pagamento do Cliente não encontrada")
    return db_condicao

@router.put("/condicoes-pag-clientes/{condicao_id}", response_model=schemas.CondicoesPagClientes)
def update_condicao_pag_cliente(condicao_id: int, condicao: schemas.CondicoesPagClientesCreate, db: Session = Depends(get_db)):
    db_condicao = db.query(models.CondicoesPagClientes).filter(models.CondicoesPagClientes.id == condicao_id).first()
    if db_condicao is None:
        raise HTTPException(status_code=404, detail="Condição de Pagamento do Cliente não encontrada")
    
    for key, value in condicao.model_dump().items():
        setattr(db_condicao, key, value)
    
    db.commit()
    db.refresh(db_condicao)
    return db_condicao

@router.delete("/condicoes-pag-clientes/{condicao_id}")
def delete_condicao_pag_cliente(condicao_id: int, db: Session = Depends(get_db)):
    db_condicao = db.query(models.CondicoesPagClientes).filter(models.CondicoesPagClientes.id == condicao_id).first()
    if db_condicao is None:
        raise HTTPException(status_code=404, detail="Condição de Pagamento do Cliente não encontrada")
    
    db.delete(db_condicao)
    db.commit()
    return {"message": "Condição de Pagamento do Cliente deletada com sucesso"}