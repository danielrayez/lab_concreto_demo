import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# ========================================
# BARRA LATERAL PRESENTACIÓN
# ========================================

linkedin = "https://www.linkedin.com/in/danielorlando-ramirez/" 
email = "ingdanielrayez@gmail.com"

st.sidebar.markdown("---")

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
        background-color: #fafafa;
    }
    a.anchor-link {
        display: none !important;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ========================================
# CONFIGURACIÓN INICIAL
# ========================================

st.set_page_config(page_title="Laboratorio Concreto", layout="wide")

st.title("Ensayo de Compresión de Cubos de Cemento")

# ========================================
# SECCIÓN 1: INFORMACIÓN Y PARÁMETROS
# ========================================

col1, col2, col3 = st.columns(3)

with col1:
    tipo_cemento = st.selectbox(
        "Tipo de Cemento:",
        options=["Cemento Portland Ordinario", "Cemento Portland Compuesto", "Cemento de Escoria", "Otro"],
        index=0,
        key='tipo_cemento_select'
    )

with col2:
    st.write("")
    norma = "NTC 220 (Colombia)"
    url = "https://www.icontec.org"
    st.markdown(
        f"""
        <h5 style='text-align: left; font-weight: bold; margin: 0; color: #2E86C1; padding: 0;'>
            <a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">
                {norma}
            </a>
        </h5>
    """,
    unsafe_allow_html=True
    )

with col3:
    fecha = date.today().strftime("%d/%m/%Y")
    st.markdown(f"<h5 style='text-align: left; font-weight: bold; margin: 0; padding: 15px;'>{fecha}</h5>", unsafe_allow_html=True)

st.divider()

# ========================================
# SECCIÓN 2: INFORMACIÓN GENERAL DEL ENSAYO
# ========================================

st.write("### Información del Ensayo")

col1, col2, col3 = st.columns(3)

with col1:
    lote_cemento = st.text_input("Lote de Cemento:", value="")
    edad_ensayo = st.selectbox("Edad de Ensayo (días):", [3, 7, 28], index=2)

with col2:
    fecha_fabricacion = st.date_input("Fecha de Fabricación:")
    humedad_ambiente = st.number_input("Humedad Relativa (%):", min_value=0.0, max_value=100.0, value=65.0)

with col3:
    temperatura_ambiente = st.number_input("Temperatura Ambiente (°C):", min_value=0.0, max_value=50.0, value=21.0)
    laboratorista = st.text_input("Laboratorista:", value="")

st.divider()

# ========================================
# SECCIÓN 3: TABLA DE DATOS DE CUBOS
# ========================================

st.write("### Resultados de Compresión - Cubos de 50 mm")

# Inicializar datos
num_cubos = st.number_input("Número de Cubos a Ensayar:", min_value=1, max_value=10, value=3, step=1)

# Crear tabla de entrada
datos_cubos = []
cols_header = st.columns([1, 2, 2, 2, 2, 2])
with cols_header[0]:
    st.write("**Cubo No.**")
with cols_header[1]:
    st.write("**Masa (g)**")
with cols_header[2]:
    st.write("**Fuerza Máxima (kN)**")
with cols_header[3]:
    st.write("**Resistencia (MPa)**")
with cols_header[4]:
    st.write("**Observaciones**")
with cols_header[5]:
    st.write("**Válido**")

for i in range(num_cubos):
    cols = st.columns([1, 2, 2, 2, 2, 2])
    
    with cols[0]:
        st.write(f"#{i+1}")
    
    with cols[1]:
        masa = st.number_input(
            f"Masa cubo {i+1}",
            min_value=0.0,
            value=330.0,
            step=0.1,
            label_visibility="collapsed",
            key=f"masa_{i}"
        )
    
    with cols[2]:
        fuerza_kn = st.number_input(
            f"Fuerza cubo {i+1}",
            min_value=0.0,
            value=0.0,
            step=0.1,
            label_visibility="collapsed",
            key=f"fuerza_{i}"
        )
    
    # Calcular resistencia: R = F / A, donde A = 50mm x 50mm = 2500 mm²
    resistencia_mpa = (fuerza_kn * 1000) / 2500 if fuerza_kn > 0 else 0.0
    
    with cols[3]:
        st.write(f"{resistencia_mpa:.2f}")
    
    with cols[4]:
        observaciones = st.text_input(
            f"Observaciones cubo {i+1}",
            value="",
            label_visibility="collapsed",
            key=f"obs_{i}"
        )
    
    with cols[5]:
        valido = st.checkbox(
            f"Válido {i+1}",
            value=True,
            label_visibility="collapsed",
            key=f"valido_{i}"
        )
    
    datos_cubos.append({
        'Cubo': f"#{i+1}",
        'Masa (g)': masa,
        'Fuerza (kN)': fuerza_kn,
        'Resistencia (MPa)': resistencia_mpa,
        'Observaciones': observaciones,
        'Válido': valido
    })

df_cubos = pd.DataFrame(datos_cubos)

st.divider()

# ========================================
# SECCIÓN 4: ANÁLISIS DE RESULTADOS
# ========================================

st.write("### Análisis de Resultados")

# Filtrar solo cubos válidos
df_validos = df_cubos[df_cubos['Válido'] == True]

if len(df_validos) > 0:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        resistencia_media = df_validos['Resistencia (MPa)'].mean()
        st.metric("Resistencia Media", f"{resistencia_media:.2f} MPa")
    
    with col2:
        resistencia_min = df_validos['Resistencia (MPa)'].min()
        st.metric("Resistencia Mínima", f"{resistencia_min:.2f} MPa")
    
    with col3:
        resistencia_max = df_validos['Resistencia (MPa)'].max()
        st.metric("Resistencia Máxima", f"{resistencia_max:.2f} MPa")
    
    with col4:
        coef_variacion = (df_validos['Resistencia (MPa)'].std() / resistencia_media * 100) if resistencia_media > 0 else 0
        st.metric("Coef. Variación", f"{coef_variacion:.2f} %")

st.divider()

# ========================================
# SECCIÓN 5: GRÁFICO DE RESULTADOS
# ========================================

st.write("### Gráfico de Resistencia por Cubo")

fig, ax = plt.subplots(figsize=(10, 6))

colores = ['green' if valido else 'red' for valido in df_cubos['Válido']]
ax.bar(df_cubos['Cubo'], df_cubos['Resistencia (MPa)'], color=colores, alpha=0.7, edgecolor='black')

if len(df_validos) > 0:
    ax.axhline(y=df_validos['Resistencia (MPa)'].mean(), color='blue', linestyle='--', linewidth=2, label='Resistencia Media')

ax.set_xlabel('Cubo', fontsize=12, fontweight='bold')
ax.set_ylabel('Resistencia (MPa)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
ax.legend(fontsize=11)
plt.tight_layout()

st.pyplot(fig)

st.divider()

# ========================================
# SECCIÓN 6: DESCARGA DE RESULTADOS
# ========================================

if st.button("Descargar Resultados como CSV"):
    csv_data = df_cubos.to_csv(index=False)
    st.download_button(
        label="Descargar CSV",
        data=csv_data,
        file_name=f"ensayo_compresion_{fecha.replace('/', '-')}.csv",
        mime="text/csv"
    )

if st.button("Descargar Gráfico"):
    fig.savefig("grafico_compresion_cubos.png", dpi=300, bbox_inches='tight')
    st.success("Gráfico descargado como 'grafico_compresion_cubos.png'")
