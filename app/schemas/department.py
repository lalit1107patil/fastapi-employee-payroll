from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    manager_name: str


class DepartmentResponse(BaseModel):
    id: int
    name: str
    manager_name: str

    class Config:
        from_attributes = True