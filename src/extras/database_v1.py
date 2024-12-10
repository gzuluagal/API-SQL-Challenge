from sqlmodel import Field, Session, SQLModel, create_engine


db_path = "company.db"
db_url = f"sqlite:///{db_path}"
engine = create_engine(db_url, echo=True)


class Employee(SQLModel, table=True):
    """Tabla que contiene la informacion del archivo hired_employees.csv"""
    id: int = Field(primary_key=True)
    name: str
    datetime: str
    department_id: int
    job_id: int

class Departments(SQLModel, table=True):
    """Tabla que contiene la informacion del archivo departments.csv"""
    id: int = Field(primary_key=True)
    deparment: str

class Jobs(SQLModel, table=True):
    """Tabla que contiene la informacion del archivo jobs.csv"""
    id: int = Field(primary_key=True)
    job: str

def init_db():
    """Crea una base de datos sqllite"""
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    db_path = "company.db"
    init_db(db_path)