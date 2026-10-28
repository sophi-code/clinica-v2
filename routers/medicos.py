from fastapi import APIRouter, HTTPException, Query 
from models import Medico, MedicoCreate
from storage import CsvRepo


# Inicializar el repositorio CSV
repo = CsvRepo("medicos.csv", Medico)


# Crear el router de médicos
router = APIRouter(
    prefix="/medicos",
    tags=["Médicos"]
)


# Registrar un nuevo médico
@router.post(
    "",
    response_model=Medico,
    status_code=201
)
def crear_medico(data: MedicoCreate):
    if any(
        m.licencia == data.licencia
        for m in repo.all()
    ):
        raise HTTPException(
            status_code=409,
            detail="Ya existe un médico con esa licencia"
        )

    return repo.add(data.model_dump())


# Listar o filtrar médicos
@router.get(
    "",
    response_model=list[Medico]
)
def listar_medicos(
    especialidad: str | None = Query(
        None,
        description="Filtrar por especialidad"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    medicos = repo.all()

    if especialidad:
        medicos = [
            m for m in medicos
            if especialidad.lower() in m.especialidad.lower()
        ]

    return medicos[skip:skip + limit]


# Obtener un médico por ID
@router.get(
    "/{medico_id}",
    response_model=Medico
)
def obtener_medico(medico_id: int):
    medico = repo.get(medico_id)

    if not medico:
        raise HTTPException(
            status_code=404,
            detail="Médico no encontrado"
        )

    return medico


# Actualizar los datos de un médico
@router.put(
    "/{medico_id}",
    response_model=Medico
)
def actualizar_medico(
    medico_id: int,
    data: MedicoCreate
):
    # Verificar que el médico exista
    if not repo.get(medico_id):
        raise HTTPException(
            status_code=404,
            detail="Médico no encontrado"
        )

    # Evitar licencias duplicadas al actualizar
    if any(
        m.id != medico_id and m.licencia == data.licencia
        for m in repo.all()
    ):
        raise HTTPException(
            status_code=409,
            detail="Ya existe otro médico con esa licencia"
        )

    return repo.update(
        medico_id,
        data.model_dump()
    )


# Eliminar un médico
@router.delete(
    "/{medico_id}",
    status_code=204
)
def eliminar_medico(medico_id: int):
    if not repo.delete(medico_id):
        raise HTTPException(
            status_code=404,
            detail="Médico no encontrado"
        )

    return None
