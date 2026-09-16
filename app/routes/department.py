from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse
)


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# GET all departments
@router.get("/", response_model=list[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db)
):

    return db.query(Department).all()


# GET department by ID
@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


# POST create department
@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=201
)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):

    new_department = Department(
        name=department.name,
        manager_name=department.manager_name
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department

