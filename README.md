# HR Insight

### Sistema de Analítica e Innovación para Recursos Humanos

HR Insight es una aplicación web desarrollada para apoyar la **gestión y toma de decisiones en Recursos Humanos** mediante el análisis de información de empleados, indicadores de desempeño, riesgos laborales, capacitación y ausentismo.

El sistema permite visualizar información de manera interactiva y detectar automáticamente situaciones que requieren atención mediante un sistema de **alertas inteligentes**.

---

## Objetivo del proyecto

El objetivo de HR Insight es transformar los datos de Recursos Humanos en información útil para la toma de decisiones.

La aplicación permite:

* Analizar indicadores de empleados.
* Comparar información entre departamentos.
* Identificar empleados con mayor nivel de riesgo.
* Detectar necesidades de capacitación.
* Analizar el ausentismo.
* Generar alertas inteligentes.
* Visualizar información mediante gráficos.
* Filtrar los resultados por departamento.
* Exportar los resultados a un reporte Excel.


##  Funcionalidades principales

###  Gestión y análisis de empleados

El sistema permite consultar información de los empleados y aplicar filtros según el departamento seleccionado.

Entre los datos analizados se encuentran:

* Nombre y apellido.
* Departamento.
* Sueldo.
* Desempeño.
* Horas de capacitación.
* Ausencias.

###  Indicadores KPI

El dashboard presenta indicadores generales y específicos del departamento seleccionado:

| Indicador                | Descripción                        |
| ------------------------ | ---------------------------------- |
| 👥 Empleados             | Cantidad total de empleados        |
| 💰 Sueldo promedio       | Promedio salarial del departamento |
| 📈 Desempeño             | Promedio de desempeño              |
| 🎓 Horas de capacitación | Promedio de horas de capacitación  |
| 🚑 Ausencias             | Total de ausencias registradas     |

Los indicadores se actualizan automáticamente al cambiar el departamento.


## Índice de Riesgo de RRHH

HR nsight cuenta con un módulo para identificar empleados que pueden presentar un mayor nivel de riesgo.

Los empleados son clasificados en:

* 🔴 **Alto riesgo**
* 🟡 **Riesgo medio**
* 🟢 **Bajo riesgo**

El sistema también permite visualizar:

* Cantidad de empleados por nivel de riesgo.
* Puntaje de riesgo.
* Desempeño.
* Horas de capacitación.
* Ausencias.
* Departamento.

Además, se presenta una tabla con los empleados que tienen los mayores índices de riesgo.

---

## Alertas Inteligentes

Una de las funcionalidades principales de HR Insight es el sistema de **Alertas Inteligentes de Recursos Humanos**.

El sistema analiza automáticamente diferentes indicadores y genera alertas cuando detecta situaciones que requieren atención.

Las alertas se clasifican en:

### 🔴 Riesgo alto

Situaciones que requieren atención prioritaria.

### 🟡 Requiere atención

Situaciones que deberían ser revisadas por Recursos Humanos.

### 🟢 Favorable

Indicadores o situaciones positivas detectadas en los empleados.

Las alertas se actualizan de acuerdo con el departamento seleccionado.

---

## Análisis de capacitación

El sistema permite identificar empleados que pueden requerir capacitación.

Se muestran datos como:

* Empleado.
* Departamento.
* Horas de capacitación.
* Desempeño.

También se muestra la cantidad de empleados identificados.

---

## Análisis de ausentismo

HR Insight permite identificar empleados con niveles elevados de ausentismo.

Se muestra:

* Empleado.
* Departamento.
* Cantidad de ausencias.

Esto permite detectar posibles situaciones que deberían ser analizadas por el área de Recursos Humanos.

---

## Visualizaciones

La aplicación utiliza gráficos interactivos para facilitar la interpretación de los datos.

### Vista general

Cuando se selecciona **Todos**, se muestran:

* 👥 Empleados por departamento.
* 💰 Sueldo promedio por departamento.
* 📈 Desempeño promedio por departamento.
* 📊 Distribución del riesgo.

### Vista por departamento

Cuando se selecciona un departamento específico, se muestran:

* 🏆 Top 15 de empleados según desempeño.
* 🎓 Top 15 según horas de capacitación.
* 📊 Distribución de evaluaciones de desempeño.
* 🎯 Índice de riesgo.
* ⚠️ Alertas inteligentes.
* 🎓 Necesidades de capacitación.
* 🚑 Ausentismo.

---

## 📥 Exportación de reportes

HR Insight permite generar un reporte en formato **Excel (.xlsx)**.

El reporte incluye información relacionada con:

* Empleados.
* Capacitación.
* Ausentismo.
* Alertas inteligentes.
* Departamento seleccionado.

El nombre del archivo se genera automáticamente según el departamento seleccionado.

Ejemplos:

```text
HR_Insight_Reporte_General.xlsx
HR_Insight_Reporte_Tecnologia.xlsx
HR_Insight_Reporte_Recursos_Humanos.xlsx
```

---

## 🛠️ Tecnologías utilizadas

### Frontend / Dashboard

