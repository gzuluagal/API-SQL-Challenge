import psycopg2
import time
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends

from sqlalchemy.orm import Session
from typing import List
from src.extras import models
from src.extras.database import engine, local_session, get_db
from src.extras import schemas


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



@app.get('/jobs', response_model=List[schemas.JobsResponse])
def get_posts(db: Session = Depends(get_db)):
    jobs = db.query(models.Jobs).all()
    return jobs

@app.post('/jobs', status_code=status.HTTP_201_CREATED, response_model=schemas.JobsResponse)
def create_job(job: schemas.CreateJobs, db: Session = Depends(get_db)):

    # cursor.execute("""INSERT INTO "Jobs" (id, job) VALUES (%s, %s) RETURNING *""", (job.id, job.job))
    # new_job = cursor.fetchone()
    # connection.commit()

    new_job = models.Jobs(**job.model_dump())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@app.get('/jobs/{id}', response_model=schemas.JobsResponse)
def get_job(id: int, db: Session = Depends(get_db)):

    job = db.query(models.Jobs).filter(models.Jobs.id == id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'job con el id: {id}, no se encontro'
        )
    return job

@app.delete('/jobs/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_job(id: int, db: Session = Depends(get_db)):

    job = db.query(models.Jobs).filter(models.Jobs.id == id)

    if not job.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'job con el id: {id}, no se encontro'
        )

    job.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/jobs/{id}", response_model=schemas.JobsResponse)
def update_job(id: int, job: schemas.CreateJobs, db: Session = Depends(get_db)):

    job_query = db.query(models.Jobs).filter(models.Jobs.id == id)

    if not job_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'job con el id: {id}, no se encontro'
        )

    job_query.update(job.model_dump(), synchronize_session=False)
    db.commit()

    return job_query.first()
