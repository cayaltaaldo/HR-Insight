import pandas as pd
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///./data/hr_insight.db"

engine = create_engine(DATABASE_URL)


# ============================================
# CARGAR EMPLEADOS
# ============================================

def get_employees():

    query = """
        SELECT
            e.id,
            e.first_name,
            e.last_name,
            e.email,
            e.age,
            e.salary,
            e.hire_date,
            e.performance_score,
            e.training_hours,
            e.absences,
            e.status,
            d.name AS department
        FROM employees e
        INNER JOIN departments d
            ON e.department_id = d.id
    """

    return pd.read_sql(query, engine)


# ============================================
# KPIs PRINCIPALES
# ============================================

def calculate_kpis(df):

    return {

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


# ============================================
# EMPLEADOS POR DEPARTAMENTO
# ============================================

def employees_by_department(df):

    result = (
        df
        .groupby("department")
        .size()
        .reset_index(
            name="employees"
        )
        .sort_values(
            "employees",
            ascending=False
        )
    )

    return result


# ============================================
# SALARIO PROMEDIO POR DEPARTAMENTO
# ============================================

def salary_by_department(df):

    result = (
        df
        .groupby("department")["salary"]
        .mean()
        .reset_index()
    )

    result["salary"] = result[
        "salary"
    ].round(2)

    return result.sort_values(
        "salary",
        ascending=False
    )


# ============================================
# DESEMPEÑO POR DEPARTAMENTO
# ============================================

def performance_by_department(df):

    result = (
        df
        .groupby("department")[
            "performance_score"
        ]
        .mean()
        .reset_index()
    )

    result["performance_score"] = (
        result["performance_score"]
        .round(2)
    )

    return result.sort_values(
        "performance_score",
        ascending=False
    )


# ============================================
# EMPLEADOS QUE NECESITAN CAPACITACIÓN
# ============================================

def employees_needing_training(df):

    result = df[
        (df["training_hours"] < 10)
        &
        (df["performance_score"] < 70)
    ].copy()

    return result.sort_values(
        "performance_score"
    )


# ============================================
# EMPLEADOS CON MAYOR AUSENTISMO
# ============================================

def employees_high_absenteeism(df):

    result = df[
        df["absences"] >= 5
    ].copy()

    return result.sort_values(
        "absences",
        ascending=False
    )

# ============================================
# SISTEMA DE ALERTAS DE RRHH
# ============================================

def generate_hr_alerts(df):

    alerts = []

    # ----------------------------------------
    # ALERTA 1: BAJO DESEMPEÑO + POCA CAPACITACIÓN
    # ----------------------------------------

    high_risk = df[
        (df["performance_score"] < 60)
        &
        (df["training_hours"] < 10)
    ]

    if len(high_risk) > 0:

        alerts.append({
            "level": "🔴 Alto",
            "title": "Bajo desempeño y poca capacitación",
            "message": (
                f"{len(high_risk)} empleados presentan "
                "bajo desempeño y pocas horas de capacitación."
            ),
            "count": len(high_risk)
        })

    # ----------------------------------------
    # ALERTA 2: AUSENTISMO
    # ----------------------------------------

    high_absenteeism = df[
        df["absences"] >= 8
    ]

    if len(high_absenteeism) > 0:

        alerts.append({
            "level": "🔴 Alto",
            "title": "Alto ausentismo",
            "message": (
                f"{len(high_absenteeism)} empleados "
                "presentan un nivel elevado de ausencias."
            ),
            "count": len(high_absenteeism)
        })

    # ----------------------------------------
    # ALERTA 3: DESEMPEÑO MODERADO
    # ----------------------------------------

    medium_performance = df[
        (df["performance_score"] >= 60)
        &
        (df["performance_score"] < 70)
    ]

    if len(medium_performance) > 0:

        alerts.append({
            "level": "🟡 Atención",
            "title": "Desempeño moderado",
            "message": (
                f"{len(medium_performance)} empleados "
                "presentan un desempeño que requiere seguimiento."
            ),
            "count": len(medium_performance)
        })

    # ----------------------------------------
    # ALERTA 4: POCA CAPACITACIÓN
    # ----------------------------------------

    low_training = df[
        df["training_hours"] < 20
    ]

    if len(low_training) > 0:

        alerts.append({
            "level": "🟡 Atención",
            "title": "Pocas horas de capacitación",
            "message": (
                f"{len(low_training)} empleados tienen "
                "menos de 20 horas de capacitación."
            ),
            "count": len(low_training)
        })

    # ----------------------------------------
    # ALERTA 5: BUEN DESEMPEÑO
    # ----------------------------------------

    high_performance = df[
        df["performance_score"] >= 85
    ]

    if len(high_performance) > 0:

        alerts.append({
            "level": "🟢 Favorable",
            "title": "Alto desempeño",
            "message": (
                f"{len(high_performance)} empleados "
                "presentan un desempeño sobresaliente."
            ),
            "count": len(high_performance)
        })

    return alerts

# ============================================
# ÍNDICE DE RIESGO DE RRHH
# ============================================

def calculate_employee_risk(df):

    result = df.copy()

    # Puntaje de riesgo
    result["risk_score"] = 0

    # Bajo desempeño
    result.loc[
        result["performance_score"] < 60,
        "risk_score"
    ] += 40

    result.loc[
        (result["performance_score"] >= 60) &
        (result["performance_score"] < 70),
        "risk_score"
    ] += 20

    # Pocas horas de capacitación
    result.loc[
        result["training_hours"] < 10,
        "risk_score"
    ] += 30

    result.loc[
        (result["training_hours"] >= 10) &
        (result["training_hours"] < 20),
        "risk_score"
    ] += 15

    # Ausentismo
    result.loc[
        result["absences"] >= 8,
        "risk_score"
    ] += 30

    result.loc[
        (result["absences"] >= 5) &
        (result["absences"] < 8),
        "risk_score"
    ] += 15

    # Clasificación
    result["risk_level"] = "🟢 Bajo"

    result.loc[
        result["risk_score"] >= 30,
        "risk_level"
    ] = "🟡 Medio"

    result.loc[
        result["risk_score"] >= 60,
        "risk_level"
    ] = "🔴 Alto"

    return result.sort_values(
        "risk_score",
        ascending=False
    )


# ============================================
# EJECUCIÓN DE PRUEBA
# ============================================

if __name__ == "__main__":

    df = get_employees()

    print("\n==============================")
    print("HR INSIGHT - ANALYTICS")
    print("==============================")

    print(
        f"\nRegistros: {len(df)}"
    )

    # KPIs

    print("\n--- KPIs ---")

    kpis = calculate_kpis(df)

    for key, value in kpis.items():

        print(
            f"{key}: {value}"
        )

    # Empleados por departamento

    print(
        "\n--- EMPLEADOS POR DEPARTAMENTO ---"
    )

    print(
        employees_by_department(df)
        .to_string(index=False)
    )

    # Salario

    print(
        "\n--- SALARIO PROMEDIO ---"
    )

    print(
        salary_by_department(df)
        .to_string(index=False)
    )

    # Desempeño

    print(
        "\n--- DESEMPEÑO PROMEDIO ---"
    )

    print(
        performance_by_department(df)
        .to_string(index=False)
    )

    # Capacitación

    training = employees_needing_training(
        df
    )

    print(
        "\n--- NECESITAN CAPACITACIÓN ---"
    )

    print(
        len(training),
        "empleados"
    )

    # Ausentismo

    absenteeism = employees_high_absenteeism(
        df
    )

    print(
        "\n--- ALTO AUSENTISMO ---"
    )

    print(
        len(absenteeism),
        "empleados"
    )

        # Alertas inteligentes

    alerts = generate_hr_alerts(
        df
    )

    print(
        "\n--- ALERTAS INTELIGENTES ---"
    )

    for alert in alerts:

        print(
            f"{alert['level']} | "
            f"{alert['title']} | "
            f"{alert['message']}"
        )