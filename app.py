import streamlit as st

# -----------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------
st.set_page_config(page_title="Inicio – Yummy Delivery", page_icon="🍽️", layout="wide")

# -----------------------------------------------
# ESTILO PERSONALIZADO – VERDE PASTEL
# -----------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e8f8f5, #d5f5e3, #f0faf5);
    }

    h1 {
        color: #2e5e4e;
        font-size: 48px;
        text-align: center;
        font-weight: 900;
        margin-top: 10px;
    }

    h2 {
        color: #355e3b;
        font-size: 28px;
        text-align: center;
        margin-top: 5px;
    }

    p {
        font-size: 18px;
        text-align: center;
        color: #2d3436;
        padding: 0 50px;
    }

    .logo-container {
        text-align: center;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    .credits-box {
        background: #ffffffcc;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 30px;
    }

    .credits-box h3 {
        color: #355e3b;
        text-align: center;
    }

    .credits-box ul {
        list-style-type: none;
        padding-left: 0;
        font-size: 18px;
        color: #2e5e4e;
        text-align: center;
    }

    .credits-box ul li {
        margin: 6px 0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------
# LOGO
# -----------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])  # proporciones (izquierda, centro, derecha)

with col2:
    st.image(
        r"C:\Users\HP\Pictures\Screenshots\Captura de pantalla 2025-12-02 145947.png",
        width=180
    )
# -----------------------------------------------
# TÍTULO
# -----------------------------------------------
st.markdown("<h1>🍽️ Yummy Delivery Dashboard</h1>", unsafe_allow_html=True)

# -----------------------------------------------
# DESCRIPCIÓN
# -----------------------------------------------
st.markdown("""
<p>
Bienvenidos a la plataforma de análisis de datos para <strong>Yummy Delivery</strong>, 
un sistema de entrega de alimentos que optimiza las operaciones a través de visualizaciones, métricas y seguimiento inteligente.
</p>

<p>
Desde este panel podrás acceder a análisis de ventas, monitoreo de repartidores, comportamiento de clientes y más.  
Todo ello con un diseño claro, moderno y adaptado a tus necesidades.
</p>
""", unsafe_allow_html=True)

# -----------------------------------------------
# CRÉDITOS DEL EQUIPO
# -----------------------------------------------
st.markdown("""
<div class="credits-box">
    <h3>👩‍💻 Desarrollado por:</h3>
    <ul>
        <li>Melani Fernandez Nuñez</li>
        <li>Wendy Herrera Muñoz</li>
        <li>Ariana Rojas Ribera</li>
        <li>Luciana Urey Ayala</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------
# PIE DE PÁGINA
# -----------------------------------------------
st.caption("Proyecto Final – Base de Datos I – UNIVALLE 2025")