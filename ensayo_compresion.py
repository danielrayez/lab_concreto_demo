import streamlit as st
import pandas as pd
from datetime import date
from calculos import resistencia_compresion, evolucion_resistencia , volumen_cilindro, densidad_cilindro


# ========================================
# ESTILOS CSS
# ========================================
#fondo gris muy claro

css = """
<style>
    .stApp {
        background-color: #fafafa;
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

# ========================================
# CONFIGURACIÓN INICIAL
# ========================================

st.set_page_config(page_title="Laboratorio Concreto", layout="wide")

st.title("Ensayo de Compresión de Cilindros de Concreto")

# ========================================
# DEFINICIONES DE NORMAS Y TIPOS DE FALLA
# ========================================
# NORMAS_COMPRESION = {
    # "🇨🇴 NTC 673 (Colombia)": "NTC 673",
    # "🇻🇪 COVENIN 338 (Venezuela)": "COVENIN 338",
    # "🇺🇸 ASTM C39 (USA)": "ASTM C39",
    # "🇧🇷 NBR 5739 (Brasil)": "NBR 5739",
    # "🇲🇽 NMX-C-083 (México)": "NMX-C-083",
    # "🇦🇷 IRAM 1546 (Argentina)": "IRAM 1546",
    # "🇵🇪 NTP 339.034 (Perú)": "NTP 339.034",
    # "🇨🇱 NCh 1010 (Chile)": "NCh 1010",
    # # "🇧🇴 NB 1225 (Bolivia)": "NB 1225",
    # "🇪🇨 NEN 1015 (Ecuador)": "NEN 1015",
# }

TIPOS_FALLA = [
    "Tipo 1: conos bien formados en ambos extremos",
    "Tipo 2: cono bien formado en un extremo",
    "Tipo 3: fisuras verticales  a traves de ambos extremos",
    "Tipo 4: fractura diagonal sin fisuras",
    "Tipo 5: fracturas en los lados en la parte superior o inferior",
    "Tipo 6: extremo puntiagudo",
]

# IMAGENES_FALLA = {
#     "Falla por compresión": "https://www.sioingenieria.com/portal/shared/rs.php?rsid=2193",
#     "Falla por cortante": "https://imgur.com/dkamL7p",
#     "Falla por tensión diagonal": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Diagonal_tension_failure.jpg/400px-Diagonal_tension_failure.jpg",
#     "Grietas radiales": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Radial_cracks.jpg/400px-Radial_cracks.jpg",
#     "Fractura cónica": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Conical_fracture.jpg/400px-Conical_fracture.jpg",
#     "Falla por desprendimiento": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Spalling_failure.jpg/400px-Spalling_failure.jpg",
#     "Falla frágil": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Brittle_failure.jpg/400px-Brittle_failure.jpg",
#     "Otra": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Concrete_specimen.jpg/400px-Concrete_specimen.jpg"
# }

# Inicializar estado de sesión
if "df_ensayos" not in st.session_state:
    st.session_state.df_ensayos = pd.DataFrame(columns=["Muestra", "Fecha", "Norma", "Edad(d)", "Carga(kN)", "Diámetro(mm)", "Altura(mm)", "Densidad(kg/m3)", "Resistencia(MPa)", "Evolución(%)", "Tipo Falla"])

df_ensayos = st.session_state.df_ensayos


# ========================================
# SECCIÓN 1: REGISTRO DE ENSAYO
# ========================================

col1, col2, col3 = st.columns(3)
with col1:
    st.write("### Registro de Ensayo")

with col2:

    st.write("") 
    norma = " NTC 673 (Colombia)" 
    url = "https://es.slideshare.net/slideshow/ntc-673-compresion-concretos/17107178"  

    norma_s = st.markdown(
        f"""
        <h5 style='text-align: left; font-weight: bold; margin: 0; color: #2E86C1; padding: 0;'>
            <a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">
                {norma}
            </a>
        </h5>
    """,
    unsafe_allow_html=True, help="Haz clic para ver la norma NTC 673")

with col3:
    #texto con fecha del día de hoy centrado y en negrita  
    fecha = date.today().strftime("%d/%m/%Y") 
    fecha_f = st.markdown(f"<h5 style='text-align: left; font-weight: bold; margin: 0; padding: 15px;'>{fecha}</h5>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)


with col1:
    muestra = st.text_input("Nombre de la muestra", placeholder="Ej: Muestra 1")
    dimensiones = st.selectbox("Dimensiones del cilindro", ["100x200 mm", "150x300 mm"])
    peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1)

        
    # Asignar valores de diámetro y altura según dimensiones
    if dimensiones == "100x200 mm":
        diametro_default = 100
        altura_default = 200
    else:
        diametro_default = 150
        altura_default = 300

with col2:
    fc = st.number_input("F'c (MPa)", min_value=15.0, step= 1.0)
    diametro = st.number_input("Diámetro (mm)", min_value=1.0, value=float(diametro_default), step=0.1)
    carga = st.number_input("Carga (kN)", min_value=0.0, step=0.1)

# Calcular resistencia
if carga > 0 and diametro > 0:
    resistencia = resistencia_compresion(carga, diametro)
else:
    resistencia = 0.0

with col3:
    edad = st.number_input("Edad (días)", min_value=1, max_value=28, value=7)
    altura = st.number_input("Altura (mm)", min_value=1.0, value=float(altura_default), step=0.1)
    tipo_falla = st.selectbox("Tipo de Falla", TIPOS_FALLA)

# Calcular densidad
if diametro > 0 and altura > 0:
    volumen = volumen_cilindro(diametro, altura)
    densidad = densidad_cilindro(volumen, peso)
else:
    densidad = 0.0

# Calcular evolución de resistencia
evolucion = evolucion_resistencia(resistencia, fc)

# Botón para registrar ensayo
if st.button("Registrar Ensayo", type="primary"):
    if carga > 0 and diametro > 0 and altura > 0:
        nuevo_ensayo = pd.DataFrame({
            "Muestra": [muestra],
            "Fecha": [fecha],       
            "Norma": [norma],
            "Edad(d)": [edad],
            "Carga(kN)": [carga],
            "Diámetro(mm)": [diametro],
            "Altura(mm)": [altura],
            "Densidad(kg/m3)": [densidad],
            "Resistencia(MPa)": [resistencia],
            "Evolución(%)": [evolucion],
            "Tipo Falla": [tipo_falla[:6]],
        })
        
        st.session_state.df_ensayos = pd.concat([st.session_state.df_ensayos, nuevo_ensayo], ignore_index=True)
        st.success("Ensayo registrado correctamente")
    else:
        st.error("Por favor completa todos los campos obligatorios: muestra, carga, diámetro y altura")

# ========================================
# SECCIÓN 2: TABLA DE RESULTADOS
# ========================================
st.divider()
st.markdown("### Resultados", help="para descargar resultados en formato csv use el icono de descarga contenido en el grupo de iconos de la esquina superior derecha de esta tabla")

if not st.session_state.df_ensayos.empty:
    # Mostrar tabla
    df_display = st.session_state.df_ensayos.copy()
    # df_display["Fecha"] = pd.to_datetime(df_display["Fecha"]).dt.strftime("%d/%m/%Y")
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
else:
    st.info("No se han registrado ensayos aún. Completa el formulario para agregar resultados.")
