import random
from datetime import datetime

from sqlalchemy import create_engine, text

from faker import Faker

#####
# Conexion a la base de datos
#####

DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'blog_univalles'
DB_HOST = 'localhost'

engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
fake = Faker()
## introducri registros en la tabla persona con 50 registros

with engine.connect() as conn:
    for _ in range(50):
        conn.execute(text('''
           INSERT INTO persona (nombre, apellido_paterno,apellido_materno,  fecha)
           VALUES (:nombre, :paterno, :materno, :fecha)   
        '''), 
        {
            'nombre': fake.first_name(),
            'paterno': fake.last_name(),
            'materno': fake.last_name(),
            'fecha': fake.date()
        })

    conn.commit()