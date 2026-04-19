import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# --- LÓGICA DE IDIOMA ---
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

st.sidebar.title("Settings / Configuración")
idioma = st.sidebar.radio("Select Language / Seleccione Idioma", ["English", "Español"])

# --- DICCIONARIO DE TRADUCCIONES ---
texts = {
    "English": {
        "sub": "Renovations and New Construction: Floors and Bathrooms",
        "menu": ["📊 Calculator", "👥 Payroll", "📋 History", "📸 Photos", "🛒 Floor & Decor Catalog"],
        "calc_h": "Material Estimate",
        "nom_h": "Payment Records",
        "hist_h": "Saved Records",
        "gal_h": "Work Gallery",
        "cat_h": "Suggested Products (Floor & Decor)",
        "cat_sub": "Select a category to view options:",
        "view_btn": "View",
        "save_btn": "Save Data",
        "client": "Client Name",
        "worker": "Worker Name",
        "hours": "Weekly Hours",
        "rate": "Rate per Hour ($)",
        "history_p": "Project History",
        "history_n": "Payroll History",
        "categories": {
            "Tile": ["Tile", "https://www.flooranddecor.com/tile", "https://images.unsplash.com/photo-1516528387618-afa90b13e000?w=400"],
            "Stone": ["Stone", "https://www.flooranddecor.com/stone", "https://images.unsplash.com/photo-1590483734724-383b853b237d?w=400"],
            "Wood": ["Wood", "https://www.flooranddecor.com/hardwood", "https://images.unsplash.com/photo-1581850518616-bcb818814e3e?w=400"],
            "Laminate": ["Laminate", "https://www.flooranddecor.com/laminate", "https://images.unsplash.com/photo-1515263487990-61b07816b324?w=400"],
            "Vinyl": ["Vinyl", "https://www.flooranddecor.com/vinyl", "https://images.unsplash.com/photo-1622397333309-3056849bc70b?w=400"],
            "Decoratives": ["Decoratives", "https://www.flooranddecor.com/decorative", "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=400"],
            "Fixtures": ["Fixtures", "https://www.flooranddecor.com/fixtures", "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=400"],
            "Inst_Mat": ["Installation Materials", "https://www.flooranddecor.com/installation-materials", "https://images.unsplash.com/photo-1589939705384-5185138a04b9?w=400"]
        }
    },
    "Español": {
        "sub": "Remodelaciones y Construcción: Pisos y Baños",
        "menu": ["📊 Calculadora", "👥 Nómina", "📋 Historial", "📸 Fotos", "🛒 Catálogo Floor & Decor"],
        "calc_h": "Estimado de Materiales",
        "nom_h": "Registro de Pagos",
        "hist_h": "Registros Guardados",
        "gal_h": "Galería de Trabajos",
        "cat_h": "Productos Sugeridos (Floor & Decor)",
        "cat_sub": "Selecciona una categoría para ver opciones:",
        "view_btn": "Ver",
        "save_btn": "Guardar Datos",
        "client": "Nombre del Cliente",
        "worker": "Nombre del Trabajador",
        "hours": "Horas Semanales",
        "rate": "Pago por Hora ($)",
        "history_p": "Historial de Proyectos",
        "history_n": "Historial de Nómina",
        "categories": {
            "Tile": ["Loseta (Tile)", "https://www.flooranddecor.com/tile", "https://images.unsplash.com/photo-1516528387618-afa90b13e000?w=400"],
            "Stone": ["Piedra (Stone)", "https://www.flooranddecor.com/stone", "https://images.unsplash.com/photo-1590483734724-383b853b237d?w=400"],
            "Wood": ["Madera (Wood)", "https://www.flooranddecor.com/hardwood", "https://images.unsplash.com/photo-1581850518616-bcb818814e3e?w=400"],
            "Laminate": ["Laminado (Laminate)", "https://www.flooranddecor.com/laminate", "https://images.unsplash.com/photo-1515263487990-61b07816b324?w=400"],
            "Vinyl": ["Vinilo (Vinyl)", "https://www.flooranddecor.com/vinyl", "https://images.unsplash.com/photo-1622397333309-3056849bc70b?w=400"],
            "Decoratives": ["Decorativos (Decoratives)", "https://www.flooranddecor.com/decorative", "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=400"],
            "Fixtures": ["Accesorios (Fixtures)", "https://www.flooranddecor.com/fixtures", "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=400"],
            "Inst_Mat": ["Materiales de Instalación", "https://www.flooranddecor.com/installation-materials", "https://images.unsplash.com/photo-1589939705384-5185138a04b9?w=400"]
        }
    }
}

t = texts[idioma]

# --- FUNCIONES DE PERSISTENCIA ---
def guardar_datos(df, filename):
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

# 2. Encabezado Profesional
col_l, col_r = st.columns([1, 3])
with col_l:
    if os.path.exists("5104.jpg"): st.image("5104.jpg", width=160)
with col_r:
    st.title("JR CRUZ MASONRY LLC")
    st.write(f"### {t['sub']}")

st.markdown("---")

# 3. Navegación
choice = st.sidebar.selectbox("Menu", t["menu"])

# --- MODULO: CALCULADORA ---
if "📊" in choice:
    st.header(t["calc_h"])
    with st.form("calc_form"):
        c_name = st.text_input(t["client"])
        l = st.number_input("Largo/Length (ft)", min_value=0.0)
        a = st.number_input("Ancho/Width (ft)", min_value=0.0)
        if st.form_submit_button(t["save_btn"]):
            area = l * a
            cajas = round((area * 1.10) / 15)
            st.success(f"Total: {area} sqft | Boxes: {cajas}")
            nuevo = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), c_name, area]], columns=["Fecha", "Cliente", "Sqft"])
            guardar_datos(nuevo, "historial.csv")

# --- MODULO: NÓMINA ---
elif "👥" in choice:
    st.header(t["nom_h"])
    with st.form("nom_form"):
        w_name = st.text_input(t["worker"])
        h = st.number_input(t["hours"], min_value=0.0)
        r = st.number_input(t["rate"], min_value=0.0)
        if st.form_submit_button(t["save_btn"]):
            total = h * r
            st.info(f"Total: ${total}")
            nuevo_p = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), w_name, h, total]], columns=["Fecha", "Empleado", "Horas", "Total"])
            guardar_datos(nuevo_p, "nomina.csv")

# --- MODULO: CATALOGO FLOOR & DECOR ---
elif "🛒" in choice:
    st.header(t["cat_h"])
    st.write(t["cat_sub"])
    items = list(t["categories"].values())
    for i in range(0, len(items), 2): # Filas de 2 para que se vea bien en iPad
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(items):
                name, link, img = items[i+j]
                with cols[j]:
                    st.image(img, use_container_width=True)
                    st.subheader(name)
                    st.link_button(f"{t['view_btn']} {name}", link)
                    st.write("---")

# --- MODULO: HISTORIAL ---
elif "📋" in choice:
    st.header(t["hist_h"])
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t["history_p"])
        if os.path.exists("historial.csv"): st.dataframe(pd.read_csv("historial.csv"))
        else: st.write("No data")
    with col2:
        st.subheader(t["history_n"])
        if os.path.exists("nomina.csv"): st.dataframe(pd.read_csv("nomina.csv"))
        else: st.write("No data")

# --- MODULO: FOTOS ---
elif "📸" in choice:
    st.header(t["gal_h"])
    f = st.file_uploader("Upload Image", type=["jpg", "png"])
    if f: st.image(f, use_container_width=True)

st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC")
