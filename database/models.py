from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.connection import Base


class Department(Base):

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False,
        unique=True
    )

    description = Column(
        String(255),
        nullable=True
    )

    employees = relationship(
        "Employee",
        back_populates="department"
    )


class Employee(Base):

    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=False,
        unique=True
    )

    age = Column(
        Integer,
        nullable=False
    )

    salary = Column(
        Float,
        nullable=False
    )

    hire_date = Column(
        Date,
        nullable=False
    )

    performance_score = Column(
        Float,
        nullable=False
    )

    training_hours = Column(
        Float,
        default=0
    )

    absences = Column(
        Integer,
        default=0
    )

    status = Column(
        String(50),
        default="Activo"
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    department = relationship(
        "Department",
        back_populates="employees"
    )


class Training(Base):

    __tablename__ = "trainings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    course_name = Column(
        String(150),
        nullable=False
    )

    hours = Column(
        Float,
        nullable=False
    )

    completion_status = Column(
        String(50),
        default="Completado"
    )


class Attendance(Base):

    __tablename__ = "attendance"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False
    )