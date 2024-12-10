from sqlalchemy import Column, Integer, String
from .database import Base


class Jobs(Base):
    __tablename__ = 'Jobs'
    id = Column(Integer, primary_key=True, nullable=False)
    job = Column(String, nullable=False)

class Employee(Base):
    __tablename__ = 'Employees'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    datetime = Column(String, nullable=False)
    department_id = Column(Integer, nullable=False)
    job_id = Column(Integer, nullable=False)

class Departments(Base):
    __tablename__ = 'Departments'
    id = Column(Integer, primary_key=True, nullable=False)
    department = Column(String, nullable=False)