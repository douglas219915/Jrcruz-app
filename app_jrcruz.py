import streamlit as st
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="centered")

# Inicializar la lista de áreas en la memoria de la sesión si no existe
if 'lista_areas' not in st.session_state:
    st.session_state.lista_areas = []

# 2. Estilo Personalizado (Azul Marino y Blanco)
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
        width: 100%;
    }
    .total-box {
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        border-left: 8px solid #1A4F8B;
        margin-top: 20px;
    }
    .area-item {
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Encabezado con Logo y Título
with st.container():
    col_logo, col_txt = st.columns([1, 2.5])
    with col_logo:
        try:
            # Se usa el nombre del archivo que subiste
            st.image("5104.jpg", width=160, output_format="JPEG")
        except:
            st.write("🏗️ [Logo no encontrado]")
        
    with col_txt:
        st.write("") # Espacio para alinear
        st.markdown("<h1>JR CRUZ MASONRY LLC</h1>", unsafe_allow_html=True)
        st.write("**Renovations and new construction: Floors and Bathrooms**")

st.markdown("---")

# 4. Menú Lateral
st.sidebar.header("Panel de Control")
menu = ["📊 Calculadora de Áreas", "👥 Nómina Semanal"]
choice = st.sidebar.selectbox("Seleccione una opción:", menu)

if choice == "📊 Calculadora de Áreas":
    st.header("Calculadora de Pies Cuadrados Acumulados")
    
    # Formulario para añadir áreas
    with st.expander("➕ Añadir Nueva Sección (Baño, Sala, Cocina...)", expanded=True):
        with st.form("nuevo_item"):
            nombre_seccion = st.text_input("Nombre de la sección", placeholder="Ej. Master Bathroom")
            c1, c2 = st.columns(2)
            largo_ft = c1.number_input("Largo (ft)", min_value=0.0, step=0.5)
            ancho_ft = c2.number_input("Ancho (ft)", min_value=0.0, step=0.5)
            
            submit_btn = st.form_submit_button("Agregar al Presupuesto")
            
            if submit_btn:
                if largo_ft > 0 and ancho_ft > 0:
                    area_total = largo_ft * ancho_ft
                    st.session_state.lista_areas.append({
                        "nombre": nombre_seccion if nombre_seccion else f"Área {len(st.session_state.lista_areas)+1}",
                        "sqft": area_total
                    })
                    st.success(f"¡Agregado!")
                else:
                    st.error("Por favor ingresa medidas válidas.")

    # 5. Mostrar la Lista y el Gran Total
    if st.session_state.lista_areas:
        st.subheader("Resumen del Proyecto")
        
        gran_total_sqft = 0
        for item in st.session_state.lista_areas:
            st.markdown(f"""
                <div class="area-item">
                    📍 <b>{item['nombre']}</b>: {item['sqft']:.2f} sqft
                </div>
            """, unsafe_allow_html=True)
            gran_total_sqft += item['sqft']
        
        # Caja destacada con el resultado final
        estimado_cajas = round((gran_total_sqft * 1.10) / 15) # +10% de desperdicio
        
        st.markdown(f"""
            <div class="total-box">
                <p style='margin:0; font-size: 1.2em;'>Pies Cuadrados Totales:</p>
                <h2 style='margin:0; color:#1A4F8B;'>{gran_total_sqft:.2f} sqft</h2>
                <hr>
                <p style='margin:0;'>📦 Estimado de cajas (basado en 15 sqft por caja + 10% de desperdicio):</p>
                <h3 style='margin:0;'>{estimado_cajas} cajas</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón para limpiar
        st.write("")
        if st.button("🗑️ Borrar todo y empezar nuevo proyecto"):
            st.session_state.lista_areas = []
            st.rerun()
    else:
        st.info("No hay áreas agregadas todavía. Usa el formulario de arriba para empezar.")

elif choice == "👥 Nómina Semanal":
    st.header("Control de Nómina")
    st.info("Esta sección estará disponible próximamente para llevar el control de pagos.")

# 6. Pie de Página
st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC | Gestión Profesional")
