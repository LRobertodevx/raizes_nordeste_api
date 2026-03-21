from fastapi import FastAPI
from app.infrastructure.database import engine, Base
from app.infrastructure import models
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Raízes do Nordeste", 
    description="Back-end MVP para gestão de pedidos e multicanalidade",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def ler_raiz():
    return {"mensagem": "API da Raízes do Nordeste 100% Operacional!"}