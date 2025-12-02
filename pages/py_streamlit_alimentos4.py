import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import altair as alt
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="Consumo por Usuario", page_icon="🧍", layout="wide")

# ---------------------------------------------------------
# CSS VERDE PASTEL
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e8f8f5 0%, #d5f5e3 40%, #f0faf5 100%);
    }
    h1 {
        color: #2e5e4e !important;
        font-size: 42px !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 5px;
    }
    h3 {
        color: #355e3b !important;
        font-weight: 700 !important;
        font-size: 24px !important;
        border-left: 6px solid #74d3ae;
        padding-left: 12px;
    }
    .metric {
        padding: 16px;
        border-radius: 14px;
        background: linear-gradient(135deg,#a8e6cf,#81ecec);
        text-align: center;
        font-size: 20px;
        font-weight: 900;
        color: #1e3d32;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #e9fff2 0%, #d6f7e6 100%);
        border-right: 2px solid #c3efd6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CONEXIÓN MYSQL
# ---------------------------------------------------------
DB_USER = "sql5809882"
DB_PASSWORD = "GPttLkDvVL"
DB_HOST = "sql5.freesqldatabase.com"
DB_NAME = "sql5809882"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# ---------------------------------------------------------
# CONSULTA SQL – CONSUMO POR USUARIO
# ---------------------------------------------------------
query = """
SELECT 
    CONCAT(u.nombre, ' ', u.apellido_paterno, ' ', u.apellido_materno) AS cliente,
    COUNT(p.id_pedido) AS total_pedidos,
    SUM(dp.cantidad * dp.precio_unitario) AS total_gastado,
    ROUND(AVG(dp.cantidad * dp.precio_unitario), 2) AS ticket_promedio
FROM usuario u
JOIN pedido p ON p.id_usuario = u.id_usuario
JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
GROUP BY u.id_usuario
ORDER BY total_gastado DESC;
"""

df = pd.read_sql_query(query, engine)

# ---------------------------------------------------------
# SIDEBAR – LOGO + FILTROS
# ---------------------------------------------------------
st.sidebar.image(
    r"C:\Users\HP\Pictures\Screenshots\Captura de pantalla 2025-12-02 145947.png",
    width=120
)

st.sidebar.title("🎯 Filtros")

clientes = df["cliente"].unique()
cliente_sel = st.sidebar.multiselect("🧍 Cliente", clientes, default=clientes)

min_pedidos = st.sidebar.slider("📦 Pedidos mínimos", 0, int(df["total_pedidos"].max()), 0)
min_gasto = st.sidebar.slider("💰 Gasto mínimo", 0.0, float(df["total_gastado"].max()), 0.0)

# ---------------------------------------------------------
# FILTROS APLICADOS
# ---------------------------------------------------------
df_filtrado = df[
    (df["cliente"].isin(cliente_sel)) &
    (df["total_pedidos"] >= min_pedidos) &
    (df["total_gastado"] >= min_gasto)
]

# ---------------------------------------------------------
# TÍTULO
# ---------------------------------------------------------
st.markdown("<h1>🧍 Consumo por Usuario</h1>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MÉTRICAS
# ---------------------------------------------------------
st.markdown("### 📌 Indicadores Clave")
c1, c2, c3 = st.columns(3)

c1.metric("👥 Clientes", df_filtrado.shape[0])
c2.metric("📦 Total Pedidos", df_filtrado["total_pedidos"].sum())
c3.metric("💵 Gasto Total", f"${df_filtrado['total_gastado'].sum():,.2f}")

st.divider()

# ---------------------------------------------------------
# GRÁFICOS
# ---------------------------------------------------------
st.subheader("📊 Visualizaciones")

with st.expander("📦 Pedidos por cliente"):
    fig1 = px.bar(df_filtrado, x="cliente", y="total_pedidos", text="total_pedidos", color_discrete_sequence=["#74b9ff"])
    fig1.update_traces(textposition="outside")
    st.plotly_chart(fig1, use_container_width=True)

with st.expander("💵 Gasto total por cliente"):
    fig2 = px.bar(df_filtrado, x="cliente", y="total_gastado", text="total_gastado", color_discrete_sequence=["#a29bfe"])
    fig2.update_traces(textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)

with st.expander("💳 Ticket promedio por cliente"):
    fig3 = px.bar(df_filtrado, x="cliente", y="ticket_promedio", text="ticket_promedio", color_discrete_sequence=["#ff7675"])
    fig3.update_traces(textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------
# TABLA FINAL + EXPORTACIÓN
# ---------------------------------------------------------
st.subheader("📋 Datos filtrados")
st.dataframe(df_filtrado, use_container_width=True)

csv = df_filtrado.to_csv(index=False)
st.download_button("📥 Descargar CSV", csv, "consumo_por_usuario.csv", "text/csv")

# ---------------------------------------------------------
# PIE DE PÁGINA
# ---------------------------------------------------------
st.caption("YUMMY DELIVERY — Dashboard de Clientes")
