import os
import avro.schema
import avro.datafile
import avro.io
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from fastapi import Depends
from typing import Type
from src.extras.database import get_db
import json


def map_column_type(column_type) -> str:
    """
    Mapea el tipo de columna de SQLAlchemy a un tipo Avro compatible.

    Args:
        column_type: Tipo de columna de SQLAlchemy.
    Returns:
        str: Tipo Avro correspondiente.
    """

    if "INTEGER" == str(column_type):
        return "int"
    elif "VARCHAR" == str(column_type):
        return "string"


def backup_table_to_avro(model: Type, output_dir: str, db: Session = Depends(get_db)):
    """
    Realiza un respaldo de una tabla en formato Avro.

    Args:
        table_model (Type): Modelo SQLAlchemy de la tabla.
        output_dir (str): Directorio donde se guardará el archivo Avro.
        db (Session): Sesión de la base de datos.
    """
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Obtener datos de la tabla
    table_name = model.__tablename__
    records = db.query(model).all()

    # Crear el esquema Avro dinámicamente
    # inspector = inspect(model)
    # print("#"*100)
    # print(inspector.type)
    schema_fields = [
        {"name": column.name, "type": map_column_type(column.type)}
        for column in model.__table__.columns
    ]

    avro_schema = {
        "type": "record",
        "name": f"{table_name}_backup",
        "fields": schema_fields,
    }
    avro_schema_json = json.dumps(avro_schema)
    # Escribir datos en archivo Avro
    output_file = os.path.join(output_dir, f"{table_name}.avro")
    with open(output_file, "wb") as avro_file:
        writer = avro.datafile.DataFileWriter(
            avro_file, avro.io.DatumWriter(), avro.schema.parse(avro_schema_json)
        )
        for record in records:
            writer.append({column.name: getattr(record, column.name)
                          for column in model.__table__.columns})
        writer.close()

    print(f"Backup de la tabla '{table_name}' guardado en {output_file}")


def restore_table_from_avro(model, avro_file_path) -> list[dict]:
    """
    Restaura datos de un archivo Avro a una tabla de la base de datos.

    Args:
        model: Modelo SQLAlchemy de la tabla.
        avro_file_path (str): Ruta al archivo Avro.
        db: Sesión de la base de datos.
    """
    # Verificar que el archivo existe
    if not os.path.exists(avro_file_path):
        raise FileNotFoundError(f"El archivo Avro no existe: {avro_file_path}")

    # Leer los datos del archivo Avro
    with open(avro_file_path, "rb") as avro_file:
        reader = avro.datafile.DataFileReader(avro_file, avro.io.DatumReader())
        records = list(reader)
        reader.close()

    # Obtener nombres de columnas de la tabla
    inspector = inspect(model)
    table_columns = {column.name for column in inspector.columns}

    # Validar que los campos del archivo Avro coincidan con los de la tabla
    if not all(field in table_columns for field in records[0].keys()):
        raise ValueError(
            "Los campos del archivo Avro no coinciden con los de la tabla.")
    return records
