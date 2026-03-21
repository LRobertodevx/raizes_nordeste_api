from fastapi import FastAPI
from app.infrastructure.database import engine, Base
from app.infrastructure import models

# Cria o banco de dados e as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Raízes do Nordeste", version="1.0.0")

@app.get("/")
def ler_raiz():
    return {"mensagem": "O Banco de Dados foi criado com sucesso!"}