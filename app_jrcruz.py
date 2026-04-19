import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# --- CSS PARA ALINEAR IMÁGENES Y ESTILO PROFESIONAL ---
st.markdown("""
    <style>
    /* Forzar que todas las imágenes del catálogo tengan la misma altura y se vean alineadas */
    [data-testid="stImage"] img {
        height: 220px;
        object-fit: cover;
        border-radius: 10px;
    }
    .stButton>button { width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; }
    h1, h2, h3 { color: #1A4F8B; font-family: 'Arial'; }
    .stApp { background-color: #fcfcfc; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IDIOMA ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["English", "Español"])

# --- DICCIONARIO DE TRADUCCIONES Y CATEGORÍAS (ENLACES CORREGIDOS) ---
texts = {
    "English": {
        "sub": "Renovations and New Construction: Floors and Bathrooms",
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Floor & Decor Catalog"],
        "view_btn": "View",
        "save_btn": "Save Data",
        "cat_sub": "Select a category to view options at Floor & Decor:",
        "categories": [
            ("Tile", "https://www.flooranddecor.com/tile", "https://images.unsplash.com/photo-1516528387618-afa90b13e000?w=500"),
            ("Stone (Marble)", "https://www.flooranddecor.com/stone", "https://images.unsplash.com/photo-1628595351029-c2bf17511435?w=500"),
            ("Wood", "https://www.flooranddecor.com/wood", "https://images.unsplash.com/photo-1505015920881-0f83c2f7c95e?w=500"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "https://images.unsplash.com/photo-1515263487990-61b07816b324?w=500"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "https://images.unsplash.com/photo-1622397333309-3056849bc70b?w=500"),
            ("Decoratives (Backsplash)", "https://www.flooranddecor.com/decorative", "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?w=500"),
            ("Fixtures (Bath & Cabinets)", "https://www.flooranddecor.com/bathroom-fixtures", "https://images.unsplash.com/photo-1620626011761-9963d7521576?w=500"),
            ("Installation Materials (Grout)", "https://www.flooranddecor.com/installation-materials", "https://images.unsplash.com/photo-1589939705384-5185138a04b9?w=500")
        ]
    },
    "Español": {
        "sub": "Remodelaciones y Construcción: Pisos y Baños",
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo Floor & Decor"],
        "view_btn": "Ver",
        "save_btn": "Guardar Datos",
        "cat_sub": "Selecciona una categoría para ver opciones en Floor & Decor:",
        "categories": [
            ("Loseta (Tile)", "https://www.flooranddecor.com/tile", "https://images.unsplash.com/photo-1516528387618-afa90b13e000?w=500"),
            ("Piedra (Marble)", "https://www.flooranddecor.com/stone", "https://images.unsplash.com/photo-1628595351029-c2bf17511435?w=500"),
            ("Madera (Wood)", "https://www.flooranddecor.com/hardwood", "https://images.unsplash.com/photo-1505015920881-0f83c2f7c95e?w=500"),
            ("Laminado (Laminate)", "https://www.flooranddecor.com/laminate", "https://images.unsplash.com/photo-1515263487990-61b07816b324?w=500"),
            ("Vinilo (Vinyl)", "https://www.flooranddecor.com/vinyl", "https://images.unsplash.com/photo-1622397333309-3056849bc70b?w=500"),
            ("Decorativos (Backsplash)", "https://www.flooranddecor.com/decorative-bathroom-tile-stone", "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?w=500"),
            ("Gabinetes y Baños (Fixtures)", "https://www.flooranddecor.com/bathroom-fixtures", "https://images.unsplash.com/photo-1620626011761-9963d7521576?w=500"),
            ("Materiales y Grout", "https://www.flooranddecor.com/installation-materials", "https://images.unsplash.com/photo-1589939705384-5185138a04b9?w=500")
        ]
    }
}

t = texts[idioma]

# --- FUNCIONES DE PERSISTENCIA ---
def guardar_datos(df, filename):
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

# 2. Encabezado
col_logo, col_txt = st.columns([1, 4])
with col_logo:
    if os.path.exists("5104.jpg"): st.image("5104.jpg", width=150)
with col_txt:
    st.title("JR CRUZ MASONRY LLC")
    st.write(f"**{t['sub']}**")

st.markdown("---")

# 3. Menú Lateral
choice = st.sidebar.selectbox("Menu", t["menu"])

# --- MÓDULO: CATÁLOGO (ENLACES CORREGIDOS) ---
if "🛒" in choice:
    st.header(t["menu"][4])
    st.write(f"### {t['cat_sub']}")
    
    # Grid de 2 columnas para mejor visualización en tablets
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
                    st.write("")

# --- MÓDULO: CALCULADORA ---
elif "📊" in choice:
    st.header(t["menu"][0])
    with st.form("calc"):
        cliente = st.text_input("Client/Cliente")
        l = st.number_input("Largo/Length (ft)", min_value=0.0, step=0.1)
        a = st.number_input("Ancho/Width (ft)", min_value=0.0, step=0.1)
        if st.form_submit_button(t["save_btn"]):
            area = round(l * a, 2)
            nuevo = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), cliente, area]], columns=["Fecha", "Cliente", "Sqft"])
            guardar_datos(nuevo, "historial.csv")
            st.success(f"Total: {area} sqft")

# --- MÓDULO: NÓMINA ---
elif "👥" in choice:
    st.header(t["menu"][1])
    with st.form("nom"):
        emp = st.text_input("Worker/Trabajador")
        hrs = st.number_input("Hours", min_value=0.0, step=0.5)
        rate = st.number_input("Rate ($)", min_value=0.0, step=1.0)
        if st.form_submit_button(t["save_btn"]):
            total = hrs * rate
            nuevo_n = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), emp, hrs, total]], columns=["Fecha", "Empleado", "Horas", "Total"])
            guardar_datos(nuevo_n, "nomina.csv")
            st.info(f"Total to Pay: ${total}")

# --- MÓDULO: HISTORIAL ---
elif "📋" in choice:
    st.header(t["menu"][2])
    tab1, tab2 = st.tabs(["Projects", "Payroll"])
    with tab1:
        if os.path.exists("historial.csv"): st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
        else: st.write("No projects saved yet.")
    with tab2:
        if os.path.exists("nomina.csv"): st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)
        else: st.write("No payroll records yet.")

# --- MÓDULO: FOTOS ---
elif "📸" in choice:
    st.header(t["menu"][3])
    f = st.file_uploader("Upload Work Photo", type=["jpg", "png", "jpeg"])
    if f: st.image(f, use_container_width=True)

st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC | Professional Management")
