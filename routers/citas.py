from fastapi import FastAPI

from routers import citas, medicos, pacientes

app = FastAPI(
    title="Clínica Citas API",
    description="API REST para gestionar pacientes, médicos y citas.",
    version="1.0.0",
)

app.include_router(pacientes.router)
app.include_router(medicos.router)
app.include_router(citas.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {
        "mensaje": "Clínica Citas API funcionando. Documentación en /docs"
    }