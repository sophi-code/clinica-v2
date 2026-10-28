
from fastapi import FastAPI

import citas
import medicos
import pacientes


# Crear la aplicación FastAPI
app = FastAPI(
    title="Clínica Citas API",
    description=(
        "API REST para gestionar pacientes, médicos y citas. "
        "Persistencia en CSV."
    ),
    version="1.0.0",
)


# Incluir los enrutadores modulares
app.include_router(pacientes.router)
app.include_router(medicos.router)
app.include_router(citas.router)


# Ruta principal de la API
@app.get("/", tags=["Inicio"])
def inicio():
    return {
        "mensaje": (
            "Clínica Citas API funcionando. "
            "Documentación en /docs"
        )
    }

