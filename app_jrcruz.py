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

# --- CSS: ESTILOS Y LOGO ---
logo_b64 = get_base64("5104.jpg")
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94))
        {f', url("data:image/jpg;base64,{logo_b64}")' if logo_b64 else ""};
        background-size: 400px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
    }}
    [data-testid="stImage"] img {{ width: 100%; height: 250px; object-fit: cover; border-radius: 15px; border: 2px solid #1A4F8B; }}
    .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; height: 45px; }}
    h1, h2, h3 {{ color: #1A4F8B; }}
    </style>
""", unsafe_allow_html=True)

# --- TRADUCCIONES (CORREGIDAS PARA EVITAR ERRORES) ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "step1": "1. Áreas y Medidas (Sqft)", "step2": "2. Desglose de Trabajo y Materiales", "step3": "3. Registro de Pagos",
        "cliente": "Cliente", "fecha": "Fecha", "desc": "Descripción", "largo": "Largo (ft)", "ancho": "Ancho (ft)",
        "mano_obra": "Mano de Obra", "costo": "Costo ($)", "item": "Artículo", "dep": "Depósito",
        "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "btn_pdf": "Guardar Registro", "btn_upd_pdf": "Descargar Recibo PDF", "ver_mas": "Ver detalles"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "step1": "1. Areas & Measurements (Sqft)", "step2": "2. Labor & Materials Breakdown", "step3": "3. Payment Record",
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item", "dep": "Deposit",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_pdf": "Save Record", "btn_upd_pdf": "Download Receipt PDF", "ver_mas": "View details"
    }
}
t = texts[idioma]

choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: ESTIMADO (CON DEPÓSITOS DINÁMICOS) ---
if "📝" in choice:
    st.title(t["menu"][0])
    c1, c2 = st.columns(2)
    cliente = c1.text_input(t["cliente"])
    fec = c2.date_input(t["fecha"])

    st.subheader(t["step1"])
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    cb1, cb2 = st.columns(2)
    if cb1.button("+ Area"): st.session_state['rows'] += 1
    if cb2.button("- Area") and st.session_state['rows'] > 1: st.session_state['rows'] -= 1
    for i in range(st.session_state['rows']):
        ca1, ca2, ca3 = st.columns([2, 1, 1])
        ca1.text_input(f"{t['desc']} {i+1}", key=f"n_{i}")
        ca2.number_input(t["largo"], min_value=0.0, key=f"l_{i}")
        ca3.number_input(t["ancho"], min_value=0.0, key=f"a_{i}")

    st.subheader(t["step2"])
    mano_obra = st.number_input(t["mano_obra"], min_value=0.0)
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button("+ " + t["item"]): st.session_state['m_rows'] += 1
    total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        cm1.text_input(f"{t['item']} {j+1}", key=f"md_{j}")
        v_mat = cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")
        total_mat += v_mat

    st.subheader(t["step3"])
    if 'dep_rows' not in st.session_state: st.session_state['dep_rows'] = 1
    cd1, cd2 = st.columns(2)
    if cd1.button("+ " + t["dep"]): st.session_state['dep_rows'] += 1
    if cd2.button("- " + t["dep"]) and st.session_state['dep_rows'] > 1: st.session_state['dep_rows'] -= 1
    
    lista_deps = []
    for k in range(st.session_state['dep_rows']):
        v_dep = st.number_input(f"{t['dep']} {k+1} ($)", min_value=0.0, key=f"dv_{k}")
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
        df = pd.DataFrame([[str(fec), cliente, total_contrato, deps_str, total_pagado, balance]], 
                          columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
        file = "historial_final.csv"
        if not os.path.exists(file): df.to_csv(file, index=False)
        else: df.to_csv(file, mode='a', header=False, index=False)
        st.success("¡Datos guardados correctamente!")

# --- MODULO 2: HISTORIAL Y PDF ---
elif "📋" in choice:
    st.title(t["menu"][1])
    file = "historial_final.csv"
    if os.path.exists(file):
        df_h = pd.read_csv(file)
        st.dataframe(df_h, use_container_width=True)
        
        st.subheader("Generar PDF de Cliente")
        sel_c = st.selectbox("Seleccione Cliente", df_h["Cliente"].unique())
        if sel_c:
            datos = df_h[df_h["Cliente"] == sel_c].iloc[-1]
            if st.button(t["btn_upd_pdf"]):
                pdf = FPDF()
                pdf.add_page()
                if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
                pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C"); pdf.ln(10)
                pdf.set_font("Arial", "B", 12); pdf.cell(0, 10, f"CLIENTE: {sel_c}", 0, 1)
                pdf.cell(0, 10, f"FECHA: {datos['Fecha']}", 0, 1); pdf.ln(5)
                
                pdf.set_fill_color(230, 230, 230)
                pdf.cell(100, 10, "CONCEPTO", 1, 0, "C", True); pdf.cell(90, 10, "MONTO", 1, 1, "C", True)
                pdf.cell(100, 10, t["total_c"], 1); pdf.cell(90, 10, f"${datos['Total']}", 1, 1, "R")
                
                deps = str(datos['Depositos']).split(";")
                for idx, d in enumerate(deps):
                    pdf.cell(100, 10, f"{t['dep']} {idx+1}", 1); pdf.cell(90, 10, f"${d}", 1, 1, "R")
                
                pdf.set_font("Arial", "B", 12)
                pdf.cell(100, 10, t["total_p"], 1); pdf.cell(90, 10, f"${datos['Pagado']}", 1, 1, "R")
                pdf.set_text_color(200, 0, 0)
                pdf.cell(100, 10, t["balance"], 1); pdf.cell(90, 10, f"${datos['Balance']}", 1, 1, "R")
                
                out = f"Recibo_{sel_c}.pdf"
                pdf.output(out)
                with open(out, "rb") as f: st.download_button("📩 Haz clic aquí para descargar", f, file_name=out)

# --- MODULO 3: CITAS (FUNCIONANDO) ---
elif "📅" in choice:
    st.title(t["menu"][2])
    with st.form("citas_form"):
        fc = st.date_input(t["fecha"]); hc = st.time_input("Hora"); clc = st.text_input(t["cliente"])
        if st.form_submit_button("Agendar Cita"):
            df_c = pd.DataFrame([[str(fc), str(hc), clc]], columns=["Fecha", "Hora", "Cliente"])
            if not os.path.exists("citas.csv"): df_c.to_csv("citas.csv", index=False)
            else: df_c.to_csv("citas.csv", mode='a', header=False, index=False)
            st.success("Cita guardada con éxito.")
    if os.path.exists("citas.csv"): st.dataframe(pd.read_csv("citas.csv"))

# --- MODULO 4: NÓMINA (FUNCIONANDO) ---
elif "👥" in choice:
    st.title(t["menu"][3])
    with st.form("nomina_form"):
        emp = st.text_input("Nombre del Empleado"); hras = st.number_input("Horas Trabajadas"); tari = st.number_input("Tarifa x Hora")
        if st.form_submit_button("Registrar Nómina"):
            total_n = hras * tari
            df_n = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), emp, total_n]], columns=["Fecha", "Empleado", "Pago Total"])
            if not os.path.exists("nomina.csv"): df_n.to_csv("nomina.csv", index=False)
            else: df_n.to_csv("nomina.csv", mode='a', header=False, index=False)
            st.success(f"Pago de ${total_n} registrado.")
    if os.path.exists("nomina.csv"): st.dataframe(pd.read_csv("nomina.csv"))

# --- MODULO 5: CATÁLOGO ---
elif "🛒" in choice:
    st.title(t["menu"][4])
    cat = [("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"), ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"), 
           ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"), ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
           ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"), ("Decoratives", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
           ("Fixtures", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"), ("Materials", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")]
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
