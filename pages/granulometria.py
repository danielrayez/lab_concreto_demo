import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import date

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

col1, col2, col3 = st.columns([5,3,2])
with col1:
    st.title("Análisis Granulométrico")

with col2:
    norma = "NTC 174 (Colombia)"
    url = "https://www.icontec.org"
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
    st.markdown(f"<h5 style='text-align: right; font-weight: bold; margin: 0; padding: 35px;'>{fecha}</h5>", unsafe_allow_html=True)
    
# ========================================
# SECCIÓN 1: Datos de entrada
# ========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.write("### Datos de entrada")

with col2:
    muestra = st.text_input("Nombre de la muestra", placeholder="Ej: Muestra 1")

with col3:
    try:
        df = pd.read_csv(r'C:\Lab_concreto_beta\ensayos\gram_limites.txt')
        df["tamaño-tmn"] = df.apply(
        lambda x: f"#{x['#tamanio']}-{x['TMN']}"
        if x["#tamanio"].isdigit()
        else x["TMN"],
        axis=1
)
        agg = st.selectbox("Selecciona el tipo de agregado", options=df['tamaño-tmn'].unique(), index=0, key='TMN_select')
        df_agg = df[df['tamaño-tmn'] == agg].copy()
        df_agg = df_agg.sort_values('tamiz_mm', ascending=False)
    except FileNotFoundError:
        st.error("Archivo 'gram_limites.txt' no encontrado")
        st.stop()


st.divider()

# ========================================
# SECCIÓN 2: TABLA DE DATOS
# ========================================
st.write(f"### Límites Granulométricos y resultados ensayo - {agg}")

col1, col2, col3, = st.columns([4,3,3])
with col1:
    peso_muestra = st.number_input("Peso inicial (g)", value = 100.0,  step = 0.1 )

df_display = df_agg[['tamiz_mm', 'limite_max', 'limite_min']].copy()
df_display.columns = ['Tamiz (mm)', 'Límite Máx (%)', 'Límite Mín (%)']
# df_display[""]
df_display['Retenido (g)'] = 0.0

# Crear inputs para la columna Retenido (g)

col_c1, col_c2, col_c3, col_c4, col_c5, col_c6, col_c7 = st.columns(7, gap="small")

with col_c1:
    st.write("**Tamiz (mm)**")
with col_c2:
    st.write("**Límite Máx (%)**")
with col_c3:
    st.write("**Límite Mín (%)**")
with col_c4:
    st.write("**Retenido (g) 🖊️**")
with col_c5:
    st.write("**Retenido (%)**")
with col_c6:
    st.write("**% Ret. Acum.**")
with col_c7:
    st.write("**% Pasante**")

pasa_inputs = []
retenido_acumulado = 0.0
pasante_values = []



for idx, row in df_display.iterrows():
    col_1, col_2, col_3, col_4, col_5, col_6, col_7 = st.columns(7, gap="small")
    with col_1:
        st.write(f"{row['Tamiz (mm)']}")
    with col_2:
        st.write(f"{row['Límite Máx (%)']}")
    with col_3:
        st.write(f"{row['Límite Mín (%)']}")
    with col_4:
        pasa_value = st.number_input(
            f"Retenido (g) {idx}",
            min_value=0.0,
            max_value= peso_muestra,
            value=0.0,
            label_visibility="collapsed",
            key=f"pasa_{idx}"
        )
        pasa_inputs.append(pasa_value)

    with col_5:
        retenido_porcentaje = (pasa_value / peso_muestra * 100) if peso_muestra > 0 else 0
        st.write(f"{retenido_porcentaje:.2f}")
    
    with col_6:
        retenido_acumulado += retenido_porcentaje
        st.write(f"{retenido_acumulado:.2f}")
    
    
    with col_7:
        pasante_porcentaje = 100 - retenido_acumulado
        pasante_values.append(pasante_porcentaje)
        st.write(f"{pasante_porcentaje:.2f}")
        
df_display['Retenido (g)'] = pasa_inputs
df_display['% Pasante'] = pasante_values

# Mostrar total de pasante
col_1, col_2, col_3, col_4, col_5, col_6, col_7 = st.columns(7)
with col_5:
    total_pasante = sum(pasa_inputs)
    st.write(f"**{total_pasante:.2f}**")

# ========================================
# SECCIÓN 2: GRÁFICO GRANULOMÉTRICO
# ========================================

fig, ax = plt.subplots(figsize=(10, 6))

# Graficar límites máximos y mínimos
ax.plot(df_agg['tamiz_mm'], df_agg['limite_max'], 'r--o', label='Límite Máximo', linewidth=1, markersize=6)
ax.plot(df_agg['tamiz_mm'], df_agg['limite_min'], 'b--o', label='Límite Mínimo', linewidth=1, markersize=6)

ax.plot(df_display['Tamiz (mm)'], df_display['% Pasante'], 'y--s', label='% Pasante', linewidth=1, markersize=6)

# Llenar el área entre límites
ax.fill_between(df_agg['tamiz_mm'], df_agg['limite_min'], df_agg['limite_max'], alpha=0.2, color='lightgreen')

# Configurar ejes
ax.set_xlabel('Tamiz (mm)', fontsize=12)
ax.set_ylabel('Porcentaje Retenido Acumulado (%)', fontsize=12)
# ax.set_title(f'Límites Granulométricos - Norma NTC174 ({agg})', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.5)
ax.legend(fontsize=11)

# Configurar escala logarítmica en eje x
ax.set_xscale('log')

tamices = df_agg["tamiz_mm"].values

ax.set_xticks(tamices)
ax.set_xticklabels([f"{t:g}" for t in tamices])

ax.xaxis.set_minor_locator(ticker.NullLocator()) 

# Invertir eje x
ax.invert_xaxis()

plt.tight_layout()

st.pyplot(fig)

# un boton para descargar la pantalla como imagen
if st.button("Descargar gráfico"):
    fig.savefig("grafico_granulometrico.png")
    st.success("Gráfico descargado como 'grafico_granulometrico.png'")

