from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import app.models, app.schemas
from app.database import engine, get_db

router = APIRouter() 


@router.post("/items/", response_model=app.schemas.Item)
def create_item(item: app.schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/items/", response_model=List[app.schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(app.models.Item).offset(skip).limit(limit).all()
    return items

@router.get("/items/{item_id}", response_model=app.schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(app.models.Item).filter(app.models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return db_item

@router.put("/items/{item_id}", response_model=app.schemas.Item)
def update_item(item_id: int, item: app.schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(app.models.Item).filter(app.models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(app.models.Item).filter(app.models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deletado com sucesso"}