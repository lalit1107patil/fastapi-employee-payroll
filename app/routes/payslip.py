from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.models.payslip import Payslip
from app.schemas.payslip import (
    PayslipCreate,
    PayslipResponse
)


router = APIRouter(
    prefix="/payslips",
    tags=["Payslips"]
)


# Generate payslip
@router.post(
    "/generate/{employee_id}",
    response_model=PayslipResponse,
    status_code=201
)
def generate_payslip(
    employee_id: int,
    payslip: PayslipCreate,
    db: Session = Depends(get_db)
):

    # Check employee
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Check duplicate payslip
    existing_payslip = db.query(Payslip).filter(
        Payslip.employee_id == employee_id,
        Payslip.month == payslip.month,
        Payslip.year == payslip.year
    ).first()

    if existing_payslip:
        raise HTTPException(
            status_code=400,
            detail="Payslip already exists for this employee and month"
        )

    # Calculate salary
    basic_salary = employee.salary
    net_pay = basic_salary - payslip.deductions

    # Create payslip
    new_payslip = Payslip(
        employee_id=employee_id,
        employee_name=employee.name,
        month=payslip.month,
        year=payslip.year,
        basic_salary=basic_salary,
        deductions=payslip.deductions,
        net_pay=net_pay
    )

    db.add(new_payslip)
    db.commit()
    db.refresh(new_payslip)

    return new_payslip


# Get all payslips
@router.get(
    "/",
    response_model=list[PayslipResponse]
)
def get_all_payslips(
    db: Session = Depends(get_db)
):

    return db.query(Payslip).all()


# Get payslips of specific employee
@router.get(
    "/{employee_id}",
    response_model=list[PayslipResponse]
)
def get_employee_payslips(
    employee_id: int,
    db: Session = Depends(get_db)
):

    # Check employee exists
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Get employee payslips
    payslips = db.query(Payslip).filter(
        Payslip.employee_id == employee_id
    ).all()

    return payslips

