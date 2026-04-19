import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
from fpdf import FPDF

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# Función para convertir el logo a base64 (fondo)
def get_base64_logo(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

# --- CSS: LOGO FONDO Y ESTILOS ---
logo_b64 = get_base64_logo("5104.jpg")
if logo_b64:
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)), url("data:image/jpg;base64,{logo_b64}");
            background-size: 500px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
        }}
        .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; }}
        h1, h2, h3 {{ color: #1A4F8B; }}
        </style>
    """, unsafe_allow_html=True)

# --- TRADUCCIONES ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📊 Calculadora", "📅 Citas", "👥 Nómina", "📋 Historial", "🛒 Catálogo"],
        "calc_t": "Calculadora Dinámica de Área",
        "add_row": "➕ Agregar otra medida",
        "del_row": "❌ Quitar última medida",
        "gen_pdf": "PDF Estimado",
        "citas_t": "Agenda de Citas",
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
        "add_row": "➕ Add another measurement",
        "del_row": "❌ Remove last measurement",
        "gen_pdf": "PDF Estimate",
        "citas_t": "Appointment Calendar",
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

# --- LÓGICA DE DATOS ---
def guardar_archivo(df, file):
    if not os.path.isfile(file): df.to_csv(file, index=False)
    else: df.to_csv(file, mode='a', header=False, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Menu", t["menu"])

# 1. CALCULADORA DINÁMICA CON MÚLTIPLES MEDIDAS
if "📊" in choice:
    st.title(t["calc_t"])
    
    # Inicializar el número de filas en la sesión
    if 'rows' not in st.session_state:
        st.session_state['rows'] = 1

    cliente = st.text_input("Cliente / Client Name")
    
    # Botones para agregar o quitar filas
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button(t["add_row"]):
            st.session_state['rows'] += 1
    with col_b2:
        if st.button(t["del_row"]) and st.session_state['rows'] > 1:
            st.session_state['rows'] -= 1

    medidas = []
    total_area = 0.0

    # Crear las celdas dinámicamente
    for i in range(st.session_state['rows']):
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            l = st.number_input(f"Largo / Length {i+1} (ft)", min_value=0.0, key=f"l_{i}")
        with c2:
            a = st.number_input(f"Ancho / Width {i+1} (ft)", min_value=0.0, key=f"a_{i}")
        with c3:
            st.write("Subtotal")
            sub = round(l * a, 2)
            st.info(f"{sub} sqft")
            medidas.append({'fila': i+1, 'l': l, 'a': a, 'sub': sub})
            total_area += sub

    st.subheader(f"Total Area: {total_area} sqft")

    if st.button("Guardar y Generar PDF"):
        # Guardar en CSV
        df_calc = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), cliente, total_area]], columns=["Fecha", "Cliente", "Sqft"])
        guardar_archivo(df_calc, "historial.csv")
        
        # Crear PDF
        pdf = FPDF()
        pdf.add_page()
        if os.path.exists("5104.jpg"):
            pdf.image("5104.jpg", 10, 8, 33)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "JR CRUZ MASONRY LLC - ESTIMATE", 0, 1, "C")
        pdf.ln(20)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", 0, 1)
        pdf.cell(0, 10, f"Client: {cliente}", 0, 1)
        pdf.ln(10)
        pdf.cell(40, 10, "Row", 1)
        pdf.cell(40, 10, "Length (ft)", 1)
        pdf.cell(40, 10, "Width (ft)", 1)
        pdf.cell(40, 10, "Subtotal", 1)
        pdf.ln()
        for m in medidas:
            pdf.cell(40, 10, str(m['fila']), 1)
            pdf.cell(40, 10, str(m['l']), 1)
            pdf.cell(40, 10, str(m['a']), 1)
            pdf.cell(40, 10, f"{m['sub']} sqft", 1)
            pdf.ln()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(120, 10, "TOTAL AREA:", 1)
        pdf.cell(40, 10, f"{total_area} sqft", 1)
        
        pdf_name = f"Estimate_{cliente}.pdf"
        pdf.output(pdf_name)
        
        with open(pdf_name, "rb") as f:
            st.download_button("📩 Descargar Estimado PDF", f, file_name=pdf_name)

# 2. CALENDARIO DE CITAS
elif "📅" in choice:
    st.title(t["citas_t"])
    with st.form("citas_form"):
        fecha_cita = st.date_input("Fecha de la cita / Date")
        hora_cita = st.time_input("Hora / Time")
        cliente_cita = st.text_input("Cliente / Client")
        nota = st.text_area("Notas (Dirección, trabajo a realizar)")
        if st.form_submit_button("Agendar Cita"):
            df_cita = pd.DataFrame([[fecha_cita, hora_cita, cliente_cita, nota]], columns=["Fecha", "Hora", "Cliente", "Notas"])
            guardar_archivo(df_cita, "citas.csv")
            st.success("Cita guardada!")
    
    if os.path.exists("citas.csv"):
        st.write("---")
        st.subheader("Próximas Citas")
        st.dataframe(pd.read_csv("citas.csv").sort_values(by="Fecha"), use_container_width=True)

# (Los demás módulos se mantienen igual: Nómina, Historial, Catálogo...)
elif "👥" in choice:
    st.title("Nómina")
    # ... código de nómina igual al anterior ...
elif "📋" in choice:
    st.title("Historial")
    # ... código de historial igual al anterior ...
elif "🛒" in choice:
    st.title("Catálogo")
    # ... código de catálogo igual al anterior ...
