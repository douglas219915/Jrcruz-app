import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import os
import base64
from fpdf import FPDF

# 1. CONFIGURACIÓN
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

# --- ESTILOS ---
logo_b64 = get_base64("5104.jpg")
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94))
        {f', url("data:image/jpg;base64,{logo_b64}")' if logo_b64 else ""};
        background-size: 400px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
    }}
    .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; height: 45px; }}
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
        "btn_save": "Guardar en Google Drive", "btn_edit": "Actualizar Pagos", "btn_pdf": "Descargar PDF",
        "ver_mas": "Ver detalles", "exito": "¡Guardado!", "cambios": "¡Actualizado!"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item", "dep": "Deposit",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_save": "Save to Drive", "btn_edit": "Update Payments", "btn_pdf": "Download PDF",
        "ver_mas": "View details", "exito": "Saved!", "cambios": "Updated!"
    }
}
t = texts[idioma]
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: ESTIMADOS ---
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
        try:
            df_h = conn.read(worksheet="Estimados").astype(str)
            d_str = ";".join(map(str, lista_deps))
            df_new = pd.DataFrame([[str(fec), cliente, str(total_c), d_str, str(total_p), str(bal)]], 
                                 columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
            conn.update(worksheet="Estimados", data=pd.concat([df_h, df_new], ignore_index=True))
            st.success(t["exito"])
        except: st.error("Error al guardar. Revisa que el enlace sea correcto y la hoja sea 'Editor'.")

# --- MODULO 2: HISTORIAL (REFORZADO) ---
elif "📋" in choice:
    st.title(t["menu"][1])
    try:
        df_h = conn.read(worksheet="Estimados", ttl=0).astype(str)
        st.dataframe(df_h, use_container_width=True)
        sel_c = st.selectbox("Seleccione Cliente", [""] + list(df_h["Cliente"].unique()))
        if sel_c != "":
            idx = df_h[df_h["Cliente"] == sel_c].index[-1]
            val_total = float(df_h.loc[idx, "Total"])
            nuevo_pago = st.number_input("Actualizar Pago Total ($)", value=float(df_h.loc[idx, "Pagado"]))
            if st.button(t["btn_edit"]):
                df_h.at[idx, "Pagado"] = str(nuevo_pago)
                df_h.at[idx, "Balance"] = str(val_total - nuevo_pago)
                conn.update(worksheet="Estimados", data=df_h)
                st.success(t["cambios"]); st.rerun()
    except: st.error("Fallo de conexión. Verifica que el archivo en Drive esté compartido como 'Editor'.")

# --- MODULOS EXTRA ---
elif "📅" in choice:
    st.title("Citas")
    with st.form("c"):
        f = st.date_input("Fecha"); hr = st.time_input("Hora"); cl = st.text_input("Cliente")
        if st.form_submit_button("Agendar"):
            df_c = conn.read(worksheet="Citas").astype(str)
            n_c = pd.DataFrame([[str(f), str(hr), cl]], columns=["Fecha", "Hora", "Cliente"])
            conn.update(worksheet="Citas", data=pd.concat([df_c, n_c], ignore_index=True))
            st.success("Cita guardada")

elif "👥" in choice:
    st.title("Nómina")
    with st.form("p"):
        em = st.text_input("Empleado"); hrs = st.number_input("Horas"); r = st.number_input("Tarifa")
        if st.form_submit_button("Registrar"):
            df_n = conn.read(worksheet="Nomina").astype(str)
            n_n = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), em, str(hrs*r)]], columns=["Fecha", "Empleado", "Total"])
            conn.update(worksheet="Nomina", data=pd.concat([df_n, n_n], ignore_index=True))
            st.success("Registrado")

# --- CATALOGO COMPLETO (RESTAURADO) ---
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

st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
