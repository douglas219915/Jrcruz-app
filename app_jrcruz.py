import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# --- CSS PARA IMÁGENES PERFECTAS ---
st.markdown("""
    <style>
    [data-testid="stImage"] img {
        height: 250px; /* Ajusta esta altura a tu gusto */
        object-fit: cover;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .stButton>button { width: 100%; background-color: #1A4F8B; color: white; font-weight: bold; }
    h1, h2, h3 { color: #1A4F8B; }
    </style>
    """, unsafe_allow_html=True)

# --- IDIOMA ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["English", "Español"])

# --- DICCIONARIO DE TRADUCCIONES ---
texts = {
    "English": {
        "view": "View Products",
        "cat_sub": "Our Project Gallery & Suggested Materials",
        "categories": [
            ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg"),
            ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg"),
            ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg"),
            ("Decoratives", "https://www.flooranddecor.com/decorative-tile", "decoratives.jpg"),
            ("Fixtures", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg"),
            ("Materials", "https://www.flooranddecor.com/installation-materials", "materials.jpg")
        ]
    },
    "Español": {
        "view": "Ver Productos",
        "cat_sub": "Galería de Proyectos y Materiales Sugeridos",
        "categories": [
            ("Loseta (Tile)", "https://www.flooranddecor.com/tile", "tile.jpg"),
            ("Piedra (Stone)", "https://www.flooranddecor.com/stone", "stone.jpg"),
            ("Madera (Wood)", "https://www.flooranddecor.com/hardwood", "wood.jpg"),
            ("Laminado (Laminate)", "https://www.flooranddecor.com/laminate", "laminate.jpg"),
            ("Vinilo (Vinyl)", "https://www.flooranddecor.com/vinyl", "vinyl.jpg"),
            ("Decorativos", "https://www.flooranddecor.com/decorative-tile", "decoratives.jpg"),
            ("Accesorios (Fixtures)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg"),
            ("Materiales", "https://www.flooranddecor.com/installation-materials", "materials.jpg")
        ]
    }
}

t = texts[idioma]

# --- ENCABEZADO ---
st.title("JR CRUZ MASONRY LLC")
st.write(f"### {t['cat_sub']}")
st.markdown("---")

# --- MOSTRAR CATÁLOGO CON TUS FOTOS ---
items = t["categories"]
for i in range(0, len(items), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(items):
            name, link, img_name = items[i+j]
            with cols[j]:
                # Verifica si la imagen existe en tu GitHub antes de mostrarla
                if os.path.exists(img_name):
                    st.image(img_name, use_container_width=True)
                else:
                    st.warning(f"Falta foto: {img_name}") # Esto te avisará si el nombre está mal
                
                st.subheader(name)
                st.link_button(f"{t['view']} {name}", link)
                st.write("")
