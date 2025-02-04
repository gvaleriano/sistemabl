from database import engine

try:
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Conexão bem sucedida!")
except Exception as e:
    print(f"Erro ao conectar: {str(e)}")