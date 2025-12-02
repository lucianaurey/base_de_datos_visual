import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from datetime import date
import pymysql

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="Seguimiento de Pedidos", page_icon="🚚", layout="wide")

# ---------------------------------------------------------
# CSS VERDE PASTEL SUAVE (igual al otro dashboard)
# ---------------------------------------------------------
st.markdown("""
<style>

    .stApp {
        background: linear-gradient(135deg, #e8f8f5 0%, #d5f5e3 40%, #f0faf5 100%);
    }

    h1 {
        color: #2e5e4e !important;
        font-size: 40px !important;
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
# TÍTULO
# ---------------------------------------------------------
st.markdown("<h1>🚚 Seguimiento de Pedidos y Repartidores</h1>", unsafe_allow_html=True)

# ---------------------------------------------------------
# CONEXIÓN MYSQL
# ---------------------------------------------------------
DB_USER = "sql5809882"
DB_PASSWORD = "GPttLkDvVL"
DB_HOST = "sql5.freesqldatabase.com"
DB_NAME = "sql5809882"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# ---------------------------------------------------------
# CONSULTA SQL
# ---------------------------------------------------------
query = """
SELECT 
    p.id_pedido,
    p.fecha_pedido,
    rp.id_repartidor,
    r.nombre AS nombre_repartidor,
    s.estado,
    s.tiempo_estimado AS hora_salida,
    s.hora_llegada,
    TIMESTAMPDIFF(
        MINUTE,
        s.tiempo_estimado,
        s.hora_llegada
    ) AS retraso_min
FROM seguimiento_pedido s
INNER JOIN repartidor_pedido rp 
    ON s.id_repartidor_pedido = rp.id_repartidor_pedido
INNER JOIN pedido p 
    ON rp.pedido_id_pedido = p.id_pedido
INNER JOIN repartidor r 
    ON rp.id_repartidor = r.id_repartidor;
"""

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_sql(query, engine)

df = cargar_datos()

df["fecha_pedido"] = pd.to_datetime(df["fecha_pedido"], errors="coerce")
df["hora_salida"] = pd.to_datetime(df["hora_salida"], errors="coerce")
df["hora_llegada"] = pd.to_datetime(df["hora_llegada"], errors="coerce")

# ---------------------------------------------------------
# SIDEBAR — LOGO + FILTROS
# ---------------------------------------------------------
st.sidebar.image(
    r"C:\Users\HP\Pictures\Screenshots\Captura de pantalla 2025-12-02 145947.png",
    width=120
)

st.sidebar.title("⚙️ Opciones")

repartidores = ["Todos"] + sorted(df["nombre_repartidor"].dropna().unique().tolist())
repartidor_sel = st.sidebar.selectbox("👤 Repartidor", repartidores)

min_fecha = df["fecha_pedido"].min().date()
max_fecha = df["fecha_pedido"].max().date()
rango_fecha = st.sidebar.date_input("📅 Rango de fechas", [min_fecha, max_fecha])

mostrar_graficos = st.sidebar.checkbox("📊 Mostrar gráficas", value=True)
mostrar_tabla = st.sidebar.checkbox("📋 Mostrar tabla", value=True)

# ---------------------------------------------------------
# FILTRAR
# ---------------------------------------------------------
df_filtrado = df.copy()

if repartidor_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["nombre_repartidor"] == repartidor_sel]

if isinstance(rango_fecha, list) and len(rango_fecha) == 2:
    f_inicio, f_fin = pd.to_datetime(rango_fecha[0]), pd.to_datetime(rango_fecha[1])
    df_filtrado = df_filtrado[(df_filtrado["fecha_pedido"] >= f_inicio) & (df_filtrado["fecha_pedido"] <= f_fin)]

# ---------------------------------------------------------
# MÉTRICAS
# ---------------------------------------------------------
st.markdown("### 📌 Resumen general")
c1, c2, c3 = st.columns(3)

c1.metric("📦 Total pedidos", df_filtrado["id_pedido"].nunique())
c2.metric("🚚 Repartidores activos", df_filtrado["id_repartidor"].nunique())
c3.metric("⏱️ Retraso promedio", f"{round(df_filtrado['retraso_min'].mean(),1)} min")

st.divider()

# ---------------------------------------------------------
# GRÁFICOS
# ---------------------------------------------------------
if mostrar_graficos:
    st.subheader("📊 Visualizaciones")

    with st.expander("📊 Retraso por pedido"):
        df_bar = df_filtrado.dropna(subset=["retraso_min"])
        if not df_bar.empty:
            fig = px.bar(
                df_bar.sort_values("retraso_min", ascending=False),
                x="id_pedido",
                y="retraso_min",
                text="retraso_min",
                labels={"id_pedido": "ID Pedido", "retraso_min": "Retraso (min)"},
            )
            fig.update_layout(template="plotly_white", height=450, title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de retraso disponibles.")

    with st.expander("🥧 Distribución de estados"):
        conteo_estado = df_filtrado["estado"].fillna("Desconocido").value_counts().reset_index()
        conteo_estado.columns = ["estado", "cantidad"]
        fig = px.pie(
            conteo_estado,
            names="estado",
            values="cantidad",
            hole=0.3
        )
        fig.update_layout(template="plotly_white", height=450, title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("⏳ Línea de tiempo de entregas"):
        df_timeline = df_filtrado.dropna(subset=["hora_salida", "hora_llegada"])
        if not df_timeline.empty:
            df_timeline["id_pedido_str"] = df_timeline["id_pedido"].astype(str)
            fig = px.timeline(
                df_timeline,
                x_start="hora_salida",
                x_end="hora_llegada",
                y="id_pedido_str",
                color="estado",
                labels={"id_pedido_str": "Pedido"},
            )
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(template="plotly_white", height=550, title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos para mostrar la línea de tiempo.")

# ---------------------------------------------------------
# TABLA FINAL
# ---------------------------------------------------------
if mostrar_tabla:
    st.subheader("📋 Tabla de datos")
    st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)

# ---------------------------------------------------------
# PIE DE PÁGINA
# ---------------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-top:30px;">
    <img src="https://cdn-icons-png.flaticon.com/512/1995/1995574.png" width="70">
    <p style="font-size:13px; color:#333;">Yummy Delivery — Seguimiento de Pedidos</p>
</div>
""", unsafe_allow_html=True)