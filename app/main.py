from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import items, bancos, cambio, cash, ativo_amostras, representadas
from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ativo_amostras.router)
app.include_router(bancos.router)
app.include_router(cambio.router)
app.include_router(cash.router)
app.include_router(representadas.router)
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Sistema Bl iniciado com sucesso!"}
