import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# --- CSS PROFESIONAL PARA EL LOGO Y DISEÑO (NO TOCAR) ---
st.markdown("""
    <style>
    /* Asegurar que el logo sea grande, nítido y completo (sin recortes) */
    .header-logo img {
        width: 100% !important;
        max-width: 500px !important; /* Ajusta este tamaño si lo quieres más grande o pequeño */
        height: auto !important;
        image-rendering: -webkit-optimize-contrast; /* Mejorar nitidez en iPad */
        object-fit: contain !important; /* Importante: muestra la imagen completa */
        border-radius: 15px;
    }
    .header-col {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Estilo de botones generales */
    .stButton>button { width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; }
    h1, h2, h3 { color: #1A4F8B; }
    </style>
    """, unsafe_allow_html=True)

# --- IDIOMA ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])

# --- DICCIONARIOS ---
texts = {
    "Español": {
        "sub": "Remodelaciones y Construcción: Pisos y Baños",
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo Floor & Decor"],
        "save_btn": "Guardar Datos",
        "cat_h": "Productos Sugeridos (Ambientes)",
        "categories": [
            ("Loseta (Tile)", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Piedra (Marble)", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Madera (Wood)", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminado", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinilo (Vinyl)", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decorativos (Backsplash)", "https://www.flooranddecor.com/decorative-tile", "decoratives.jpg.jpeg"),
            ("Baños/Gabinetes (Fixtures)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materiales (Grout)", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    },
    "English": {
        "sub": "Renovations and New Construction: Floors and Bathrooms",
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Floor & Decor Catalog"],
        "save_btn": "Save Data",
        "cat_h": "Suggested Products (Environments)",
        "categories": [
            ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Stone (Marble)", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decoratives (Backsplash)", "https://www.flooranddecor.com/decorative-tile", "decoratives.jpg.jpeg"),
            ("Fixtures (Bathroom/Cabinets)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materials (Grout/Supplies)", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    }
}
t = texts[idioma]

# --- FUNCIONES ---
def guardar_datos(df, filename):
    if not os.path.isfile(filename): df.to_csv(filename, index=False)
    else: df.to_csv(filename, mode='a', header=False, index=False)

# 2. Encabezado Centrado y Nítido
st.markdown('<div class="header-col header-logo">', unsafe_allow_html=True)
if os.path.exists("5104.jpg"):
    # Usamos container_width para que se vea completo y grande
    st.image("5104.jpg", use_container_width=True)
else:
    st.error("⚠️ Error: El archivo 5104.jpg no está en GitHub.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# 3. Navegación
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MÓDULOS ---
if "📊" in choice:
    st.header(t["menu"][0])
    with st.form("calc"):
        c = st.text_input("Cliente")
        l = st.number_input("Largo (ft)", 0.0)
        a = st.number_input("Ancho (ft)", 0.0)
        if st.form_submit_button(t["save_btn"]):
            area = l * a
            guardar_datos(pd.DataFrame([[datetime.now().date(), c, area]], columns=["Fecha", "Cliente", "Sqft"]), "historial.csv")
            st.success(f"Total: {area} sqft")

elif "👥" in choice:
    st.header(t["menu"][1])
    with st.form("nom"):
        w = st.text_input("Trabajador")
        h = st.number_input("Horas", 0.0)
        p = st.number_input("Pago por hora", 0.0)
        if st.form_submit_button(t["save_btn"]):
            total = h * p
            guardar_datos(pd.DataFrame([[datetime.now().date(), w, total]], columns=["Fecha", "Empleado", "Total"]), "nomina.csv")
            st.info(f"Pagar: ${total}")

elif "📋" in choice:
    st.header(t["menu"][2])
    tab1, tab2 = st.tabs(["Proyectos", "Nómina"])
    with tab1:
        if os.path.exists("historial.csv"): st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
        else: st.write("No hay proyectos.")
    with tab2:
        if os.path.exists("nomina.csv"): st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)
        else: st.write("No hay nómina.")

elif "📸" in choice:
    st.header(t["menu"][3])
    foto = st.file_uploader("Subir", type=["jpg", "png", "jpeg"])
    if foto: st.image(foto, use_container_width=True)

elif "🛒" in choice:
    st.header(t["cat_h"])
    items = t["categories"]
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(items):
                name, link, img = items[i+j]
                with cols[j]:
                    if os.path.exists(img):
                        # Aplicamos CSS para que las fotos de ambientes también sean nítidas y alineadas
                        st.markdown(f'<div class="header-logo"><img src="data:image/png;base64,{st.image(img).tobytes()}" /></div>', unsafe_allow_html=True)
                        st.image(img, use_container_width=True) # Fallback si el markdown falla
                    st.subheader(name)
                    st.link_button("Ver en Floor & Decor", link)
                    st.write("")

st.markdown("---")
st.caption("©️ 2026 JR CRUZ MASONRY LLC | Profesional | Fort Myers, FL")
