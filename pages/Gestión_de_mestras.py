import streamlit as st
import pandas as pd
from datetime import datetime
import os
import sys

# Agregar la carpeta ensayos al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ensayos'))

# Importar lista de ensayos disponibles
try:
    from cubos_cemento import get_tests as get_cement_tests
    from granulometria import get_tests as get_aggregate_tests
    from ensayo_compresion import get_tests as get_concrete_tests
except ImportError:
    # Fallback si los módulos no tienen la función get_tests
    cement_tests = ["Resistencia a compresión", "Finura Blaine", "Fraguado"]
    aggregate_tests = ["Granulometría", "Módulo de finura", "Absorción"]
    concrete_tests = ["Resistencia a compresión", "Asentamiento", "Slump"]

st.set_page_config(page_title="Gestión de Muestras", layout="wide")

st.title("🔬 Gestión de Muestras")
st.markdown("---")

# Inicializar session state
if 'muestras' not in st.session_state:
    st.session_state.muestras = []

# Tipos de muestras disponibles
TIPOS_MUESTRA = {
    "Cemento": {
        "icon": "🏭",
        "tests": ["Resistencia a compresión", "Finura Blaine", "Fraguado", "Autoclavado"]
    },
    "Agregado Grueso": {
        "icon": "⚫",
        "tests": ["Granulometría", "Módulo de finura", "Absorción", "Densidad"]
    },
    "Agregado Fino": {
        "icon": "🟤",
        "tests": ["Granulometría", "Módulo de finura", "Absorción", "Densidad", "Equivalente de arena"]
    },
    "Concreto": {
        "icon": "🏗️",
        "tests": ["Resistencia a compresión", "Asentamiento (Slump)", "Densidad", "Contenido de aire"]
    }
}

# Formulario para agregar nueva muestra
st.subheader("➕ Registrar Nueva Muestra")

col1, col2, col3 = st.columns(3)

with col1:
    tipo_muestra = st.selectbox(
        "Tipo de Muestra",
        options=list(TIPOS_MUESTRA.keys()),
        key="tipo_muestra"
    )

with col2:
    obra = st.text_input(
        "Obra/Proyecto",
        placeholder="Nombre de la obra",
        help="Seleccione o ingrese la obra a la que pertenece la muestra (módulo en desarrollo)"
    )

with col3:
    codigo_muestra = st.text_input(
        "Código de Muestra",
        placeholder="ej: MU-001-2024",
        help="Identificador único de la muestra"
    )

col4, col5 = st.columns(2)

with col4:
    fecha_ingreso = st.date_input(
        "Fecha de Ingreso",
        value=datetime.today()
    )

with col5:
    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        value=1,
        help="Número de especímenes/unidades"
    )

# Selección de ensayos
st.markdown("#### Ensayos a Realizar")
ensayos_disponibles = TIPOS_MUESTRA[tipo_muestra]["tests"]

col_ensayos = st.columns(2)
ensayos_seleccionados = []

for idx, ensayo in enumerate(ensayos_disponibles):
    col = col_ensayos[idx % 2]
    if col.checkbox(ensayo, key=f"ensayo_{ensayo}"):
        ensayos_seleccionados.append(ensayo)

# Comentarios adicionales
st.markdown("#### Comentarios Adicionales")
comentarios = st.text_area(
    "Notas",
    placeholder="Agregue comentarios, observaciones o información relevante sobre la muestra...",
    height=100,
    label_visibility="collapsed"
)

# Botón para agregar muestra
col_btn1, col_btn2 = st.columns([1, 5])

