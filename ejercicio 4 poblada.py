from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime, timedelta

# ===============================
# Conexión
# ===============================
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "ejercicio4"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
fake = Faker("es_ES")

# ===============================
# Poblar tablas con SQL puro
# ===============================
with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    tablas = [
        "reserva",
        "direccion_cliente",
        "telefono_cliente",
        "cliente",
        "mesa",
        "estado_reserva",
        "metodo_pago"
    ]
    for t in tablas:
        conn.execute(text(f"TRUNCATE TABLE {t}"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    # -------------------------------
    # CLIENTES
    # -------------------------------
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO cliente (nombre_cliente, codigo_cliente, email)
            VALUES (:nombre, :codigo, :email)
        """), {
            "nombre": fake.name(),
            "codigo": f"C-{fake.unique.random_int(min=1000, max=9999)}",
            "email": fake.email()
        })

    # -------------------------------
    # TELÉFONOS DE CLIENTES
    # -------------------------------
    for id_cliente in range(1, 51):
        for _ in range(random.randint(1, 2)):
            conn.execute(text("""
                INSERT INTO telefono_cliente (telefono, id_cliente)
                VALUES (:telefono, :id_cliente)
            """), {
                "telefono": fake.phone_number(),
                "id_cliente": id_cliente
            })

    # -------------------------------
    # DIRECCIONES DE CLIENTES
    # -------------------------------
    for id_cliente in range(1, 51):
        conn.execute(text("""
            INSERT INTO direccion_cliente (ciudad, zona, calle, id_cliente)
            VALUES (:ciudad, :zona, :calle, :id_cliente)
        """), {
            "ciudad": fake.city(),
            "zona": fake.word(),
            "calle": fake.street_name(),
            "id_cliente": id_cliente
        })

    # -------------------------------
    # MESAS
    # -------------------------------
    for i in range(1, 51):
        conn.execute(text("""
            INSERT INTO mesa (numero_mesa, capacidad)
            VALUES (:numero, :capacidad)
        """), {
            "numero": f"M-{i}",
            "capacidad": random.choice([2, 4, 6, 8])
        })

    # -------------------------------
    # ESTADOS DE RESERVA
    # -------------------------------
    estados = ["Pendiente", "Confirmada", "Cancelada", "Completada"]
    for estado in estados:
        conn.execute(text("""
            INSERT INTO estado_reserva (nombre_estado_reserva)
            VALUES (:estado)
        """), {"estado": estado})

    # -------------------------------
    # MÉTODOS DE PAGO
    # -------------------------------
    metodos = ["Efectivo", "Tarjeta", "Transferencia", "Código QR"]
    for metodo in metodos:
        conn.execute(text("""
            INSERT INTO metodo_pago (tipo_pago)
            VALUES (:metodo)
        """), {"metodo": metodo})

    # -------------------------------
    # RESERVAS
    # -------------------------------
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO reserva (hora, fecha_reservacion, cantidad_personas, id_cliente, id_mesa, id_estado_reserva)
            VALUES (:hora, :fecha, :cantidad, :cliente, :mesa, :estado)
        """), {
            "hora": fake.time(pattern="%H:%M:%S"),
            "fecha": fake.date_between(start_date="-1y", end_date="+1y"),
            "cantidad": random.choice([2, 3, 4, 5, 6]),
            "cliente": random.randint(1, 20),
            "mesa": random.randint(1, 10),
            "estado": random.randint(1, len(estados))
        })

    conn.commit()

print("✅ Datos insertados correctamente en la base de datos 'ejercicio4'")
