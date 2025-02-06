# database.py
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from app import models

# Configurações do banco de dados
DB_USER = "sisbladm"
DB_PASSWORD = quote_plus("pTMtXIXbp1756kUHTwq0YAoUhXz6P3NU")  # Codifica caracteres especiais na senha
DB_HOST = "dpg-cuhakid6l47c73do5i3g-a.oregon-postgres.render.com"
DB_PORT = "5432"
DB_NAME = "sistemabl"  # Nome do banco de dados

# Construindo a URL com parâmetros adicionais
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

try:
    # Criando o engine com configurações adicionais
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,  # Verifica conexão antes de usar
        connect_args={
            'client_encoding': 'utf8',
            'options': '-c timezone=utc'
        }
    )

    # Teste de conexão
    with engine.connect() as connection:
        print("Conexão com o banco de dados estabelecida com sucesso!")

except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

