import streamlit as st
import pandas as pd
from datetime import date
from calculos.cal_concreto import area_cilindro, resistencia_compresion, evolucion_resistencia , volumen_cilindro, densidad_cilindro
from utils.report.compresion_cilindros_pdf import compresion_cilindros_pdf as generar_pdf
from utils.factores_ld import factor_ld

# ========================================
# CONFIGURACIÓN INICIAL
# ========================================
st.set_page_config(page_title="Laboratorio Concreto", layout="wide")

# ========================================
# BARRA LATERAL PRESENTACIÓN
# ========================================
linkedin = "https://www.linkedin.com/in/danielorlando-ramirez/" 
email = "ingdanielrayez@gmail.com"

st.sidebar.markdown(
    "<div style='height:32px;'></div>",  
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

    /* Compactar márgenes del contenido principal */
    .block-container {
        padding-top: 1.4rem !important;   /* antes 0.6rem */
        padding-bottom: 0.6rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* Menos separación vertical entre bloques */
    div[data-testid="stVerticalBlock"] > div:has(> div.element-container) {
        gap: 0.35rem !important;
    }

    a.anchor-link {
        display: none !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 24px; /* antes 28px */
    }   

    /* Fondo destacado para el campo Carga */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFF8E1 !important;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

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

# Inicializar encabezado PDF (si no existe)
if "pdf_encabezado" not in st.session_state:
    st.session_state.pdf_encabezado = {
  
        "ciudad": "Medellín",
        "fecha_generacion": date.today().strftime("%d/%m/%Y %H:%M"),
        "obra": "",
        "desarrollado_por": "Daniel Ramírez",
    }

col1, col2, col3 = st.columns([5,3,2])

with col1:
    st.title("Compresión de Cilindros")

with col2:
    norma = "NTC 673 (Colombia)"
    url = "https://es.slideshare.net/slideshow/ntc-673-compresion-concretos/17107178"
    st.markdown(
        f"""
        <h5 style='text-align: right; font-weight: bold; margin: 0; color: #2E86C1; padding: 35px;'>
            <a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">
                {norma}
            </a>
        </h5>
    """,
    unsafe_allow_html=True
    )

with col3:
    fecha = date.today().strftime("%d/%m/%Y")
    st.markdown(
        f"<h5 style='text-align: right; font-weight: bold; margin: 0; padding: 35px;'>{fecha}</h5>",
        unsafe_allow_html=True
    )



# Formulario compacto (entre título y "Registro de Ensayo")
with st.form("form_encabezado_pdf", clear_on_submit=False):
    c1, c2, c3, c4 = st.columns([2, 2, 3, 3])
    with c1:
        ciudad = st.text_input("Ciudad", value=st.session_state.pdf_encabezado["ciudad"])
    with c2:
        fecha_gen = st.text_input("Fecha generación", value=st.session_state.pdf_encabezado["fecha_generacion"])
    with c3:
        obra = st.text_input("Obra", value=st.session_state.pdf_encabezado["obra"])
    with c4:
        desarrollado_por = st.text_input("Elaborado por", value=st.session_state.pdf_encabezado["desarrollado_por"])

    guardar_hdr = st.form_submit_button("Guardar encabezado", use_container_width=True)

if guardar_hdr:
    st.session_state.pdf_encabezado = {
        "ciudad": ciudad.strip(),
        "fecha_generacion": fecha_gen.strip(),
        "obra": obra.strip(),
        "desarrollado_por": desarrollado_por.strip(),
    }
   

st.markdown("### Registro de Ensayo")

col1, col2, col3 = st.columns(3)

with col1:
    muestra = st.text_input("Nombre de la muestra", placeholder="Ej: Muestra 1")
    dimensiones = st.selectbox("Dimensiones del cilindro", ["100x200 mm", "150x300 mm", "Otras dimensiones"], help="Selecciona las dimensiones estándar o elige 'Otras dimensiones' para ingresar medidas personalizadas")
    peso = st.number_input("Peso (kg)", value= None , placeholder="Ej: 3,5")

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

    with st.container(border=True):
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

    # Altura dinámica según número de ensayos (filas)
    altura_tabla = 38 + (len(df_display) * 35)  # header + filas

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=altura_tabla
    )
    
else:
    st.info("No se han registrado ensayos aún. Completa el formulario para agregar resultados.")

st.divider()
pdf_data = (
    generar_pdf(st.session_state.df_ensayos, st.session_state.pdf_encabezado)
    if not st.session_state.df_ensayos.empty
    else b""
)
st.download_button(
    label="Generar PDF",
    data=pdf_data,
    file_name=f"ensayos_compresion_{date.today().isoformat()}.pdf",
    mime="application/pdf",
    type="secondary",
    disabled=st.session_state.df_ensayos.empty,
)

