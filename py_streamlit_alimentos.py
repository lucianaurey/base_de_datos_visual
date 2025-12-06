import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import altair as alt

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="Productos Más Vendidos", page_icon="📦", layout="wide")

# ---------------------------------------------------------
# CSS AVANZADO – TEMA VERDE PASTEL COMPLETO
# ---------------------------------------------------------
st.markdown("""
<style>

    /* Fondo general verde pastel */
    .stApp {
        background: linear-gradient(135deg, #e8f8f5 0%, #d5f5e3 40%, #f0faf5 100%);
    }

    /* Título principal */
    h1 {
        color: #2e5e4e !important;
        font-size: 48px !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.25);
        text-align: center;
        margin-bottom: 10px;
    }

    /* Subtítulos */
    h3 {
        color: #355e3b !important;
        font-weight: 800 !important;
        font-size: 26px !important;
        margin-top: 25px;
        border-left: 8px solid #74d3ae;
        padding-left: 12px;
    }

    /* Tarjetas */
    .card {
        background-color: rgba(255,255,255,0.96);
        padding: 25px;
        border-radius: 14px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        border-left: 10px solid #81e0a6;
        margin-top: 15px;
        margin-bottom: 30px;
    }

    /* Métricas */
    .metric {
        padding: 18px;
        border-radius: 14px;
        background: linear-gradient(135deg,#a8e6cf,#81ecec);
        text-align: center;
        font-size: 22px;
        font-weight: 900;
        color: #1e3d32;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        margin-bottom: 10px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #e9fff2 0%, #d6f7e6 100%);
        border-right: 2px solid #c3efd6;
    }

    /* Expander pastel */
    details {
        background-color: #f4fff8 !important;
        border: 1px solid #c8efd9 !important;
        border-radius: 10px !important;
        padding: 8px !important;
        margin-bottom: 12px !important;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TÍTULO
# ---------------------------------------------------------
st.markdown("<h1>📦 Dashboard – Productos Más Vendidos</h1>", unsafe_allow_html=True)

# ---------------------------------------------------------
# CONEXIÓN MYSQL
# ---------------------------------------------------------
DB_USER = "sql5809882"
DB_PASSWORD = "GPttLkDvVL"
DB_HOST = "sql5.freesqldatabase.com"
DB_NAME = "sql5809882"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# ---------------------------------------------------------
# CONSULTA SQL CON PROVEEDOR + STOCK
# ---------------------------------------------------------
query = """
SELECT 
    pr.nombre AS producto,
    pv.nombre AS proveedor,
    pr.stock_disponible,
    SUM(dp.cantidad) AS total_vendido
FROM detalle_pedido dp
JOIN producto pr ON dp.id_producto = pr.id_producto
JOIN proveedor pv ON pr.id_proveedor = pv.id_proveedor
GROUP BY pr.id_producto, pv.id_proveedor
ORDER BY total_vendido DESC;
"""

df = pd.read_sql_query(query, engine)

# ---------------------------------------------------------
# SIDEBAR – LOGO + FILTROS
# ---------------------------------------------------------
# LOGO EN EL SIDEBAR
# LOGO CORRECTO
st.sidebar.image("images/logo_yummy.png", width=120)

st.sidebar.title("🎨 Filtros")

producto_sel = st.sidebar.multiselect("Producto", df["producto"].unique())
proveedor_sel = st.sidebar.multiselect("Proveedor", df["proveedor"].unique())

stock_min, stock_max = st.sidebar.slider(
    "Stock disponible",
    int(df["stock_disponible"].min()),
    int(df["stock_disponible"].max()),
    (int(df["stock_disponible"].min()), int(df["stock_disponible"].max()))
)

venta_min, venta_max = st.sidebar.slider(
    "Cantidad vendida",
    int(df["total_vendido"].min()),
    int(df["total_vendido"].max()),
    (int(df["total_vendido"].min()), int(df["total_vendido"].max()))
)

# ---------------------------------------------------------
# FILTROS APLICADOS
# ---------------------------------------------------------
df_filtrado = df.copy()

if producto_sel:
    df_filtrado = df_filtrado[df_filtrado["producto"].isin(producto_sel)]

if proveedor_sel:
    df_filtrado = df_filtrado[df_filtrado["proveedor"].isin(proveedor_sel)]

df_filtrado = df_filtrado[
    (df_filtrado["stock_disponible"].between(stock_min, stock_max)) &
    (df_filtrado["total_vendido"].between(venta_min, venta_max))
]

# ---------------------------------------------------------
# MÉTRICAS
# ---------------------------------------------------------
st.markdown("<h3>📊 Resumen General</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='metric'>📦 Productos mostrados: {len(df_filtrado)}</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='metric'>🏪 Proveedores: {df_filtrado['proveedor'].nunique()}</div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='metric'>📈 Total vendido: {df_filtrado['total_vendido'].sum()}</div>", unsafe_allow_html=True)

# =========================================================
# GRÁFICOS OCULTOS – PALETA MODERNA NO VERDE
# =========================================================

color1 = "#74b9ff"   # Azul pastel
color2 = "#a29bfe"   # Morado suave
color3 = "#ff7675"   # Coral suave
color4 = "#ffeaa7"   # Amarillo pastel

with st.expander("📊 1️⃣ Barras – Productos más vendidos"):
    chart1 = alt.Chart(df_filtrado).mark_bar(color=color1).encode(
        x=alt.X("producto:N", sort="-y"),
        y="total_vendido:Q",
        tooltip=["producto", "total_vendido"]
    )
    st.altair_chart(chart1, use_container_width=True)

with st.expander("🥧 2️⃣ Pastel – Distribución porcentual"):
    df_filtrado["porcentaje"] = df_filtrado["total_vendido"] / df_filtrado["total_vendido"].sum() * 100
    chart2 = alt.Chart(df_filtrado).mark_arc(innerRadius=60).encode(
        theta="porcentaje:Q",
        color=alt.Color(
            "producto:N",
            scale=alt.Scale(range=[color1, color2, color3, color4])
        ),
        tooltip=["producto", "porcentaje"]
    )
    st.altair_chart(chart2, use_container_width=True)

with st.expander("📊 3️⃣ Horizontal – Comparación"):
    chart3 = alt.Chart(df_filtrado).mark_bar(color=color2).encode(
        x="total_vendido:Q",
        y=alt.Y("producto:N", sort="-x"),
        tooltip=["producto", "total_vendido"]
    )
    st.altair_chart(chart3, use_container_width=True)

with st.expander("📈 4️⃣ Tendencia – Ranking"):
    df_filtrado["ranking"] = df_filtrado["total_vendido"].rank(ascending=False)
    chart4 = alt.Chart(df_filtrado).mark_line(
        point=True,
        color=color3,
        strokeWidth=3
    ).encode(
        x="producto:N",
        y="ranking:Q",
        tooltip=["producto", "ranking"]
    )
    st.altair_chart(chart4, use_container_width=True)

# ---------------------------------------------------------
# TABLA FINAL OCULTA
# ---------------------------------------------------------
with st.expander("📋 Mostrar Tabla"):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.dataframe(df_filtrado, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Proyecto Final – Base de Datos I – UNIVALLE 2025")