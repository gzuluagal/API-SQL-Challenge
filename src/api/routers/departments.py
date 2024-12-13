from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Dict

from src.extras import models
from src.extras.database import get_db
from src.extras import schemas


router = APIRouter(
    prefix='/departments'
)


@router.get('/', response_model=List[schemas.DepartementsResponse])
def get_departments(db: Session = Depends(get_db)) -> List[Dict]:
    """
    Obtiene todos los departamentos de la base de datos.

    Args:
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        List[schemas.DepartementsResponse]: Lista de departamentos obtenidos de la base de datos.

    """
    departments = db.query(models.Departments).all()
    return departments


@router.get(
    '/{id}', status_code=status.HTTP_200_OK,
    response_model=schemas.DepartementsResponse
)
def get_department(id: int, db: Session = Depends(get_db)) -> schemas.DepartementsResponse:
    """
    Obtiene un departamento específico de la base de datos mediante su ID.

    Args:
        id (int): ID del departamento a obtener.
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        schemas.DepartementsResponse: Información del departamento.
    """
    department = db.query(
        models.Departments
    ).filter(models.Departments.id == id).first()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Department con el id: {id}, no se encontro'
        )

    return department


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.DepartementsResponse)
def create_department(department: schemas.BaseDepartments, db: Session = Depends(get_db)) -> schemas.DepartementsResponse:
    """
    Crea un nuevo departamento en la base de datos.

    Args:
        department (schemas.BaseDepartments): Datos del nuevo departamento a crear.
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        Dict: Información del departamento creado.
    """
    new_department = models.Departments(**department.model_dump())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_department(id: int, db: Session = Depends(get_db)):
    """
    Elimina un departamento específico de la base de datos mediante su ID.

    Args:
        id (int): ID del departamento a eliminar.
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        Response: Respuesta con código de estado 204 (No Content) si la eliminación fue exitosa.
    """
    department = db.query(models.Departments).filter(
        models.Departments.id == id)

    if not department.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Department con el id {id}, no se encontro'
        )
    department.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.DepartementsResponse)
def update_department(
    id: int,
    department: schemas.BaseDepartments,
    db: Session = Depends(get_db)
) -> schemas.DepartementsResponse:
    """
    Actualiza la información de un departamento específico en la base de datos.

    Args:
        id (int): ID del departamento a actualizar.
        department (schemas.BaseDepartments): Nuevos datos del departamento.
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        schemas.DepartementsResponse: Información del departamento actualizado.
    """
    department_query = db.query(models.Departments).filter(
        models.Departments.id == id)

    if not department_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Department con el id {id}, no se encontro'
        )

    department_query.update(
        department.model_dump(),
        synchronize_session=False
    )
    db.commit()

    return department_query.first()