with col_btn1:
    if st.button("✅ Registrar Muestra", use_container_width=True):
        if not codigo_muestra:
            st.error("⚠️ Por favor ingrese un código de muestra")
        elif not obra:
            st.error("⚠️ Por favor seleccione una obra")
        elif not ensayos_seleccionados:
            st.error("⚠️ Por favor seleccione al menos un ensayo")
        else:
            nueva_muestra = {
                "Código": codigo_muestra,
                "Tipo": tipo_muestra,
                "Obra": obra,
                "Fecha Ingreso": fecha_ingreso.strftime("%d/%m/%Y"),
                "Cantidad": int(cantidad),
                "Ensayos": ", ".join(ensayos_seleccionados),
                "Comentarios": comentarios,
                "Estado": "Pendiente"
            }
            st.session_state.muestras.append(nueva_muestra)
            st.success(f"✅ Muestra '{codigo_muestra}' registrada correctamente")
            st.rerun()

# Mostrar muestras registradas
st.markdown("---")
st.subheader("📋 Muestras Registradas")

if st.session_state.muestras:
    # Filtros
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        filtro_tipo = st.multiselect(
            "Filtrar por tipo",
            options=list(TIPOS_MUESTRA.keys()),
            default=list(TIPOS_MUESTRA.keys())
        )
    
    with col_f2:
        filtro_obra = st.multiselect(
            "Filtrar por obra",
            options=list(set([m["Obra"] for m in st.session_state.muestras])),
            default=list(set([m["Obra"] for m in st.session_state.muestras]))
        )
    
    with col_f3:
        filtro_estado = st.multiselect(
            "Filtrar por estado",
            options=["Pendiente", "En Proceso", "Completado"],
            default=["Pendiente", "En Proceso", "Completado"]
        )
    
    # Aplicar filtros
    muestras_filtradas = [
        m for m in st.session_state.muestras 
        if m["Tipo"] in filtro_tipo and m["Obra"] in filtro_obra and m["Estado"] in filtro_estado
    ]
    
    if muestras_filtradas:
        # Crear DataFrame para mostrar
        df_muestras = pd.DataFrame(muestras_filtradas)
        
        # Mostrar tabla
        st.dataframe(df_muestras, use_container_width=True)
        
        # Expandible con detalles
        st.markdown("#### Detalles de Muestras")
        for idx, muestra in enumerate(muestras_filtradas):
            with st.expander(f"📦 {muestra['Código']} - {muestra['Tipo']} ({muestra['Estado']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Obra:** {muestra['Obra']}")
                    st.write(f"**Tipo:** {muestra['Tipo']}")
                    st.write(f"**Cantidad:** {muestra['Cantidad']} unidad(es)")
                    st.write(f"**Fecha Ingreso:** {muestra['Fecha Ingreso']}")
                
                with col2:
                    nuevo_estado = st.selectbox(
                        "Estado",
                        options=["Pendiente", "En Proceso", "Completado"],
                        index=["Pendiente", "En Proceso", "Completado"].index(muestra["Estado"]),
                        key=f"estado_{idx}"
                    )
                    if nuevo_estado != muestra["Estado"]:
                        st.session_state.muestras[st.session_state.muestras.index(muestra)]["Estado"] = nuevo_estado
                        st.rerun()
                
                st.markdown("**Ensayos a Realizar:**")
                st.write(muestra['Ensayos'])
                
                if muestra['Comentarios']:
                    st.markdown("**Comentarios:**")
                    st.info(muestra['Comentarios'])
                
                # Opción de eliminar
                if st.button("🗑️ Eliminar muestra", key=f"btn_delete_{idx}"):
                    st.session_state.muestras.pop(st.session_state.muestras.index(muestra))
                    st.success("Muestra eliminada")
                    st.rerun()
    else:
        st.info("No hay muestras que coincidan con los filtros seleccionados")
else:
    st.info("📭 No hay muestras registradas aún. Complete el formulario para agregar una nueva muestra.")

# Barra inferior con información
st.markdown("---")
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.metric("Total de Muestras", len(st.session_state.muestras))

with col_info2:
    pendientes = len([m for m in st.session_state.muestras if m["Estado"] == "Pendiente"])
    st.metric("Muestras Pendientes", pendientes)

with col_info3:
    completadas = len([m for m in st.session_state.muestras if m["Estado"] == "Completado"])
    st.metric("Muestras Completadas", completadas)

st.caption("💡 Nota: Las obras y módulos de gestión están en desarrollo")
