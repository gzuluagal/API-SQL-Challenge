from src.extras import models


MODELS = [
    {'path': "./src/data/departments.csv", 'model': models.Departments,
        'backup_path': 'src/backups/Departments.avro'},
    {'path': "./src/data/jobs.csv", 'model': models.Jobs,
        'backup_path': 'src/backups/jobs.avro'},
    {'path': "./src/data/hired_employees.csv", 'model': models.Employees,
        'backup_path': 'src/backups/Employees.avro'}
]

BACKUP_DIR = "src/backups/"