* [Streamlit](https://streamlit.io/)
* Python
* Plotly
* Pandas

### Procesamiento y análisis

* Python
* Pandas
* Funciones propias de análisis de datos

### Reportes

* Excel
* OpenPyXL

### Control de versiones

* Git
* GitHub

---

## 📁 Estructura del proyecto

```text
HR-Insight/
│
├── app/
│   └── dashboard.py
│
├── utils/
│   ├── analytics.py
│   ├── api_client.py
│   └── reports.py
│
├── reports/
│   └── generated/
│
├── data/
│
├── requirements.txt
├── .gitignore
└── README.md
```

> Algunas carpetas pueden no aparecer en el repositorio si no contienen archivos necesarios para la ejecución o si están excluidas mediante `.gitignore`.

---

## ⚙️ Requisitos

Antes de ejecutar el proyecto se necesita tener instalado:

* Python 3.10 o superior.
* Git.
* Pip.

Se recomienda utilizar un entorno virtual para instalar las dependencias.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/cayaltaaldo/HR-Insight.git
```

### 2. Entrar al proyecto

```bash
cd HR-Insight
```

### 3. Crear un entorno virtual

En Windows:

```bash
python -m venv venv
```

### 4. Activar el entorno virtual

```bash
venv\Scripts\activate
```

En PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecutar la aplicación

Una vez instaladas las dependencias:

```bash
streamlit run app/dashboard.py
```

Streamlit mostrará una dirección similar a:

```text
Local URL: http://localhost:8501
```

Abrir esa dirección en el navegador para acceder al dashboard.

---

## 🔎 Uso del sistema

### Paso 1 — Abrir el dashboard

Al iniciar la aplicación se muestra el dashboard principal de HR Insight.

### Paso 2 — Seleccionar un departamento

Desde el panel lateral se puede seleccionar:

```text
Todos
Tecnología
Recursos Humanos
...
```

La información se actualizará automáticamente.

### Paso 3 — Revisar los KPI

Los indicadores superiores muestran un resumen de la situación del departamento.

### Paso 4 — Analizar el riesgo

Se puede revisar la distribución de empleados según:

```text
🔴 Alto
🟡 Medio
🟢 Bajo
```

### Paso 5 — Revisar alertas

El sistema muestra las alertas inteligentes generadas para el departamento seleccionado.

### Paso 6 — Revisar capacitación y ausentismo

Se pueden consultar los empleados que requieren atención en estas áreas.

### Paso 7 — Generar el reporte

Finalmente, el usuario puede descargar un reporte Excel con los resultados obtenidos.

---

## 🧠 Arquitectura general

La aplicación está organizada separando las responsabilidades principales.

```text
                 ┌──────────────────────┐
                 │      HR Insight      │
                 │      Dashboard       │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        API Client      Analytics       Reports
             │              │              │
             ▼              ▼              ▼
        Datos RRHH     Indicadores       Excel
             │
             ▼
      Filtrado por
      departamento
             │
             ▼
      ┌───────────────┐
      │   Dashboard   │
      └───────────────┘
```

### `app/dashboard.py`

Contiene la interfaz principal del sistema y coordina:

* Filtros.
* KPIs.
* Gráficos.
* Índice de riesgo.
* Alertas.
* Capacitación.
* Ausentismo.
* Reportes.

### `utils/api_client.py`

Centraliza las llamadas utilizadas para obtener información relacionada con:

* Empleados.
* KPIs.
* Riesgo.
* Capacitación.
* Ausentismo.
* Alertas.

### `utils/analytics.py`

Contiene las funciones utilizadas para realizar análisis y generar información para las visualizaciones.

### `utils/reports.py`

Se encarga de generar los reportes Excel.

---

## 🔐 Seguridad

El proyecto utiliza `.gitignore` para evitar subir información que no debería formar parte del repositorio.

Entre los elementos excluidos se encuentran:

```text
venv/
.env
__pycache__/
*.db
*.sqlite
*.sqlite3
.vscode/
reports/generated/
data/temp/
```

Las variables sensibles y credenciales deben mantenerse fuera del repositorio.

---

## 📊 Beneficios del sistema

HR Insight permite que el área de Recursos Humanos pueda:

* Centralizar información relevante.
* Analizar indicadores rápidamente.
* Detectar empleados que requieren atención.
* Identificar riesgos.
* Detectar necesidades de capacitación.
* Analizar ausentismo.
* Comparar departamentos.
* Obtener información visual.
* Generar reportes para análisis posterior.

De esta manera, los datos pueden convertirse en información útil para apoyar la toma de decisiones.

---

## 🎓 Contexto académico

Este proyecto fue desarrollado como parte de un proyecto académico de desarrollo de software, aplicando conocimientos de:

* Desarrollo de aplicaciones.
* Python.
* Análisis de datos.
* Visualización de información.
* Consumo de APIs.
* Generación de reportes.
* Control de versiones.
* Diseño de dashboards.

---

## Autor

**Dayron Cayalta**

Proyecto académico — **HR Insight**

---

## Estado del proyecto

🟢 **Proyecto funcional**

El sistema cuenta con:

* ✅ Dashboard interactivo.
* ✅ Filtros por departamento.
* ✅ KPIs.
* ✅ Índice de riesgo.
* ✅ Alertas inteligentes.
* ✅ Análisis de capacitación.
* ✅ Análisis de ausentismo.
* ✅ Visualizaciones.
* ✅ Exportación a Excel.
* ✅ Repositorio GitHub.
