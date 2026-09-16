from pydantic import BaseModel, Field


class PayslipCreate(BaseModel):
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000)
    deductions: float = Field(default=0, ge=0)


class PayslipResponse(BaseModel):
    id: int
    employee_id: int | None
    employee_name: str | None
    month: int
    year: int
    basic_salary: float
    deductions: float
    net_pay: float

    class Config:
        from_attributes = True