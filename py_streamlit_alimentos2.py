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
# CSS VERDE PASTEL SUAVE
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
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #e9fff2 0%, #d6f7e6 100%);
        border-right: 2px solid #c3efd6;
        text-align: center;
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
    s.tiempo_estimado,
    s.hora_llegada,
    TIMESTAMPDIFF(MINUTE, s.tiempo_estimado, s.hora_llegada) AS retraso_min
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

# ---------------------------------------------------------
# CORRECCIÓN DE FECHAS
# ---------------------------------------------------------
df["fecha_pedido"] = pd.to_datetime(df["fecha_pedido"], errors="coerce")

df["tiempo_estimado"] = pd.to_datetime(df["tiempo_estimado"], errors="coerce") + pd.to_timedelta("08:00:00")
df["hora_llegada"] = pd.to_datetime(df["hora_llegada"], errors="coerce") + pd.to_timedelta("09:00:00")

df["retraso_min"] = (df["hora_llegada"] - df["tiempo_estimado"]).dt.total_seconds() / 60
df["retraso_min"] = df["retraso_min"].clip(lower=0)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

# LOGO CORRECTO
st.sidebar.image("images/logo_yummy.png", width=120)

st.sidebar.title("⚙️ Opciones")

repartidores = ["Todos"] + sorted(df["nombre_repartidor"].dropna().unique().tolist())
repartidor_sel = st.sidebar.selectbox("👤 Repartidor", repartidores)

min_fecha = df["fecha_pedido"].min().date()
max_fecha = df["fecha_pedido"].max().date()

rango_fecha = st.sidebar.date_input("📅 Rango de fechas", [min_fecha, max_fecha])

mostrar_graficos = st.sidebar.checkbox("📊 Mostrar gráficas", value=True)
mostrar_tabla = st.sidebar.checkbox("📋 Mostrar tabla", value=True)

# ---------------------------------------------------------
# FILTROS
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

    # -----------------------------------------------------
    # Retraso por pedido
    # -----------------------------------------------------
    with st.expander("📊 Retraso por pedido"):
        df_bar = df_filtrado.dropna(subset=["retraso_min"])
        if not df_bar.empty:
            fig = px.bar(
                df_bar.sort_values("retraso_min", ascending=False),
                x="id_pedido",
                y="retraso_min",
                text="retraso_min",
                labels={"id_pedido": "Pedido", "retraso_min": "Retraso (min)"}
            )
            fig.update_traces(marker_color="#74b9ff", textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de retraso disponibles.")

    # -----------------------------------------------------
    # Distribución de estados
    # -----------------------------------------------------
    with st.expander("🥧 Distribución de estados"):
        conteo_estado = df_filtrado["estado"].fillna("Desconocido").value_counts().reset_index()
        conteo_estado.columns = ["estado", "cantidad"]

        fig = px.pie(
            conteo_estado,
            names="estado",
            values="cantidad",
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------------------
    # Scatterplot: Duración por repartidor
    # -----------------------------------------------------
    with st.expander("📈 Duración de entregas por repartidor (scatterplot)"):
        df_scatter = df_filtrado.copy()

        df_scatter["duracion_min"] = (
            df_scatter["hora_llegada"] - df_scatter["tiempo_estimado"]
        ).dt.total_seconds() / 60

        df_scatter = df_scatter.dropna(subset=["duracion_min"])

        if not df_scatter.empty:
            fig_scatter = px.scatter(
                df_scatter,
                x="nombre_repartidor",
                y="duracion_min",
                color="estado",
                size="duracion_min",
                hover_data=["id_pedido"],
                labels={"nombre_repartidor": "Repartidor", "duracion_min": "Duración (min)"},
                title="Duración de entregas por repartidor"
            )

            fig_scatter.update_layout(template="plotly_white", height=500, title_x=0.5)
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No hay datos suficientes para graficar duración.")

    # -----------------------------------------------------
    # Gráfico extra: Retraso promedio por repartidor
    # -----------------------------------------------------
    with st.expander("📈 Retraso promedio por repartidor"):
        df_rep = df_filtrado.groupby("nombre_repartidor", as_index=False)["retraso_min"].mean()
        df_rep["retraso_min"] = df_rep["retraso_min"].round(1)

        if not df_rep.empty:
            fig_extra = px.bar(
                df_rep,
                x="nombre_repartidor",
                y="retraso_min",
                text="retraso_min",
                color_discrete_sequence=["#ff7675"],
                labels={"nombre_repartidor": "Repartidor", "retraso_min": "Retraso Promedio (min)"}
            )
            fig_extra.update_traces(textposition="outside")
            st.plotly_chart(fig_extra, use_container_width=True)
        else:
            st.info("No hay datos suficientes para calcular retraso promedio.")

# ---------------------------------------------------------
# TABLA GENERAL
# ---------------------------------------------------------
with st.expander("📋 Mostrar Tabla"):
    if mostrar_tabla:
        st.subheader("📋 Datos filtrados")
        st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)

# ---------------------------------------------------------
# PIE DE PÁGINA
# ---------------------------------------------------------
st.caption("Proyecto Final – Base de Datos I – UNIVALLE 2025")
