# FastAPI Employee & Payroll Management API

## Project Overview

This project is a backend API for managing employees, departments, and employee payslips.

It is built using FastAPI, SQLAlchemy, Pydantic, and PostgreSQL.

## Features

- Create and view departments
- Create, view, update and delete employees
- Assign employees to departments
- Generate employee payslips
- Calculate net salary
- Prevent duplicate payslips
- View all payslips
- View payslips of a specific employee
- Proper error handling with HTTP status codes
- Pydantic validation
- Swagger API documentation

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

## Database

PostgreSQL database is used to store:

- Departments
- Employees
- Payslips

## API Endpoints

### Departments

| Method | Endpoint | Description |
|---|---|---|
| POST | `/departments/` | Create department |
| GET | `/departments/` | Get all departments |
| GET | `/departments/{id}` | Get department by ID |

### Employees

| Method | Endpoint | Description |
|---|---|---|
| POST | `/employees/` | Create employee |
| GET | `/employees/` | Get all employees |
| GET | `/employees/{id}` | Get employee by ID |
| PUT | `/employees/{id}` | Update employee |
| DELETE | `/employees/{id}` | Delete employee |

### Payslips

| Method | Endpoint | Description |
|---|---|---|
| POST | `/payslips/generate/{employee_id}` | Generate payslip |
| GET | `/payslips/` | Get all payslips |
| GET | `/payslips/{employee_id}` | Get employee payslips |

## Payslip Calculation

```text
Net Pay = Basic Salary - Deductions