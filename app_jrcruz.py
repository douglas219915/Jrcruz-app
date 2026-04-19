import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# Función para el logo de fondo
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- CSS: LOGO SOMBREADO Y ESTILOS ---
if os.path.exists("5104.jpg"):
    bin_str = get_base64("5104.jpg")
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url("data:image/jpg;base64,{bin_str}");
            background-size: 500px;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; }}
        [data-testid="stImage"] img {{ border-radius: 15px; object-fit: cover; height: 250px; }}
        h1, h2, h3 {{ color: #1A4F8B; }}
        </style>
    """, unsafe_allow_html=True)

# --- DICCIONARIO COMPLETO DE TRADUCCIONES ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])

texts = {
    "Español": {
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo"],
        "calc_t": "Calculadora de Área",
        "nom_t": "Nómina Semanal",
        "hist_t": "Historial de Registros",
        "foto_t": "Galería de Obra",
        "cat_t": "Catálogo Floor & Decor",
        "cliente": "Nombre del Cliente",
        "largo": "Largo (ft)",
        "ancho": "Ancho (ft)",
        "btn_guardar": "Calcular y Guardar",
        "trabajador": "Nombre del Trabajador",
        "horas": "Horas Trabajadas",
        "pago": "Pago por Hora",
        "btn_pago": "Registrar Pago",
        "ver_mas": "Ver en Floor & Decor",
        "cat_list": [
            ("Loseta (Tile)", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Piedra (Stone)", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Madera (Wood)", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminado (Laminate)", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG")
        ]
    },
    "English": {
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Catalog"],
        "calc_t": "Area Calculator",
        "nom_t": "Weekly Payroll",
        "hist_t": "Record History",
        "foto_t": "Work Gallery",
        "cat_t": "Floor & Decor Catalog",
        "cliente": "Client Name",
        "largo": "Length (ft)",
        "ancho": "Width (ft)",
        "btn_guardar": "Calculate & Save",
        "trabajador": "Employee Name",
        "horas": "Hours Worked",
        "pago": "Pay per Hour",
        "btn_pago": "Register Payment",
        "ver_mas": "View at Floor & Decor",
        "cat_list": [
            ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG")
        ]
    }
}

t = texts[idioma]

# --- LÓGICA DE DATOS ---
def guardar(df, file):
    if not os.path.isfile(file): df.to_csv(file, index=False)
    else: df.to_csv(file, mode='a', header=False, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Menu", t["menu"])

# 1. CALCULADORA
if "📊" in choice:
    st.title(t["calc_t"])
    with st.form("calc"):
        c = st.text_input(t["cliente"])
        l = st.number_input(t["largo"], min_value=0.0)
        a = st.number_input(t["ancho"], min_value=0.0)
        if st.form_submit_button(t["btn_guardar"]):
            res = round(l * a, 2)
            guardar(pd.DataFrame([[datetime.now().date(), c, res]], columns=["Fecha", "Cliente", "Sqft"]), "historial.csv")
            st.success(f"Total: {res} sqft")

# 2. NÓMINA
elif "👥" in choice:
    st.title(t["nom_t"])
    with st.form("nom"):
        n = st.text_input(t["trabajador"])
        h = st.number_input(t["horas"], min_value=0.0)
        p = st.number_input(t["pago"], min_value=0.0)
        if st.form_submit_button(t["btn_pago"]):
            tot = h * p
            guardar(pd.DataFrame([[datetime.now().date(), n, tot]], columns=["Fecha", "Empleado", "Total"]), "nomina.csv")
            st.info(f"Total: ${tot}")

# 3. HISTORIAL
elif "📋" in choice:
    st.title(t["hist_t"])
    if os.path.exists("historial.csv"): 
        st.subheader("Projects / Proyectos")
        st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
    if os.path.exists("nomina.csv"): 
        st.subheader("Payroll / Nómina")
        st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)

# 4. FOTOS
elif "📸" in choice:
    st.title(t["foto_t"])
    f = st.file_uploader("Upload / Subir", type=["jpg", "png", "jpeg"])
    if f: st.image(f, use_container_width=True)

# 5. CATÁLOGO
elif "🛒" in choice:
    st.title(t["cat_t"])
    for i in range(0, len(t["cat_list"]), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(t["cat_list"]):
                name, link, img = t["cat_list"][i+j]
                with cols[j]:
                    if os.path.exists(img): st.image(img, use_container_width=True)
                    st.subheader(name)
                    st.link_button(t["ver_mas"], link)

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
