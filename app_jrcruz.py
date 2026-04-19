import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# --- CSS PROFESIONAL Y CORRECCIÓN DE ALINEACIÓN ---
st.markdown("""
    <style>
    /* Forzar tamaño de imágenes para que todo esté alineado */
    [data-testid="stImage"] img {
        height: 220px;
        object-fit: cover;
        border-radius: 12px;
        border: 1px solid #ddd;
    }
    /* Estilo de botones */
    .stButton>button { 
        width: 100%; 
        background-color: #1A4F8B; 
        color: white; 
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover { border: 2px solid #1A4F8B; color: #1A4F8B; }
    h1, h2, h3 { color: #1A4F8B; }
    </style>
    """, unsafe_allow_html=True)

# --- IDIOMA ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["English", "Español"])

# --- DATOS DEL CATÁLOGO (ENLACES RE-VERIFICADOS) ---
texts = {
    "English": {
        "sub": "Renovations and New Construction: Floors and Bathrooms",
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Floor & Decor Catalog"],
        "view_btn": "View",
        "save_btn": "Save Data",
        "cat_sub": "Official Floor & Decor Categories:",
        "categories": [
            ("Tile", "https://www.flooranddecor.com/tile", "https://images.unsplash.com/photo-1516528387618-afa90b13e000?w=500"),
            ("Stone (Marble)", "https://www.flooranddecor.com/stone", "https://images.unsplash.com/photo-1628595351029-c2bf17511435?w=500"),
            ("Wood", "https://www.flooranddecor.com/wood", "https://images.unsplash.com/photo-1505015920881-0f83c2f7c95e?w=500"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "https://images.unsplash.com/photo-1515263487990-61b07816b324?w=500"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "https://images.unsplash.com/photo-1622397333309-3056849bc70b?w=500"),
            ("Decoratives", "https://www.flooranddecor.com/decoratives", "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?w=500"),
            ("Fixtures", "https://www.flooranddecor.com/bathroom-fixtures", "https://images.unsplash.com/photo-1620626011761-9963d7521576?w=500"),
            ("Installation Materials", "https://www.flooranddecor.com/installation-materials", "https://images.unsplash.com/photo-1589939705384-5185138a04b9?w=500")
        ]
    },
    "Español": {
        "sub": "Remodelaciones y Construcción: Pisos y Baños",
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo Floor & Decor"],
        "view_btn": "Ver",
        "save_btn": "Guardar Datos",
        "cat_sub": "Categorías Oficiales de Floor & Decor:",
        "categories": [
            ("Loseta (Tile)", "https://www.flooranddecor.com/tile", "https://images.unsplash.com/photo-1516528387618-afa90b13e000?w=500"),
            ("Piedra (Marble)", "https://www.flooranddecor.com/stone", "https://images.unsplash.com/photo-1628595351029-c2bf17511435?w=500"),
            ("Madera (Wood)", "https://www.flooranddecor.com/wood", "https://images.unsplash.com/photo-1505015920881-0f83c2f7c95e?w=500"),
            ("Laminado (Laminate)", "https://www.flooranddecor.com/laminate", "https://images.unsplash.com/photo-1515263487990-61b07816b324?w=500"),
            ("Vinilo (Vinyl)", "https://www.flooranddecor.com/vinyl", "https://images.unsplash.com/photo-1622397333309-3056849bc70b?w=500"),
            ("Decorativos (Backsplash)", "https://www.flooranddecor.com/decorative-tile", "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?w=500"),
            ("Baños y Llaves (Fixtures)", "https://www.flooranddecor.com/bathroom-fixtures", "https://images.unsplash.com/photo-1620626011761-9963d7521576?w=500"),
            ("Materiales de Instalación", "https://www.flooranddecor.com/installation-materials", "https://images.unsplash.com/photo-1589939705384-5185138a04b9?w=500")
        ]
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
col_l, col_r = st.columns([1, 4])
with col_l:
    if os.path.exists("5104.jpg"): st.image("5104.jpg", width=140)
with col_r:
    st.title("JR CRUZ MASONRY LLC")
    st.write(f"### {t['sub']}")

st.markdown("---")
choice = st.sidebar.selectbox("Menu", t["menu"])

# --- MODULO CATALOGO ---
if "🛒" in choice:
    st.header(t["menu"][4])
    st.write(t["cat_sub"])
    items = t["categories"]
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(items):
                name, link, img = items[i+j]
                with cols[j]:
                    st.image(img, use_container_width=True)
                    st.subheader(name)
                    st.link_button(f"{t['view_btn']} {name}", link)
                    st.write("---")

# --- MODULO CALCULADORA ---
elif "📊" in choice:
    st.header(t["menu"][0])
    with st.form("calc"):
        cli = st.text_input("Client")
        l = st.number_input("Largo (ft)", 0.0)
        a = st.number_input("Ancho (ft)", 0.0)
        if st.form_submit_button(t["save_btn"]):
            area = l * a
            guardar_datos(pd.DataFrame([[datetime.now().date(), cli, area]], columns=["Fecha", "Cliente", "Sqft"]), "historial.csv")
            st.success(f"Total: {area} sqft")

# --- MODULO NOMINA ---
elif "👥" in choice:
    st.header(t["menu"][1])
    with st.form("nom"):
        w = st.text_input("Worker")
        h = st.number_input("Hours", 0.0)
        r = st.number_input("Rate", 0.0)
        if st.form_submit_button(t["save_btn"]):
            total = h * r
            guardar_datos(pd.DataFrame([[datetime.now().date(), w, total]], columns=["Fecha", "Empleado", "Total"]), "nomina.csv")
            st.info(f"Pay: ${total}")

# --- MODULO HISTORIAL ---
elif "📋" in choice:
    st.header(t["menu"][2])
    if os.path.exists("historial.csv"): 
        st.write("### Projects")
        st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
    if os.path.exists("nomina.csv"): 
        st.write("### Payroll")
        st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)

# --- MODULO FOTOS ---
elif "📸" in choice:
    st.header(t["menu"][3])
    f = st.file_uploader("Upload", type=["jpg", "png"])
    if f: st.image(f, use_container_width=True)

st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC")
