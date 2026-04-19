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

# --- CSS: LOGO Y ESTILOS ---
logo_b64 = get_base64("5104.jpg")
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94))
        {f', url("data:image/jpg;base64,{logo_b64}")' if logo_b64 else ""};
        background-size: 400px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
    }}
    [data-testid="stImage"] img {{
        width: 100%; height: 250px; object-fit: cover; border-radius: 15px; border: 2px solid #1A4F8B;
    }}
    .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; height: 45px; }}
    h1, h2, h3 {{ color: #1A4F8B; }}
    </style>
""", unsafe_allow_html=True)

# --- DICCIONARIO BILINGÜE ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "step1": "1. Áreas y Medidas (Sqft)", "step2": "2. Desglose de Trabajo y Materiales", "step3": "3. Registro de Pagos",
        "cliente": "Cliente", "fecha": "Fecha", "desc": "Descripción", "largo": "Largo (ft)", "ancho": "Ancho (ft)",
        "mano_obra": "Mano de Obra", "costo": "Costo ($)", "item": "Artículo",
        "dep": "Depósito", "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "btn_pdf": "Generar PDF de Estimado", "btn_upd_pdf": "Descargar PDF Actualizado", "ver_mas": "Ver detalles"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "step1": "1. Areas & Measurements (Sqft)", "step2": "2. Labor & Materials Breakdown", "step3": "3. Payment Record",
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item",
        "dep": "Deposit", "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_pdf": "Generate Estimate PDF", "btn_upd_pdf": "Download Updated PDF", "ver_mas": "View details"
    }
}
t = texts[idioma]

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: ESTIMADO ---
if "📝" in choice:
    st.title(t["menu"][0])
    c_inf1, c_inf2 = st.columns(2)
    cliente = c_inf1.text_input(t["cliente"])
    fecha_input = c_inf2.date_input(t["fecha"])

    st.subheader(t["step1"])
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    col_b1, col_b2 = st.columns(2)
    if col_b1.button(f"+ {t['desc']}"): st.session_state['rows'] += 1
    if col_b2.button(f"- {t['desc']}") and st.session_state['rows'] > 1: st.session_state['rows'] -= 1

    for i in range(st.session_state['rows']):
        ca1, ca2, ca3 = st.columns([2, 1, 1])
        ca1.text_input(f"{t['desc']} {i+1}", key=f"n_{i}")
        ca2.number_input(t["largo"], min_value=0.0, key=f"l_{i}")
        ca3.number_input(t["ancho"], min_value=0.0, key=f"a_{i}")

    st.subheader(t["step2"])
    mano_obra = st.number_input(t["mano_obra"], min_value=0.0)
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button(f"+ {t['item']}"): st.session_state['m_rows'] += 1
    
    total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        cm1.text_input(f"{t['item']} {j+1}", key=f"md_{j}")
        v_mat = cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")
        total_mat += v_mat

    st.subheader(t["step3"])
    if 'dep_rows' not in st.session_state: st.session_state['dep_rows'] = 1
    cd1, cd2 = st.columns(2)
    if cd1.button(f"+ {t['dep']}"): st.session_state['dep_rows'] += 1
    if cd2.button(f"- {t['dep']}") and st.session_state['dep_rows'] > 1: st.session_state['dep_rows'] -= 1
    
    lista_deps = []
    for k in range(st.session_state['dep_rows']):
        v_dep = st.number_input(f"{t['dep']} {k+1}", min_value=0.0, key=f"dep_val_{k}")
        lista_deps.append(v_dep)

    total_contrato = mano_obra + total_mat
    total_pagado = sum(lista_deps)
    balance = total_contrato - total_pagado

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric(t["total_c"], f"${total_contrato}")
    m2.metric(t["total_p"], f"${total_pagado}")
    m3.metric(t["balance"], f"${balance}")

    if st.button(t["btn_pdf"]):
        deps_str = ";".join(map(str, lista_deps))
        df_new = pd.DataFrame([[str(fecha_input), cliente, total_contrato, deps_str, total_pagado, balance]], 
                              columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
        if not os.path.exists("historial_final.csv"): df_new.to_csv("historial_final.csv", index=False)
        else: df_new.to_csv("historial_final.csv", mode='a', header=False, index=False)
        st.success("Guardado en Historial.")

# --- MODULO 2: HISTORIAL CON PDF ---
elif "📋" in choice:
    st.title(t["menu"][1])
    if os.path.exists("historial_final.csv"):
        df_h = pd.read_csv("historial_final.csv")
        st.dataframe(df_h, use_container_width=True)
        
        st.subheader("Descargar Recibo de Cliente")
        sel = st.selectbox("Seleccione Cliente", df_h["Cliente"].unique())
        if sel:
            row = df_h[df_h["Cliente"] == sel].iloc[-1]
            if st.button(t["btn_upd_pdf"]):
                pdf = FPDF()
                pdf.add_page()
                if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 33)
                pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C"); pdf.ln(10)
                pdf.set_font("Arial", "B", 12); pdf.cell(0, 10, f"CLIENTE: {sel}", 0, 1)
                pdf.cell(0, 10, f"FECHA: {row['Fecha']}", 0, 1); pdf.ln(5)
                
                pdf.set_fill_color(230, 230, 230)
                pdf.cell(100, 10, "CONCEPTO", 1, 0, "C", True); pdf.cell(90, 10, "MONTO", 1, 1, "C", True)
                pdf.cell(100, 10, t["total_c"], 1); pdf.cell(90, 10, f"${row['Total']}", 1, 1, "R")
                
                deps = str(row['Depositos']).split(";")
                for idx, d in enumerate(deps):
                    pdf.cell(100, 10, f"{t['dep']} {idx+1}", 1); pdf.cell(90, 10, f"${d}", 1, 1, "R")
                
                pdf.set_font("Arial", "B", 12)
                pdf.cell(100, 10, t["total_p"], 1); pdf.cell(90, 10, f"${row['Pagado']}", 1, 1, "R")
                pdf.set_text_color(200, 0, 0)
                pdf.cell(100, 10, t["balance"], 1); pdf.cell(90, 10, f"${row['Balance']}", 1, 1, "R")
                
                p_file = f"Recibo_{sel}.pdf"
                pdf.output(p_file)
                with open(p_file, "rb") as f: st.download_button("📩 Descargar PDF Ahora", f, file_name=p_file)

# --- CITAS Y NÓMINA (SIN CAMBIOS) ---
elif "📅" in choice:
    st.title(t["menu"][2]); st.write("Módulo de Citas operativo.")
elif "👥" in choice:
    st.title(t["menu"][3]); st.write("Módulo de Nómina operativo.")

# --- CATÁLOGO (8 ARTÍCULOS) ---
elif "🛒" in choice:
    st.title(t["menu"][4])
    cat = [
        ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
        ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
        ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
        ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
        ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
        ("Decoratives", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
        ("Fixtures", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
        ("Materials", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
    ]
    for i in range(0, len(cat), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(cat):
                n, l, img = cat[i+j]
                with cols[j]:
                    if os.path.exists(img): st.image(img)
                    st.subheader(n); st.link_button(t["ver_mas"], l)

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
