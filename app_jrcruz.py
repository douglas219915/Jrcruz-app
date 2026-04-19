import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# --- CSS PARA ALINEAR IMÁGENES Y ESTILO ---
st.markdown("""
    <style>
    /* Forzar que todas las imágenes del catálogo tengan la misma altura */
    [data-testid="stImage"] img {
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
    }
    .stButton>button { width: 100%; background-color: #1A4F8B; color: white; }
    h1, h2, h3 { color: #1A4F8B; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IDIOMA ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["English", "Español"])

# --- DICCIONARIO DE TRADUCCIONES Y CATEGORÍAS ---
texts = {
    "English": {
        "sub": "Renovations and New Construction: Floors and Bathrooms",
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Floor & Decor Catalog"],
        "view_btn": "View",
        "save_btn": "Save Data",
        "cat_sub": "Select a category to view options at Floor & Decor:",
        "categories": {
            "Tile": ["Tile", "https://www.flooranddecor.com/tile", "https://images.unsplash.com/photo-1516528387618-afa90b13e000?w=500"],
            "Stone": ["Stone (Marble)", "https://www.flooranddecor.com/stone", "https://images.unsplash.com/photo-1628595351029-c2bf17511435?w=500"],
            "Wood": ["Wood", "https://www.flooranddecor.com/hardwood", "https://images.unsplash.com/photo-1505015920881-0f83c2f7c95e?w=500"],
            "Laminate": ["Laminate", "https://www.flooranddecor.com/laminate", "https://images.unsplash.com/photo-1515263487990-61b07816b324?w=500"],
            "Vinyl": ["Vinyl", "https://www.flooranddecor.com/vinyl", "https://images.unsplash.com/photo-1622397333309-3056849bc70b?w=500"],
            "Decoratives": ["Decoratives (Backsplash)", "https://www.flooranddecor.com/decorative", "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?w=500"],
            "Fixtures": ["Fixtures (Bathroom)", "https://www.flooranddecor.com/fixtures", "https://images.unsplash.com/photo-1620626011761-9963d7521576?w=500"],
            "Inst_Mat": ["Installation Materials (Grout)", "https://www.flooranddecor.com/installation-materials", "https://images.unsplash.com/photo-1589939705384-5185138a04b9?w=500"]
        }
    },
    "Español": {
        "sub": "Remodelaciones y Construcción: Pisos y Baños",
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo Floor & Decor"],
        "view_btn": "Ver",
        "save_btn": "Guardar Datos",
        "cat_sub": "Selecciona una categoría para ver opciones en Floor & Decor:",
        "categories": {
            "Tile": ["Loseta (Tile)", "https://www.flooranddecor.com/tile", "https://images.unsplash.com/photo-1516528387618-afa90b13e000?w=500"],
            "Stone": ["Piedra (Marble)", "https://www.flooranddecor.com/stone", "https://images.unsplash.com/photo-1628595351029-c2bf17511435?w=500"],
            "Wood": ["Madera (Wood)", "https://www.flooranddecor.com/hardwood", "https://images.unsplash.com/photo-1505015920881-0f83c2f7c95e?w=500"],
            "Laminate": ["Laminado (Laminate)", "https://www.flooranddecor.com/laminate", "https://images.unsplash.com/photo-1515263487990-61b07816b324?w=500"],
            "Vinyl": ["Vinilo (Vinyl)", "https://www.flooranddecor.com/vinyl", "https://images.unsplash.com/photo-1622397333309-3056849bc70b?w=500"],
            "Decoratives": ["Decorativos (Backsplash)", "https://www.flooranddecor.com/decorative", "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?w=500"],
            "Fixtures": ["Gabinetes y Llaves (Fixtures)", "https://www.flooranddecor.com/fixtures", "https://images.unsplash.com/photo-1620626011761-9963d7521576?w=500"],
            "Inst_Mat": ["Materiales / Grout", "https://www.flooranddecor.com/installation-materials", "https://images.unsplash.com/photo-1589939705384-5185138a04b9?w=500"]
        }
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
    if os.path.exists("5104.jpg"): st.image("5104.jpg", width=160)
with col_txt:
    st.title("JR CRUZ MASONRY LLC")
    st.write(f"### {t['sub']}")

st.markdown("---")

# 3. Menú Lateral
choice = st.sidebar.selectbox("Menu", t["menu"])

# --- MÓDULO: CATÁLOGO (ACTUALIZADO CON FOTOS CORRECTAS) ---
if "🛒" in choice:
    st.header(t["menu"][4])
    st.write(t["cat_sub"])
    
    items = list(t["categories"].values())
    # Crear filas de 3 columnas
    for i in range(0, len(items), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(items):
                name, link, img = items[i+j]
                with cols[j]:
                    st.image(img, use_container_width=True)
                    st.subheader(name)
                    st.link_button(f"{t['view_btn']} {name}", link)
                    st.write("")

# --- MÓDULO: CALCULADORA ---
elif "📊" in choice:
    st.header(t["menu"][0])
    with st.form("calc"):
        cliente = st.text_input("Client/Cliente")
        l = st.number_input("Largo/Length (ft)", min_value=0.0)
        a = st.number_input("Ancho/Width (ft)", min_value=0.0)
        if st.form_submit_button(t["save_btn"]):
            area = l * a
            nuevo = pd.DataFrame([[datetime.now().date(), cliente, area]], columns=["Fecha", "Cliente", "Area"])
            guardar_datos(nuevo, "historial.csv")
            st.success(f"Total: {area} sqft")

# --- MÓDULO: NÓMINA ---
elif "👥" in choice:
    st.header(t["menu"][1])
    with st.form("nom"):
        emp = st.text_input("Worker/Trabajador")
        hrs = st.number_input("Hours", min_value=0.0)
        rate = st.number_input("Rate ($)", min_value=0.0)
        if st.form_submit_button(t["save_btn"]):
            total = hrs * rate
            nuevo_n = pd.DataFrame([[datetime.now().date(), emp, total]], columns=["Fecha", "Empleado", "Total"])
            guardar_datos(nuevo_n, "nomina.csv")
            st.info(f"Total: ${total}")

# --- MÓDULO: HISTORIAL ---
elif "📋" in choice:
    st.header(t["menu"][2])
    if os.path.exists("historial.csv"):
        st.write("### Projects")
        st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
    if os.path.exists("nomina.csv"):
        st.write("### Payroll")
        st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)

# --- MÓDULO: FOTOS ---
elif "📸" in choice:
    st.header(t["menu"][3])
    f = st.file_uploader("Upload", type=["jpg", "png"])
    if f: st.image(f, use_container_width=True)

st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC")
