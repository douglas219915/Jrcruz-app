import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de la página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# --- CSS PROFESIONAL Y ALINEACIÓN DE IMÁGENES ---
st.markdown("""
    <style>
    /* Forzar que las imágenes de ambiente tengan la misma altura */
    [data-testid="stImage"] img {
        height: 300px;
        object-fit: cover;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
    }
    /* Estilo para los botones de Floor & Decor */
    .stButton>button {
        width: 100%;
        background-color: #1A4F8B;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        height: 45px;
    }
    /* Estilo del panel lateral */
    .css-1d391kg { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1A4F8B; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ARCHIVOS (PERSISTENCIA) ---
def guardar_datos(df, filename):
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

# --- TRADUCCIONES Y CATEGORÍAS ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])

texts = {
    "Español": {
        "sub": "Remodelaciones y Construcción: Pisos y Baños",
        "menu": ["📊 Calculadora", "👥 Nómina Semanal", "📋 Historial", "📸 Fotos de Obra", "🛒 Catálogo Floor & Decor"],
        "cat_title": "Productos Sugeridos (Ambientes Reales)",
        "view_btn": "Ver en Floor & Decor",
        "categories": [
            ("Tile (Loseta)", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Stone (Piedra/Marble)", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Wood (Madera)", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminate (Laminado)", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinyl (Vinilo)", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decoratives (Backsplash)", "https://www.flooranddecor.com/decorative-tile", "decoratives.jpg.jpeg"),
            ("Fixtures (Baño y Gabinetes)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materials (Grout/Pegamento)", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    },
    "English": {
        "sub": "Renovations and New Construction: Floors and Bathrooms",
        "menu": ["📊 Calculator", "👥 Weekly Payroll", "📋 History", "📸 Work Photos", "🛒 Floor & Decor Catalog"],
        "cat_title": "Suggested Products (Real Environments)",
        "view_btn": "View at Floor & Decor",
        "categories": [
            ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg"),
            ("Stone (Marble)", "https://www.flooranddecor.com/stone", "stone.jpg"),
            ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg"),
            ("Decoratives (Backsplash)", "https://www.flooranddecor.com/decorative-tile", "decoratives.jpg"),
            ("Fixtures (Bathroom/Cabinets)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg"),
            ("Materials (Grout/Supplies)", "https://www.flooranddecor.com/installation-materials", "materials.jpg")
        ]
    }
}

t = texts[idioma]

# --- ENCABEZADO PRINCIPAL ---
col_logo, col_txt = st.columns([1, 4])
with col_logo:
    if os.path.exists("5104.jpg"):
        st.image("5104.jpg", width=150)
with col_txt:
    st.title("JR CRUZ MASONRY LLC")
    st.write(f"**{t['sub']}**")

st.markdown("---")
choice = st.sidebar.selectbox("Panel de Control", t["menu"])

# --- 1. CALCULADORA ---
if "📊" in choice:
    st.header(t["menu"][0])
    with st.form("calc_form"):
        cliente = st.text_input("Nombre del Cliente / Proyecto")
        col_dim1, col_dim2 = st.columns(2)
        with col_dim1: l = st.number_input("Largo (ft)", min_value=0.0, step=0.1)
        with col_dim2: a = st.number_input("Ancho (ft)", min_value=0.0, step=0.1)
        if st.form_submit_button("Calcular y Guardar"):
            area = round(l * a, 2)
            nuevo_p = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), cliente, area]], columns=["Fecha", "Cliente", "Sqft"])
            guardar_datos(nuevo_p, "historial.csv")
            st.success(f"Área Total: {area} sqft")

# --- 2. NÓMINA SEMANAL ---
elif "👥" in choice:
    st.header(t["menu"][1])
    with st.form("payroll_form"):
        nombre = st.text_input("Nombre del Trabajador")
        c1, c2 = st.columns(2)
        with c1: horas = st.number_input("Horas Semanales", min_value=0.0, step=0.5)
        with c2: pago = st.number_input("Pago por Hora ($)", min_value=0.0, step=1.0)
        if st.form_submit_button("Registrar Pago"):
            total = horas * pago
            nuevo_n = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), nombre, horas, total]], columns=["Fecha", "Empleado", "Horas", "Total"])
            guardar_datos(nuevo_n, "nomina.csv")
            st.info(f"Total a pagar a {nombre}: ${total}")

# --- 3. HISTORIAL ---
elif "📋" in choice:
    st.header(t["menu"][2])
    tab1, tab2 = st.tabs(["Proyectos", "Pagos de Nómina"])
    with tab1:
        if os.path.exists("historial.csv"): st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
        else: st.write("No hay proyectos registrados.")
    with tab2:
        if os.path.exists("nomina.csv"): st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)
        else: st.write("No hay registros de nómina.")

# --- 4. FOTOS ---
elif "📸" in choice:
    st.header(t["menu"][3])
    foto = st.file_uploader("Subir foto del progreso", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, caption="Vista previa de obra", use_container_width=True)

# --- 5. CATÁLOGO (CON TUS IMÁGENES ELEGANTES) ---
elif "🛒" in choice:
    st.header(t["cat_title"])
    st.write("Selecciona una categoría para ver opciones en Floor & Decor:")
    
    items = t["categories"]
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(items):
                name, link, img_file = items[i+j]
                with cols[j]:
                    if os.path.exists(img_file):
                        st.image(img_file, use_container_width=True)
                    else:
                        st.warning(f"Falta imagen: {img_file}")
                    st.subheader(name)
                    st.link_button(t["view_btn"], link)
                    st.write("")

st.markdown("---")
st.caption(f"©️ 2026 JR CRUZ MASONRY LLC | Gestión Profesional | Fort Myers, FL")
