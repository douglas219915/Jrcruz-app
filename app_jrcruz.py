import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import os
import base64
from fpdf import FPDF

# 1. CONFIGURACIÓN E INICIO DE CONEXIÓN
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# CONEXIÓN A GOOGLE SHEETS (Basada en tus Secrets configurados)
conn = st.connection("gsheets", type=GSheetsConnection)

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

# --- ESTILOS VISUALES ORIGINALES ---
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
        height: 280px !important;
        object-fit: cover !important;
        border-radius: 12px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- TRADUCCIONES COMPLETAS ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "cliente": "Cliente", "fecha": "Fecha", "desc": "Descripción", "largo": "Largo (ft)", "ancho": "Ancho (ft)",
        "mano_obra": "Mano de Obra", "costo": "Costo ($)", "item": "Artículo", "dep": "Depósito",
        "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "btn_save": "Guardar en Google Drive", "btn_edit": "Actualizar Pagos en Drive", "btn_pdf": "Descargar Recibo PDF",
        "ver_mas": "Ver detalles", "m_citas": "Módulo de Citas", "m_nomina": "Módulo de Nómina",
        "hora": "Hora", "agendar": "Agendar Cita", "empleado": "Empleado", "horas": "Horas Trabajadas",
        "tarifa": "Tarifa por Hora", "reg_pago": "Registrar Pago", "seleccione": "Seleccione Cliente",
        "agregar_celda": "+ Agregar Celda de Depósito", "exito": "¡Guardado!", "cambios": "¡Actualizado!"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item", "dep": "Deposit",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_save": "Save to Google Drive", "btn_edit": "Update Payments in Drive", "btn_pdf": "Download Receipt PDF",
        "ver_mas": "View details", "m_citas": "Appointments Module", "m_nomina": "Payroll Module",
        "hora": "Time", "agendar": "Schedule Appointment", "empleado": "Employee", "horas": "Hours Worked",
        "tarifa": "Hourly Rate", "reg_pago": "Register Payment", "seleccione": "Select Client",
        "agregar_celda": "+ Add Deposit Cell", "exito": "Saved!", "cambios": "Updated!"
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
    
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    if st.button("+ Area"): st.session_state['rows'] += 1
    for i in range(st.session_state['rows']):
        ca1, ca2, ca3 = st.columns([2, 1, 1])
        ca1.text_input(f"{t['desc']} {i+1}", key=f"n_{i}")
        ca2.number_input(t["largo"], min_value=0.0, key=f"l_{i}")
        ca3.number_input(t["ancho"], min_value=0.0, key=f"a_{i}")
    
    mano_obra = st.number_input(t["mano_obra"], min_value=0.0)
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button("+ Item"): st.session_state['m_rows'] += 1
    total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        cm1.text_input(f"{t['item']} {j+1}", key=f"md_{j}")
        v_mat = cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")
        total_mat += v_mat

    if 'dep_rows' not in st.session_state: st.session_state['dep_rows'] = 1
    if st.button("+ " + t["dep"]): st.session_state['dep_rows'] += 1
    lista_deps = []
    for k in range(st.session_state['dep_rows']):
        v_dep = st.number_input(f"{t['dep']} {k+1}", min_value=0.0, key=f"dv_{k}")
        lista_deps.append(v_dep)

    total_c = float(mano_obra + total_mat)
    total_p = float(sum(lista_deps))
    bal = total_c - total_p

    if st.button(t["btn_save"]):
        d_str = ";".join(map(str, lista_deps))
        df_new = pd.DataFrame([[str(fec), cliente, total_c, d_str, total_p, bal]], 
                             columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
        try:
            df_h = conn.read(worksheet="Estimados").astype(str)
            df_final = pd.concat([df_h, df_new.astype(str)], ignore_index=True)
            conn.update(worksheet="Estimados", data=df_final)
            st.success(t["exito"])
        except Exception as e:
            st.error(f"Error de conexión: Asegúrate de que la hoja 'Estimados' exista en tu Drive.")

# --- MODULO 2: HISTORIAL Y PAGOS ---
elif "📋" in choice:
    st.title(t["menu"][1])
    try:
        df_h = conn.read(worksheet="Estimados").astype(str)
        st.dataframe(df_h, use_container_width=True)
        
        st.markdown("---")
        sel_c = st.selectbox(t["seleccione"], [""] + list(df_h["Cliente"].unique()))
        
        if sel_c != "":
            idx = df_h[df_h["Cliente"] == sel_c].index[-1]
            val_total = float(df_h.loc[idx, "Total"])
            deps_list = [float(d) for d in str(df_h.loc[idx, "Depositos"]).split(";") if d and d != 'nan']
            
            if 'edit_count' not in st.session_state: st.session_state['edit_count'] = len(deps_list)
            if st.button(t["agregar_celda"]): st.session_state['edit_count'] += 1
            
            nuevos_val_deps = []
            for i in range(st.session_state['edit_count']):
                d_def = deps_list[i] if i < len(deps_list) else 0.0
                v = st.number_input(f"{t['dep']} {i+1}", value=float(d_def), key=f"ed_{i}")
                nuevos_val_deps.append(v)
            
            n_p = sum(nuevos_val_deps)
            n_b = val_total - n_p
            
            if st.button(t["btn_edit"]):
                # SOLUCIÓN AL TYPEERROR: Forzar tipo objeto antes de la asignación
                df_h["Depositos"] = df_h["Depositos"].astype(object)
                df_h.at[idx, "Depositos"] = ";".join(map(str, nuevos_val_deps))
                df_h.at[idx, "Pagado"] = str(n_p)
                df_h.at[idx, "Balance"] = str(n_b)
                conn.update(worksheet="Estimados", data=df_h)
                st.success(t["cambios"])
                st.rerun()

            if st.button(t["btn_pdf"]):
                pdf = FPDF()
                pdf.add_page()
                if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
                pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C"); pdf.ln(10)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"{t['cliente'].upper()}: {sel_c}", 0, 1)
                pdf.cell(0, 10, f"{t['total_c']}: ${val_total}", 0, 1)
                for i, d in enumerate(nuevos_val_deps):
                    pdf.cell(0, 10, f"{t['dep']} {i+1}: ${d}", 0, 1)
                pdf.set_text_color(200, 0, 0)
                pdf.cell(0, 10, f"{t['balance']}: ${n_b}", 0, 1)
                name_pdf = f"Recibo_{sel_c}.pdf"
                pdf.output(name_pdf)
                with open(name_pdf, "rb") as f: st.download_button(f"📩 {t['btn_pdf']}", f, file_name=name_pdf)
    except:
        st.error("Error de conexión con Google Sheets. Revisa tus permisos.")

# --- MODULOS: CITAS Y NÓMINA ---
elif "📅" in choice:
    st.title(t["m_citas"])
    with st.form("c"):
        f = st.date_input(t["fecha"]); hr = st.time_input(t["hora"]); cl = st.text_input(t["cliente"])
        if st.form_submit_button(t["agendar"]):
            try:
                df_c = conn.read(worksheet="Citas").astype(str)
                n_c = pd.DataFrame([[str(f), str(hr), cl]], columns=["Fecha", "Hora", "Cliente"])
                conn.update(worksheet="Citas", data=pd.concat([df_c, n_c.astype(str)], ignore_index=True))
                st.success(t["exito"])
            except: st.error("Crea la pestaña 'Citas' en tu Drive.")
    try: st.dataframe(conn.read(worksheet="Citas"))
    except: pass

elif "👥" in choice:
    st.title(t["m_nomina"])
    with st.form("p"):
        em = st.text_input(t["empleado"]); hrs = st.number_input(t["horas"]); r = st.number_input(t["tarifa"])
        if st.form_submit_button(t["reg_pago"]):
            try:
                tot = hrs * r
                df_n = conn.read(worksheet="Nomina").astype(str)
                n_n = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), em, str(tot)]], columns=["Fecha", "Empleado", "Total"])
                conn.update(worksheet="Nomina", data=pd.concat([df_n, n_n.astype(str)], ignore_index=True))
                st.success(f"{t['exito']} ${tot}")
            except: st.error("Crea la pestaña 'Nomina' en tu Drive.")
    try: st.dataframe(conn.read(worksheet="Nomina"))
    except: pass

# --- CATÁLOGO ---
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
        cs = st.columns(2)
        for j in range(2):
            if i+j < len(cat):
                n, l, img = cat[i+j]
                with cs[j]:
                    if os.path.exists(img): st.image(img)
                    st.subheader(n); st.link_button(t["ver_mas"], l)

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
