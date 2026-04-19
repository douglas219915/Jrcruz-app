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

# --- CSS: ESTILOS, LOGO FONDO Y BOTONES ---
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

# --- DICCIONARIO DE TRADUCCIÓN COMPLETO ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Estimado y Pagos", "📅 Citas", "👥 Nómina", "📋 Historial", "🛒 Catálogo"],
        "calc_t": "Estimado y Control de Pagos",
        "btn_pdf": "Generar PDF en Español",
        "step1": "1. Áreas y Medidas (Sqft)",
        "step2": "2. Desglose de Trabajo y Materiales",
        "step3": "3. Registro de Pagos (Depósitos)",
        "cliente": "Cliente", "fecha": "Fecha", "desc": "Descripción",
        "largo": "Largo (ft)", "ancho": "Ancho (ft)", "total_area": "Área Total",
        "mano_obra": "Mano de Obra", "costo": "Costo ($)", "item": "Artículo",
        "dep1": "Depósito 1 ($)", "dep2": "Depósito 2 ($)", "dep3": "Depósito 3 ($)",
        "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "status_p": "PAGADO POR COMPLETO", "status_pen": "BALANCE PENDIENTE",
        "cat_t": "Catálogo Floor & Decor", "ver_mas": "Ver detalles"
    },
    "English": {
        "menu": ["📝 Estimate & Payments", "📅 Appointments", "👥 Payroll", "📋 History", "🛒 Catalog"],
        "calc_t": "Estimate & Payment Control",
        "btn_pdf": "Generate PDF in English",
        "step1": "1. Areas & Measurements (Sqft)",
        "step2": "2. Labor & Materials Breakdown",
        "step3": "3. Payment Record (Deposits)",
        "cliente": "Client", "fecha": "Date", "desc": "Description",
        "largo": "Length (ft)", "ancho": "Width (ft)", "total_area": "Total Area",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item",
        "dep1": "Deposit 1 ($)", "dep2": "Deposit 2 ($)", "dep3": "Deposit 3 ($)",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "status_p": "PAID IN FULL", "status_pen": "PENDING BALANCE",
        "cat_t": "Floor & Decor Catalog", "ver_mas": "View details"
    }
}
t = texts[idioma]

