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
        .status-paid {{ background-color: #D4EDDA; color: #155724; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; }}
        .status-pending {{ background-color: #FFF3CD; color: #856404; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; }}
        </style>
    """, unsafe_allow_html=True)

# --- DICCIONARIO BILINGÜE COMPLETO ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "calc_t": "Estimado y Control de Pagos",
        "btn_pdf": "Generar PDF en Español",
        "step1": "1. Áreas y Medidas (Sqft)",
        "step2": "2. Desglose de Trabajo y Materiales",
        "step3": "3. Registro de Pagos (Depósitos)",
        "cliente": "Cliente", "fecha": "Fecha", "desc": "Descripción",
        "largo": "Largo (ft)", "ancho": "Ancho (ft)",
        "mano_obra": "Mano de Obra", "costo": "Costo ($)", "item": "Artículo",
        "dep1": "Depósito 1", "dep2": "Depósito 2", "dep3": "Depósito 3",
        "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "status_p": "PAGADO POR COMPLETO", "status_pen": "BALANCE PENDIENTE",
        "hist_t": "Historial y Actualización de Pagos",
        "edit_t": "Actualizar Pagos de Cliente Existente",
        "edit_btn": "Guardar Cambios de Pago",
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
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "calc_t": "Estimate & Payment Control",
        "btn_pdf": "Generate PDF in English",
        "step1": "1. Areas & Measurements (Sqft)",
        "step2": "2. Labor & Materials Breakdown",
        "step3": "3. Payment Record (Deposits)",
        "cliente": "Client", "fecha": "Date", "desc": "Description",
        "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item",
        "dep1": "Deposit 1", "dep2": "Deposit 2", "dep3": "Deposit 3",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "status_p": "PAID IN FULL", "status_pen": "PENDING BALANCE",
        "hist_t": "History & Payment Update",
        "edit_t": "Update Existing Client Payments",
        "edit_btn": "Save Payment Changes",
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

COLUMNAS_HISTORIAL = ["Fecha", "Cliente", "TotalContract", "Dep1", "Dep2", "Dep3", "TotalPaid", "BalanceDue"]

# --- FUNCIÓN PARA GUARDAR DATOS ---
def guardar_datos(df_nuevo, filename):
    if not os.path.isfile(filename):
        df_nuevo.to_csv(filename, index=False)
    else:
        try:
            df_existente = pd.read_csv(filename)
            if list(df_existente.columns) != COLUMNAS_HISTORIAL:
                df_nuevo.to_csv(filename, index=False)
            else:
                df_nuevo.to_csv(filename, mode='a', header=False, index=False)
        except:
            df_nuevo.to_csv(filename, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: ESTIMADO Y PAGOS ---
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
    
    lista_mat = []; total_mat = 0.0
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
        nuevo_h = pd.DataFrame([[str(fecha_input), cliente, total_contrato, d1, d2, d3, total_pagado, balance_pendiente]], columns=COLUMNAS_HISTORIAL)
        guardar_datos(nuevo_h, "historial.csv")
        
        pdf = FPDF()
        pdf.add_page()
        if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
        pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C"); pdf.ln(10)
        pdf.set_font("Arial", "B", 12); pdf.cell(0, 8, f"{t['cliente']}: {cliente}", 0, 1)
        pdf.set_font("Arial", "", 10); pdf.cell(0, 8, f"{t['fecha']}: {fecha_input}", 0, 1); pdf.ln(5)
        
        pdf.set_fill_color(26, 79, 139); pdf.set_text_color(255, 255, 255)
        pdf.cell(140, 8, t["desc"], 1, 0, "C", True); pdf.cell(50, 8, t["costo"], 1, 1, "C", True)
        pdf.set_text_color(0, 0, 0); pdf.cell(140, 8, t["mano_obra"], 1); pdf.cell(50, 8, f"${mano_obra}", 1, 1, "R")
        for m in lista_mat: pdf.cell(140, 8, str(m[0]), 1); pdf.cell(50, 8, f"${m[1]}", 1, 1, "R")
        
        pdf.ln(5); pdf.set_font("Arial", "B", 11)
        pdf.cell(140, 10, t["total_c"], 1); pdf.cell(50, 10, f"${total_contrato}", 1, 1, "R")
        if d1 > 0: pdf.cell(140, 10, t["dep1"], 1); pdf.cell(50, 10, f"- ${d1}", 1, 1, "R")
        if d2 > 0: pdf.cell(140, 10, t["dep2"], 1); pdf.cell(50, 10, f"- ${d2}", 1, 1, "R")
        if d3 > 0: pdf.cell(140, 10, t["dep3"], 1); pdf.cell(50, 10, f"- ${d3}", 1, 1, "R")
        pdf.set_text_color(200, 0, 0); pdf.cell(140, 10, t["balance"], 1); pdf.cell(50, 10, f"${balance_pendiente}", 1, 1, "R")
        
        p_f = f"Invoice_{cliente}.pdf"
        pdf.output(p_f)
        with open(p_f, "rb") as f: st.download_button(f"📩 {t['btn_pdf']}", f, file_name=p_f)

# --- MODULO 2: HISTORIAL EDITABLE ---
elif "📋" in choice:
    st.title(t["hist_t"])
    if os.path.exists("historial.csv"):
        try:
            df_hist = pd.read_csv("historial.csv")
            df_visual = df_hist.copy()
            df_visual.columns = ["Date", "Client", t["total_c"], t["dep1"], t["dep2"], t["dep3"], t["total_p"], t["balance"]]
            st.dataframe(df_visual, use_container_width=True)
            
            st.markdown("---")
            st.subheader(t["edit_t"])
            lista_clientes = df_hist["Cliente"].unique().tolist()
            sel_cli = st.selectbox(f"Select {t['cliente']}", lista_clientes)
            
            if sel_cli:
                datos = df_hist[df_hist["Cliente"] == sel_cli].iloc[0]
                idx = df_hist[df_hist["Cliente"] == sel_cli].index[0]
                
                ec1, ec2, ec3 = st.columns(3)
                with ec1: st.info(f"{t['dep1']}: ${datos['Dep1']}")
                with ec2: n_d2 = st.number_input(f"{t['dep2']} ($)", value=float(datos['Dep2']))
                with ec3: n_d3 = st.number_input(f"{t['dep3']} ($)", value=float(datos['Dep3']))
                
                if st.button(t["edit_btn"]):
                    n_pagado = datos['Dep1'] + n_d2 + n_d3
                    df_hist.at[idx, 'Dep2'] = n_d2
                    df_hist.at[idx, 'Dep3'] = n_d3
                    df_hist.at[idx, 'TotalPaid'] = n_pagado
                    df_hist.at[idx, 'BalanceDue'] = datos['TotalContract'] - n_pagado
                    df_hist.to_csv("historial.csv", index=False)
                    st.success("Updated!")
                    st.rerun()
            if st.button("Reset Historial"): os.remove("historial.csv"); st.rerun()
        except: st.error("Error en archivo CSV. Crea un nuevo estimado para resetear.")

# --- MODULO 5: CATÁLOGO COMPLETO ---
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
                    st.subheader(name)
                    st.link_button(t["ver_mas"], link)
                    st.write("")

# --- OTROS MÓDULOS ---
elif "📅" in choice:
    st.title(t["menu"][2])
    st.write("Módulo de Citas")
elif "👥" in choice:
    st.title(t["menu"][3])
    st.write("Módulo de Nómina")

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
