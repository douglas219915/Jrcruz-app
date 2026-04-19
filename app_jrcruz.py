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

# --- CSS: ESTILOS, LOGO FONDO Y CORRECCIÓN DE IMÁGENES ---
logo_b64 = get_base64("5104.jpg")
if logo_b64:
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94)), url("data:image/jpg;base64,{logo_b64}");
            background-size: 500px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
        }}
        [data-testid="stImage"] img {{
            width: 100%; height: 250px; object-fit: cover; border-radius: 12px;
            border: 1px solid #ddd; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        }}
        .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; height: 45px; }}
        h1, h2, h3 {{ color: #1A4F8B; }}
        .metric-box {{ background-color: rgba(26, 79, 139, 0.1); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #1A4F8B; }}
        .status-paid {{ background-color: #D4EDDA; color: #155724; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; }}
        .status-pending {{ background-color: #FFF3CD; color: #856404; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; }}
        </style>
    """, unsafe_allow_html=True)

# --- TRADUCCIONES ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Estimado y Pagos", "📅 Citas", "👥 Nómina", "📋 Historial", "🛒 Catálogo"],
        "calc_t": "Estimado y Control de Pagos",
        "btn_pdf": "Generar PDF de Factura/Estimado",
        "materiales_t": "Desglose de Trabajo y Materiales",
        "mano_obra": "Mano de Obra (Labor)",
        "desc": "Descripción", "costo": "Costo ($)",
        "pago_t": "Registro de Pagos del Cliente",
        "deposito": "Depósito / Adelanto ($)",
        "otros_pagos": "Otros Abonos / Pagos ($)",
        "cat_t": "Catálogo Floor & Decor", "ver_mas": "Ver detalles",
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
        "menu": ["📝 Estimate & Payments", "📅 Appointments", "👥 Payroll", "📋 History", "🛒 Catalog"],
        "calc_t": "Estimate & Payment Control",
        "btn_pdf": "Generate Invoice/Estimate PDF",
        "materiales_t": "Labor & Materials Breakdown",
        "mano_obra": "Labor Cost",
        "desc": "Description", "costo": "Cost ($)",
        "pago_t": "Client Payment Record",
        "deposito": "Deposit / Down Payment ($)",
        "otros_pagos": "Additional Payments ($)",
        "cat_t": "Floor & Decor Catalog", "ver_mas": "View details",
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

def guardar_datos(df, filename):
    if not os.path.isfile(filename): df.to_csv(filename, index=False)
    else: df.to_csv(filename, mode='a', header=False, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: ESTIMADO Y PAGOS ---
if "📝" in choice:
    st.title(t["calc_t"])
    col_c1, col_c2 = st.columns(2)
    with col_c1: cliente = st.text_input("Cliente / Client")
    with col_c2: fecha = st.date_input("Fecha / Date")

    st.markdown("---")
    st.subheader("1. Áreas y Medidas")
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    
    cb1, cb2 = st.columns(2)
    with cb1:
        if st.button("+ Área"): st.session_state['rows'] += 1
    with cb2:
        if st.button("- Área") and st.session_state['rows'] > 1: st.session_state['rows'] -= 1

    total_sqft = 0.0
    medidas = []
    for i in range(st.session_state['rows']):
        c1, c2, c3 = st.columns([2, 1, 1])
        n_a = c1.text_input(f"Área {i+1}", key=f"n_{i}")
        l = c2.number_input(f"Largo", min_value=0.0, key=f"l_{i}")
        a = c3.number_input(f"Ancho", min_value=0.0, key=f"a_{i}")
        sub = round(l * a, 2)
        total_sqft += sub
        medidas.append([n_a, l, a, sub])

    st.markdown("---")
    st.subheader(f"2. {t['materiales_t']}")
    mano_obra = st.number_input(f"{t['mano_obra']}", min_value=0.0)
    
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button("+ Item"): st.session_state['m_rows'] += 1
    
    lista_mat = []
    total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        d = cm1.text_input(f"Descripción {j+1}", key=f"md_{j}")
        v = cm2.number_input(f"Costo $ {j+1}", min_value=0.0, key=f"mv_{j}")
        total_mat += v
        if d: lista_mat.append([d, v])

    total_contrato = mano_obra + total_mat

    st.markdown("---")
    st.subheader(f"3. {t['pago_t']}")
    col_p1, col_p2 = st.columns(2)
    with col_p1: deposito = st.number_input(t["deposito"], min_value=0.0)
    with col_p2: otros_pagos = st.number_input(t["otros_pagos"], min_value=0.0)
    
    total_pagado = deposito + otros_pagos
    balance_pendiente = total_contrato - total_pagado

    # INDICADORES DE TOTALES
    st.markdown("---")
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Total Contrato", f"${total_contrato}")
    res2.metric("Total Pagado", f"${total_pagado}", delta=f"+{total_pagado}")
    res3.metric("Balance Pendiente", f"${balance_pendiente}", delta=f"-{balance_pendiente}", delta_color="inverse")
    
    with res4:
        if balance_pendiente <= 0 and total_contrato > 0:
            st.markdown(f"<div class='status-paid'>PAID IN FULL / PAGADO</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='status-pending'>PENDING / PENDIENTE</div>", unsafe_allow_html=True)

    if st.button(t["btn_pdf"]):
        guardar_datos(pd.DataFrame([[str(fecha), cliente, total_contrato, total_pagado, balance_pendiente]], 
                                   columns=["Fecha", "Cliente", "Total", "Pagado", "Balance"]), "historial.csv")
        pdf = FPDF()
        pdf.add_page()
        if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
        pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C"); pdf.ln(15)
        pdf.set_font("Arial", "B", 12); pdf.cell(0, 8, f"Client: {cliente}", 0, 1)
        pdf.set_font("Arial", "", 10); pdf.cell(0, 8, f"Date: {fecha}", 0, 1); pdf.ln(5)
        
        # Tabla de Cargos
        pdf.set_fill_color(26, 79, 139); pdf.set_text_color(255, 255, 255)
        pdf.cell(140, 8, "Description", 1, 0, "C", True); pdf.cell(50, 8, "Amount", 1, 1, "C", True)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(140, 8, "Labor / Mano de Obra", 1); pdf.cell(50, 8, f"${mano_obra}", 1, 1, "R")
        for m in lista_mat:
            pdf.cell(140, 8, str(m[0]), 1); pdf.cell(50, 8, f"${m[1]}", 1, 1, "R")
        
        pdf.set_font("Arial", "B", 11)
        pdf.cell(140, 10, "TOTAL CONTRACT AMOUNT", 1); pdf.cell(50, 10, f"${total_contrato}", 1, 1, "R")
        pdf.set_text_color(0, 100, 0)
        pdf.cell(140, 10, "TOTAL PAID TO DATE", 1); pdf.cell(50, 10, f"- ${total_pagado}", 1, 1, "R")
        pdf.set_text_color(200, 0, 0)
        pdf.cell(140, 10, "BALANCE DUE", 1); pdf.cell(50, 10, f"${balance_pendiente}", 1, 1, "R")
        
        if balance_pendiente <= 0:
            pdf.ln(5); pdf.set_text_color(0, 128, 0); pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "STATUS: PAID IN FULL", 0, 1, "C")

        p_f = f"Invoice_{cliente}.pdf"
        pdf.output(p_f)
        with open(p_f, "rb") as f: st.download_button("📩 Download Invoice/PDF", f, file_name=p_f)

# --- MODULOS RESTANTES (SE MANTIENEN IGUAL) ---
elif "📅" in choice:
    st.title(t["menu"][1])
    with st.form("f_c"):
        f = st.date_input("Fecha"); h = st.time_input("Hora"); c = st.text_input("Cliente"); n = st.text_area("Notas")
        if st.form_submit_button("Agendar"):
            guardar_datos(pd.DataFrame([[str(f), str(h), c, n]], columns=["Fecha", "Hora", "Cliente", "Notas"]), "citas.csv")
            st.success("Guardado")
    if os.path.exists("citas.csv"): st.dataframe(pd.read_csv("citas.csv"), use_container_width=True)

elif "👥" in choice:
    st.title(t["menu"][2])
    with st.form("f_n"):
        nom = st.text_input("Nombre"); hrs = st.number_input("Horas", min_value=0.0); pag = st.number_input("Pago/Hr", min_value=0.0)
        if st.form_submit_button("Registrar"):
            tot = hrs * pag
            guardar_datos(pd.DataFrame([[str(datetime.now().date()), nom, tot]], columns=["Fecha", "Empleado", "Total"]), "nomina.csv")
            st.info(f"Total: ${tot}")

elif "📋" in choice:
    st.title(t["menu"][3])
    t1, t2 = st.tabs(["Estimados/Pagos", "Nómina"])
    with t1:
        if os.path.exists("historial.csv"): st.dataframe(pd.read_csv("historial.csv"), use_container_width=True)
    with t2:
        if os.path.exists("nomina.csv"): st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)

elif "🛒" in choice:
    st.title(t["cat_t"])
    it = t["cat_list"]
    for i in range(0, len(it), 2):
        cs = st.columns(2)
        for j in range(2):
            if i+j < len(it):
                name, link, img = it[i+j]
                with cs[j]:
                    if os.path.exists(img): st.image(img, use_container_width=True)
                    st.subheader(name); st.link_button(t["ver_mas"], link); st.write("")

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
