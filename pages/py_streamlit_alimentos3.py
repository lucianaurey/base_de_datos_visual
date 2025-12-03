import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# ==========================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================================
st.set_page_config(
    page_title="Ventas por Día",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CSS ESTILO VERDE PASTEL Y TARJETAS KPI
# ==========================================================
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
    }

    h3 {
        color: #355e3b !important;
        font-weight: 700 !important;
        font-size: 24px !important;
        border-left: 6px solid #74d3ae;
        padding-left: 12px;
    }

    /* Tarjetas KPI estilo Yummy pastel */
    .kpi-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 18px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        font-weight: 700;
        color: #1e3d32;
        border: 1px solid #ffffff55;
    }

    .kpi-title {
        font-size: 18px;
        font-weight: 900;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: 900;
        margin-top: 6px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #e9fff2 0%, #d6f7e6 100%);
        border-right: 2px solid #c3efd6;
    }

    details {
        background-color: #f4fff8 !important;
        border: 1px solid #c8efd9 !important;
        border-radius: 10px !important;
        padding: 8px !important;
        margin-bottom: 12px !important;
    }

</style>
""", unsafe_allow_html=True)

# ==========================================================
# CONEXIÓN MYSQL
# ==========================================================
usuario = "root"
contraseña = ""
host = "localhost"
puerto = 3306
base = "alimentos"

conexion_str = f"mysql+pymysql://{usuario}:{contraseña}@{host}:{puerto}/{base}"
engine = create_engine(conexion_str)

# ==========================================================
# CONSULTAS SQL
# ==========================================================
query_ventas = """
SELECT 
    p.fecha_prevista_entrega AS fecha,
    SUM(dp.cantidad * dp.precio_unitario) AS total_ventas,
    COUNT(DISTINCT p.id_pedido) AS total_pedidos
FROM pedido p
JOIN detalle_pedido dp ON dp.id_pedido = p.id_pedido
GROUP BY fecha
ORDER BY fecha ASC;
"""

query_top_productos = """
SELECT 
    p.nombre AS producto,
    SUM(dp.cantidad) AS cantidad_vendida,
    SUM(dp.cantidad * dp.precio_unitario) AS total
FROM detalle_pedido dp
JOIN producto p ON p.id_producto = dp.id_producto
GROUP BY p.id_producto, p.nombre
ORDER BY total DESC
LIMIT 20;
"""

df_ventas = pd.read_sql_query(query_ventas, engine)
df_top = pd.read_sql_query(query_top_productos, engine)

df_ventas["fecha"] = pd.to_datetime(df_ventas["fecha"])
df_ventas["dia_semana"] = df_ventas["fecha"].dt.day_name()

# ==========================================================
# TÍTULO
# ==========================================================
st.markdown("<h1>📊 Ventas por Día</h1>", unsafe_allow_html=True)

# ==========================================================
# FILTROS
# ==========================================================
st.sidebar.title("🔍 Filtros")

fecha_min = df_ventas["fecha"].min()
fecha_max = df_ventas["fecha"].max()

rango_fechas = st.sidebar.date_input("📅 Rango de fechas", [fecha_min, fecha_max])

dias = st.sidebar.multiselect(
    "📆 Días de la semana",
    options=df_ventas["dia_semana"].unique(),
    default=df_ventas["dia_semana"].unique()
)

min_venta = st.sidebar.slider(
    "💵 Ventas mínimas",
    float(df_ventas["total_ventas"].min()),
    float(df_ventas["total_ventas"].max()),
    float(df_ventas["total_ventas"].min())
)

min_pedidos = st.sidebar.slider(
    "🛒 Pedidos mínimos",
    int(df_ventas["total_pedidos"].min()),
    int(df_ventas["total_pedidos"].max()),
    int(df_ventas["total_pedidos"].min())
)

productos_lista = df_top["producto"].unique()
prod_select = st.sidebar.multiselect(
    "🏆 Productos más vendidos",
    options=productos_lista,
    default=productos_lista
)

# ==========================================================
# APLICAR FILTROS
# ==========================================================
df_filtrado = df_ventas[
    (df_ventas["fecha"] >= pd.to_datetime(rango_fechas[0])) &
    (df_ventas["fecha"] <= pd.to_datetime(rango_fechas[1])) &
    (df_ventas["dia_semana"].isin(dias)) &
    (df_ventas["total_ventas"] >= min_venta) &
    (df_ventas["total_pedidos"] >= min_pedidos)
]

df_top_filtered = df_top[df_top["producto"].isin(prod_select)]

# ==========================================================
# CALCULAR KPIs
# ==========================================================
total_pedidos = df_filtrado["total_pedidos"].sum()
total_ventas = df_filtrado["total_ventas"].sum()
ticket_promedio = total_ventas / total_pedidos if total_pedidos > 0 else 0

# ==========================================================
# TARJETAS KPI
# ==========================================================
st.markdown("### 📌 Resumen General")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">💵 Ventas Totales</div>
        <div class="kpi-value">${total_ventas:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">🛒 Pedidos Totales</div>
        <div class="kpi-value">{total_pedidos}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">📆 Días Analizados</div>
        <div class="kpi-value">{df_filtrado.shape[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">💳 Ticket Promedio</div>
        <div class="kpi-value">${ticket_promedio:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================================
# VISUALIZACIONES
# ==========================================================
st.subheader("📊 Visualizaciones")

with st.expander("📈 Ventas por día"):
    fig = px.line(df_filtrado, x="fecha", y="total_ventas", markers=True)
    fig.update_traces(marker_color="#74b9ff")
    st.plotly_chart(fig, use_container_width=True)

with st.expander("🛒 Pedidos por día"):
    fig2 = px.bar(df_filtrado, x="fecha", y="total_pedidos")
    fig2.update_traces(marker_color="#55efc4")
    st.plotly_chart(fig2, use_container_width=True)

with st.expander("🏆 Top productos más vendidos"):
    fig3 = px.bar(df_top_filtered, x="producto", y="total", text="cantidad_vendida")
    fig3.update_traces(marker_color="#a29bfe", textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)

with st.expander("📅 Ventas por día de la semana"):
    df_semana = df_filtrado.groupby("dia_semana", as_index=False)["total_ventas"].sum()

    orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df_semana["dia_semana"] = pd.Categorical(df_semana["dia_semana"], categories=orden_dias, ordered=True)
    df_semana = df_semana.sort_values("dia_semana")

    fig4 = px.bar(
        df_semana,
        x="dia_semana",
        y="total_ventas",
        text="total_ventas",
        labels={"dia_semana": "Día", "total_ventas": "Ventas ($)"},
        color_discrete_sequence=["#ff7675"]
    )
    fig4.update_traces(textposition="outside")
    st.plotly_chart(fig4, use_container_width=True)

# ==========================================================
# TABLA + EXPORTACIÓN
# ==========================================================
with st.expander("📋 Mostrar Tabla"):
    st.subheader("📋 Datos filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

    csv = df_filtrado.to_csv(index=False)
    st.download_button("📥 Descargar CSV", csv, "ventas_filtradas.csv", "text/csv")

# ==========================================================
# ANÁLISIS AUTOMÁTICO
# ==========================================================
st.subheader("🗣️ Análisis Automático")

st.write(f"""
✔ El análisis incluye ventas entre *{rango_fechas[0]}* y *{rango_fechas[1]}*.  
✔ Se registraron *{total_pedidos} pedidos* en total.  
✔ Las ventas alcanzaron *${total_ventas:,.2f}*.  
✔ El filtro aplicado permite observar tendencias por día, ventas mínimas y productos.
""")

st.caption("Proyecto Final – Base de Datos I – UNIVALLE 2025")
