import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
from fpdf import FPDF

# 1. CONFIGURACIÓN
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
    [data-testid="stImage"] img {{
        width: 100% !important;
        height: 300px !important;
        object-fit: cover !important;
        border-radius: 15px;
        border: 2px solid #1A4F8B;
    }}
    </style>
""", unsafe_allow_html=True)

# --- TRADUCCIONES ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "cliente": "Cliente", "fecha": "Fecha", "desc": "Descripción", "largo": "Largo (ft)", "ancho": "Ancho (ft)",
        "mano_obra": "Mano de Obra", "costo": "Costo ($)", "item": "Artículo", "dep": "Depósito",
        "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "btn_save": "Guardar Nuevo Registro", "btn_edit": "Actualizar Pagos y Guardar", "btn_pdf": "Descargar Recibo PDF",
        "ver_mas": "Ver detalles", "m_citas": "Módulo de Citas", "m_nomina": "Módulo de Nómina",
        "hora": "Hora", "agendar": "Agendar Cita", "empleado": "Empleado", "horas": "Horas Trabajadas",
        "tarifa": "Tarifa por Hora", "reg_pago": "Registrar Pago", "seleccione": "Seleccione Cliente",
        "agregar_celda": "+ Agregar Celda de Depósito", "exito": "¡Registro guardado!", "cambios": "¡Cambios guardados!"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item", "dep": "Deposit",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_save": "Save New Record", "btn_edit": "Update Payments & Save", "btn_pdf": "Download Receipt PDF",
        "ver_mas": "View details", "m_citas": "Appointments Module", "m_nomina": "Payroll Module",
        "hora": "Time", "agendar": "Schedule Appointment", "empleado": "Employee", "horas": "Hours Worked",
        "tarifa": "Hourly Rate", "reg_pago": "Register Payment", "seleccione": "Select Client",
        "agregar_celda": "+ Add Deposit Cell", "exito": "Record saved!", "cambios": "Changes saved!"
    }
}
t = texts[idioma]
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: NUEVO ESTIMADO (SIN CAMBIOS) ---
if "📝" in choice:
    st.title(t["menu"][0])
    c1, c2 = st.columns(2)
    cliente = c1.text_input(t["cliente"])
    fec = c2.date_input(t["fecha"])
    st.subheader("1. " + ("Medidas" if idioma == "Español" else "Measurements"))
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    if st.button("+ Area"): st.session_state['rows'] += 1
    for i in range(st.session_state['rows']):
        ca1, ca2, ca3 = st.columns([2, 1, 1])
        ca1.text_input(f"{t['desc']} {i+1}", key=f"n_{i}")
        ca2.number_input(t["largo"], min_value=0.0, key=f"l_{i}")
        ca3.number_input(t["ancho"], min_value=0.0, key=f"a_{i}")
    st.subheader("2. " + ("Materiales" if idioma == "Español" else "Materials"))
    mano_obra = st.number_input(t["mano_obra"], min_value=0.0)
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button("+ Item"): st.session_state['m_rows'] += 1
    total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        cm1.text_input(f"{t['item']} {j+1}", key=f"md_{j}")
        v_mat = cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")
        total_mat += v_mat
    st.subheader("3. " + t["dep"])
    if 'dep_rows' not in st.session_state: st.session_state['dep_rows'] = 1
    if st.button("+ " + t["dep"]): st.session_state['dep_rows'] += 1
    lista_deps = []
    for k in range(st.session_state['dep_rows']):
        v_dep = st.number_input(f"{t['dep']} {k+1}", min_value=0.0, key=f"dv_{k}")
        lista_deps.append(v_dep)
    total_contrato = mano_obra + total_mat
    total_pagado = sum(lista_deps)
    balance = total_contrato - total_pagado
    if st.button(t["btn_save"]):
        deps_str = ";".join(map(str, lista_deps))
        df = pd.DataFrame([[str(fec), cliente, float(total_contrato), str(deps_str), float(total_pagado), float(balance)]], 
                          columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
        file = "historial_final.csv"
        if not os.path.exists(file): df.to_csv(file, index=False)
        else: df.to_csv(file, mode='a', header=False, index=False)
        st.success(t["exito"])

# --- MODULO 2: HISTORIAL Y EDICIÓN (CORREGIDO PARA EVITAR TYPEERROR) ---
elif "📋" in choice:
    st.title(t["menu"][1])
    file = "historial_final.csv"
    if os.path.exists(file):
        df_h = pd.read_csv(file)
        st.dataframe(df_h, use_container_width=True)
        st.markdown("---")
        sel_c = st.selectbox(t["seleccione"], [""] + list(df_h["Cliente"].unique()))
        
        if sel_c != "":
            # Localizar fila
            idx = df_h[df_h["Cliente"] == sel_c].index[-1]
            # Convertir valores a tipos correctos para evitar errores de pandas
            total_val = float(df_h.loc[idx, "Total"])
            deps_actuales = [float(d) for d in str(df_h.loc[idx, "Depositos"]).split(";") if d]
            
            if 'edit_count' not in st.session_state: st.session_state['edit_count'] = len(deps_actuales)
            if st.button(t["agregar_celda"]): st.session_state['edit_count'] += 1
            
            nuevos_deps = []
            for i in range(st.session_state['edit_count']):
                val_default = deps_actuales[i] if i < len(deps_actuales) else 0.0
                v = st.number_input(f"{t['dep']} {i+1}", value=float(val_default), key=f"edit_dep_{i}")
                nuevos_deps.append(v)
            
            n_pagado = sum(nuevos_deps)
            n_balance = total_val - n_pagado
            
            if st.button(t["btn_edit"]):
                # Actualización directa para evitar conflictos de tipo de dato
                df_h.loc[idx, "Depositos"] = ";".join(map(str, nuevos_deps))
                df_h.loc[idx, "Pagado"] = float(n_pagado)
                df_h.loc[idx, "Balance"] = float(n_balance)
                df_h.to_csv(file, index=False)
                st.success(t["cambios"])
                st.rerun()

            if st.button(t["btn_pdf"]):
                pdf = FPDF()
                pdf.add_page()
                if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
                pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C"); pdf.ln(10)
                pdf.set_font("Arial", "B", 12); pdf.cell(0, 10, f"{t['cliente'].upper()}: {sel_c}", 0, 1)
                pdf.cell(0, 10, f"{t['fecha'].upper()}: {df_h.loc[idx, 'Fecha']}", 0, 1); pdf.ln(5)
                pdf.cell(100, 10, t["total_c"], 1); pdf.cell(90, 10, f"${total_val}", 1, 1, "R")
                for i, d in enumerate(nuevos_deps):
                    pdf.cell(100, 10, f"{t['dep']} {i+1}", 1); pdf.cell(90, 10, f"${d}", 1, 1, "R")
                pdf.cell(100, 10, t["total_p"], 1); pdf.cell(90, 10, f"${n_pagado}", 1, 1, "R")
                pdf.set_text_color(200, 0, 0)
                pdf.cell(100, 10, t["balance"], 1); pdf.cell(90, 10, f"${n_balance}", 1, 1, "R")
                out = f"Recibo_{sel_c}.pdf"
                pdf.output(out)
                with open(out, "rb") as f: st.download_button(f"📩 {t['btn_pdf']}", f, file_name=out)

# --- MODULOS RESTANTES (SIN CAMBIOS) ---
elif "📅" in choice:
    st.title(t["m_citas"])
    with st.form("citas"):
        f = st.date_input(t["fecha"]); h = st.time_input(t["hora"]); c = st.text_input(t["cliente"])
        if st.form_submit_button(t["agendar"]):
            df_c = pd.DataFrame([[str(f), str(h), c]], columns=["Fecha", "Hora", "Cliente"])
            df_c.to_csv("citas.csv", mode='a', index=False, header=not os.path.exists("citas.csv"))
            st.success(t["exito"])
    if os.path.exists("citas.csv"): st.dataframe(pd.read_csv("citas.csv"))

elif "👥" in choice:
    st.title(t["m_nomina"])
    with st.form("payroll"):
        e = st.text_input(t["empleado"]); hs = st.number_input(t["horas"]); tr = st.number_input(t["tarifa"])
        if st.form_submit_button(t["reg_pago"]):
            tp = hs * tr
            df_p = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), e, tp]], columns=["Fecha", "Empleado", "Total"])
            df_p.to_csv("payroll.csv", mode='a', index=False, header=not os.path.exists("payroll.csv"))
            st.success(f"{t['exito']} ${tp}")
    if os.path.exists("payroll.csv"): st.dataframe(pd.read_csv("payroll.csv"))

elif "🛒" in choice:
    st.title(t["menu"][4])
    items = [
        ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"), 
        ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"), 
        ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"), 
        ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
        ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
        ("Decoratives", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
        ("Fixtures", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
        ("Materials", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
    ]
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(items):
                name, link, img_path = items[i+j]
                with cols[j]:
                    if os.path.exists(img_path): st.image(img_path, use_container_width=True)
                    st.subheader(name)
                    st.link_button(t["ver_mas"], link)

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
