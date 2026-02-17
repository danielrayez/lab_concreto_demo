import streamlit as st
import pandas as pd
from datetime import date
from ensayos.cal_concreto import area_cilindro, resistencia_compresion, evolucion_resistencia , volumen_cilindro, densidad_cilindro
from ensayos.factores_ld import factor_ld

# ========================================
# BARRA LATERAL PRESENTACIÓN
# ========================================

linkedin = "https://www.linkedin.com/in/danielorlando-ramirez/" 
email = "ingdanielrayez@gmail.com"

st.sidebar.markdown(
    "<div style='height:240px;'></div>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    f"""
    <div style='text-align: center; font-size: 12px; color: #888888; line-height: 1.6;'> 
        Desarrollado por<br>
        <strong>Daniel Ramírez</strong><br>
        Ingeniero Civil | Desarrollo de Soluciones Analíticas<br><br>
        <a href="{linkedin}" target="_blank" style="color: #888888; text-decoration: none;">
            LinkedIn
        </a> |
        <a href="mailto:{email}" style="color: #888888; text-decoration: none;">
            Email
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
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

# ========================================
# CONFIGURACIÓN INICIAL
# ========================================

st.set_page_config(page_title="Laboratorio Concreto", layout="wide")

#2 COLUMNAS
col_e1, col_e2 = st.columns([7,3])

with col_e1:
    st.title("Compresión de Cilindros de Concreto")

with col_e2:

    norma = " NTC 673 (Colombia)" 
    url = "https://es.slideshare.net/slideshow/ntc-673-compresion-concretos/17107178"  

    norma_s = st.markdown(
        f"""
        <h5 style='text-align: left; font-weight: bold; margin: 0; color: #2E86C1; padding: 40px;'>
            <a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">
                {norma}
            </a>
        </h5>
    """,
    unsafe_allow_html=True, help="Haz clic para ver la norma NTC 673")

# ========================================
#  AUXILIARES
# ========================================

TIPOS_FALLA = [
    "Tipo 1: conos bien formados en ambos extremos",
    "Tipo 2: cono bien formado en un extremo",
    "Tipo 3: fisuras verticales  a traves de ambos extremos",
    "Tipo 4: fractura diagonal sin fisuras",
    "Tipo 5: fracturas en los lados en la parte superior o inferior",
    "Tipo 6: extremo puntiagudo",
]

# Inicializar estado de sesión
if "df_ensayos" not in st.session_state:
    st.session_state.df_ensayos = pd.DataFrame(columns=["Muestra", "Fecha", "Edad(d)",  "Diámetro(mm)", "Altura(mm)", "Densidad(kg/m3)", "Carga Máxima(kN)", "Resistencia(MPa)", "Evolución(%)", "Tipo Falla"])

df_ensayos = st.session_state.df_ensayos

# ========================================
# SECCIÓN 1: REGISTRO DE ENSAYO
# ========================================

col1, col2, col3 = st.columns(3)
with col1:
    st.write("### Registro de Ensayo")

with col2:   #Norma técnica con enlace
    fecha = date.today().strftime("%d/%m/%Y") 
    fecha_f = st.markdown(f"<h5 style='text-align: left; font-weight: bold; margin: 0; padding: 15px;'>{fecha}</h5>", unsafe_allow_html=True)


# with col3:     #texto con fecha del día de hoy centrado y en negrita  

#     fecha = date.today().strftime("%d/%m/%Y") 
#     fecha_f = st.markdown(f"<h5 style='text-align: left; font-weight: bold; margin: 0; padding: 15px;'>{fecha}</h5>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    muestra = st.text_input("Nombre de la muestra", placeholder="Ej: Muestra 1")
    dimensiones = st.selectbox("Dimensiones del cilindro", ["100x200 mm", "150x300 mm", "Otras dimensiones"], help="Selecciona las dimensiones estándar o elige 'Otras dimensiones' para ingresar medidas personalizadas")
    peso = st.number_input("Peso (kg)", value= None , placeholder="Ej: 3.5")

    # Asignar valores de diámetro y altura según dimensiones
    if dimensiones == "100x200 mm":
        diametro_default = 100
        altura_default = 200
    elif dimensiones == "150x300 mm":
        diametro_default = 150
        altura_default = 300
    else:
        diametro_default = 100
        altura_default = 100

with col2:
    fc = st.number_input("F'c (MPa)", min_value=15.0, step= 1.0)
    diametro = st.number_input("Diámetro (mm)", min_value=1.0, value=float(diametro_default), step=0.1)
    area = area_cilindro(diametro)
    carga = st.number_input("Carga (kN)", min_value=1.0, step=0.1)


with col3:

    edad = st.selectbox("Edad (días)", ["1 (+- 0.5h)", "3 (+-2h)", "7 (+-6h)", "28 (+-20h)", "90 (48h)"])  
    altura = st.number_input("Altura (mm)", min_value=1.0, value=float(altura_default), step=0.1)
    tipo_falla = st.selectbox("Tipo de Falla", TIPOS_FALLA)
    rel_ld = altura / diametro
    factor_ld_value = factor_ld.loc[factor_ld["ld"] == round(rel_ld, 2), "factor"].values[0] if 1.0 <= rel_ld <= 1.99 else 1.0

    # Calcular resistencia
if dimensiones == "Otras dimensiones" and 1.0 <= rel_ld <= 1.99:
    resistencia = resistencia_compresion(carga, diametro)
    resistencia = round(resistencia * factor_ld_value, 2)
    evolucion = evolucion_resistencia(fc, resistencia)

elif dimensiones != "Otras dimensiones" and carga > 0 and diametro > 0:
    resistencia = resistencia_compresion(carga, diametro)
    evolucion = evolucion_resistencia(fc, resistencia)
else:
    st.error("La relación L/D debe estar entre 1.00 y 2.00 para cilindros de otras dimensiones.")

# Calcular densidad
if peso == None:
    peso = 0.0
if diametro > 0 and altura > 0:
    volumen = volumen_cilindro(diametro, altura)
    densidad = densidad_cilindro(volumen, float(peso))
else:
    densidad = 0.0

# Botón para registrar ensayo
if st.button("Registrar Ensayo", type="primary"):
    if muestra and carga > 0:
        nuevo_ensayo = pd.DataFrame({
            "Muestra": [muestra],
            "Fecha": [fecha],       
            "Edad(d)": [edad.split(" ")[0]],
            "Diámetro(mm)": [diametro],
            "Altura(mm)": [altura],
            "Densidad(kg/m3)": [densidad],            
            "Carga Máxima(kN)": [carga],
            "Resistencia(MPa)": [resistencia],
            "Evolución(%)": [evolucion],
            "Tipo Falla": [tipo_falla[:6]],
        })
        
        st.session_state.df_ensayos = pd.concat([st.session_state.df_ensayos, nuevo_ensayo], ignore_index=True)
        st.success("Ensayo registrado correctamente")
    else:
        st.error("Completa todos los campos obligatorios: muestra y carga")

# ========================================
# SECCIÓN 2: TABLA DE RESULTADOS
# ========================================
st.divider()
st.markdown("### Resultados", help="para descargar resultados en formato csv use el icono de descarga contenido en el grupo de iconos de la esquina superior derecha de esta tabla")

if not st.session_state.df_ensayos.empty:
    # Mostrar tabla
    df_display = st.session_state.df_ensayos.copy()
    st.dataframe(df_display, width= "content", hide_index=True)
    
else:
    st.info("No se han registrado ensayos aún. Completa el formulario para agregar resultados.")

