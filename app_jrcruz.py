import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
from fpdf import FPDF

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

# --- CSS: ESTILOS Y LOGO FONDO ---
logo_b64 = get_base64("5104.jpg")
if logo_b64:
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94)), url("data:image/jpg;base64,{logo_b64}");
            background-size: 500px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
        }}
        .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; height: 45px; }}
        h1, h2, h3 {{ color: #1A4F8B; }}
        .metric-box {{ background-color: rgba(26, 79, 139, 0.1); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #1A4F8B; }}
        </style>
    """, unsafe_allow_html=True)

# --- TRADUCCIONES ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Generar Estimado", "📅 Citas", "👥 Nómina", "📋 Historial", "🛒 Catálogo"],
        "calc_t": "Nuevo Estimado para Cliente",
        "btn_pdf": "Generar y Descargar PDF",
        "materiales_t": "Detalle de Materiales y Otros Cargos",
        "mano_obra": "Mano de Obra (Labor)",
        "desc": "Descripción del Material/Servicio",
        "costo": "Costo ($)",
        "cat_t": "Catálogo Floor & Decor",
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
        "menu": ["📝 Create Estimate", "📅 Appointments", "👥 Payroll", "📋 History", "🛒 Catalog"],
        "calc_t": "New Client Estimate",
        "btn_pdf": "Generate & Download PDF",
        "materiales_t": "Materials & Other Charges Details",
        "mano_obra": "Labor Cost",
        "desc": "Description of Material/Service",
        "costo": "Cost ($)",
        "cat_t": "Floor & Decor Catalog",
        "ver_mas": "View details",
        "cat_list": [
            ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decoratives", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
            ("Fixtures (Bathroom)", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Installation Materials", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    }
}
t = texts[idioma]

def guardar_datos(df, file):
    if not os.path.isfile(file): df.to_csv(file, index=False)
    else: df.to_csv(file, mode='a', header=False, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: GENERAR ESTIMADO (CALCULADORA + MATERIALES + PDF) ---
if "📝" in choice:
    st.title(t["calc_t"])
    
    col_c1, col_c2 = st.columns(2)
    with col_c1: cliente = st.text_input("Cliente / Client")
    with col_c2: fecha = st.date_input("Fecha / Date")

    st.markdown("---")
    st.subheader("1. Medidas de Áreas (Sqft)")
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("+ Añadir Área / Add Area"): st.session_state['rows'] += 1
    with col_btn2:
        if st.button("- Quitar Área / Remove Area") and st.session_state['rows'] > 1: st.session_state['rows'] -= 1

    total_sqft = 0.0
    medidas = []
    for i in range(st.session_state['rows']):
        c1, c2, c3 = st.columns([2, 1, 1])
        nombre_area = c1.text_input(f"Descripción (ej. Master Bath)", key=f"n_{i}")
        l = c2.number_input(f"Largo (ft)", min_value=0.0, key=f"l_{i}")
        a = c3.number_input(f"Ancho (ft)", min_value=0.0, key=f"a_{i}")
        sub = round(l * a, 2)
        total_sqft += sub
        medidas.append([nombre_area, l, a, sub])

    st.markdown("---")
    st.subheader(f"2. {t['materiales_t']}")
    
    mano_obra = st.number_input(f"{t['mano_obra']} ($)", min_value=0.0, step=100.0)
    
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button("+ Añadir Material / Add Item"): st.session_state['m_rows'] += 1
    
    lista_materiales = []
    total_materiales = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        d = cm1.text_input(f"{t['desc']} {j+1}", key=f"md_{j}")
        v = cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")
        total_materiales += v
        if d: lista_materiales.append([d, v])

    gran_total = mano_obra + total_materiales
    st.markdown("---")
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric("Total Sqft", f"{total_sqft} ft²")
    res_c2.metric("Items/Materials", f"${total_materiales}")
    res_c3.markdown(f"<div class='metric-box'><h3>TOTAL ESTIMATE</h3><h2 style='color:#1A4F8B'>${gran_total}</h2></div>", unsafe_allow_html=True)

    if st.button(t["btn_pdf"]):
        guardar_datos(pd.DataFrame([[fecha, cliente, total_sqft, gran_total]], columns=["Fecha", "Cliente", "Sqft", "Total"]), "historial.csv")
        
        pdf = FPDF()
        pdf.add_page()
        if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
        pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C")
        pdf.set_font("Arial", "", 10); pdf.cell(0, 5, "Professional Tile & Stone Installation", 0, 1, "C")
        pdf.ln(15)
        pdf.set_font("Arial", "B", 12); pdf.cell(0, 8, f"Estimate for: {cliente}", 0, 1)
        pdf.set_font("Arial", "", 10); pdf.cell(0, 8, f"Date: {fecha}", 0, 1); pdf.ln(5)

        # Tabla Áreas
        pdf.set_fill_color(26, 79, 139); pdf.set_text_color(255, 255, 255)
        pdf.cell(100, 8, "Area Description", 1, 0, "C", True); pdf.cell(90, 8, "Sqft", 1, 1, "C", True)
        pdf.set_text_color(0, 0, 0)
        for med in medidas:
            pdf.cell(100, 8, str(med[0]), 1); pdf.cell(90, 8, f"{med[3]} ft2", 1, 1, "R")
        pdf.ln(5)

        # Tabla Costos
        pdf.set_fill_color(26, 79, 139); pdf.set_text_color(255, 255, 255)
        pdf.cell(140, 8, "Description (Labor & Materials)", 1, 0, "C", True); pdf.cell(50, 8, "Amount", 1, 1, "C", True)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(140, 8, "Labor / Mano de Obra", 1); pdf.cell(50, 8, f"${mano_obra}", 1, 1, "R")
        for mat in lista_materiales:
            pdf.cell(140, 8, str(mat[0]), 1); pdf.cell(50, 8, f"${mat[1]}", 1, 1, "R")
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(140, 10, "TOTAL ESTIMATED COST", 1); pdf.cell(50, 10, f"${gran_total}", 1, 1, "R")
        
        pdf_file = f"Estimate_{cliente}.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("📩 Download PDF", f, file_name=pdf_file)

# --- MODULO 2: CITAS ---
elif "📅" in choice:
    st.title(t["menu"][1])
    with st.form("f_citas"):
        f = st.date_input("Fecha"); h = st.time_input("Hora"); c = st.text_input("Cliente"); n = st.text_area("Notas")
        if st.form_submit_button("Agendar / Schedule"):
            guardar_datos(pd.DataFrame([[f, h, c, n]], columns=["Fecha", "Hora", "Cliente", "Notas"]), "citas.csv")
            st.success("Cita guardada!")
    if os.path.exists("citas.csv"): st.dataframe(pd.read_csv("citas.csv").sort_values(by="Fecha"), use_container_width=True)

# --- MODULO 3: NÓMINA ---
elif "👥" in choice:
    st.title(t["menu"][2])
    with st.form("f_nom"):
        nom = st.text_input("Nombre"); hrs = st.number_input("Horas", min_value=0.0); pag = st.number_input("Pago/Hr", min_value=0.0)
        if st.form_submit_button("Registrar"):
            tot = hrs * pag
            guardar_datos(pd.DataFrame([[datetime.now().date(), nom, tot]], columns=["Fecha", "Empleado", "Total"]), "nomina.csv")
            st.info(f"Total: ${tot}")

# --- MODULO 4: HISTORIAL ---
elif "📋" in choice:
    st.title(t["menu"][3])
    tab1, tab2 = st.tabs(["Proyectos/Estimados", "Nómina"])
    with tab1:
        if os.path.exists("historial.csv"): st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
    with tab2:
        if os.path.exists("nomina.csv"): st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)

# --- MODULO 5: CATÁLOGO ---
elif "🛒" in choice:
    st.title(t["menu"][4])
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
