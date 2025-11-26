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
DB_NAME = "alimentos"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
fake = Faker()


with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

    tablas = [
        "alerta_pedido", "alerta", "pedido_resena", "resena",
        "tipo_promocion", "direccion_restaurante", "direccion_minimarket",
        "direccion_empleado", "direccion_usuario", "telefono_proveedor",
        "telefono_restaurante", "telefono_repartidor", "telefono_empleado",
        "telefono_usuario", "soporte_chat", "empleado_pedido",
        "seguimiento_pedido", "repartidor_pedido", "entrega",
        "seguimiento_entrega", "detalle_compra", "detalle_pedido",
        "producto_restaurante", "producto_minimarket", "vehiculo",
        "factura", "pago_unico", "pedido", "producto", "restaurante",
        "empleado", "repartidor", "usuario", "promocion", "inventario",
        "menu", "minimarket", "proveedor", "rol_usuario", "compra"
    ]

    for t in tablas:
        conn.execute(text(f"TRUNCATE TABLE {t}"))

    # ==========================================================
    # 1. Rol de usuario (50)
    # ==========================================================
    roles = ["cliente", "repartidor", "administrador", "empleado"]
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO rol_usuario (cliente, repartidor, administrador, empleado, rol_usuariocol, nivel_fidelidad, calificacion, nivel, cargo, fecha_ingreso, horario)
            VALUES (:cliente, :repartidor, :administrador, :empleado, :rol, :fidelidad, :calif, :nivel, :cargo, :fecha, :horario)
        """), {
            "cliente": random.choice(["Sí", "No"]),
            "repartidor": random.choice(["Sí", "No"]),
            "administrador": random.choice(["Sí", "No"]),
            "empleado": random.choice(["Sí", "No"]),
            "rol": random.choice(roles),
            "fidelidad": random.choice(["Bronce", "Plata", "Oro"]),
            "calif": str(random.randint(1, 5)),
            "nivel": str(random.randint(1, 10)),
            "cargo": fake.job(),
            "fecha": fake.date_between(start_date="-3y", end_date="today").strftime("%Y-%m-%d"),
            "horario": f"{random.randint(6, 10)}:00-{random.randint(15, 22)}:00"
        })

    # ==========================================================
    # 2. Proveedor (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO proveedor (contacto, correo_electronico, tipo_proveedor, nombre)
            VALUES (:contacto, :correo, :tipo, :nombre)
        """), {
            "contacto": fake.name(),
            "correo": fake.company_email(),
            "tipo": random.choice(["Alimentos", "Bebidas", "Limpieza", "Tecnología"]),
            "nombre": fake.company()
        })

    # ==========================================================
    # 3. Minimarket (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO minimarket (nombre, encargado)
            VALUES (:nombre, :encargado)
        """), {
            "nombre": f"MiniMarket {fake.word().capitalize()}",
            "encargado": fake.name()
        })

    # ==========================================================
    # 4. Menú (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO menu (descripcion, fecha_actualizacion, nombre_menu, estado)
            VALUES (:desc, :fecha, :nombre, :estado)
        """), {
            "desc": fake.sentence(),
            "fecha": fake.date_this_year(),
            "nombre": f"Menú {fake.word().capitalize()}",
            "estado": random.choice(["activo", "inactivo"])
        })

    # ==========================================================
    # 5. Inventario (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO inventario (cantidad_disponible, fecha_actualizacion)
            VALUES (:cantidad, :fecha)
        """), {
            "cantidad": random.randint(5, 500),
            "fecha": fake.date_this_year()
        })

    # ==========================================================
    # 6. Promociones (50)
    # ==========================================================
    for _ in range(50):
        inicio = fake.date_between(start_date="-3m", end_date="today")
        fin = inicio + timedelta(days=random.randint(10, 60))
        conn.execute(text("""
            INSERT INTO promocion (codigo, fecha_inicio, fecha_fin, valor, uso_maximo)
            VALUES (:codigo, :inicio, :fin, :valor, :uso)
        """), {
            "codigo": fake.bothify("PROMO-####"),
            "inicio": inicio,
            "fin": fin,
            "valor": round(random.uniform(5, 50), 2),
            "uso": str(random.randint(10, 100))
        })

    # ==========================================================
    # 7. Usuario (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, correo_electronico, id_rol_usuario)
            VALUES (:nombre, :ap_pat, :ap_mat, :correo, :rol)
        """), {
            "nombre": fake.first_name(),
            "ap_pat": fake.last_name(),
            "ap_mat": fake.last_name(),
            "correo": fake.email(),
            "rol": random.randint(1, 50)
        })

    # ==========================================================
    # 8. Repartidor (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO repartidor (apellido_paterno, apellido_materno, nombre, fecha_prevista_entrega, control, disponibilidad)
            VALUES (:ap_pat, :ap_mat, :nombre, :fecha, :control, :disp)
        """), {
            "ap_pat": fake.last_name(),
            "ap_mat": fake.last_name(),
            "nombre": fake.first_name(),
            "fecha": fake.date_time_this_year(),
            "control": random.choice(["Activo", "Inactivo"]),
            "disp": random.choice(["Disponible", "Ocupado"])
        })

    # ==========================================================
    # 9. Empleado (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO empleado (nombre, ci, apellido_paterno, apellido_materno, correo_electronico)
            VALUES (:nombre, :ci, :ap_pat, :ap_mat, :correo)
        """), {
            "nombre": fake.first_name(),
            "ci": fake.bothify("########"),
            "ap_pat": fake.last_name(),
            "ap_mat": fake.last_name(),
            "correo": fake.email()
        })

    # ==========================================================
    # 10. Restaurante (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO restaurante (nombre, descripcion, horario_atencion, ruc, id_menu)
            VALUES (:nombre, :desc, :horario, :ruc, :menu)
        """), {
            "nombre": f"Restaurante {fake.word().capitalize()}",
            "desc": fake.sentence(),
            "horario": fake.date_this_year(),
            "ruc": fake.bothify("RUC-#####"),
            "menu": random.randint(1, 50)
        })

    # ==========================================================
    # 11. Producto (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO producto (nombre, descripcion, stock_disponible, id_proveedor, id_inventario)
            VALUES (:nombre, :desc, :stock, :prov, :inv)
        """), {
            "nombre": fake.word().capitalize(),
            "desc": fake.sentence(),
            "stock": random.randint(10, 100),
            "prov": random.randint(1, 50),
            "inv": random.randint(1, 50)
        })

    # ==========================================================
    # 12. Pedido (50)
    # ==========================================================
    for _ in range(50):
        fecha = fake.date_between(start_date="-3m", end_date="today")
        conn.execute(text("""
            INSERT INTO pedido (fecha_pedido, metodo_entrega, costo_envio, fecha_prevista_entrega, id_usuario, id_promocion)
            VALUES (:fecha, :metodo, :costo, :fecha_entrega, :usuario, :promo)
        """), {
            "fecha": fecha,
            "metodo": random.choice(["Delivery", "Recoger en tienda"]),
            "costo": round(random.uniform(1, 10), 2),
            "fecha_entrega": fecha + timedelta(days=random.randint(1, 5)),
            "usuario": random.randint(1, 50),
            "promo": random.randint(1, 50)
        })

    # ==========================================================
    # 13. Factura (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO factura (cuf)
            VALUES (:cuf)
        """), {"cuf": fake.bothify("CUF-#####")})

    # ==========================================================
    # 14. Pago único (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO pago_unico (fecha_pago, monto, nombre_banco, comprobante, numero_cuenta, cambio, tipo, numero_tarjeta, id_pedido)
            VALUES (:fecha, :monto, :banco, :comp, :cuenta, :cambio, :tipo, :tarjeta, :pedido)
        """), {
            "fecha": fake.date_this_year(),
            "monto": round(random.uniform(20, 200), 2),
            "banco": fake.company(),
            "comp": fake.uuid4(),
            "cuenta": fake.bban(),
            "cambio": round(random.uniform(0, 5), 2),
            "tipo": random.choice(["Débito", "Crédito", "Efectivo"]),
            "tarjeta": fake.credit_card_number(),
            "pedido": random.randint(1, 50)
        })

    # ==========================================================
    # 15. Compra (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO compra (fecha, monto_total, id_proveedor)
            VALUES (:fecha, :monto, :prov)
        """), {
            "fecha": fake.date_between(start_date="-1y", end_date="today"),
            "monto": round(random.uniform(100, 1000), 2),
            "prov": random.randint(1, 50)
        })


    # ==========================================================
    # 1. Detalle de compra (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO detalle_compra (id_compra, id_producto, cantidad, precio_unitario)
            VALUES (:compra, :producto, :cantidad, :precio)
        """), {
            "compra": random.randint(1, 50),
            "producto": random.randint(1, 50),
            "cantidad": random.randint(1, 20),
            "precio": round(random.uniform(5, 200), 2)
        })

    # ==========================================================
    # 2. Detalle de pedido (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO detalle_pedido (precio_unitario, cantidad, id_pedido, id_producto)
            VALUES (:precio, :cantidad, :pedido, :producto)
        """), {
            "precio": round(random.uniform(5, 50), 2),
            "cantidad": random.randint(1, 10),
            "pedido": random.randint(1, 50),
            "producto": random.randint(1, 50)
        })

    # ==========================================================
    # 3. Producto - minimarket (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO producto_minimarket (id_producto, id_minimarket)
            VALUES (:producto, :minimarket)
        """), {
            "producto": random.randint(1, 50),
            "minimarket": random.randint(1, 50)
        })

    # ==========================================================
    # 4. Producto - restaurante (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO producto_restaurante (id_producto, id_restaurante)
            VALUES (:producto, :restaurante)
        """), {
            "producto": random.randint(1, 50),
            "restaurante": random.randint(1, 50)
        })

    # ==========================================================
    # 5. Seguimiento entrega (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO seguimiento_entrega (longitud, direccion, velocidad, ts_timestamp)
            VALUES (:longitud, :direccion, :velocidad, :timestamp)
        """), {
            "longitud": round(random.uniform(-68.1, -67.9), 6),
            "direccion": fake.street_address(),
            "velocidad": random.randint(10, 100),
            "timestamp": datetime.now()
        })

    # ==========================================================
    # 6. Entrega (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO entrega (tipo_proveedor, fecha_asignacion, fecha_aceptacion, id_seguimiento_entrega, id_repartidor)
            VALUES (:tipo, :asignacion, :aceptacion, :seguimiento, :repartidor)
        """), {
            "tipo": random.choice(["Restaurante", "Minimarket", "Proveedor"]),
            "asignacion": fake.date_this_year(),
            "aceptacion": fake.date_this_year(),
            "seguimiento": random.randint(1, 50),
            "repartidor": random.randint(1, 50)
        })

    # ==========================================================
    # 7. Repartidor - pedido (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO repartidor_pedido (id_repartidor, pedido_id_pedido, nombre, ubicacion_repartidor)
            VALUES (:repartidor, :pedido, :nombre, :ubicacion)
        """), {
            "repartidor": random.randint(1, 50),
            "pedido": random.randint(1, 50),
            "nombre": fake.name(),
            "ubicacion": fake.address()
        })

    # ==========================================================
    # 8. Seguimiento de pedido (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO seguimiento_pedido (tiempo_estimado, hora_llegada, estado, id_repartidor_pedido)
            VALUES (:tiempo, :llegada, :estado, :rep_pedido)
        """), {
            "tiempo": fake.date_this_year(),
            "llegada": fake.date_this_year(),
            "estado": random.choice(["En camino", "Entregado", "Cancelado"]),
            "rep_pedido": random.randint(1, 50)
        })

    # ==========================================================
    # 9. Empleado - pedido (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO empleado_pedido (id_empleado, id_pedido, fecha_registro, fecha_entrega)
            VALUES (:empleado, :pedido, :registro, :entrega)
        """), {
            "empleado": random.randint(1, 50),
            "pedido": random.randint(1, 50),
            "registro": fake.date_this_year(),
            "entrega": fake.date_this_year()
        })

    # ==========================================================
    # 10. Soporte chat (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO soporte_chat (fecha_inicio, tipo_chat, estado, fecha_cierre, usuario_id_usuario)
            VALUES (:inicio, :tipo, :estado, :cierre, :usuario)
        """), {
            "inicio": fake.date_this_year(),
            "tipo": random.choice(['soporte_repartidor', 'soporte_cliente', 'soporte_restaurante']),
            "estado": random.choice(["Abierto", "Cerrado"]),
            "cierre": fake.date_this_year(),
            "usuario": random.randint(1, 50)
        })

    # ==========================================================
    # 11. Teléfonos (50 por tipo)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("INSERT INTO telefono_usuario (numero_telefono, id_usuario) VALUES (:tel, :id)"),
                     {"tel": fake.phone_number(), "id": random.randint(1, 50)})
        conn.execute(text("INSERT INTO telefono_empleado (numero_telefono, id_empleado) VALUES (:tel, :id)"),
                     {"tel": fake.phone_number(), "id": random.randint(1, 50)})
        conn.execute(text("INSERT INTO telefono_repartidor (numero_telefono, id_repartidor) VALUES (:tel, :id)"),
                     {"tel": fake.phone_number(), "id": random.randint(1, 50)})
        conn.execute(text("INSERT INTO telefono_restaurante (numero_telefono, id_restaurante) VALUES (:tel, :id)"),
                     {"tel": fake.phone_number(), "id": random.randint(1, 50)})
        conn.execute(text("INSERT INTO telefono_proveedor (numero_telefono, id_proveedor) VALUES (:tel, :id)"),
                     {"tel": fake.phone_number(), "id": random.randint(1, 50)})

    # ==========================================================
    # 12. Direcciones (50 por tipo)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO direccion_usuario (ciudad, numero, calle, zona, id_usuario)
            VALUES (:ciudad, :num, :calle, :zona, :id)
        """), {
            "ciudad": fake.city(),
            "num": str(random.randint(1, 999)),
            "calle": fake.street_name(),
            "zona": fake.word(),
            "id": random.randint(1, 50)
        })
        conn.execute(text("""
            INSERT INTO direccion_empleado (ciudad, numero, calle, zona, id_empleado)
            VALUES (:ciudad, :num, :calle, :zona, :id)
        """), {
            "ciudad": fake.city(),
            "num": str(random.randint(1, 999)),
            "calle": fake.street_name(),
            "zona": fake.word(),
            "id": random.randint(1, 50)
        })
        conn.execute(text("""
            INSERT INTO direccion_minimarket (ciudad, numero, calle, zona, id_minimarket)
            VALUES (:ciudad, :num, :calle, :zona, :id)
        """), {
            "ciudad": fake.city(),
            "num": str(random.randint(1, 999)),
            "calle": fake.street_name(),
            "zona": fake.word(),
            "id": random.randint(1, 50)
        })
        conn.execute(text("""
            INSERT INTO direccion_restaurante (ciudad, numero, calle, zona, id_restaurante)
            VALUES (:ciudad, :num, :calle, :zona, :id)
        """), {
            "ciudad": fake.city(),
            "num": str(random.randint(1, 999)),
            "calle": fake.street_name(),
            "zona": fake.word(),
            "id": random.randint(1, 50)
        })

    # ==========================================================
    # 13. Tipo de promoción (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO tipo_promocion (nombre, descripcion, id_promocion)
            VALUES (:nombre, :desc, :promo)
        """), {
            "nombre": f"Tipo {fake.word().capitalize()}",
            "desc": fake.sentence(),
            "promo": random.randint(1, 50)
        })

    # ==========================================================
    # 14. Reseñas (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO resena (descripcion, comentario, horario_atencion, calificacion)
            VALUES (:desc, :coment, :horario, :calif)
        """), {
            "desc": fake.sentence(),
            "coment": fake.text(max_nb_chars=100),
            "horario": fake.date_time_this_year(),
            "calif": str(random.randint(1, 5))
        })

    # ==========================================================
    # 15. Pedido - reseña (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO pedido_resena (id_pedido, id_resena)
            VALUES (:pedido, :resena)
        """), {
            "pedido": random.randint(1, 50),
            "resena": random.randint(1, 50)
        })

    # ==========================================================
    # 16. Vehículo (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO vehiculo (tipo, placa, marca, id_repartidor)
            VALUES (:tipo, :placa, :marca, :repartidor)
        """), {
            "tipo": random.choice(["Moto", "Auto", "Bicicleta"]),
            "placa": fake.bothify("???-####"),
            "marca": random.choice(["Toyota", "Nissan", "Suzuki", "Honda"]),
            "repartidor": random.randint(1, 50)
        })

    # ==========================================================
    # 17. Alerta (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO alerta (tiempo_estimado, hora_llegada, confirmacion_pedido)
            VALUES (:tiempo, :hora, :confirm)
        """), {
            "tiempo": fake.time(),
            "hora": fake.time(),
            "confirm": random.choice(["Sí", "No"])
        })

    # ==========================================================
    # 18. Alerta - pedido (50)
    # ==========================================================
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO alerta_pedido (fecha_registro, id_alerta, id_pedido)
            VALUES (:fecha, :alerta, :pedido)
        """), {
            "fecha": fake.date_this_year(),
            "alerta": random.randint(1, 50),
            "pedido": random.randint(1, 50)
        })

        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    conn.commit()
print("✅ completada:.")

