from io import BytesIO

import pandas as pd


def generate_excel_report(
    employees_df,
    training_df,
    absenteeism_df,
    alerts,
    department_name
):
    """
    Genera un reporte Excel completo de Recursos Humanos.

    Retorna:
        BytesIO: archivo Excel listo para descargar.
    """

    output = BytesIO()

    # ============================================
    # PREPARAR DATOS
    # ============================================

    total_employees = len(employees_df)

    average_salary = (
        employees_df["salary"].mean()
        if not employees_df.empty
        else 0
    )

    average_performance = (
        employees_df["performance_score"].mean()
        if not employees_df.empty
        else 0
    )

    average_training = (
        employees_df["training_hours"].mean()
        if not employees_df.empty
        else 0
    )

    total_absences = (
        employees_df["absences"].sum()
        if not employees_df.empty
        else 0
    )

    # ============================================
    # RESUMEN
    # ============================================

    summary_df = pd.DataFrame({
        "Indicador": [
            "Departamento",
            "Total de empleados",
            "Sueldo promedio",
            "Desempeño promedio",
            "Horas promedio de capacitación",
            "Total de ausencias",
            "Empleados que necesitan capacitación",
            "Empleados con alto ausentismo",
            "Alertas generadas"
        ],
        "Valor": [
            department_name,
            total_employees,
            round(average_salary, 2),
            round(average_performance, 2),
            round(average_training, 2),
            int(total_absences),
            len(training_df),
            len(absenteeism_df),
            len(alerts)
        ]
    })

    # ============================================
    # ALERTAS
    # ============================================

    if alerts:

        alerts_df = pd.DataFrame([
            {
                "Nivel": alert["level"],
                "Título": alert["title"],
                "Mensaje": alert["message"],
                "Cantidad": alert["count"]
            }
            for alert in alerts
        ])

    else:

        alerts_df = pd.DataFrame({
            "Nivel": [],
            "Título": [],
            "Mensaje": [],
            "Cantidad": []
        })

    # ============================================
    # GENERAR EXCEL
    # ============================================

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # ----------------------------------------
        # RESUMEN
        # ----------------------------------------

        summary_df.to_excel(
            writer,
            sheet_name="Resumen",
            index=False
        )

        # ----------------------------------------
        # EMPLEADOS
        # ----------------------------------------

        employees_df.to_excel(
            writer,
            sheet_name="Empleados",
            index=False
        )

        # ----------------------------------------
        # CAPACITACIÓN
        # ----------------------------------------

        training_df.to_excel(
            writer,
            sheet_name="Capacitación",
            index=False
        )

        # ----------------------------------------
        # AUSENTISMO
        # ----------------------------------------

        absenteeism_df.to_excel(
            writer,
            sheet_name="Ausentismo",
            index=False
        )

        # ----------------------------------------
        # ALERTAS
        # ----------------------------------------

        alerts_df.to_excel(
            writer,
            sheet_name="Alertas",
            index=False
        )

        # ========================================
        # FORMATO DE COLUMNAS
        # ========================================

        for worksheet in writer.book.worksheets:

            for column in worksheet.columns:

                max_length = 0

                column_letter = column[0].column_letter

                for cell in column:

                    try:

                        if cell.value is not None:

                            max_length = max(
                                max_length,
                                len(str(cell.value))
                            )

                    except Exception:

                        pass

                worksheet.column_dimensions[
                    column_letter
                ].width = min(
                    max_length + 2,
                    50
                )

            # Congelar primera fila

            worksheet.freeze_panes = "A2"

    output.seek(0)

    return output