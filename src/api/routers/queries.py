from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Dict
from sqlalchemy.sql import text

from src.extras import models
from src.extras.database import get_db
from src.extras import schemas
from src.sql.queries import QUARTERS, AVG_HIRED

router = APIRouter(
    prefix='/queries'
)


@router.get('/quarters', response_model=List[schemas.QuartersResponse])
def get_quarters(db: Session = Depends(get_db)) -> List[Dict]:
    """
    Obtiene el número de empleados contratados por cuarto

    Args:
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        List[schemas.QuartersResponse]: Lista con los resultados de la query `QUARTERS`.

    """

    quarters = db.execute(text(QUARTERS)).fetchall()
    result = []
    for row in quarters:
        result.append({
            'department': row[0],
            'job': row[1],
            'Q1': row[2],
            'Q2': row[3],
            'Q3': row[4],
            'Q4': row[5],
        })

    return result


@router.get('/avg_hired', response_model=List[schemas.AvgResponse])
def get_departments_above_average(db: Session = Depends(get_db)) -> List[Dict]:
    """
    Obtiene todos los departamentos que contrataron más empleados que la media de empleados contratados en 2021.

    Args:
        db (Session): Sesión de la base de datos proporcionada mediante la dependencia `Depends(get_db)`.

    Returns:
        List[schemas.DepartmentResponse]: Lista con los departamentos que contrataron más empleados que la media en 2021.
    """

    departments = db.execute(text(AVG_HIRED)).fetchall()

    result = []
    for row in departments:
        result.append({
            'id': row[0],
            'department': row[1],
            'hired_count': row[2],
        })

    return result
