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
    """
    Devuelve el esquema correspondiente basado en el archivo proporcionado.

    Args:
        path (str): Ruta o nombre del archivo que contiene los datos.

    Returns:
        List: Lista de nombres de campos correspondientes al esquema.
    """
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
    """
    Parsea un archivo CSV en una lista de diccionarios con base en un esquema definido.

    Args:
        path (str): Ruta al archivo CSV que se desea parsear.

    Returns:
        dict: Lista de diccionarios, donde cada diccionario representa una fila del CSV mapeada al esquema.
    """
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
    """
    Filtra los registros que ya existen en la base de datos según sus IDs.

    Args:
        data (List[Dict]): Lista de diccionarios que representan los registros a validar.
        model (Type): Modelo SQLAlchemy correspondiente a la tabla de la base de datos.
        db (Session): Sesión activa de la base de datos.

    Returns:
        list[dict]: Lista de diccionarios con los registros que no tienen ID en la base de datos.
    """
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
    """
    Valida los registros según las restricciones definidas en el modelo SQLAlchemy.

    Args:
        data (List[Dict]): Lista de registros a validar, donde cada registro es un diccionario.
        model (Type): Modelo SQLAlchemy que define la estructura y restricciones de la tabla.

    Returns:
        list[dict]: Lista de registros válidos que cumplen con las restricciones del modelo.
    """
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
    """
    Valida que el número de filas en la lista no exceda el límite permitido.

    Args:
        data (List[Dict]): Lista de registros a validar.
        limit (int, opcional): Límite máximo permitido de filas. Por defecto es 999.

    Returns:
        list[dict]: Lista con un máximo de `limit` filas.

    Logs:
        - Genera una advertencia si la cantidad de filas en `data` excede el límite.
    """
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
