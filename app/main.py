from fastapi import FastAPI
from app.database import Base, engine

from app.models.department import Department
from app.models.employee import Employee
from app.models.payslip import Payslip

from app.routes.department import router as department_router
from app.routes.employee import router as employee_router
from app.routes.payslip import router as payslip_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee & Payroll Management API"
)


# Department routes
app.include_router(department_router)
app.include_router(employee_router)
app.include_router(payslip_router)

@app.get("/")
def root():
    return {
        "message": "Employee Payroll API is running"
    }
