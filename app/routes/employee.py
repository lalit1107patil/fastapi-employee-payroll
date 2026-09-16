from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# GET all employees
@router.get("/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):

    return db.query(Employee).all()


# GET employee by ID
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# POST create employee
@router.post("/", response_model=EmployeeResponse, status_code=201)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    # Check duplicate email
    existing_employee = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Employee with this email already exists"
        )

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        phone=employee.phone,
        salary=employee.salary,
        joining_date=employee.joining_date,
        department_id=employee.department_id
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# PUT update employee
@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    existing_employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not existing_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Check if email belongs to another employee
    duplicate_email = db.query(Employee).filter(
        Employee.email == employee.email,
        Employee.id != employee_id
    ).first()

    if duplicate_email:
        raise HTTPException(
            status_code=400,
            detail="Another employee already uses this email"
        )

    existing_employee.name = employee.name
    existing_employee.email = employee.email
    existing_employee.phone = employee.phone
    existing_employee.salary = employee.salary
    existing_employee.joining_date = employee.joining_date
    existing_employee.department_id = employee.department_id

    db.commit()
    db.refresh(existing_employee)

    return existing_employee


# DELETE employee
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }
