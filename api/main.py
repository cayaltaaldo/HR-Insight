from fastapi import FastAPI
from typing import Optional

from utils.analytics import (
    get_employees,
    employees_by_department,
    employees_needing_training,
    employees_high_absenteeism,
    generate_hr_alerts,
    calculate_employee_risk
)


# =========================================================
# CONFIGURACIÓN DE LA API
# =========================================================

app = FastAPI(
    title="HR Insight API",
    description="API REST para analítica de Recursos Humanos",
    version="1.0.0"
)


# =========================================================
# RUTA PRINCIPAL
# =========================================================

@app.get("/")
def root():

    return {
        "message": "HR Insight API funcionando",
        "version": "1.0.0",
        "status": "online"
    }


# =========================================================
# EMPLEADOS
# =========================================================

@app.get("/employees")
def get_all_employees(
    department: Optional[str] = None
):

    print("🔥 EL DASHBOARD SOLICITÓ LOS EMPLEADOS A LA API")

    df = get_employees()

    # Filtrar por departamento si se recibió
    if department:
        df = df[
            df["department"] == department
        ]

    return df.to_dict(
        orient="records"
    )


# =========================================================
# KPIs
# =========================================================

@app.get("/kpis")
def get_kpis(
    department: Optional[str] = None
):

    print("📊 EL DASHBOARD SOLICITÓ LOS KPIs A LA API")

    df = get_employees()

    # Filtrar por departamento
    if department:
        df = df[
            df["department"] == department
        ]

    # Evitar problemas si no existen empleados
    if df.empty:

        return {
            "total_employees": 0,
            "average_salary": 0,
            "average_performance": 0,
            "average_training_hours": 0,
            "total_absences": 0
        }

    kpis = {

        "total_employees":
            len(df),

        "average_salary":
            round(
                df["salary"].mean(),
                2
            ),

        "average_performance":
            round(
                df["performance_score"].mean(),
                2
            ),

        "average_training_hours":
            round(
                df["training_hours"].mean(),
                2
            ),

        "total_absences":
            int(
                df["absences"].sum()
            )
    }

    return kpis


# =========================================================
# DEPARTAMENTOS
# =========================================================

@app.get("/departments")
def get_departments():

    print(
        "🏢 EL DASHBOARD SOLICITÓ LOS DEPARTAMENTOS A LA API"
    )

    df = get_employees()

    result = employees_by_department(
        df
    )

    return result.to_dict(
        orient="records"
    )


# =========================================================
# ÍNDICE DE RIESGO
# =========================================================

@app.get("/risk")
def get_employee_risk(
    department: Optional[str] = None
):

    print(
        "🎯 EL DASHBOARD SOLICITÓ EL RIESGO A LA API"
    )

    df = get_employees()

    # Filtrar por departamento
    if department:
        df = df[
            df["department"] == department
        ]

    result = calculate_employee_risk(
        df
    )

    return result[
        [
            "id",
            "first_name",
            "last_name",
            "department",
            "performance_score",
            "training_hours",
            "absences",
            "risk_score",
            "risk_level"
        ]
    ].to_dict(
        orient="records"
    )


# =========================================================
# EMPLEADOS QUE NECESITAN CAPACITACIÓN
# =========================================================

@app.get("/training")
def get_training(
    department: Optional[str] = None
):

    print(
        "🎓 EL DASHBOARD SOLICITÓ CAPACITACIÓN A LA API"
    )

    df = get_employees()

    # Filtrar por departamento
    if department:
        df = df[
            df["department"] == department
        ]

    result = employees_needing_training(
        df
    )

    return result[
        [
            "id",
            "first_name",
            "last_name",
            "department",
            "training_hours",
            "performance_score"
        ]
    ].to_dict(
        orient="records"
    )


# =========================================================
# EMPLEADOS CON ALTO AUSENTISMO
# =========================================================

@app.get("/absenteeism")
def get_absenteeism(
    department: Optional[str] = None
):

    print(
        "🚑 EL DASHBOARD SOLICITÓ AUSENTISMO A LA API"
    )

    df = get_employees()

    # Filtrar por departamento
    if department:
        df = df[
            df["department"] == department
        ]

    result = employees_high_absenteeism(
        df
    )

    return result[
        [
            "id",
            "first_name",
            "last_name",
            "department",
            "absences"
        ]
    ].to_dict(
        orient="records"
    )


# =========================================================
# ALERTAS INTELIGENTES
# =========================================================

@app.get("/alerts")
def get_alerts(
    department: Optional[str] = None
):

    print(
        "⚠️ EL DASHBOARD SOLICITÓ ALERTAS A LA API"
    )

    df = get_employees()

    # Filtrar por departamento
    if department:
        df = df[
            df["department"] == department
        ]

    alerts = generate_hr_alerts(
        df
    )

    return alerts