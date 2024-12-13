from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Dict

from src.extras import models
from src.extras.database import get_db
from src.extras import schemas

router = APIRouter(
    prefix='/employees'
)


@router.get('/')
def get_employees(db: Session = Depends(get_db)):
    """
    Recupera la lista completa de empleados de la base de datos.

    Args:
        db (Session): Sesión de la base de datos proporcionada mediante `Depends(get_db)`.

    Returns:
        List[models.Employees]: Lista de todos los empleados almacenados en la base de datos.

    """
    employees = db.query(models.Employees).all()
    return employees


@router.post(
    '/', status_code=status.HTTP_201_CREATED,
    response_model=schemas.EmployeesResponse
)
def create_employees(
    employee: schemas.BaseEmployees,
    db: Session = Depends(get_db)
) -> schemas.BaseEmployees:
    """
    Crea un nuevo registro de empleado en la base de datos.

    Args:
        employee (schemas.BaseEmployees): Información del empleado a crear.
        db (Session): Sesión de la base de datos proporcionada mediante `Depends(get_db)`.

    Returns:
        schemas.EmployeesResponse: Datos del empleado creado.

    Raises:
        HTTPException: Si ocurre algún error durante la creación.
    """
    new_employee = models.Employees(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.EmployeesResponse
)
def get_employee(id: int, db: Session = Depends(get_db)):
    """
    Recupera un empleado específico de la base de datos según su ID.

    Args:
        id (int): ID del empleado a recuperar.
        db (Session): Sesión de la base de datos proporcionada mediante `Depends(get_db)`.

    Returns:
        schemas.EmployeesResponse: Datos del empleado.

    Raises:
        HTTPException:
            - 404: Si el empleado con el ID proporcionado no existe.
    """
    employee = db.query(models.Employees).filter(
        models.Employees.id == id).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Employee con el id {id}, no se encontro'
        )

    return employee


@router.put('/{id}', response_model=schemas.EmployeesResponse)
def update_employee(id: int, employee: schemas.BaseEmployees, db: Session = Depends(get_db)) -> schemas.EmployeesResponse:
    """
    Actualiza la información de un empleado existente.

    Args:
        id (int): ID del empleado a actualizar.
        employee (schemas.BaseEmployees): Datos nuevos para actualizar el registro.
        db (Session): Sesión de la base de datos proporcionada mediante `Depends(get_db)`.

    Returns:
        schemas.EmployeesResponse: Datos actualizados del empleado.
    """
    employee_query = db.query(models.Employees).filter(
        models.Employees.id == id)

    if not employee_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee con el id {id}, no se encontro'
        )

    employee_query.update(employee.model_dump(), synchronize_session=False)
    db.commit()

    return employee_query.first()
