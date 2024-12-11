import psycopg2
import time
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict

from src.extras import models
from src.extras.database import engine, get_db
from src.extras import schemas
from src.api.routers import jobs, employees, departments

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5433,
            database="company_db",
            user="postgres",
            password="password",
            cursor_factory=RealDictCursor
        )
        cursor = connection.cursor()
        print("Conexión exitosa")
        break
    except OperationalError as e:
        print(f"No se logro la conexion a la BD: {e}")
        time.sleep(2)


app.include_router(jobs.router)
app.include_router(employees.router)
app.include_router(departments.router)