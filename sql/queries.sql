-- ============================================
-- HR INSIGHT
-- Consultas SQL para análisis de RRHH
-- ============================================


-- 1. Listar empleados activos

SELECT
    id,
    first_name,
    last_name,
    email,
    salary
FROM employees
WHERE status = 'Activo';


-- 2. Promedio salarial por departamento

SELECT
    d.name AS department,
    AVG(e.salary) AS average_salary
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.id
GROUP BY d.name
ORDER BY average_salary DESC;


-- 3. Promedio de desempeño por departamento

SELECT
    d.name AS department,
    ROUND(AVG(e.performance_score), 2)
        AS average_performance
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.id
GROUP BY d.name
ORDER BY average_performance DESC;


-- 4. Empleados con muchas ausencias

SELECT
    first_name,
    last_name,
    absences
FROM employees
WHERE absences >= 5
ORDER BY absences DESC;


-- 5. Empleados que necesitan capacitación

SELECT
    first_name,
    last_name,
    training_hours,
    performance_score
FROM employees
WHERE training_hours < 10
AND performance_score < 70
ORDER BY performance_score ASC;