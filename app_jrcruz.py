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

# --- CSS: LOGO, BOTONES Y UNIFORMIDAD DE IMÁGENES ---
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
    .status-box {{ padding: 20px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 20px; }}
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
        "dep1": "Depósito 1", "dep2": "Depósito 2", "dep3": "Depósito 3",
        "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "btn_pdf": "Generar PDF en Español", "ver_mas": "Ver detalles"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "step1": "1. Areas & Measurements (Sqft)", "step2": "2. Labor & Materials Breakdown", "step3": "3. Payment Record",
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item",
        "dep1": "Deposit 1", "dep2": "Deposit 2", "dep3": "Deposit 3",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_pdf": "Generate PDF in English", "ver_mas": "View details"
    }
}
t = texts[idioma]

COLUMNAS_HISTORIAL = ["Fecha", "Cliente", "TotalContract", "Dep1", "Dep2", "Dep3", "TotalPaid", "BalanceDue"]

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: ESTIMADO (RESTAURADO) ---
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

    total_sqft = 0.0
    for i in range(st.session_state['rows']):
        ca1, ca2, ca3 = st.columns([2, 1, 1])
        ca1.text_input(f"{t['desc']} {i+1}", key=f"n_{i}")
        l = ca2.number_input(t["largo"], min_value=0.0, key=f"l_{i}")
        a = ca3.number_input(t["ancho"], min_value=0.0, key=f"a_{i}")
        total_sqft += (l * a)

    st.subheader(t["step2"])
    mano_obra = st.number_input(t["mano_obra"], min_value=0.0)
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button(f"+ {t['item']}"): st.session_state['m_rows'] += 1
    
    lista_mat = []; total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        d_mat = cm1.text_input(f"{t['item']} {j+1}", key=f"md_{j}")
        v_mat = cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")
        total_mat += v_mat
        if d_mat: lista_mat.append([d_mat, v_mat])

    st.subheader(t["step3"])
    total_contrato = mano_obra + total_mat
    cp1, cp2, cp3 = st.columns(3)
    d1 = cp1.number_input(t["dep1"], min_value=0.0)
    d2 = cp2.number_input(t["dep2"], min_value=0.0)
    d3 = cp3.number_input(t["dep3"], min_value=0.0)
    
    total_pagado = d1 + d2 + d3
    balance = total_contrato - total_pagado

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric(t["total_c"], f"${total_contrato}")
    m2.metric(t["total_p"], f"${total_pagado}")
    m3.metric(t["balance"], f"${balance}")

    if st.button(t["btn_pdf"]):
        df_new = pd.DataFrame([[str(fecha_input), cliente, total_contrato, d1, d2, d3, total_pagado, balance]], columns=COLUMNAS_HISTORIAL)
        if not os.path.exists("historial.csv"): df_new.to_csv("historial.csv", index=False)
        else: df_new.to_csv("historial.csv", mode='a', header=False, index=False)
        st.success("PDF Generado y Registro Guardado.")

# --- MODULO 2: HISTORIAL EDITABLE ---
elif "📋" in choice:
    st.title(t["menu"][1])
    if os.path.exists("historial.csv"):
        df_h = pd.read_csv("historial.csv")
        st.dataframe(df_h, use_container_width=True)
        st.subheader("Actualizar Pagos")
        sel = st.selectbox("Cliente", df_h["Cliente"].unique())
        if sel:
            idx = df_h[df_h["Cliente"] == sel].index[0]
            c_e1, c_e2 = st.columns(2)
            nd2 = c_e1.number_input(t["dep2"], value=float(df_h.at[idx, 'Dep2']))
            nd3 = c_e2.number_input(t["dep3"], value=float(df_h.at[idx, 'Dep3']))
            if st.button("Guardar Cambios"):
                df_h.at[idx, 'Dep2'], df_h.at[idx, 'Dep3'] = nd2, nd3
                tp = df_h.at[idx, 'Dep1'] + nd2 + nd3
                df_h.at[idx, 'TotalPaid'], df_h.at[idx, 'BalanceDue'] = tp, df_h.at[idx, 'TotalContract'] - tp
                df_h.to_csv("historial.csv", index=False)
                st.rerun()

# --- MODULO 3: CITAS ---
elif "📅" in choice:
    st.title(t["menu"][2])
    with st.form("citas"):
        f_c = st.date_input(t["fecha"]); h_c = st.time_input("Hora"); cli_c = st.text_input(t["cliente"])
        if st.form_submit_button("Agendar"):
            st.success("Cita guardada")

# --- MODULO 4: NÓMINA ---
elif "👥" in choice:
    st.title(t["menu"][3])
    with st.form("nomina"):
        nom = st.text_input("Nombre"); hrs = st.number_input("Horas"); ph = st.number_input("Pago x Hora")
        if st.form_submit_button("Registrar"):
            st.info(f"Total a pagar: ${hrs*ph}")

# --- MODULO 5: CATÁLOGO (8 ARTÍCULOS) ---
elif "🛒" in choice:
    st.title(t["menu"][4])
    cat_items = [
        ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
        ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
        ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
        ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
        ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
        ("Decoratives", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
        ("Fixtures", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
        ("Materials", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
    ]
    for i in range(0, len(cat_items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(cat_items):
                name, link, img = cat_items[i+j]
                with cols[j]:
                    if os.path.exists(img): st.image(img)
                    st.subheader(name)
                    st.link_button(t["ver_mas"], link)
                    st.write("")

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
