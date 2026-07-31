from datetime import date, timedelta
import random

from faker import Faker

from database.connection import SessionLocal
from database.models import (
    Department,
    Employee,
    Training,
    Attendance
)


fake = Faker("es_ES")


# ============================================
# CONFIGURACIÓN
# ============================================

NUM_EMPLOYEES = 1500


DEPARTMENTS = [
    {
        "name": "Recursos Humanos",
        "description": "Gestión y desarrollo del talento humano."
    },
    {
        "name": "Tecnología",
        "description": "Desarrollo, infraestructura y soporte tecnológico."
    },
    {
        "name": "Finanzas",
        "description": "Gestión financiera y contable."
    },
    {
        "name": "Marketing",
        "description": "Marketing, comunicación y posicionamiento."
    },
    {
        "name": "Operaciones",
        "description": "Gestión y optimización de operaciones."
    },
    {
        "name": "Ventas",
        "description": "Gestión comercial y atención de clientes."
    },
    {
        "name": "Riesgos",
        "description": "Gestión y análisis de riesgos."
    },
    {
        "name": "Administración",
        "description": "Gestión administrativa y documental."
    }
]


TRAINING_COURSES = [
    "Excel Avanzado",
    "Python para Análisis de Datos",
    "SQL y Bases de Datos",
    "Ciberseguridad",
    "Liderazgo",
    "Comunicación Efectiva",
    "Gestión del Tiempo",
    "Power BI",
    "Gestión de Proyectos",
    "Atención al Cliente"
]


ATTENDANCE_STATUSES = [
    "Presente",
    "Presente",
    "Presente",
    "Presente",
    "Falta",
    "Tardanza",
    "Permiso"
]


# ============================================
# GENERAR DEPARTAMENTOS
# ============================================

def create_departments(session):

    print("Creando departamentos...")

    departments = []

    for department_data in DEPARTMENTS:

        department = Department(
            name=department_data["name"],
            description=department_data["description"]
        )

        session.add(department)
        departments.append(department)

    session.commit()

    print(f"✓ {len(departments)} departamentos creados.")

    return departments


# ============================================
# GENERAR EMPLEADOS
# ============================================

def create_employees(session, departments):

    print("Generando empleados...")

    employees = []

    for _ in range(NUM_EMPLOYEES):

        department = random.choice(departments)

        age = random.randint(21, 60)

        salary = round(
            random.uniform(1800, 8500),
            2
        )

        performance = round(
            random.uniform(45, 100),
            2
        )

        training_hours = round(
            random.uniform(0, 80),
            2
        )

        absences = random.randint(0, 12)

        hire_date = fake.date_between(
            start_date="-10y",
            end_date="today"
        )

        first_name = fake.first_name()
        last_name = fake.last_name()

        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}"
            f"{random.randint(1000, 9999)}"
            "@hrinsight.local"
        )

        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            age=age,
            salary=salary,
            hire_date=hire_date,
            performance_score=performance,
            training_hours=training_hours,
            absences=absences,
            status=random.choices(
                ["Activo", "Inactivo"],
                weights=[95, 5]
            )[0],
            department=department
        )

        session.add(employee)
        employees.append(employee)

    session.commit()

    print(f"✓ {len(employees)} empleados creados.")

    return employees


# ============================================
# GENERAR CAPACITACIONES
# ============================================

def create_trainings(session, employees):

    print("Generando capacitaciones...")

    total = 0

    for employee in employees:

        number_of_trainings = random.randint(0, 5)

        for _ in range(number_of_trainings):

            training = Training(
                employee_id=employee.id,
                course_name=random.choice(
                    TRAINING_COURSES
                ),
                hours=random.choice(
                    [4, 6, 8, 10, 12, 16, 20]
                ),
                completion_status=random.choices(
                    [
                        "Completado",
                        "En progreso",
                        "Pendiente"
                    ],
                    weights=[70, 20, 10]
                )[0]
            )

            session.add(training)

            total += 1

    session.commit()

    print(f"✓ {total} capacitaciones creadas.")


# ============================================
# GENERAR ASISTENCIAS
# ============================================

def create_attendance(session, employees):

    print("Generando registros de asistencia...")

    total = 0

    start_date = date.today() - timedelta(days=30)

    for employee in employees:

        for day in range(30):

            current_date = (
                start_date +
                timedelta(days=day)
            )

            # No registrar fines de semana
            if current_date.weekday() >= 5:
                continue

            status = random.choice(
                ATTENDANCE_STATUSES
            )

            attendance = Attendance(
                employee_id=employee.id,
                date=current_date,
                status=status
            )

            session.add(attendance)

            total += 1

    session.commit()

    print(f"✓ {total} registros de asistencia creados.")


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def generate_data():

    session = SessionLocal()

    try:

        print()
        print("=" * 50)
        print("HR INSIGHT - GENERADOR DE DATOS")
        print("=" * 50)
        print()

        departments = create_departments(
            session
        )

        employees = create_employees(
            session,
            departments
        )

        create_trainings(
            session,
            employees
        )

        create_attendance(
            session,
            employees
        )

        print()
        print("=" * 50)
        print("✓ DATOS GENERADOS CORRECTAMENTE")
        print("=" * 50)
        print()

    except Exception as error:

        session.rollback()

        print()
        print("❌ ERROR:")
        print(error)

    finally:

        session.close()


if __name__ == "__main__":
    generate_data()