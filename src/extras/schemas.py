from pydantic import BaseModel


class BaseJobs(BaseModel):
    id: int
    job: str

class CreateJobs(BaseJobs):
    pass

class JobsResponse(BaseModel):
    job: str
    class Config:
        from_attributes = True
