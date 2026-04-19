import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# Función para convertir imagen local a Base64 para el fondo
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- CSS PARA LOGO SOMBREADO EN EL FONDO Y DISEÑO LIMPIO ---
if os.path.exists("5104.jpg"):
    img_base64 = get_base64_image("5104.jpg")
    bg_style = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("data:image/jpg;base64,{img_base64}");
        background-size: 600px;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    /* Ajustes adicionales de visibilidad */
    .stApp {{ background-color: transparent; }}
    [data-testid="stImage"] img {{
        height: 280px;
        object-fit: cover;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }}
    .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; }}
    h1, h2, h3 {{ color: #1A4F8B; text-shadow: 1px 1px 2px white; }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# --- IDIOMA ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])

# --- DICCIONARIOS ---
texts = {
    "Español": {
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo Floor & Decor"],
        "cat_h": "Catálogo de Materiales Sugeridos",
        "categories": [
            ("Tile (Loseta)", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Stone (Piedra)", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Wood (Madera)", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminate (Laminado)", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinyl (Vinilo)", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decoratives (Backsplash)", "https://www.flooranddecor.com/decorative-tile", "decoratives.jpg.jpeg"),
            ("Fixtures (Baño)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materials (Grout)", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    },
    "English": {
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Floor & Decor Catalog"],
        "cat_h": "Suggested Materials Catalog",
        "categories": [
            ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decoratives (Backsplash)", "https://www.flooranddecor.com/decorative-tile", "decoratives.jpg.jpeg"),
            ("Fixtures (Bathroom)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materials (Supplies)", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    }
}
t = texts[idioma]

# --- ENCABEZADO ---
st.title("JR CRUZ MASONRY LLC")
st.write("---")

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MÓDULO CATÁLOGO (CORREGIDO) ---
if "🛒" in choice:
    st.header(t["cat_h"])
    items = t["categories"]
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(items):
                name, link, img = items[i+j]
                with cols[j]:
                    if os.path.exists(img):
                        st.image(img, use_container_width=True)
                    else:
                        st.warning(f"Imagen no disponible: {img}")
                    st.subheader(name)
                    st.link_button(f"Ver {name}", link)
                    st.write("")

# --- OTROS MÓDULOS (CALCULADORA, NÓMINA, ETC) ---
# (Se mantienen igual para no fallar)
elif "📊" in choice:
    st.header(t["menu"][0])
    # ... código de calculadora ...
