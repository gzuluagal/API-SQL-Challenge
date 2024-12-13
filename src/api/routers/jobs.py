from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Dict

from src.extras import models
from src.extras.database import get_db
from src.extras import schemas

router = APIRouter(
    prefix='/jobs'
)


@router.get('/', response_model=List[schemas.JobsResponse])
def get_jobs(db: Session = Depends(get_db)) -> List[Dict]:
    """
    Obtiene todos los trabajos de la base de datos.

    Args:
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        List[schemas.JobsResponse]: Lista de trabajos obtenidos de la base de datos.
    """
    jobs = db.query(models.Jobs).all()
    return jobs


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.JobsResponse)
def create_job(job: schemas.BaseJobs, db: Session = Depends(get_db)) -> schemas.JobsResponse:
    """
    Crea un nuevo trabajo en la base de datos.

    Args:
        job (schemas.BaseJobs): Datos del nuevo trabajo a crear.
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        schemas.JobsResponse: Información del trabajo recién creado.
    """
    new_job = models.Jobs(**job.model_dump())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.get('/{id}', response_model=schemas.JobsResponse)
def get_job(id: int, db: Session = Depends(get_db)) -> schemas.JobsResponse:
    """
    Obtiene un trabajo específico de la base de datos mediante su ID.

    Args:
        id (int): ID del trabajo a obtener.
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        schemas.JobsResponse: Información del trabajo.
    """
    job = db.query(models.Jobs).filter(models.Jobs.id == id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'job con el id: {id}, no se encontro'
        )
    return job


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_job(id: int, db: Session = Depends(get_db)):
    """
    Elimina un trabajo específico de la base de datos mediante su ID.

    Args:
        id (int): ID del trabajo a eliminar.
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        Response: Respuesta con código de estado 204 (No Content) si la eliminación fue exitosa.
    """
    job = db.query(models.Jobs).filter(models.Jobs.id == id)

    if not job.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'job con el id: {id}, no se encontro'
        )

    job.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.JobsResponse)
def update_job(id: int, job: schemas.BaseJobs, db: Session = Depends(get_db)) -> schemas.JobsResponse:
    """
    Actualiza la información de un trabajo específico en la base de datos.

    Args:
        id (int): ID del trabajo a actualizar.
        job (schemas.BaseJobs): Nuevos datos del trabajo.
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        schemas.JobsResponse: Información del trabajo actualizado.
    """
    job_query = db.query(models.Jobs).filter(models.Jobs.id == id)

    if not job_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'job con el id: {id}, no se encontro'
        )

    job_query.update(job.model_dump(), synchronize_session=False)
    db.commit()

    return job_query.first()
