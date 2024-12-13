from src.extras import models


MODELS = [
    {'path': "./src/data/departments.csv", 'model': models.Departments},
    {'path': "./src/data/jobs.csv", 'model': models.Jobs},
    {'path': "./src/data/hired_employees.csv", 'model': models.Employees}
]
