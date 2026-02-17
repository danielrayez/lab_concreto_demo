import streamlit as st
import os
import sys

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Laboratorio de Concreto",
    page_icon="🏗️",
    layout="wide"
)

# Título principal
st.title("🏗️ Bienvenido al Laboratorio de Concreto")
st.markdown("Sistema de Gestión de Ensayos")



# ========================================
# ESTILOS CSS
# ========================================

css = """
<style>
    .stApp {
        background-color: #fafafa; /*gris claro*/
    }
    a.anchor-link {
        display: none !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }   
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.markdown("""
<div style='margin-top:40px; font-size:18px; max-width:800px;'>
Esta aplicación es una muestra de un <b>Sistema de Gestión para Laboratorios de Concreto</b>,
que cubre el proceso completo: desde la recepción de muestras hasta la generación de informes técnicos.
<br><br>
Diseñado especialmente para <b>Pymes en la industria de la construcción</b> que buscan digitalizar y organizar sus ensayos sin sistemas complejos ni costosos.
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<div style='height:80px;'></div>",
    unsafe_allow_html=True
)



linkedin = "https://www.linkedin.com/in/danielorlando-ramirez/" 
email = "ingdanielrayez@gmail.com"

st.markdown(
    f"""
    <div style='text-align: center; font-size: 12px; color: #000000; line-height: 1.6;'> 
        Desarrollado por<br>
        <strong>Daniel Ramírez</strong><br>
        Ingeniero Civil | Desarrollo de Soluciones Analíticas<br><br>
        <a href="{linkedin}" target="_blank" style="color: #000000; text-decoration: none;">
            LinkedIn
        </a> |
        <a href="mailto:{email}" style="color: #000000; text-decoration: none;">
            ingdanielrayez@gmail.com
        </a>
    </div>
    """,
    unsafe_allow_html=True
)