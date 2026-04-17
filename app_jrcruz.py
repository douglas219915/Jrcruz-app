import streamlit as st
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="centered")

# 2. Diseño y Colores (Azul Marino y Blanco)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1 { color: #1A4F8B; font-family: 'Arial'; border-bottom: 3px solid #000000; }
    .stButton>button { 
        background-color: #1A4F8B; 
        color: white; 
        width: 100%; 
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .sidebar .sidebar-content { background-color: #1A4F8B; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Encabezado con Imagen (Usaremos el nombre por ahora mientras vinculas tu imagen real)
st.title("🏗️ JR CRUZ MASONRY LLC")
st.markdown("### *Renovations and new construction: Floors and Bathrooms*")

# 4. Navegación
menu = ["📊 Calculadora de Materiales", "👥 Nómina Semanal", "📋 Historial de Clientes"]
choice = st.sidebar.selectbox("Panel de Control", menu)

if choice == "📊 Calculadora de Materiales":
    st.header("Estimado de Materiales")
    
    with st.container():
        cliente = st.text_input("Nombre del Cliente", placeholder="Ej. Residencia Smith")
        col1, col2 = st.columns(2)
        with col1:
            largo = st.number_input("Largo del piso (ft)", min_value=0.0, step=1.0)
        with col2:
            ancho = st.number_input("Ancho del piso (ft)", min_value=0.0, step=1.0)
            
    if largo > 0 and ancho > 0:
        area = largo * ancho
        st.success(f"Área Total: **{area} sqft**")
        
        # Cálculos rápidos de ejemplo
        bultos_thinset = round(area / 60) # Aproximación estándar
        st.info(f"📦 Material sugerido: **{bultos_thinset} bultos de Thinset** (aprox).")
        
        if st.button("Generar Presupuesto"):
            st.balloons()
            st.write(f"✅ Presupuesto para {cliente} listo para enviar.")

elif choice == "👥 Nómina Semanal":
    st.header("Control de Pagos")
    st.write("Aquí podrás marcar las horas de tus muchachos.")
    # Próximamente agregaremos la tabla de horas aquí

# Pie de página
st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC | Sistema de Gestión Profesional")
