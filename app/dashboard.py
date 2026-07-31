import sys
from pathlib import Path
# ============================================
# CONFIGURAR RUTA DEL PROYECTO
# ============================================

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ============================================
# IMPORTACIONES
# ============================================

import streamlit as st
import plotly.express as px
import pandas as pd

from utils.analytics import (
    employees_by_department,
    salary_by_department,
    performance_by_department
)

from utils.api_client import (
    get_employees as api_get_employees,
    get_kpis as api_get_kpis,
    get_risk as api_get_risk,
    get_training as api_get_training,
    get_absenteeism as api_get_absenteeism,
    get_alerts as api_get_alerts
)

from utils.reports import generate_excel_report

# ============================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================

st.set_page_config(
    page_title="HR Insight",
    page_icon="📊",
    layout="wide"
)



# ============================================
# TÍTULO
# ============================================

st.title("📊 HR Insight")

st.subheader(
    "Sistema de Analítica e Innovación para Recursos Humanos"
)


# ============================================
# CARGAR DATOS
# ============================================

df = pd.DataFrame(
    api_get_employees()
)

# ============================================
# SIDEBAR
# ============================================

st.sidebar.header("🔎 Filtros")

departments = [
    "Todos"
] + sorted(
    df["department"].unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Departamento",
    departments,
    key="department_selector"
)

# ============================================
# APLICAR FILTRO
# ============================================

filtered_df = df.copy()

if selected_department != "Todos":

    filtered_df = filtered_df[
        filtered_df["department"]
        == selected_department
    ]

# =========================================================
# ÍNDICE DE RIESGO
# =========================================================

risk_df = pd.DataFrame(
    api_get_risk(
        selected_department
    )
)

# =========================================================
# ANÁLISIS Y ALERTAS
# =========================================================

training_df = pd.DataFrame(
    api_get_training(
        selected_department
    )
)

absenteeism_df = pd.DataFrame(
    api_get_absenteeism(
        selected_department
    )
)

alerts = api_get_alerts(
    selected_department
)

# ============================================
# KPIs
# ============================================

filtered_kpis = api_get_kpis(
    selected_department
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "👥 Empleados",
        filtered_kpis["total_employees"]
    )


with col2:

    st.metric(
        "💰 Sueldo promedio",
        f"S/ {filtered_kpis['average_salary']:,.2f}"
    )


with col3:

    st.metric(
        "📈 Desempeño",
        f"{filtered_kpis['average_performance']:.2f}"
    )


with col4:

    st.metric(
        "🎓 Horas capacitación",
        f"{filtered_kpis['average_training_hours']:.1f}"
    )


with col5:

    st.metric(
        "🚑 Ausencias",
        int(filtered_kpis["total_absences"])
    )


st.divider()

# ============================================
# RESUMEN DE RIESGO
# ============================================

st.header("🎯 Índice de Riesgo de RRHH")


# ============================================
# VALIDAR DATOS DE RIESGO
# ============================================

high_risk = 0
medium_risk = 0
low_risk = 0

if not risk_df.empty and "risk_level" in risk_df.columns:

    high_risk = len(
        risk_df[
            risk_df["risk_level"] == "🔴 Alto"
        ]
    )

    medium_risk = len(
        risk_df[
            risk_df["risk_level"] == "🟡 Medio"
        ]
    )

    low_risk = len(
        risk_df[
            risk_df["risk_level"] == "🟢 Bajo"
        ]
    )

else:

    st.warning(
        "⚠️ No hay datos de riesgo disponibles "
        "para el departamento seleccionado."
    )


# ============================================
# TARJETAS DE RESUMEN
# ============================================

risk_col1, risk_col2, risk_col3 = st.columns(3)


with risk_col1:

    st.metric(
        "🔴 Alto riesgo",
        high_risk
    )


with risk_col2:

    st.metric(
        "🟡 Riesgo medio",
        medium_risk
    )


with risk_col3:

    st.metric(
        "🟢 Bajo riesgo",
        low_risk
    )


# ============================================
# EMPLEADOS CON MAYOR RIESGO
# ============================================

st.subheader(
    "🚨 Empleados con mayor índice de riesgo"
)

if (
    not risk_df.empty
    and "risk_level" in risk_df.columns
    and "risk_score" in risk_df.columns
):

    risk_display = (
        risk_df
        .sort_values(
            "risk_score",
            ascending=False
        )
        [
            [
                "first_name",
                "last_name",
                "department",
                "performance_score",
                "training_hours",
                "absences",
                "risk_score",
                "risk_level"
            ]
        ]
        .head(20)
    )

    st.dataframe(
        risk_display,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No hay empleados disponibles para "
        "mostrar información de riesgo."
    )

