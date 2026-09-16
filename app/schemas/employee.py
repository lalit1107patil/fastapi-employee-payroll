from pydantic import BaseModel, EmailStr
from datetime import date


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    salary: float
    joining_date: date
    department_id: int | None = None


class EmployeeUpdate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    salary: float
    joining_date: date
    department_id: int | None = None


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    salary: float
    joining_date: date
    department_id: int | None

    class Config:
        from_attributes = True