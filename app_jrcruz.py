import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# Función para preparar la imagen de fondo
def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- CSS PARA LOGO SOMBREADO Y DISEÑO ---
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

# --- LÓGICA DE DATOS ---
def guardar_datos(df, filename):
    if not os.path.isfile(filename): df.to_csv(filename, index=False)
    else: df.to_csv(filename, mode='a', header=False, index=False)

# --- MENÚ LATERAL ---
idioma = st.sidebar.radio("🌐 Idioma", ["Español", "English"])
menu_options = {
    "Español": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo"],
    "English": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Catalog"]
}
choice = st.sidebar.selectbox("Seleccione una opción", menu_options[idioma])

# --- MÓDULOS PRINCIPALES ---

# 1. CALCULADORA
if "📊" in choice:
    st.title("📊 Calculadora de Área")
    with st.form("calc_form"):
        cliente = st.text_input("Nombre del Proyecto/Cliente")
        col1, col2 = st.columns(2)
        with col1: largo = st.number_input("Largo (ft)", min_value=0.0)
        with col2: ancho = st.number_input("Ancho (ft)", min_value=0.0)
        if st.form_submit_button("Calcular y Guardar"):
            total = round(largo * ancho, 2)
            nuevo = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), cliente, total]], columns=["Fecha", "Cliente", "Sqft"])
            guardar_datos(nuevo, "historial.csv")
            st.success(f"Total: {total} sqft")

# 2. NÓMINA
elif "👥" in choice:
    st.title("👥 Nómina Semanal")
    with st.form("nomina_form"):
        nombre = st.text_input("Nombre del Trabajador")
        h = st.number_input("Horas", min_value=0.0)
        p = st.number_input("Pago por Hora", min_value=0.0)
        if st.form_submit_button("Registrar Pago"):
            total_pago = h * p
            nuevo_p = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), nombre, total_pago]], columns=["Fecha", "Empleado", "Total"])
            guardar_datos(nuevo_p, "nomina.csv")
            st.info(f"Total a pagar: ${total_pago}")

# 3. HISTORIAL
elif "📋" in choice:
    st.title("📋 Historial de Registros")
    if os.path.exists("historial.csv"):
        st.subheader("Proyectos")
        st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
    if os.path.exists("nomina.csv"):
        st.subheader("Nómina")
        st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)

# 4. FOTOS
elif "📸" in choice:
    st.title("📸 Galería de Obra")
    archivo = st.file_uploader("Subir foto de progreso", type=["jpg", "png", "jpeg"])
    if archivo: st.image(archivo, use_container_width=True)

# 5. CATÁLOGO
elif "🛒" in choice:
    st.title("🛒 Catálogo Floor & Decor")
    # Nombres exactos de tus archivos en GitHub
    cat = [
        ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
        ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
        ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
        ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG")
    ]
    for i in range(0, len(cat), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(cat):
                n, l, img = cat[i+j]
                with cols[j]:
                    if os.path.exists(img): st.image(img, use_container_width=True)
                    st.subheader(n)
                    st.link_button(f"Ver {n}", l)

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
