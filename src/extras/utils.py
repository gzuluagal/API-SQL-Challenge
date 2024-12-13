import csv
from pathlib import Path
from . import schemas
from fastapi import Depends
from typing import List, Type, Dict
from src.extras.database import get_db
from sqlalchemy.orm import Session
from src.extras import models
from sqlalchemy import Integer, String
from .logger import custom_logger

logger = custom_logger()


def get_schema(path: str) -> List:
    if 'departments' in path:
        schema = list(schemas.BaseDepartments.__annotations__.keys())
    elif 'jobs' in path:
        schema = list(schemas.BaseJobs.__annotations__.keys())
    elif 'employees' in path:
        schema = list(schemas.BaseEmployees.__annotations__.keys())
    else:
        raise ValueError("No se encontro el esquema proporcionado")
    return schema


def parse_csv(path: str) -> dict:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            'El archivo entregado no exite en la ruta proporcionada')

    with file_path.open(mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        data_list = [row for row in reader]

    schema = get_schema(path)
    data = [{key: row[index]
             for index, key in enumerate(schema)} for row in data_list]

    return data


def get_existing_ids(
        data: List[Dict],
        model: Type,
        db: Session = Depends(get_db)
) -> list[dict]:

    existing_ids: List[int] = [
        int(table.id)
        for table in db.query(model.id).all()
    ]

    new_data = [
        fields for fields in data
        if int(fields['id']) not in existing_ids
    ]

    return new_data


def validate_rows(data: List[Dict], model: Type) -> list[dict]:
    valid_rows = []
    for row in data:
        try:
            # Validar tipos y valores
            for column in model.__table__.columns:
                col_name = column.name
                col_type = column.type
                value = row.get(col_name)

                if value is None or value == "":
                    # Registra si el campo es nulo y no debe serlo
                    if not column.nullable:
                        logger.error(
                            f"El campo '{col_name}' no puede ser nulo o vacio.")
                        raise ValueError(
                            f"El campo '{col_name}' no puede ser nulo o vacio.")
                elif isinstance(col_type, Integer):
                    # Valida que los enteros sean validos
                    if not str(value).isdigit():
                        logger.error(
                            f"El campo '{col_name}' debe ser un entero valido.")
                        raise ValueError(
                            f"El campo '{col_name}' debe ser un entero valido.")
                elif isinstance(col_type, String):
                    # Valida que las cadenas sean valdas
                    if not isinstance(value, str):
                        logger.error(
                            f"El campo '{col_name}' debe ser una cadena de texto.")
                        raise ValueError(
                            f"El campo '{col_name}' debe ser una cadena de texto.")

            valid_rows.append(row)

        except (ValueError, TypeError, KeyError) as e:
            logger.error(f"Fila inválida: {row}. Error: {e}")

    return valid_rows


def validate_row_limit(data: List[Dict], limit: int = 999) -> list[dict]:
    """Valida que el nnmero de filas no exceda el limite."""
    if len(data) > limit:
        logger.warning(
            (f"El numero de filas en el archivo CSV({len(data)}) excede el limite permitido de {limit}."
             f" Solo se cargaran las primeras {limit} filas.")
        )
    return data[:limit]


if __name__ == '__main__':
    data = parse_csv('API-SQL-Challenge/src/data/departments.csv')
    print(data)
    print(len(data))
