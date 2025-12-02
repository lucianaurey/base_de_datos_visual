from sqlalchemy import create_engine, text
from faker import Faker   
import random
from datetime import datetime, timedelta

# ==========================================================
# CONFIGURACIÓN DE CONEXIÓN
# ==========================================================
DB_USER = "sql5809882"
DB_PASSWORD = "GPttLkDvVL"
DB_HOST = "sql5.freesqldatabase.com"
DB_NAME = "sql5809882"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

fake = Faker()


with engine.connect() as conn:


    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))



    tablas = [
        "detalle_factura", "detalle_pedido", "detalle_compra",
        "pedido_resena", "producto_restaurante", "producto_minimarket",
        "repartidor_pedido", "seguimiento_pedido", "empleado_pedido",
        "telefono_usuario", "telefono_empleado", "telefono_repartidor",
        "telefono_restaurante", "telefono_proveedor",
        "direccion_usuario", "direccion_empleado",
        "direccion_minimarket", "direccion_restaurante",
        "tipo_promocion", "resena", "alerta_pedido", "alerta", "vehiculo",
        "entrega", "seguimiento_entrega",
        "pago_unico", "factura", "pedido",
        "producto", "restaurante", "usuario",
        "empleado", "repartidor", "promocion", "inventario",
        "menu", "minimarket", "proveedor", "rol_usuario", "compra"
    ]

    for t in tablas:
        conn.execute(text(f"TRUNCATE TABLE {t}"))

    # ==========================================================
    # SECCIÓN 1: TABLAS BASE
    # ==========================================================

    # 1. Rol de usuario
    roles = ["cliente", "repartidor", "administrador", "empleado"]
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO rol_usuario 
            (cliente, repartidor, administrador, empleado, rol_usuariocol, nivel_fidelidad, calificacion, nivel, cargo, fecha_ingreso, horario)
            VALUES (:cliente, :repartidor, :administrador, :empleado, :rol, :fidelidad, :calif, :nivel, :cargo, :fecha, :horario)
        """), {
            "cliente": random.choice(["Sí", "No"]),
            "repartidor": random.choice(["Sí", "No"]),
            "administrador": random.choice(["Sí", "No"]),
            "empleado": random.choice(["Sí", "No"]),
            "rol": random.choice(roles),
            "fidelidad": random.choice(["Bronce", "Plata", "Oro"]),
            "calif": str(random.randint(1,5)),
            "nivel": str(random.randint(1,10)),
            "cargo": fake.job(),
            "fecha": fake.date_between(start_date="-3y", end_date="today"),
            "horario": f"{random.randint(6,10)}:00-{random.randint(15,22)}:00"
        })

    # 2. Proveedor
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO proveedor (contacto, correo_electronico, tipo_proveedor, nombre)
            VALUES (:contacto, :correo, :tipo, :nombre)
        """), {
            "contacto": fake.name(),
            "correo": fake.company_email(),
            "tipo": random.choice(["Alimentos","Bebidas","Limpieza","Tecnología"]),
            "nombre": fake.company()
        })

    # 3. Minimarket
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO minimarket (nombre, encargado)
            VALUES (:nombre, :encargado)
        """), {
            "nombre": f"MiniMarket {fake.word().capitalize()}",
            "encargado": fake.name()
        })

    # 4. Menú
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO menu (descripcion, fecha_actualizacion, nombre_menu, estado)
            VALUES (:desc, :fecha, :nombre, :estado)
        """), {
            "desc": fake.sentence(),
            "fecha": fake.date_this_year(),
            "nombre": f"Menu {fake.word().capitalize()}",
            "estado": random.choice(["activo","inactivo"])
        })

    # 5. Inventario
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO inventario (cantidad_disponible, fecha_actualizacion)
            VALUES (:cantidad, :fecha)
        """), {
            "cantidad": random.randint(5,500),
            "fecha": fake.date_this_year()
        })

    # 6. Promoción
    for _ in range(50):
        inicio = fake.date_between(start_date="-3m", end_date="today")
        fin = inicio + timedelta(days=random.randint(10,60))
        conn.execute(text("""
            INSERT INTO promocion (codigo, fecha_inicio, fecha_fin, valor, uso_maximo)
            VALUES (:codigo, :inicio, :fin, :valor, :uso)
        """), {
            "codigo": fake.bothify("PROMO-####"),
            "inicio": inicio,
            "fin": fin,
            "valor": round(random.uniform(5,50),2),
            "uso": str(random.randint(10,100))
        })

    # ==========================================================
    # SECCIÓN 2: USUARIOS, EMPLEADOS, REPARTIDORES, RESTAURANTES
    # ==========================================================

    # 7. Usuario
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, correo_electronico, id_rol_usuario)
            VALUES (:nombre,:ap_pat,:ap_mat,:correo,:rol)
        """), {
            "nombre": fake.first_name(),
            "ap_pat": fake.last_name(),
            "ap_mat": fake.last_name(),
            "correo": fake.email(),
            "rol": random.randint(1,50)
        })

    # 8. Repartidor
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO repartidor 
            (apellido_paterno, apellido_materno, nombre, fecha_prevista_entrega, control, disponibilidad)
            VALUES (:ap_pat,:ap_mat,:nombre,:fecha,:control,:disp)
        """), {
            "ap_pat": fake.last_name(),
            "ap_mat": fake.last_name(),
            "nombre": fake.first_name(),
            "fecha": fake.date_time_this_year(),
            "control": random.choice(["Activo","Inactivo"]),
            "disp": random.choice(["Disponible","Ocupado"])
        })

    # 9. Empleado
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO empleado (nombre, ci, apellido_paterno, apellido_materno, correo_electronico)
            VALUES (:nombre,:ci,:ap_pat,:ap_mat,:correo)
        """), {
            "nombre": fake.first_name(),
            "ci": fake.bothify("########"),
            "ap_pat": fake.last_name(),
            "ap_mat": fake.last_name(),
            "correo": fake.email()
        })

    # 10. Restaurante
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO restaurante (nombre, descripcion, horario_atencion, ruc, id_menu)
            VALUES (:nombre,:desc,:horario,:ruc,:menu)
        """), {
            "nombre": f"Restaurante {fake.word().capitalize()}",
            "desc": fake.sentence(),
            "horario": fake.date_this_year(),
            "ruc": fake.bothify("RUC-#####"),
            "menu": random.randint(1,50)
        })

    # ==========================================================
    # SECCIÓN 3: PRODUCTOS Y PEDIDOS
    # ==========================================================

    # 11. Producto
    fake_products = [
    "Hamburguesa Clásica", "Pizza Napolitana", "Pollo Frito", "Tacos al Pastor", 
    "Ensalada César", "Sopa de Verduras", "Lomo Saltado", "Pasta Alfredo",
    "Empanada", "Sandwich de Pollo", "Lasaña", "Arepa", "Salchipapas",
    "Ceviche", "Ramen", "Sushi Roll", "Café Americano", "Agua Mineral 2L", 
    "Gaseosa Cola 500ml", "Galletas Oreo", "Arroz 1kg", "Leche Entera",
    "Huevos (12 unidades)", "Café Instantáneo 200g", "Fideos Spaghetti 1kg",
    "Atún en Lata", "Chocolate Barra", "Papas Fritas Bolsa", "Yogurt Natural",
    "Aceite Vegetal 1L"
]

    for _ in range(50):
        conn.execute(text("""
            INSERT INTO producto (nombre, descripcion, stock_disponible, id_proveedor, id_inventario)
            VALUES (:nombre, :desc, :stock, :prov, :inv)
        """), {
            "nombre": random.choice(fake_products),
            "desc": fake.sentence(),
            "stock": random.randint(10, 100),
            "prov": random.randint(1, 50),
            "inv": random.randint(1, 50)
        })

    # 12. Pedido
    for _ in range(50):
        fecha = fake.date_between(start_date="-3m", end_date="today")
        conn.execute(text("""
            INSERT INTO pedido (fecha_pedido, metodo_entrega, costo_envio, fecha_prevista_entrega, id_usuario, id_promocion)
            VALUES (:fecha,:metodo,:costo,:entrega,:usuario,:promo)
        """), {
            "fecha": fecha,
            "metodo": random.choice(["Delivery","Recoger en tienda"]),
            "costo": round(random.uniform(1,10),2),
            "entrega": fecha + timedelta(days=random.randint(1,5)),
            "usuario": random.randint(1,50),
            "promo": random.randint(1,50)
        })

    # ==========================================================
    # SECCIÓN 4: FACTURACIÓN Y PAGOS
    # ==========================================================

    # 13. Factura
    for _ in range(50):
        conn.execute(text("INSERT INTO factura (cuf) VALUES (:cuf)"),
                      {"cuf": fake.bothify("CUF-#####")})

    # 14. Pago único
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO pago_unico 
            (fecha_pago, monto, nombre_banco, comprobante, numero_cuenta, cambio, tipo, numero_tarjeta, id_pedido)
            VALUES (:fecha,:monto,:banco,:comp,:cuenta,:cambio,:tipo,:tarjeta,:pedido)
        """), {
            "fecha": fake.date_this_year(),
            "monto": round(random.uniform(20,200),2),
            "banco": fake.company(),
            "comp": fake.uuid4(),
            "cuenta": fake.bban(),
            "cambio": round(random.uniform(0,5),2),
            "tipo": random.choice(["Débito","Crédito","Efectivo"]),
            "tarjeta": fake.credit_card_number(),
            "pedido": random.randint(1,50)
        })

    # Obtener IDs reales
    id_pagos = [r[0] for r in conn.execute(text("SELECT id_pago_unico FROM pago_unico"))]
    id_facturas = [r[0] for r in conn.execute(text("SELECT id_factura FROM factura"))]

    # 15. Detalle factura (CORREGIDO)
    for _ in range(50):
        cantidad = random.randint(1,10)
        precio = round(random.uniform(5,200),2)
        total = cantidad * precio

        conn.execute(text("""
            INSERT INTO detalle_factura 
            (nit, razon_social, fecha_emision, monto_total, cantidad, descripcion_producto, total, id_pago_unico, id_factura)
            VALUES (:nit,:razon,:fecha,:monto,:cantidad,:desc,:total,:pago,:factura)
        """), {
            "nit": fake.msisdn(),
            "razon": fake.company(),
            "fecha": fake.date_time_between(start_date="-1y", end_date="now"),
            "monto": total,
            "cantidad": cantidad,
            "desc": fake.sentence(),
            "total": total,
            "pago": random.choice(id_pagos),
            "factura": random.choice(id_facturas)
        })

    # ==========================================================
    # SECCIÓN 5: COMPRAS Y RELACIONES PRODUCTOS
    # ==========================================================

    # 16. Compra
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO compra (fecha, monto_total, id_proveedor)
            VALUES (:fecha,:monto,:prov)
        """), {
            "fecha": fake.date_between(start_date="-1y", end_date="today"),
            "monto": round(random.uniform(100,1000),2),
            "prov": random.randint(1,50)
        })

    # 17. Detalle compra
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO detalle_compra (id_compra, id_producto, cantidad, precio_unitario)
            VALUES (:compra,:prod,:cantidad,:precio)
        """), {
            "compra": random.randint(1,50),
            "prod": random.randint(1,50),
            "cantidad": random.randint(1,20),
            "precio": round(random.uniform(5,200),2)
        })

    # 18. Detalle pedido
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO detalle_pedido (precio_unitario, cantidad, id_pedido, id_producto)
            VALUES (:precio,:cantidad,:pedido,:producto)
        """), {
            "precio": round(random.uniform(5,50),2),
            "cantidad": random.randint(1,10),
            "pedido": random.randint(1,50),
            "producto": random.randint(1,50)
        })

    # 19. Producto-minimarket
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO producto_minimarket (id_producto,id_minimarket)
            VALUES (:p,:m)
        """), {
            "p": random.randint(1,50),
            "m": random.randint(1,50)
        })

    # 20. Producto-restaurante
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO producto_restaurante (id_producto,id_restaurante)
            VALUES (:p,:r)
        """), {
            "p": random.randint(1,50),
            "r": random.randint(1,50)
        })

    # ==========================================================
    # SECCIÓN 6: ENTREGA, SEGUIMIENTOS Y ASIGNACIONES
    # ==========================================================

    # 21. Seguimiento entrega
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO seguimiento_entrega (longitud, direccion, velocidad, ts_timestamp)
            VALUES (:long,:dir,:vel,:ts)
        """), {
            "long": round(random.uniform(-68.1,-67.9),6),
            "dir": fake.street_address(),
            "vel": random.randint(10,100),
            "ts": datetime.now()
        })

    # 22. Entrega
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO entrega 
            (tipo_proveedor, fecha_asignacion, fecha_aceptacion, id_seguimiento_entrega, id_repartidor)
            VALUES (:tipo,:asig,:acep,:seg,:rep)
        """), {
            "tipo": random.choice(["Restaurante","Minimarket","Proveedor"]),
            "asig": fake.date_this_year(),
            "acep": fake.date_this_year(),
            "seg": random.randint(1,50),
            "rep": random.randint(1,50)
        })

    # 23. Repartidor-pedido
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO repartidor_pedido (id_repartidor, pedido_id_pedido, nombre, ubicacion_repartidor)
            VALUES (:rep,:ped,:nom,:ubi)
        """), {
            "rep": random.randint(1,50),
            "ped": random.randint(1,50),
            "nom": fake.name(),
            "ubi": fake.address()
        })

    # 24. Seguimiento pedido
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO seguimiento_pedido (tiempo_estimado,hora_llegada,estado,id_repartidor_pedido)
            VALUES (:t,:l,:e,:rp)
        """), {
            "t": fake.date_this_year(),
            "l": fake.date_this_year(),
            "e": random.choice(["En camino","Entregado","Cancelado"]),
            "rp": random.randint(1,50)
        })

    # ==========================================================
    # SECCIÓN 7: EMPLEADO, SOPORTE, TELÉFONOS, DIRECCIONES
    # ==========================================================

    # 25. Empleado-pedido
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO empleado_pedido (id_empleado,id_pedido,fecha_registro,fecha_entrega)
            VALUES (:e,:p,:r,:f)
        """), {
            "e": random.randint(1,50),
            "p": random.randint(1,50),
            "r": fake.date_this_year(),
            "f": fake.date_this_year()
        })

    # 26. Soporte chat
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO soporte_chat (fecha_inicio,tipo_chat,estado,fecha_cierre,usuario_id_usuario)
            VALUES (:ini,:tipo,:est,:fin,:u)
        """), {
            "ini": fake.date_this_year(),
            "tipo": random.choice(["soporte_repartidor","soporte_cliente","soporte_restaurante"]),
            "est": random.choice(["Abierto","Cerrado"]),
            "fin": fake.date_this_year(),
            "u": random.randint(1,50)
        })

    # 27. Teléfonos
    for _ in range(50):
        conn.execute(text("INSERT INTO telefono_usuario (numero_telefono,id_usuario) VALUES (:t,:i)"),
                     {"t": fake.phone_number(), "i": random.randint(1,50)})

        conn.execute(text("INSERT INTO telefono_empleado (numero_telefono,id_empleado) VALUES (:t,:i)"),
                     {"t": fake.phone_number(), "i": random.randint(1,50)})

        conn.execute(text("INSERT INTO telefono_repartidor (numero_telefono,id_repartidor) VALUES (:t,:i)"),
                     {"t": fake.phone_number(), "i": random.randint(1,50)})

        conn.execute(text("INSERT INTO telefono_restaurante (numero_telefono,id_restaurante) VALUES (:t,:i)"),
                     {"t": fake.phone_number(), "i": random.randint(1,50)})

        conn.execute(text("INSERT INTO telefono_proveedor (numero_telefono,id_proveedor) VALUES (:t,:i)"),
                     {"t": fake.phone_number(), "i": random.randint(1,50)})

    # 28. Direcciones
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO direccion_usuario (ciudad,numero,calle,zona,id_usuario)
            VALUES (:c,:n,:cl,:z,:id)
        """), {
            "c": fake.city(),
            "n": str(random.randint(1,999)),
            "cl": fake.street_name(),
            "z": fake.word(),
            "id": random.randint(1,50)
        })

        conn.execute(text("""
            INSERT INTO direccion_empleado (ciudad,numero,calle,zona,id_empleado)
            VALUES (:c,:n,:cl,:z,:id)
        """), {
            "c": fake.city(),
            "n": str(random.randint(1,999)),
            "cl": fake.street_name(),
            "z": fake.word(),
            "id": random.randint(1,50)
        })

        conn.execute(text("""
            INSERT INTO direccion_minimarket (ciudad,numero,calle,zona,id_minimarket)
            VALUES (:c,:n,:cl,:z,:id)
        """), {
            "c": fake.city(),
            "n": str(random.randint(1,999)),
            "cl": fake.street_name(),
            "z": fake.word(),
            "id": random.randint(1,50)
        })

        conn.execute(text("""
            INSERT INTO direccion_restaurante (ciudad,numero,calle,zona,id_restaurante)
            VALUES (:c,:n,:cl,:z,:id)
        """), {
            "c": fake.city(),
            "n": str(random.randint(1,999)),
            "cl": fake.street_name(),
            "z": fake.word(),
            "id": random.randint(1,50)
        })

    # ==========================================================
    # SECCIÓN 8: PROMOCIONES Y RESEÑAS
    # ==========================================================

    # 29. Tipo promoción
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO tipo_promocion (nombre,descripcion,id_promocion)
            VALUES (:n,:d,:p)
        """), {
            "n": f"Tipo {fake.word().capitalize()}",
            "d": fake.sentence(),
            "p": random.randint(1,50)
        })

    # 30. Reseñas
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO resena (descripcion,comentario,horario_atencion,calificacion)
            VALUES (:d,:c,:h,:k)
        """), {
            "d": fake.sentence(),
            "c": fake.text(max_nb_chars=100),
            "h": fake.date_time_this_year(),
            "k": str(random.randint(1,5))
        })

    # 31. Pedido - reseña
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO pedido_resena (id_pedido,id_resena)
            VALUES (:p,:r)
        """), {
            "p": random.randint(1,50),
            "r": random.randint(1,50)
        })

    # ==========================================================
    # SECCIÓN 9: VEHÍCULOS Y ALERTAS
    # ==========================================================

    # 32. Vehículo
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO vehiculo (tipo,placa,marca,id_repartidor)
            VALUES (:t,:pl,:m,:r)
        """), {
            "t": random.choice(["Moto","Auto","Bicicleta"]),
            "pl": fake.bothify("???-####"),
            "m": random.choice(["Toyota","Nissan","Suzuki","Honda"]),
            "r": random.randint(1,50)
        })

    # 33. Alerta
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO alerta (tiempo_estimado,hora_llegada,confirmacion_pedido)
            VALUES (:t,:h,:c)
        """), {
            "t": fake.time(),
            "h": fake.time(),
            "c": random.choice(["Sí","No"])
        })

    # 34. Alerta - pedido
    for _ in range(50):
        conn.execute(text("""
            INSERT INTO alerta_pedido (fecha_registro,id_alerta,id_pedido)
            VALUES (:f,:a,:p)
        """), {
            "f": fake.date_this_year(),
            "a": random.randint(1,50),
            "p": random.randint(1,50)
        })

    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    conn.commit()

    print("✅ SCRIPT COMPLETADO: 41 TABLAS POBLADAS CORRECTAMENTE")
