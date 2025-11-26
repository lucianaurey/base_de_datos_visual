import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title="Productos Más Vendidos", page_icon="📦", layout="wide")

# ESTILOS
st.markdown("""
<style>
    .stApp { background-color: #f7f9fc; }
    h1 { color: #2c3e50 !important; font-weight: 900 !important; }
    h3 { color: #1e272e !important; font-weight: 800 !important; }
    .card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.06); border-left: 6px solid #4b7bec;
        margin-bottom: 20px;
    }
    .metric {
        padding: 15px; border-radius: 10px; background-color: #dfe6e9;
        text-align: center; font-size: 18px; font-weight: 700; color: #2d3436;
        border-left: 6px solid #0984e3;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📦 Productos Más Vendidos</h1>", unsafe_allow_html=True)

# CONEXIÓN A MYSQL
engine = create_engine("mysql+pymysql://root:@localhost:3306/alimentos")

# CONSULTA
query = """
SELECT 
    pr.nombre AS producto,
    SUM(dp.cantidad) AS total_vendido
FROM detalle_pedido dp
JOIN producto pr ON dp.id_producto = pr.id_producto
GROUP BY pr.id_producto
ORDER BY total_vendido DESC;
"""

df = pd.read_sql_query(query, engine)

# SIDEBAR
st.sidebar.header("🔍 Filtros")

productos = ["(Todos)"] + df["producto"].unique().tolist()
producto_sel = st.sidebar.selectbox("Seleccionar producto", productos)

df_filtrado = df.copy()

if producto_sel != "(Todos)":
    df_filtrado = df_filtrado[df_filtrado["producto"] == producto_sel]

limite = st.sidebar.slider("Número de productos mostrados", 5, len(df_filtrado), 10)
df_filtrado = df_filtrado.head(limite)

# MÉTRICAS
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<div class='metric'>Productos mostrados: {len(df_filtrado)}</div>", unsafe_allow_html=True)

with col2:
    total_sum = int(df_filtrado["total_vendido"].sum())
    st.markdown(f"<div class='metric'>Total vendido: {total_sum}</div>", unsafe_allow_html=True)

# TABLA
st.markdown("<h3>📊 Tabla de productos más vendidos</h3>", unsafe_allow_html=True)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.dataframe(df_filtrado, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# GRÁFICO
st.markdown("<h3>📈 Gráfico de Ventas</h3>", unsafe_allow_html=True)
st.bar_chart(df_filtrado.set_index("producto")["total_vendido"])

# FOOTER
st.markdown("---")
st.caption("© 2025 Yummy Delivery | Proyecto Base de Datos I — UNIVALLE")