def guardar_datos(df, filename):
    if not os.path.isfile(filename): df.to_csv(filename, index=False)
    else: df.to_csv(filename, mode='a', header=False, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel", t["menu"])

if "📝" in choice:
    st.title(t["calc_t"])
    col_c1, col_c2 = st.columns(2)
    with col_c1: cliente = st.text_input(t["cliente"])
    with col_c2: fecha_input = st.date_input(t["fecha"])

    st.markdown("---")
    st.subheader(t["step1"])
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    
    cb1, cb2 = st.columns(2)
    with cb1:
        if st.button(f"+ {t['desc']}"): st.session_state['rows'] += 1
    with cb2:
        if st.button(f"- {t['desc']}") and st.session_state['rows'] > 1: st.session_state['rows'] -= 1

    total_sqft = 0.0
    for i in range(st.session_state['rows']):
        c1, c2, c3 = st.columns([2, 1, 1])
        n_a = c1.text_input(f"{t['desc']} {i+1}", key=f"n_{i}")
        l = c2.number_input(t["largo"], min_value=0.0, key=f"l_{i}")
        a = c3.number_input(t["ancho"], min_value=0.0, key=f"a_{i}")
        total_sqft += round(l * a, 2)

    st.markdown("---")
    st.subheader(t["step2"])
    mano_obra = st.number_input(t["mano_obra"], min_value=0.0)
    
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button(f"+ {t['item']}"): st.session_state['m_rows'] += 1
    
    lista_mat = []
    total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        d = cm1.text_input(f"{t['item']} {j+1}", key=f"md_{j}")
        v = cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")
        total_mat += v
        if d: lista_mat.append([d, v])

    total_contrato = mano_obra + total_mat

    st.markdown("---")
    st.subheader(t["step3"])
    cp1, cp2, cp3 = st.columns(3)
    d1 = cp1.number_input(t["dep1"], min_value=0.0)
    d2 = cp2.number_input(t["dep2"], min_value=0.0)
    d3 = cp3.number_input(t["dep3"], min_value=0.0)
    
    total_pagado = d1 + d2 + d3
    balance_pendiente = total_contrato - total_pagado

    st.markdown("---")
    res1, res2, res3, res4 = st.columns(4)
    res1.metric(t["total_c"], f"${total_contrato}")
    res2.metric(t["total_p"], f"${total_pagado}")
    res3.metric(t["balance"], f"${balance_pendiente}")
    
    with res4:
        st.markdown(f"<div class='{'status-paid' if balance_pendiente <= 0 else 'status-pending'}'>{t['status_p'] if balance_pendiente <= 0 else t['status_pen']}</div>", unsafe_allow_html=True)

    if st.button(t["btn_pdf"]):
        guardar_datos(pd.DataFrame([[str(fecha_input), cliente, total_contrato, d1, d2, d3, total_pagado, balance_pendiente]], 
                                   columns=["Fecha", "Cliente", "Total", "Dep1", "Dep2", "Dep3", "Pagado", "Balance"]), "historial.csv")
        pdf = FPDF()
        pdf.add_page()
        if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
        pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C"); pdf.ln(15)
        pdf.set_font("Arial", "B", 12); pdf.cell(0, 8, f"{t['cliente']}: {cliente}", 0, 1)
        pdf.set_font("Arial", "", 10); pdf.cell(0, 8, f"{t['fecha']}: {fecha_input}", 0, 1); pdf.ln(5)
        
        pdf.set_fill_color(26, 79, 139); pdf.set_text_color(255, 255, 255)
        pdf.cell(140, 8, t["desc"], 1, 0, "C", True); pdf.cell(50, 8, t["costo"], 1, 1, "C", True)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(140, 8, t["mano_obra"], 1); pdf.cell(50, 8, f"${mano_obra}", 1, 1, "R")
        for m in lista_mat:
            pdf.cell(140, 8, m[0], 1); pdf.cell(50, 8, f"${m[1]}", 1, 1, "R")
        
        pdf.ln(5); pdf.set_font("Arial", "B", 11)
        pdf.cell(140, 8, t["total_c"], 1); pdf.cell(50, 8, f"${total_contrato}", 1, 1, "R")
        if d1 > 0: pdf.cell(140, 8, t["dep1"], 1); pdf.cell(50, 8, f"- ${d1}", 1, 1, "R")
        if d2 > 0: pdf.cell(140, 8, t["dep2"], 1); pdf.cell(50, 8, f"- ${d2}", 1, 1, "R")
        if d3 > 0: pdf.cell(140, 8, t["dep3"], 1); pdf.cell(50, 8, f"- ${d3}", 1, 1, "R")
        pdf.set_text_color(200, 0, 0)
        pdf.cell(140, 10, t["balance"], 1); pdf.cell(50, 10, f"${balance_pendiente}", 1, 1, "R")
        
        pdf_file = f"Invoice_{cliente}.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f: st.download_button(f"📩 {t['btn_pdf']}", f, file_name=pdf_file)

elif "📋" in choice:
    st.title(t["menu"][3])
    t1, t2 = st.tabs([t["menu"][0], t["menu"][2]])
    with t1:
        if os.path.exists("historial.csv"):
            df = pd.read_csv("historial.csv")
            # Traducir encabezados del historial en pantalla
            df.columns = [t['fecha'], t['cliente'], t['total_c'], t['dep1'], t['dep2'], t['dep3'], t['total_p'], t['balance']]
            st.dataframe(df, use_container_width=True)
            if st.button("Reset Historial"): os.remove("historial.csv"); st.rerun()
    with t2:
        if os.path.exists("nomina.csv"): st.dataframe(pd.read_csv("nomina.csv"), use_container_width=True)

# Los demás módulos (Citas, Nómina, Catálogo) se mantienen con lógica similar bilingüe
elif "📅" in choice:
    st.title(t["menu"][1])
    with st.form("f_c"):
        f = st.date_input(t["fecha"]); h = st.time_input("Time"); c = st.text_input(t["cliente"]); n = st.text_area("Notes")
        if st.form_submit_button("Save"):
            guardar_datos(pd.DataFrame([[str(f), str(h), c, n]], columns=["Date", "Time", "Client", "Notes"]), "citas.csv")
            st.success("Saved!")
    if os.path.exists("citas.csv"): st.dataframe(pd.read_csv("citas.csv"), use_container_width=True)

elif "👥" in choice:
    st.title(t["menu"][2])
    with st.form("f_n"):
        nom = st.text_input("Name"); hrs = st.number_input("Hours", min_value=0.0); pag = st.number_input("Pay/Hr", min_value=0.0)
        if st.form_submit_button("Register"):
            guardar_datos(pd.DataFrame([[str(datetime.now().date()), nom, hrs*pag]], columns=["Date", "Employee", "Total"]), "nomina.csv")
            st.info(f"Total: ${hrs*pag}")

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