# ============================================
# CAPACITACIÓN Y AUSENTISMO
# ============================================

training_col, absenteeism_col = st.columns(2)

# =========================================================
# DISTRIBUCIÓN DEL RIESGO
# =========================================================

st.subheader(
    "📊 Distribución de Riesgo de RRHH"
)


risk_summary = pd.DataFrame({

    "Nivel": [
        "🔴 Alto",
        "🟡 Medio",
        "🟢 Bajo"
    ],

    "Empleados": [
        high_risk,
        medium_risk,
        low_risk
    ]
})


fig = px.bar(
    risk_summary,
    x="Nivel",
    y="Empleados",
    title="Distribución de Riesgo de RRHH",
    text="Empleados",
    labels={
        "Nivel": "Nivel de riesgo",
        "Empleados": "Cantidad de empleados"
    }
)


fig.update_traces(
    textposition="outside"
)


fig.update_layout(
    height=400,
    yaxis_title="Cantidad de empleados",
    xaxis_title="Nivel de riesgo"
)


st.plotly_chart(
    fig,
    use_container_width=True,
    key="risk_distribution_chart"
)

# =========================================================
# EXPORTACIÓN DE REPORTES
# =========================================================

st.divider()

st.header(
    "📥 Exportación de Reportes"
)

st.write(
    "Genera automáticamente un reporte Excel "
    "con los indicadores y resultados del análisis."
)


# ============================================
# GENERAR REPORTE
# ============================================

report_file = generate_excel_report(
    employees_df=filtered_df,
    training_df=training_df,
    absenteeism_df=absenteeism_df,
    alerts=alerts,
    department_name=selected_department
)


# ============================================
# NOMBRE DEL ARCHIVO
# ============================================

if selected_department == "Todos":

    file_name = "HR_Insight_Reporte_General.xlsx"

else:

    safe_department = (
        selected_department
        .replace(" ", "_")
        .replace("/", "_")
    )

    file_name = (
        f"HR_Insight_Reporte_{safe_department}.xlsx"
    )


# ============================================
# BOTÓN DE DESCARGA
# ============================================

st.download_button(
    label="📊 Descargar reporte Excel",
    data=report_file,
    file_name=file_name,
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    ),
    use_container_width=True
)

# =========================================================
# VISTA GENERAL — TODOS LOS DEPARTAMENTOS
# =========================================================

