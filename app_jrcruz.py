import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# Función para convertir el logo a base64 para usarlo como marca de agua
def get_base64_logo(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- CSS: LOGO SOMBREADO EN EL FONDO Y ESTILOS DE INTERFAZ ---
if os.path.exists("5104.jpg"):
    logo_base64 = get_base64_logo("5104.jpg")
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)), url("data:image/jpg;base64,{logo_base64}");
            background-size: 550px;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        .stButton>button {{ 
            width: 100%; 
            background-color: #1A4F8B; 
            color: white; 
            border-radius: 8px; 
            font-weight: bold; 
            height: 45px;
        }}
        [data-testid="stImage"] img {{ 
            border-radius: 15px; 
            object-fit: cover; 
            height: 280px; 
            border: 1px solid #ddd;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        }}
        h1, h2, h3 {{ color: #1A4F8B; }}
        </style>
    """, unsafe_allow_html=True)

# --- DICCIONARIO MAESTRO DE TRADUCCIONES ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])

texts = {
    "Español": {
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo"],
        "calc_t": "Calculadora de Área",
        "nom_t": "Nómina Semanal",
        "hist_t": "Historial de Registros",
        "foto_t": "Galería de Obra",
        "cat_t": "Catálogo (Materiales)",
        "cliente": "Nombre del Cliente / Proyecto",
        "largo": "Largo (ft)",
        "ancho": "Ancho (ft)",
        "btn_guardar": "Calcular y Guardar en Historial",
        "trabajador": "Nombre del Trabajador",
        "horas": "Horas Trabajadas",
        "pago": "Pago por Hora ($)",
        "btn_pago": "Registrar Pago en Nómina",
        "ver_mas": "Ver",
        "cat_list": [
            ("Loseta (Tile)", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Piedra (Stone)", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Madera (Wood)", "https://www.flooranddecor.com/wood", "wood.jpg.png"),
            ("Laminado (Laminate)", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinilo (Vinyl)", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decorativos (Backsplash)", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
            ("Baños y Gabinetes (Fixtures)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materiales (Grout/Cement)", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    },
    "English": {
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Catalog"],
        "calc_t": "Area Calculator",
        "nom_t": "Weekly Payroll",
        "hist_t": "Record History",
        "foto_t": "Work Gallery",
        "cat_t": "Catalog (Materials)",
        "cliente": "Client / Project Name",
        "largo": "Length (ft)",
        "ancho": "Width (ft)",
        "btn_guardar": "Calculate & Save to History",
        "trabajador": "Employee Name",
        "horas": "Hours Worked",
        "pago": "Pay per Hour ($)",
        "btn_pago": "Register Payment",
        "ver_mas": "View",
        "cat_list": [
            ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Wood", "https://www.flooranddecor.com/wood", "wood.jpg.png"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decoratives", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
            ("Fixtures (Bathroom)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Installation Materials", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    }
}

t = texts[idioma]

# --- LÓGICA DE ALMACENAMIENTO ---
def guardar_archivo(df, file):
    if not os.path.isfile(file): 
        df.to_csv(file, index=False)
    else: 
        df.to_csv(file, mode='a', header=False, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Menu", t["menu"])

# 1. CALCULADORA
if "📊" in choice:
    st.title(t["calc_t"])
    with st.form("calc"):
        c = st.text_input(t["cliente"])
        col1, col2 = st.columns(2)
        with col1: l = st.number_input(t["largo"], min_value=0.0, step=0.1)
        with col2: a = st.number_input(t["ancho"], min_value=0.0, step=0.1)
        if st.form_submit_button(t["btn_guardar"]):
            area_total = round(l * a, 2)
            df_calc = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), c, area_total]], columns=["Fecha", "Cliente", "Sqft"])
            guardar_archivo(df_calc, "historial.csv")
            st.success(f"Total: {area_total} sqft")

# 2. NÓMINA
elif "👥" in choice:
    st.title(t["nom_t"])
    with st.form("nom"):
        nombre = st.text_input(t["trabajador"])
        col_h, col_p = st.columns(2)
        with col_h: horas = st.number_input(t["horas"], min_value=0.0, step=0.5)
        with col_p: pago = st.number_input(t["pago"], min_value=0.0, step=1.0)
        if st.form_submit_button(t["btn_pago"]):
            total_nomina = round(horas * pago, 2)
            df_nom = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), nombre, total_nomina]], columns=["Fecha", "Empleado", "Total"])
            guardar_archivo(df_nom, "nomina.csv")
            st.info(f"Total: ${total_nomina}")

# 3. HISTORIAL
elif "📋" in choice:
    st.title(t["hist_t"])
    tab1, tab2 = st.tabs(["Projects / Proyectos", "Payroll / Nómina"])
    with tab1:
        if os.path.exists("historial.csv"): 
            st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
        else: st.write("No records yet.")
    with tab2:
        if os.path.exists("nomina.csv"): 
            st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)
        else: st.write("No records yet.")

# 4. FOTOS
elif "📸" in choice:
    st.title(t["foto_t"])
    uploaded_file = st.file_uploader("Upload Work Progress / Subir progreso", type=["jpg", "png", "jpeg"])
    if uploaded_file: 
        st.image(uploaded_file, caption="Work Progress", use_container_width=True)

# 5. CATÁLOGO COMPLETO (8 CATEGORÍAS)
elif "🛒" in choice:
    st.title(t["cat_t"])
    items = t["cat_list"]
    for i in range(0, len(items), 2):
        row_cols = st.columns(2)
        for j in range(2):
            if i + j < len(items):
                cat_name, cat_url, cat_img = items[i + j]
                with row_cols[j]:
                    if os.path.exists(cat_img): 
                        st.image(cat_img, use_container_width=True)
                    else:
                        st.warning(f"Missing file: {cat_img}")
                    st.subheader(cat_name)
                    st.link_button(t["ver_mas"], cat_url)
                    st.write("")

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC | Professional Service")
