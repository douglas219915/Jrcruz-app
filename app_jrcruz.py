import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
from fpdf import FPDF

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# Función para el logo de fondo (Marca de agua)
def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

# --- CSS: LOGO SOMBREADO Y ESTILOS ---
logo_b64 = get_base64("5104.jpg")
if logo_b64:
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)), url("data:image/jpg;base64,{logo_b64}");
            background-size: 500px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
        }}
        .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; height: 45px; }}
        [data-testid="stImage"] img {{ border-radius: 15px; object-fit: cover; height: 250px; border: 1px solid #ddd; }}
        h1, h2, h3 {{ color: #1A4F8B; }}
        </style>
    """, unsafe_allow_html=True)

# --- TRADUCCIONES Y TEXTOS ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])

texts = {
    "Español": {
        "menu": ["📊 Calculadora", "📅 Citas", "👥 Nómina", "📋 Historial", "🛒 Catálogo"],
        "calc_t": "Calculadora Dinámica de Área",
        "add_row": "➕ Agregar fila",
        "del_row": "❌ Quitar fila",
        "btn_pdf": "Guardar y Descargar PDF",
        "citas_t": "Agenda de Citas",
        "nom_t": "Nómina Semanal",
        "hist_t": "Historial General",
        "cat_t": "Catálogo de Materiales",
        "cliente": "Nombre del Cliente",
        "precio_sqft": "Precio por Sqft ($)",
        "ver_mas": "Ver detalles",
        "cat_list": [
            ("Loseta (Tile)", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Piedra (Stone)", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Madera (Wood)", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminado (Laminate)", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinilo (Vinyl)", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decorativos (Backsplash)", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
            ("Baños y Gabinetes (Fixtures)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materiales (Grout/Cement)", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    },
    "English": {
        "menu": ["📊 Calculator", "📅 Appointments", "👥 Payroll", "📋 History", "🛒 Catalog"],
        "calc_t": "Dynamic Area Calculator",
        "add_row": "➕ Add row",
        "del_row": "❌ Remove row",
        "btn_pdf": "Save & Download PDF",
        "citas_t": "Appointment Calendar",
        "nom_t": "Weekly Payroll",
        "hist_t": "General History",
        "cat_t": "Material Catalog",
        "cliente": "Client Name",
        "precio_sqft": "Price per Sqft ($)",
        "ver_mas": "View details",
        "cat_list": [
            ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decoratives", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
            ("Fixtures", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materials", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    }
}
t = texts[idioma]

# --- FUNCIONES DE PERSISTENCIA ---
def guardar_datos(df, file):
    if not os.path.isfile(file): df.to_csv(file, index=False)
    else: df.to_csv(file, mode='a', header=False, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel de Control", t["menu"])

# 1. CALCULADORA DINÁMICA + PDF
if "📊" in choice:
    st.title(t["calc_t"])
    
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    
    cliente = st.text_input(t["cliente"])
    p_unitario = st.number_input(t["precio_sqft"], min_value=0.0, step=0.1)

    c_b1, c_b2 = st.columns(2)
    with c_b1:
        if st.button(t["add_row"]): st.session_state['rows'] += 1
    with c_b2:
        if st.button(t["del_row"]) and st.session_state['rows'] > 1: st.session_state['rows'] -= 1

    medidas = []
    total_sqft = 0.0
    for i in range(st.session_state['rows']):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1: l = st.number_input(f"Largo/Length {i+1}", min_value=0.0, key=f"l_{i}")
        with col2: a = st.number_input(f"Ancho/Width {i+1}", min_value=0.0, key=f"a_{i}")
        sub = round(l * a, 2)
        total_sqft += sub
        medidas.append({'id': i+1, 'l': l, 'a': a, 'sub': sub})
        with col3: st.write("Subtotal"); st.code(f"{sub} sqft")

    total_dinero = round(total_sqft * p_unitario, 2)
    st.markdown("---")
    res1, res2 = st.columns(2)
    res1.metric("Total Sqft", f"{total_sqft} ft²")
    res2.metric("Total Estimate", f"${total_dinero}")

    if st.button(t["btn_pdf"]):
        # Guardar en Historial
        nuevo_h = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), cliente, total_sqft, total_dinero]], columns=["Fecha", "Cliente", "Sqft", "Total$"])
        guardar_datos(nuevo_h, "historial.csv")
        
        # Generar PDF
        pdf = FPDF()
        pdf.add_page()
        if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
        pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C")
        pdf.set_font("Arial", "", 10); pdf.cell(0, 5, "Estimate / Cotización", 0, 1, "C")
        pdf.ln(15)
        pdf.set_font("Arial", "B", 12); pdf.cell(0, 10, f"Client: {cliente}", 0, 1)
        pdf.set_font("Arial", "", 11); pdf.cell(0, 7, f"Date: {datetime.now().strftime('%m/%d/%Y')}", 0, 1)
        pdf.ln(5)
        # Tabla
        pdf.set_fill_color(26, 79, 139); pdf.set_text_color(255, 255, 255)
        pdf.cell(30, 10, "Row", 1, 0, "C", True); pdf.cell(50, 10, "Length (ft)", 1, 0, "C", True)
        pdf.cell(50, 10, "Width (ft)", 1, 0, "C", True); pdf.cell(50, 10, "Subtotal", 1, 1, "C", True)
        pdf.set_text_color(0, 0, 0)
        for m in medidas:
            pdf.cell(30, 10, str(m['id']), 1); pdf.cell(50, 10, str(m['l']), 1)
            pdf.cell(50, 10, str(m['a']), 1); pdf.cell(50, 10, f"{m['sub']} sqft", 1); pdf.ln()
        pdf.ln(5); pdf.set_font("Arial", "B", 12)
        pdf.cell(130, 10, "TOTAL AREA:", 1); pdf.cell(50, 10, f"{total_sqft} sqft", 1, 1)
        pdf.cell(130, 10, "TOTAL PRICE:", 1); pdf.cell(50, 10, f"${total_dinero}", 1, 1)
        
        output_pdf = f"Estimate_{cliente}.pdf"
        pdf.output(output_pdf)
        with open(output_pdf, "rb") as f:
            st.download_button("📩 Download PDF / Descargar", f, file_name=output_pdf)

# 2. CITAS
elif "📅" in choice:
    st.title(t["citas_t"])
    with st.form("f_citas"):
        f = st.date_input("Fecha"); h = st.time_input("Hora"); c = st.text_input("Cliente"); n = st.text_area("Notas")
        if st.form_submit_button("Agendar"):
            guardar_datos(pd.DataFrame([[f, h, c, n]], columns=["Fecha", "Hora", "Cliente", "Notas"]), "citas.csv")
            st.success("Cita guardada")
    if os.path.exists("citas.csv"): st.dataframe(pd.read_csv("citas.csv").sort_values(by="Fecha"), use_container_width=True)

# 3. NÓMINA
elif "👥" in choice:
    st.title(t["nom_t"])
    with st.form("f_nom"):
        nom = st.text_input("Nombre"); hrs = st.number_input("Horas", min_value=0.0); pag = st.number_input("Pago/Hr", min_value=0.0)
        if st.form_submit_button("Registrar"):
            tot = hrs * pag
            guardar_datos(pd.DataFrame([[datetime.now().date(), nom, tot]], columns=["Fecha", "Empleado", "Total"]), "nomina.csv")
            st.info(f"Total a pagar: ${tot}")

# 4. HISTORIAL
elif "📋" in choice:
    st.title(t["hist_t"])
    if os.path.exists("historial.csv"): st.subheader("Proyectos"); st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
    if os.path.exists("nomina.csv"): st.subheader("Nómina"); st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)

# 5. CATÁLOGO
elif "🛒" in choice:
    st.title(t["cat_t"])
    items = t["cat_list"]
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(items):
                name, link, img = items[i+j]
                with cols[j]:
                    if os.path.exists(img): st.image(img, use_container_width=True)
                    st.subheader(name); st.link_button(t["ver_mas"], link); st.write("")

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