if selected_department == "Todos":

    st.header(
        "📈 Análisis de Recursos Humanos"
    )

    col1, col2 = st.columns(2)


    # ========================================
    # EMPLEADOS POR DEPARTAMENTO
    # ========================================

    with col1:

        department_data = employees_by_department(
            filtered_df
        )

        fig = px.bar(
            department_data,
            x="department",
            y="employees",
            title="👥 Empleados por Departamento",
            labels={
                "department": "Departamento",
                "employees": "Empleados"
            },
            text="employees"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            height=450,
            xaxis_tickangle=-45,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=100
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="employees_by_department_chart"
        )


    # ========================================
    # SUELDO PROMEDIO
    # ========================================

    with col2:

        salary_data = salary_by_department(
            filtered_df
        )

        fig = px.bar(
            salary_data,
            x="department",
            y="salary",
            title="💰 Sueldo Promedio por Departamento",
            labels={
                "department": "Departamento",
                "salary": "Sueldo promedio"
            },
            text="salary"
        )

        fig.update_traces(
            texttemplate="S/ %{text:,.0f}",
            textposition="outside"
        )

        fig.update_layout(
            height=450,
            xaxis_tickangle=-45,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=100
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="salary_by_department_chart"
        )


    # ========================================
    # DESEMPEÑO POR DEPARTAMENTO
    # ========================================

    performance_data = performance_by_department(
        filtered_df
    )

    fig = px.bar(
        performance_data,
        x="department",
        y="performance_score",
        title="📈 Desempeño Promedio por Departamento",
        labels={
            "department": "Departamento",
            "performance_score":
                "Desempeño promedio"
        },
        text="performance_score"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        xaxis_tickangle=-45,
        yaxis=dict(
            range=[0, 100]
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=100
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="performance_by_department_chart"
    )


# =========================================================
# VISTA DEPARTAMENTO ESPECÍFICO
# =========================================================

else:

    st.header(
        f"📊 Análisis de {selected_department}"
    )

    st.write(
        f"Análisis detallado del departamento de "
        f"**{selected_department}**."
    )

    col1, col2 = st.columns(2)


    # ========================================
    # TOP DESEMPEÑO
    # ========================================

    with col1:

        performance_chart = filtered_df[
            [
                "first_name",
                "last_name",
                "performance_score"
            ]
        ].copy()

        performance_chart["employee"] = (
            performance_chart["first_name"]
            + " "
            + performance_chart["last_name"]
        )

        performance_chart = (
            performance_chart
            .sort_values(
                "performance_score",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            performance_chart,
            x="performance_score",
            y="employee",
            orientation="h",
            title="🏆 Top 15 - Desempeño",
            labels={
                "performance_score": "Desempeño",
                "employee": "Empleado"
            },
            text="performance_score"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside"
        )

        fig.update_layout(
            height=550,
            xaxis=dict(
                range=[0, 100]
            ),
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="employee_performance_chart"
        )


    # ========================================
    # TOP CAPACITACIÓN
    # ========================================

    with col2:

        training_chart = filtered_df[
            [
                "first_name",
                "last_name",
                "training_hours"
            ]
        ].copy()

        training_chart["employee"] = (
            training_chart["first_name"]
            + " "
            + training_chart["last_name"]
        )

        training_chart = (
            training_chart
            .sort_values(
                "training_hours",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            training_chart,
            x="training_hours",
            y="employee",
            orientation="h",
            title="🎓 Top 15 - Horas de Capacitación",
            labels={
                "training_hours":
                    "Horas de capacitación",
                "employee": "Empleado"
            },
            text="training_hours"
        )

        fig.update_traces(
            texttemplate="%{text:.1f} h",
            textposition="outside"
        )

        fig.update_layout(
            height=550,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="employee_training_chart"
        )


    # ========================================
    # DISTRIBUCIÓN DE DESEMPEÑO
    # ========================================

    st.subheader(
        "📊 Distribución del Desempeño"
    )

    fig = px.histogram(
        filtered_df,
        x="performance_score",
        nbins=10,
        title="Distribución de Evaluaciones de Desempeño",
        labels={
            "performance_score":
                "Puntaje de desempeño",
            "count":
                "Cantidad de empleados"
        }
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="performance_distribution_chart"
    )


# =========================================================
# ALERTAS INTELIGENTES
# =========================================================

st.divider()

st.header(
    "⚠️ Alertas Inteligentes de Recursos Humanos"
)

st.write(
    "El sistema analiza automáticamente los indicadores "
    "de los empleados e identifica situaciones que "
    "requieren atención."
)


# ============================================
# CLASIFICAR ALERTAS
# ============================================

high_alerts = [
    alert
    for alert in alerts
    if "🔴" in alert["level"]
]

medium_alerts = [
    alert
    for alert in alerts
    if "🟡" in alert["level"]
]

positive_alerts = [
    alert
    for alert in alerts
    if "🟢" in alert["level"]
]


# ============================================
# RESUMEN
# ============================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🔴 Riesgo alto",
        len(high_alerts)
    )


with col2:

    st.metric(
        "🟡 Requiere atención",
        len(medium_alerts)
    )


with col3:

    st.metric(
        "🟢 Favorable",
        len(positive_alerts)
    )


st.divider()


# ============================================
# MOSTRAR ALERTAS
# ============================================

if alerts:

    for alert in alerts:

        if "🔴" in alert["level"]:

            st.error(
                f"**{alert['title']}**\n\n"
                f"{alert['message']}"
            )

        elif "🟡" in alert["level"]:

            st.warning(
                f"**{alert['title']}**\n\n"
                f"{alert['message']}"
            )

        else:

            st.success(
                f"**{alert['title']}**\n\n"
                f"{alert['message']}"
            )

else:

    st.success(
        "No se detectaron situaciones que "
        "requieran atención."
    )

# ============================================
# CAPACITACIÓN
# ============================================

with training_col:

    st.subheader(
        "🎓 Necesitan capacitación"
    )

    st.metric(
        "Empleados identificados",
        len(training_df)
    )

    if not training_df.empty:

        st.dataframe(
            training_df[
                [
                    "first_name",
                    "last_name",
                    "department",
                    "training_hours",
                    "performance_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No se detectaron empleados "
            "que necesiten capacitación urgente."
        )


# ============================================
# AUSENTISMO
# ============================================

with absenteeism_col:

    st.subheader(
        "🚑 Alto ausentismo"
    )

    st.metric(
        "Empleados identificados",
        len(absenteeism_df)
    )

    if not absenteeism_df.empty:

        st.dataframe(
            absenteeism_df[
                [
                    "first_name",
                    "last_name",
                    "department",
                    "absences"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No se detectaron empleados "
            "con alto ausentismo."
        )


# =========================================================
# TABLA GENERAL
# =========================================================

st.divider()

st.header(
    "👥 Empleados"
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)