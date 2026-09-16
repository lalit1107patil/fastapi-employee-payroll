from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint, String
from datetime import datetime
from app.database import Base


class Payslip(Base):
    __tablename__ = "payslips"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="SET NULL"),
        nullable=True
    )

    employee_name = Column(String, nullable=False)

    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    basic_salary = Column(Float, nullable=False)
    deductions = Column(Float, default=0)
    net_pay = Column(Float, nullable=False)

    generated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "month",
            "year",
            name="unique_employee_month_year"
        ),
    )