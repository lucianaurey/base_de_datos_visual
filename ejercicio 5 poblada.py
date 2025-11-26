from sqlalchemy import create_engine, text
from faker import Faker
import random

# ===============================
# Conexión
# ===============================
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "ejercicio5"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
fake = Faker()

# ===============================
# Inserciones con SQL puro
# ===============================
with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    tablas = [
        "detalle_compra",
        "inventario",
        "producto",
        "compra",
        "direccion_proveedor",
        "telefono_proveedor",
        "proveedor",
        "estado",
        "categoria"
    ]
    for t in tablas:
        conn.execute(text(f"TRUNCATE TABLE {t}"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    # ===============================
    # Categorías
    # ===============================
    categorias = [
        "Bebidas", "Snacks", "Lácteos", "Carnes", "Frutas", "Verduras", "Limpieza",
        "Higiene", "Tecnología", "Panadería", "Cereales", "Embutidos", "Condimentos",
        "Congelados", "Pescados"
    ]
    for nombre in categorias:
        conn.execute(text("""
            INSERT INTO categoria (nombre_categoria)
            VALUES (:nombre)
        """), {"nombre": nombre})

    # ===============================
    # Estados de producto
    # ===============================
    estados = ["Disponible", "Agotado", "Descontinuado"]
    for nombre in estados:
        conn.execute(text("""
            INSERT INTO estado (nombre_estado)
            VALUES (:nombre)
        """), {"nombre": nombre})

    # ===============================
    # Proveedores (50)
    # ===============================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO proveedor (nombre_proveedor)
            VALUES (:nombre)
        """), {"nombre": fake.company()})

    # ===============================
    # Teléfonos de proveedores
    # ===============================
    for id_proveedor in range(1, 51):
        for _ in range(random.randint(1, 2)):
            conn.execute(text("""
                INSERT INTO telefono_proveedor (telefono, id_proveedor)
                VALUES (:telefono, :id_proveedor)
            """), {
                "telefono": fake.phone_number(),
                "id_proveedor": id_proveedor
            })

    # ===============================
    # Direcciones de proveedores
    # ===============================
    for id_proveedor in range(1, 51):
        conn.execute(text("""
            INSERT INTO direccion_proveedor (ciudad, zona, calle, id_proveedor)
            VALUES (:ciudad, :zona, :calle, :id_proveedor)
        """), {
            "ciudad": fake.city(),
            "zona": fake.street_name(),
            "calle": fake.street_address(),
            "id_proveedor": id_proveedor
        })

    # ===============================
    # Productos (50)
    # ===============================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO producto (codigo_producto, nombre_producto, precio_venta, id_categoria, id_estado)
            VALUES (:codigo, :nombre, :precio, :categoria, :estado)
        """), {
            "codigo": fake.bothify(text="PRD-####"),
            "nombre": fake.word().capitalize(),
            "precio": round(random.uniform(10, 500), 2),
            "categoria": random.randint(1, len(categorias)),
            "estado": random.randint(1, len(estados))
        })

    # ===============================
    # Inventario (50)
    # ===============================
    for id_producto in range(1, 51):
        conn.execute(text("""
            INSERT INTO inventario (cantidad_disponible, ultima_actualizacion, id_producto)
            VALUES (:cantidad, :fecha, :id_producto)
        """), {
            "cantidad": random.randint(0, 100),
            "fecha": fake.date_this_year(),
            "id_producto": id_producto
        })

    # ===============================
    # Compras (50)
    # ===============================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO compra (fecha_compra, id_proveedor)
            VALUES (:fecha, :id_proveedor)
        """), {
            "fecha": fake.date_between(start_date="-2y", end_date="today"),
            "id_proveedor": random.randint(1, 50)
        })

    # ===============================
    # Detalle de compra
    # ===============================
    for id_compra in range(1, 51):
        for _ in range(random.randint(2, 5)):
            conn.execute(text("""
                INSERT INTO detalle_compra (cantidad_comprada, precio_compra, id_compra, id_producto)
                VALUES (:cantidad, :precio, :id_compra, :id_producto)
            """), {
                "cantidad": random.randint(1, 50),
                "precio": round(random.uniform(5, 300), 2),
                "id_compra": id_compra,
                "id_producto": random.randint(1, 50)
            })

    conn.commit()

print("✅ Base de datos 'ejercicio5' poblada correctamente con 50 registros por tabla principal.")
