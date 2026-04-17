import streamlit as st
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️")

# 2. Estilo personalizado (Azul Marino y Blanco)
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stButton>button { 
        background-color: #1A4F8B; 
        color: white; 
        border-radius: 10px;
        border: 2px solid #000000;
    }
    h1 { color: #1A4F8B; border-bottom: 2px solid #000000; }
    </style>
    """, unsafe_allow_html=True)

# 3. Título y Eslogan
st.title("🏗️ JR CRUZ MASONRY LLC")
st.write("### *Renovations and new construction: Floors and Bathrooms*")

# 4. Menú Lateral
st.sidebar.header("Menú de Control")
opcion = st.sidebar.selectbox("¿Qué desea hacer?", ["Nuevo Presupuesto", "Nómina", "Inventario"])

if opcion == "Nuevo Presupuesto":
    st.subheader("📊 Calculadora de Materiales")
    cliente = st.text_input("Nombre del Cliente")
    col1, col2 = st.columns(2)
    with col1:
        largo = st.number_input("Largo (ft)", min_value=0.0)
    with col2:
        ancho = st.number_input("Ancho (ft)", min_value=0.0)
    
    if largo > 0 and ancho > 0:
        area = largo * ancho
        st.info(f"El área total es de: {area} sqft")
        if st.button("Guardar Cotización"):
            st.success(f"Cotización para {cliente} guardada con éxito.")

elif opcion == "Nómina":
    st.subheader("👥 Registro de Empleados")
    st.write("Módulo de pagos en construcción...")

# Pie de página
st.write("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC | Gestión Profesional")
