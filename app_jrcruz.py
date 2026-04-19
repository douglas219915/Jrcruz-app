import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# --- TRADUCCIONES ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])

texts = {
    "Español": {
        "sub": "**Remodelaciones y construcción: Pisos y Baños**",
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo Floor & Decor"],
        "calc_h": "Estimado de Materiales",
        "nom_h": "Registro de Pagos",
        "hist_h": "Registros Guardados",
        "gal_h": "Galería de Trabajos",
        "cat_h": "Productos Sugeridos (Floor & Decor)",
        "btn_save": "Guardar",
        "worker": "Nombre del Trabajador",
        "client": "Nombre del Cliente",
        "area": "Área Total"
    },
    "English": {
        "sub": "**Renovations and New Construction: Floors and Bathrooms**",
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Floor & Decor Catalog"],
        "calc_h": "Material Estimate",
        "nom_h": "Payment Records",
        "hist_h": "Saved Records",
        "gal_h": "Work Gallery",
        "cat_h": "Suggested Products (Floor & Decor)",
        "btn_save": "Save",
        "worker": "Worker Name",
        "client": "Client Name",
        "area": "Total Area"
    }
}

t = texts[idioma]

# --- FUNCIONES ---
def guardar_datos(df, filename):
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

# 2. Encabezado
col_logo, col_txt = st.columns([1, 3])
with col_logo:
    if os.path.exists("5104.jpg"): st.image("5104.jpg", width=150)
with col_txt:
    st.title("JR CRUZ MASONRY LLC")
    st.write(t["sub"])

st.markdown("---")

# 3. Menú Lateral
choice = st.sidebar.selectbox("Menu", t["menu"])

# --- MÓDULO: CALCULADORA ---
if "📊" in choice:
    st.header(t["calc_h"])
    with st.form("calc"):
        cliente = st.text_input(t["client"])
        largo = st.number_input("Largo (ft)", min_value=0.0)
        ancho = st.number_input("Ancho (ft)", min_value=0.0)
        if st.form_submit_button(t["btn_save"]):
            area = largo * ancho
            cajas = round((area * 1.10) / 15)
            st.success(f"{t['area']}: {area} sqft | Boxes: {cajas}")
            nuevo = pd.DataFrame([[datetime.now().date(), cliente, area]], columns=["Fecha", "Cliente", "Area"])
            guardar_datos(nuevo, "historial.csv")

# --- MÓDULO: NÓMINA ---
elif "👥" in choice:
    st.header(t["nom_h"])
    with st.form("nom"):
        emp = st.text_input(t["worker"])
        hrs = st.number_input("Hours", min_value=0.0)
        rate = st.number_input("Rate ($)", min_value=0.0)
        if st.form_submit_button(t["btn_save"]):
            total = hrs * rate
            nuevo_p = pd.DataFrame([[datetime.now().date(), emp, total]], columns=["Fecha", "Empleado", "Total"])
            guardar_datos(nuevo_p, "nomina.csv")
            st.success(f"Total: ${total}")

# --- MÓDULO: CATÁLOGO FLOOR & DECOR ---
elif "🛒" in choice:
    st.header(t["cat_h"])
    st.write("Selecciona una categoría para ver opciones en Floor & Decor:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Tile (Loseta)")
        st.image("https://images.flooranddecor.com/routing/tile.jpg", width=200) # Imagen de ejemplo
        st.link_button("Ver Tiles", "https://www.flooranddecor.com/tile")
        
    with col2:
        st.subheader("Wood (Madera)")
        st.image("https://images.flooranddecor.com/routing/wood.jpg", width=200)
        st.link_button("Ver Madera", "https://www.flooranddecor.com/hardwood")
        
    with col3:
        st.subheader("Stone (Piedra)")
        st.image("https://images.flooranddecor.com/routing/stone.jpg", width=200)
        st.link_button("Ver Piedra", "https://www.flooranddecor.com/stone")

# --- MÓDULO: HISTORIAL ---
elif "📋" in choice:
    st.header(t["hist_h"])
    if os.path.exists("nomina.csv"):
        st.write("### Payroll")
        st.dataframe(pd.read_csv("nomina.csv"))
    if os.path.exists("historial.csv"):
        st.write("### Projects")
        st.dataframe(pd.read_csv("historial.csv"))

# --- MÓDULO: FOTOS ---
elif "📸" in choice:
    st.header(t["gal_h"])
    foto = st.file_uploader("Upload Job Photo", type=["jpg", "png"])
    if foto: st.image(foto, use_container_width=True)

st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC")
