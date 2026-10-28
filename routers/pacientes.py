
from fastapi import APIRouter, HTTPException, Query

from models import Paciente, PacienteCreate
from storage import CsvRepo


# Inicializar el repositorio CSV de pacientes
repo = CsvRepo("pacientes.csv", Paciente)


# Crear el enrutador de pacientes
router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)


# Registrar un nuevo paciente
@router.post(
    "",
    response_model=Paciente,
    status_code=201,
    summary="Registrar un nuevo paciente"
)
def crear_paciente(data: PacienteCreate):
    """
    Registra un paciente nuevo y valida que su documento
    no esté registrado previamente.
    """
    if any(
        p.documento == data.documento
        for p in repo.all()
    ):
        raise HTTPException(
            status_code=409,
            detail="Ya existe un paciente con ese documento"
        )

    return repo.add(data.model_dump())


# Listar o buscar pacientes
@router.get(
    "",
    response_model=list[Paciente],
    summary="Listar pacientes"
)
def listar_pacientes(
    nombre: str | None = Query(
        None,
        description="Buscar por parte del nombre"
    ),
    skip: int = Query(
        0,
        ge=0,
        description="Registros a saltar"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Máximo de registros"
    ),
):
    """
    Obtiene la lista de pacientes con búsqueda por nombre
    y paginación.
    """
    pacientes = repo.all()

    if nombre:
        pacientes = [
            p for p in pacientes
            if nombre.lower() in p.nombre.lower()
        ]

    return pacientes[skip: skip + limit]


# Obtener un paciente por ID
@router.get(
    "/{paciente_id}",
    response_model=Paciente,
    summary="Buscar paciente por ID"
)
def obtener_paciente(paciente_id: int):
    """
    Busca un paciente según su ID.
    """
    paciente = repo.get(paciente_id)

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    return paciente


# Actualizar los datos de un paciente
@router.put(
    "/{paciente_id}",
    response_model=Paciente,
    summary="Actualizar paciente"
)
def actualizar_paciente(
    paciente_id: int,
    data: PacienteCreate
):
    """
    Actualiza la información de un paciente existente.
    """
    paciente = repo.update(
        paciente_id,
        data.model_dump()
    )

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    return paciente


# Eliminar un paciente
@router.delete(
    "/{paciente_id}",
    status_code=204,
    summary="Eliminar paciente"
)
def eliminar_paciente(paciente_id: int):
    """
    Elimina un paciente del archivo CSV.
    """
    if not repo.delete(paciente_id):
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    return None
