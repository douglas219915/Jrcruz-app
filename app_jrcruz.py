import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
from fpdf import FPDF

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

# --- ESTILOS VISUALES ---
logo_b64 = get_base64("5104.jpg")
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94))
        {f', url("data:image/jpg;base64,{logo_b64}")' if logo_b64 else ""};
        background-size: 400px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
    }}
    .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; height: 45px; }}
    h1, h2, h3 {{ color: #1A4F8B; }}
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE TRADUCCIÓN (CORREGIDO PARA EVITAR KEYERROR) ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "cliente": "Cliente", "fecha": "Fecha", "desc": "Descripción", "largo": "Largo (ft)", "ancho": "Ancho (ft)",
        "mano_obra": "Mano de Obra", "costo": "Costo ($)", "item": "Artículo", "dep": "Depósito",
        "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "btn_save": "Guardar Nuevo Registro", "btn_edit": "Actualizar Pagos y Guardar", "btn_pdf": "Descargar Recibo PDF",
        "ver_mas": "Ver detalles", "m_citas": "Módulo de Citas", "m_nomina": "Módulo de Nómina"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item", "dep": "Deposit",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_save": "Save New Record", "btn_edit": "Update Payments & Save", "btn_pdf": "Download Receipt PDF",
        "ver_mas": "View details", "m_citas": "Appointments Module", "m_nomina": "Payroll Module"
    }
}
t = texts[idioma]
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: NUEVO ESTIMADO ---
if "📝" in choice:
    st.title(t["menu"][0])
    c1, c2 = st.columns(2)
    cliente = c1.text_input(t["cliente"])
    fec = c2.date_input(t["fecha"])

    st.subheader("1. Áreas y Medidas")
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    col_a1, col_a2 = st.columns(2)
    if col_a1.button("+ Area"): st.session_state['rows'] += 1
    if col_a2.button("- Area") and st.session_state['rows'] > 1: st.session_state['rows'] -= 1
    for i in range(st.session_state['rows']):
        ca1, ca2, ca3 = st.columns([2, 1, 1])
        ca1.text_input(f"{t['desc']} {i+1}", key=f"n_{i}")
        ca2.number_input(t["largo"], min_value=0.0, key=f"l_{i}")
        ca3.number_input(t["ancho"], min_value=0.0, key=f"a_{i}")

    st.subheader("2. Labor y Materiales")
    mano_obra = st.number_input(t["mano_obra"], min_value=0.0)
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button("+ Material"): st.session_state['m_rows'] += 1
    total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        cm1.text_input(f"{t['item']} {j+1}", key=f"md_{j}")
        v_mat = cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")
        total_mat += v_mat

    st.subheader("3. Registro de Pagos")
    if 'dep_rows' not in st.session_state: st.session_state['dep_rows'] = 1
    if st.button("+ " + t["dep"]): st.session_state['dep_rows'] += 1
    
    lista_deps = []
    for k in range(st.session_state['dep_rows']):
        v_dep = st.number_input(f"{t['dep']} {k+1}", min_value=0.0, key=f"dv_{k}")
        lista_deps.append(v_dep)

    total_contrato = mano_obra + total_mat
    total_pagado = sum(lista_deps)
    balance = total_contrato - total_pagado

    st.markdown("---")
    res1, res2, res3 = st.columns(3)
    res1.metric(t["total_c"], f"${total_contrato}")
    res2.metric(t["total_p"], f"${total_pagado}")
    res3.metric(t["balance"], f"${balance}")

    if st.button(t["btn_save"]):
        deps_str = ";".join(map(str, lista_deps))
        df = pd.DataFrame([[str(fec), cliente, total_contrato, deps_str, total_pagado, balance]], 
                          columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
        file = "historial_final.csv"
        if not os.path.exists(file): df.to_csv(file, index=False)
        else: df.to_csv(file, mode='a', header=False, index=False)
        st.success("¡Registro guardado exitosamente!")

# --- MODULO 2: HISTORIAL Y EDICIÓN DINÁMICA ---
elif "📋" in choice:
    st.title(t["menu"][1])
    file = "historial_final.csv"
    if os.path.exists(file):
        df_h = pd.read_csv(file)
        st.dataframe(df_h, use_container_width=True)
        
        st.markdown("---")
        st.subheader("🛠️ Gestionar Pagos por Cliente")
        sel_c = st.selectbox("Seleccione Cliente", [""] + list(df_h["Cliente"].unique()))
        
        if sel_c != "":
            idx = df_h[df_h["Cliente"] == sel_c].index[-1]
            datos = df_h.loc[idx]
            deps_actuales = [float(d) for d in str(datos["Depositos"]).split(";") if d]

            if 'edit_count' not in st.session_state: st.session_state['edit_count'] = len(deps_actuales)
            if st.button("+ Agregar Celda de Depósito"): st.session_state['edit_count'] += 1
            
            nuevos_deps = []
            for i in range(st.session_state['edit_count']):
                val_default = deps_actuales[i] if i < len(deps_actuales) else 0.0
                v = st.number_input(f"{t['dep']} {i+1}", value=val_default, key=f"edit_dep_{i}")
                nuevos_deps.append(v)

            n_pagado = sum(nuevos_deps)
            n_balance = datos["Total"] - n_pagado

            col_btn1, col_btn2 = st.columns(2)
            if col_btn1.button(t["btn_edit"]):
                df_h.at[idx, "Depositos"] = ";".join(map(str, nuevos_deps))
                df_h.at[idx, "Pagado"] = n_pagado
                df_h.at[idx, "Balance"] = n_balance
                df_h.to_csv(file, index=False)
                st.success("¡Cambios guardados!")
                st.rerun()

            if col_btn2.button(t["btn_pdf"]):
                pdf = FPDF()
                pdf.add_page()
                if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
                pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C"); pdf.ln(10)
                pdf.set_font("Arial", "B", 12); pdf.cell(0, 10, f"CLIENTE: {sel_c}", 0, 1)
                pdf.cell(0, 10, f"FECHA: {datos['Fecha']}", 0, 1); pdf.ln(5)
                
                pdf.cell(100, 10, t["total_c"], 1); pdf.cell(90, 10, f"${datos['Total']}", 1, 1, "R")
                for i, d in enumerate(nuevos_deps):
                    pdf.cell(100, 10, f"{t['dep']} {i+1}", 1); pdf.cell(90, 10, f"${d}", 1, 1, "R")
                
                pdf.cell(100, 10, t["total_p"], 1); pdf.cell(90, 10, f"${n_pagado}", 1, 1, "R")
                pdf.set_text_color(200, 0, 0)
                pdf.cell(100, 10, t["balance"], 1); pdf.cell(90, 10, f"${n_balance}", 1, 1, "R")
                
                out_pdf = f"Recibo_{sel_c}.pdf"
                pdf.output(out_pdf)
                with open(out_pdf, "rb") as f: st.download_button("📩 Descargar PDF Actualizado", f, file_name=out_pdf)

# --- MODULO 3: CITAS ---
elif "📅" in choice:
    st.title(t["m_citas"])
    with st.form("form_citas"):
        fc_cita = st.date_input(t["fecha"])
        hr_cita = st.time_input("Hora / Time")
        cl_cita = st.text_input(t["cliente"])
        if st.form_submit_button("Agendar Cita"):
            df_c = pd.DataFrame([[str(fc_cita), str(hr_cita), cl_cita]], columns=["Fecha", "Hora", "Cliente"])
            df_c.to_csv("citas.csv", mode='a', index=False, header=not os.path.exists("citas.csv"))
            st.success("Cita agendada correctamente.")
    if os.path.exists("citas.csv"): st.dataframe(pd.read_csv("citas.csv"))

# --- MODULO 4: NÓMINA ---
elif "👥" in choice:
    st.title(t["m_nomina"])
    with st.form("form_payroll"):
        emp_nom = st.text_input("Empleado / Employee")
        hrs_tr = st.number_input("Horas / Hours", min_value=0.0)
        tar_hr = st.number_input("Tarifa / Rate", min_value=0.0)
        if st.form_submit_button("Registrar Pago"):
            tot_p = hrs_tr * tar_hr
            df_p = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), emp_nom, tot_p]], columns=["Fecha", "Empleado", "Total"])
            df_p.to_csv("payroll.csv", mode='a', index=False, header=not os.path.exists("payroll.csv"))
            st.success(f"Pago de ${tot_p} registrado para {emp_nom}.")
    if os.path.exists("payroll.csv"): st.dataframe(pd.read_csv("payroll.csv"))

# --- MODULO 5: CATÁLOGO ---
elif "🛒" in choice:
    st.title(t["menu"][4])
    items = [("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"), 
             ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"), 
             ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"), 
             ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG")]
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(items):
                name, link, img_path = items[i+j]
                with cols[j]:
                    if os.path.exists(img_path): st.image(img_path)
                    st.subheader(name)
                    st.link_button(t["ver_mas"], link)

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
