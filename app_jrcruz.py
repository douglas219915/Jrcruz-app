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

# --- ESTILOS Y LOGO ---
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

# --- DICCIONARIO DE IDIOMAS ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "cliente": "Cliente", "fecha": "Fecha", "desc": "Descripción", "largo": "Largo (ft)", "ancho": "Ancho (ft)",
        "mano_obra": "Mano de Obra", "costo": "Costo ($)", "item": "Artículo", "dep": "Depósito",
        "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "btn_save": "Guardar Nuevo Registro", "btn_edit": "Actualizar Pagos y Guardar", "btn_pdf": "Descargar Recibo PDF"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item", "dep": "Deposit",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_save": "Save New Record", "btn_edit": "Update Payments & Save", "btn_pdf": "Download Receipt PDF"
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

    st.subheader("3. Depósitos Iniciales")
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
        df = pd.DataFrame([[str(fec), cliente, total_contrato, deps_str, total_pagado, balance]], 
                          columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
        file = "historial_final.csv"
        if not os.path.exists(file): df.to_csv(file, index=False)
        else: df.to_csv(file, mode='a', header=False, index=False)
        st.success("Guardado en Historial.")

# --- MODULO 2: HISTORIAL Y EDICIÓN DINÁMICA ---
elif "📋" in choice:
    st.title(t["menu"][1])
    file = "historial_final.csv"
    if os.path.exists(file):
        df_h = pd.read_csv(file)
        st.dataframe(df_h, use_container_width=True)
        
        st.markdown("---")
        st.subheader("🔍 Actualizar Depósitos de Cliente")
        sel_c = st.selectbox("Seleccione Cliente", [""] + list(df_h["Cliente"].unique()))
        
        if sel_c != "":
            idx = df_h[df_h["Cliente"] == sel_c].index[-1]
            datos = df_h.loc[idx]
            # Recuperar depósitos guardados
            deps_actuales = [float(d) for d in str(datos["Depositos"]).split(";") if d]

            # Control dinámico de celdas en edición
            if 'edit_count' not in st.session_state: st.session_state['edit_count'] = len(deps_actuales)
            
            col_eb1, col_eb2 = st.columns(2)
            if col_eb1.button("+ Agregar Celda de Depósito"): st.session_state['edit_count'] += 1
            
            nuevos_deps = []
            for i in range(st.session_state['edit_count']):
                val_default = deps_actuales[i] if i < len(deps_actuales) else 0.0
                v = st.number_input(f"{t['dep']} {i+1}", value=val_default, key=f"edit_dep_{i}")
                nuevos_deps.append(v)

            n_pagado = sum(nuevos_deps)
            n_balance = datos["Total"] - n_pagado

            st.write(f"**Nuevo Balance:** ${n_balance}")

            if st.button(t["btn_edit"]):
                df_h.at[idx, "Depositos"] = ";".join(map(str, nuevos_deps))
                df_h.at[idx, "Pagado"] = n_pagado
                df_h.at[idx, "Balance"] = n_balance
                df_h.to_csv(file, index=False)
                st.success("¡Datos Actualizados!")
                st.rerun()

            if st.button(t["btn_pdf"]):
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
                
                out = f"Recibo_{sel_c}.pdf"
                pdf.output(out)
                with open(out, "rb") as f: st.download_button("📩 Descargar PDF Actualizado", f, file_name=out)

# --- MODULO 3: CITAS ---
elif "📅" in choice:
    st.title(t["menu"][2])
    with st.form("form_citas"):
        f_c = st.date_input(t["fecha"]); h_c = st.time_input("Hora"); cl_c = st.text_input(t["cliente"])
        if st.form_submit_button("Agendar"):
            df_c = pd.DataFrame([[str(f_c), str(h_c), cl_c]], columns=["Fecha", "Hora", "Cliente"])
            df_c.to_csv("citas.csv", mode='a', index=False, header=not os.path.exists("citas.csv"))
            st.success("Cita Agendada")
    if os.path.exists("citas.csv"): st.dataframe(pd.read_csv("citas.csv"))

# --- MODULO 4: NÓMINA ---
elif "👥" in choice:
    st.title(t["menu"][3])
    with st.form("form_nomina"):
        nom = st.text_input("Empleado"); h_t = st.number_input("Horas"); t_h = st.number_input("Tarifa")
        if st.form_submit_button("Registrar Pago"):
            pago = h_t * t_h
            df_n = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), nom, pago]], columns=["Fecha", "Empleado", "Total"])
            df_n.to_csv("nomina.csv", mode='a', index=False, header=not os.path.exists("nomina.csv"))
            st.success(f"Registrado: ${pago}")
    if os.path.exists("nomina.csv"): st.dataframe(pd.read_csv("nomina.csv"))

# --- MODULO 5: CATÁLOGO ---
elif "🛒" in choice:
    st.title(t["menu"][4])
    cat = [("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"), ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"), 
           ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"), ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG")]
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
