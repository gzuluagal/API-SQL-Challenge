from pydantic import BaseModel


class BaseJobs(BaseModel):
    id: int
    job: str


class JobsResponse(BaseJobs):
    class Config:
        from_attributes = True

class BaseEmployees(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

class EmployeesResponse(BaseModel):
    id: int
    name: str
    datetime: str
    class Config:
        from_attributes = True

class BaseDepartments(BaseModel):
    id: int
    department: str

class DepartementsResponse(BaseDepartments):

    class Config:
        from_attributes = True