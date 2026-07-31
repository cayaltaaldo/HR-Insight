import pandas as pd

from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///./data/hr_insight.db"

engine = create_engine(
    DATABASE_URL
)


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

    df = pd.read_sql(
        query,
        engine
    )

    return df


def calculate_kpis(df):

    kpis = {

        "total_employees":
            len(df),

        "average_salary":
            round(df["salary"].mean(), 2),

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


if __name__ == "__main__":

    df = get_employees()

    print("\nDATOS CARGADOS:")
    print(df.head())

    print("\nTOTAL REGISTROS:")
    print(len(df))

    print("\nKPIs:")

    kpis = calculate_kpis(df)

    for name, value in kpis.items():

        print(
            f"{name}: {value}"
        )