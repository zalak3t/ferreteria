from fastapi import FastAPI
from app.routers import usuarios

app = FastAPI(
    title="API de gestión de usuarios",
    version="1.0.0",
    description="API para gestionar usuario ferremas usando FastAPI y Oracle"
)

<<<<<<< HEAD
=======

@app.get("/")
def root():
    return {"mensaje": "API de usuarios funcionando"}


>>>>>>> 9c50cf0 (actualizacion de uso de apis para iniciar sesion)
#Traeremos lo de las rutas(routers):
app.include_router(usuarios.router)