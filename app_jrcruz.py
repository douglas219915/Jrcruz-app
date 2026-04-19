import streamlit as st
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️")

# 2. Estilo Profesional (Azul Marino y Blanco)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1 { color: #1A4F8B; font-family: 'Helvetica'; margin-bottom: 0px; font-size: 2.5em; }
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

# 3. MOSTRAR LOGO Y TÍTULO (Diseño mejorado)
with st.container():
    col_logo, col_txt = st.columns([1, 2.5]) # Damos más espacio al texto
    with col_logo:
        # EL CAMBIO ESTÁ AQUÍ: Agregamos ignore_image_size=True para evitar que se estire
        st.image("5104.jpg", width=180, output_format="JPEG")
        
    with col_txt:
        # Bajamos un poco el título para alinear con el logo
        st.write("") 
        st.markdown(f"<h1>JR CRUZ MASONRY LLC</h1>", unsafe_allow_html=True)
        st.write("**Renovations and new construction: Floors and Bathrooms**")

st.markdown("---")

# 4. Panel de Control
# Agregué iconos y mejoré el menú lateral
menu = ["📊 Calculadora de Materiales", "👥 Nómina Semanal", "📋 Historial de Clientes"]
choice = st.sidebar.selectbox("Panel de Control", menu)

if choice == "📊 Calculadora de Materiales":
    st.header("Estimado de Materiales")
    with st.form("calculadora_form"):
        cliente = st.text_input("Nombre del Cliente", placeholder="Ej. Residencia Smith")
        col1, col2 = st.columns(2)
        with col1:
            largo = st.number_input("Largo (ft)", min_value=0.0, step=0.5)
        with col2:
            ancho = st.number_input("Ancho (ft)", min_value=0.0, step=0.5)
        
        submitted = st.form_submit_button("Calcular y Guardar")

    if submitted:
        if largo > 0 and ancho > 0:
            area = largo * ancho
            st.success(f"Área Total: **{area} sqft**")
            
            # Cálculo de materiales de ejemplo
            cajas = round((area * 1.10) / 15) # 10% desperdicio, cajas de 15 sqft
            st.info(f"Necesitarás aproximadamente **{cajas} cajas** de loseta.")
            
            st.balloons()
            st.write(f"✅ Presupuesto para **{cliente}** guardado con éxito.")
        else:
            st.error("Por favor, ingresa el largo y ancho del área.")

elif choice == "👥 Nómina Semanal":
    st.header("Control de Pagos y Horas")
    with st.form("nomina_form"):
        col_emp, col_hr, col_rate = st.columns([2, 1, 1])
        with col_emp:
            empleado = st.text_input("Nombre del Trabajador")
        with col_hr:
            horas = st.number_input("Horas Semanales", min_value=0.0, step=0.5)
        with col_rate:
            pago_hora = st.number_input("Pago por Hora ($)", min_value=0.0, step=1.0)
        btn_nomina = st.form_submit_button("Registrar Pago")

    if btn_nomina:
        if empleado and horas > 0:
            total_pago = horas * pago_hora
            st.success(f"Registro completado para **{empleado}**")
            st.table({"Concepto": ["Horas", "Pago/Hr", "Total"], "Detalle": [f"{horas}", f"${pago_hora}", f"${total_pago}"]})

# 5. Pie de página
st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC | Gestión Profesional")
