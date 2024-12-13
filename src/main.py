from fastapi import FastAPI

from src.extras import models
from src.extras.database import engine
from src.api.routers import jobs, employees, departments, files


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(jobs.router)
app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(files.router)
