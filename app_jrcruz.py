import streamlit as st
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️")

# 2. Estilo Profesional (Azul Marino y Blanco)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1 { color: #1A4F8B; font-family: 'Helvetica'; margin-bottom: 0px; }
    .stButton>button { 
        background-color: #1A4F8B; 
        color: white; 
        border-radius: 8px;
        border: 2px solid #000000;
        font-weight: bold;
    }
    .css-17lsk0u { color: #1A4F8B; } /* Color del texto lateral */
    </style>
    """, unsafe_allow_html=True)

# 3. MOSTRAR LOGO Y TÍTULO
col_logo, col_txt = st.columns([1, 2])
with col_logo:
    try:
        st.image("5104.jpg", width=150)
    except:
        st.write("🏗️") # Si la imagen no carga, muestra un icono

with col_txt:
    st.title("JR CRUZ MASONRY LLC")
    st.write("**Renovations and new construction: Floors and Bathrooms**")

st.markdown("---")

# 4. Panel de Control
menu = ["📊 Calculadora de Materiales", "👥 Nómina Semanal", "📋 Historial"]
choice = st.sidebar.selectbox("Panel de Control", menu)

if choice == "📊 Calculadora de Materiales":
    st.header("Estimado de Materiales")
    cliente = st.text_input("Nombre del Cliente")
    
    col1, col2 = st.columns(2)
    with col1:
        largo = st.number_input("Largo (ft)", min_value=0.0, step=0.5)
    with col2:
        ancho = st.number_input("Ancho (ft)", min_value=0.0, step=0.5)
        
    if largo > 0 and ancho > 0:
        area = largo * ancho
        st.success(f"Área Total: {area} sqft")
        
        # Cálculos de materiales
        cajas = (area * 1.10) / 15 # Ejemplo: cajas de 15 sqft + 10% desperdicio
        st.info(f"Necesitarás aproximadamente **{int(cajas)} cajas** de loseta.")
        
        if st.button("Guardar Presupuesto"):
            st.balloons()
            st.write(f"✅ Proyecto '{cliente}' registrado.")

# 5. Pie de página
st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC | Sistema Profesional")
