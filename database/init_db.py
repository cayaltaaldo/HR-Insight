from database.connection import engine, Base

from database.models import (
    Department,
    Employee,
    Training,
    Attendance
)


def init_database():

    print("Creando base de datos...")

    Base.metadata.create_all(
        bind=engine
    )

    print("Base de datos creada correctamente.")


if __name__ == "__main__":
    init_database()