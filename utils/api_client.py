import requests


API_URL = "http://127.0.0.1:8000"


# ============================================
# EMPLEADOS
# ============================================

def get_employees(department=None):

    params = {}

    if department and department != "Todos":
        params["department"] = department

    response = requests.get(
        f"{API_URL}/employees",
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ============================================
# KPIs
# ============================================

def get_kpis(department=None):

    params = {}

    if department and department != "Todos":
        params["department"] = department

    response = requests.get(
        f"{API_URL}/kpis",
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ============================================
# DEPARTAMENTOS
# ============================================

def get_departments():

    response = requests.get(
        f"{API_URL}/departments",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ============================================
# RIESGO
# ============================================

def get_risk(department=None):

    params = {}

    if department and department != "Todos":
        params["department"] = department

    response = requests.get(
        f"{API_URL}/risk",
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ============================================
# ============================================
# CAPACITACIÓN
# ============================================

def get_training(department=None):

    params = {}

    if department and department != "Todos":
        params["department"] = department

    response = requests.get(
        f"{API_URL}/training",
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ============================================
# AUSENTISMO
# ============================================

def get_absenteeism(department=None):

    params = {}

    if department and department != "Todos":
        params["department"] = department

    response = requests.get(
        f"{API_URL}/absenteeism",
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ============================================
# ALERTAS
# ============================================

def get_alerts(department=None):

    params = {}

    if department and department != "Todos":
        params["department"] = department

    response = requests.get(
        f"{API_URL}/alerts",
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()