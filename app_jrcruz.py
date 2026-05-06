import streamlit as st
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="centered")

# Memoria para las áreas y el idioma
if 'lista_areas' not in st.session_state:
    st.session_state.lista_areas = []
if 'idioma' not in st.session_state:
    st.session_state.idioma = "Español"

# 2. Diccionario de Idiomas
textos = {
    "Español": {
        "eslogan": "Renovaciones y nueva construcción: Pisos y Baños",
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "🖼️ Catálogo"],
        "calc_titulo": "Calculadora de Materiales (Suma Total)",
        "nombre_sec": "Nombre de la sección",
        "largo": "Largo (ft)",
        "ancho": "Ancho (ft)",
        "btn_agregar": "Añadir al Total",
        "resumen": "Resumen del Proyecto",
        "borrar": "Borrar todo",
        "nomina_t": "Control de Nómina Semanal",
        "historial_t": "Historial de Clientes",
        "catalogo_t": "Catálogo de Trabajos"
    },
    "English": {
        "eslogan": "Renovations and new construction: Floors and Bathrooms",
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "🖼️ Catalog"],
        "calc_titulo": "Material Calculator (Total Sum)",
        "nombre_sec": "Section Name",
        "largo": "Length (ft)",
        "ancho": "Width (ft)",
        "btn_agregar": "Add to Total",
        "resumen": "Project Summary",
        "borrar": "Clear all",
        "nomina_t": "Weekly Payroll Control",
        "historial_t": "Customer History",
        "catalogo_t": "Work Catalog"
    }
}

# 3. Estilo Profesional
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1 { color: #1A4F8B; font-family: 'Helvetica'; margin-bottom: 0px; }
    .stButton>button { background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; }
    .total-destacado { padding: 15px; background-color: #f0f2f6; border-radius: 10px; border-left: 5px solid #1A4F8B; }
    </style>
    """, unsafe_allow_html=True)

# 4. Selector de Idioma en la parte superior
st.session_state.idioma = st.sidebar.radio("Language / Idioma", ["Español", "English"])
t = textos[st.session_state.idioma]

# 5. Encabezado (Logo y Título)
col_logo, col_txt = st.columns([1, 2.5])
with col_logo:
    try:
        st.image("5104.jpg", width=150)
    except:
        st.write("🏗️")
with col_txt:
    st.markdown(f"<h1>JR CRUZ MASONRY LLC</h1>", unsafe_allow_html=True)
    st.write(f"*{t['eslogan']}*")

st.markdown("---")

# 6. Menú Lateral Completo
choice = st.sidebar.selectbox("Menu", t["menu"])

if "Calculadora" in choice or "Calculator" in choice:
    st.header(t["calc_titulo"])
    with st.form("calc_form"):
        nombre = st.text_input(t["nombre_sec"], placeholder="Ej. Master Bath")
        c1, c2 = st.columns(2)
        largo = c1.number_input(t["largo"], min_value=0.0, step=0.5)
        ancho = c2.number_input(t["ancho"], min_value=0.0, step=0.5)
        btn = st.form_submit_button(t["btn_agregar"])
    
    if btn and largo > 0 and ancho > 0:
        st.session_state.lista_areas.append({"nombre": nombre, "sqft": largo * ancho})

    if st.session_state.lista_areas:
        st.subheader(t["resumen"])
        total = 0
        for item in st.session_state.lista_areas:
            st.write(f"📍 {item['nombre']}: {item['sqft']:.2f} sqft")
            total += item['sqft']
        
        st.markdown(f"<div class='total-destacado'><h2>TOTAL: {total:.2f} sqft</h2></div>", unsafe_allow_html=True)
        if st.button(t["borrar"]):
            st.session_state.lista_areas = []
            st.rerun()

elif "Nómina" in choice or "Payroll" in choice:
    st.header(t["nomina_t"])
    st.write("Módulo para registro de horas y pagos.")

elif "Historial" in choice or "History" in choice:
    st.header(t["historial_t"])
    st.write("Lista de presupuestos guardados anteriormente.")

elif "Catálogo" in choice or "Catalog" in choice:
    st.header(t["catalogo_t"])
    st.write("Galería de fotos de proyectos terminados.")

# Pie de página
st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC")
