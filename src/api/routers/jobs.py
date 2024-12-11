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
    jobs = db.query(models.Jobs).all()
    return jobs

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.JobsResponse)
def create_job(job: schemas.BaseJobs, db: Session = Depends(get_db)) -> Dict:

    # cursor.execute("""INSERT INTO "Jobs" (id, job) VALUES (%s, %s) RETURNING *""", (job.id, job.job))
    # new_job = cursor.fetchone()
    # connection.commit()

    new_job = models.Jobs(**job.model_dump())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get('/{id}', response_model=schemas.JobsResponse)
def get_job(id: int, db: Session = Depends(get_db)) -> Dict:

    job = db.query(models.Jobs).filter(models.Jobs.id == id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'job con el id: {id}, no se encontro'
        )
    return job

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_job(id: int, db: Session = Depends(get_db)):

    job = db.query(models.Jobs).filter(models.Jobs.id == id)

    if not job.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'job con el id: {id}, no se encontro'
        )

    job.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.JobsResponse)
def update_job(id: int, job: schemas.BaseJobs, db: Session = Depends(get_db)) -> Dict:

    job_query = db.query(models.Jobs).filter(models.Jobs.id == id)

    if not job_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'job con el id: {id}, no se encontro'
        )

    job_query.update(job.model_dump(), synchronize_session=False)
    db.commit()

    return job_query.first()