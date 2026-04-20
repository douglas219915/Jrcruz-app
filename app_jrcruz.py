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

# --- ESTILOS VISUALES MEJORADOS ---
logo_b64 = get_base64("5104.jpg")
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92))
        {f', url("data:image/jpg;base64,{logo_b64}")' if logo_b64 else ""};
        background-size: 350px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
    }}
    .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; height: 45px; border: none; }}
    .stButton>button:hover {{ background-color: #0d2b4d; color: #fff; }}
    h1, h2, h3 {{ color: #1A4F8B; font-weight: bold; }}
    .stImage img {{ border-radius: 12px; border: 2px solid #1A4F8B; object-fit: cover; }}
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
        "btn_save": "💾 Guardar Registro", "btn_edit": "🔄 Actualizar y Guardar", "btn_pdf": "📄 Descargar PDF",
        "ver_mas": "Ver catálogo", "m_citas": "Calendario de Citas", "m_nomina": "Control de Nómina",
        "exito": "¡Guardado!", "cambios": "¡Actualizado!"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item", "dep": "Deposit",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_save": "💾 Save Record", "btn_edit": "🔄 Update & Save", "btn_pdf": "📄 Download PDF",
        "ver_mas": "View catalog", "m_citas": "Appointments Schedule", "m_nomina": "Payroll Control",
        "exito": "Saved!", "cambios": "Updated!"
    }
}
t = texts[idioma]
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: NUEVO ESTIMADO ---
if "📝" in choice:
    st.title(t["menu"][0])
    with st.container(border=True):
        c1, c2 = st.columns(2)
        cliente = c1.text_input(t["cliente"])
        fec = c2.date_input(t["fecha"])
    
    st.subheader("📐 Áreas / Areas")
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    if st.button("+ Area"): st.session_state['rows'] += 1
    for i in range(st.session_state['rows']):
        ca1, ca2, ca3 = st.columns([2, 1, 1])
        ca1.text_input(f"{t['desc']} {i+1}", key=f"n_{i}")
        ca2.number_input(t["largo"], min_value=0.0, key=f"l_{i}")
        ca3.number_input(t["ancho"], min_value=0.0, key=f"a_{i}")
    
    st.subheader("💰 Costos / Costs")
    mano_obra = st.number_input(t["mano_obra"], min_value=0.0)
    
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button("+ Item"): st.session_state['m_rows'] += 1
    total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        cm1.text_input(f"{t['item']} {j+1}", key=f"md_{j}")
        total_mat += cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")

    st.subheader("💳 Depósitos / Deposits")
    if 'dep_rows' not in st.session_state: st.session_state['dep_rows'] = 1
    if st.button("+ " + t["dep"]): st.session_state['dep_rows'] += 1
    lista_deps = []
    for k in range(st.session_state['dep_rows']):
        lista_deps.append(st.number_input(f"{t['dep']} {k+1}", min_value=0.0, key=f"dv_{k}"))

    total_c = float(mano_obra + total_mat)
    total_p = float(sum(lista_deps))
    bal = total_c - total_p

    st.markdown(f"### **Total: ${total_c:,.21f} | Balance: ${bal:,.21f}**")
    if st.button(t["btn_save"]):
        d_str = ";".join(map(str, lista_deps))
        df_new = pd.DataFrame([[str(fec), cliente, total_c, d_str, total_p, bal]], 
                             columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
        file = "historial_final.csv"
        df_new.to_csv(file, mode='a', header=not os.path.exists(file), index=False)
        st.success(t["exito"])

# --- MODULO 2: HISTORIAL Y PAGOS ---
elif "📋" in choice:
    st.title(t["menu"][1])
    file = "historial_final.csv"
    if os.path.exists(file):
        df_h = pd.read_csv(file, dtype={'Depositos': str})
        st.dataframe(df_h, use_container_width=True)
        
        sel_c = st.selectbox(t["cliente"], [""] + list(df_h["Cliente"].unique()))
        if sel_c != "":
            idx = df_h[df_h["Cliente"] == sel_c].index[-1]
            val_total = float(df_h.loc[idx, "Total"])
            deps_list = [float(d) for d in str(df_h.loc[idx, "Depositos"]).split(";") if d and d != 'nan']
            
            if 'edit_count' not in st.session_state: st.session_state['edit_count'] = len(deps_list)
            if st.button("+ Add Deposit"): st.session_state['edit_count'] += 1
            
            nuevos_val_deps = []
            for i in range(st.session_state['edit_count']):
                d_def = deps_list[i] if i < len(deps_list) else 0.0
                nuevos_val_deps.append(st.number_input(f"{t['dep']} {i+1}", value=float(d_def), key=f"ed_{i}"))
            
            n_p = sum(nuevos_val_deps)
            n_b = val_total - n_p
            
            c_btn1, c_btn2 = st.columns(2)
            if c_btn1.button(t["btn_edit"]):
                df_h.at[idx, "Depositos"] = ";".join(map(str, nuevos_val_deps))
                df_h.at[idx, "Pagado"] = n_p
                df_h.at[idx, "Balance"] = n_b
                df_h.to_csv(file, index=False)
                st.success(t["cambios"])
                st.rerun()

            if c_btn2.button(t["btn_pdf"]):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C")
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 10, f"Date: {df_h.loc[idx, 'Fecha']}", 0, 1)
                pdf.cell(0, 10, f"Client: {sel_c}", 0, 1)
                pdf.ln(5)
                pdf.cell(0, 10, f"Total Contract: ${val_total:,.21f}", 1, 1)
                for i, d in enumerate(nuevos_val_deps):
                    pdf.cell(0, 10, f"Deposit {i+1}: ${d:,.21f}", 0, 1)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"BALANCE DUE: ${n_b:,.21f}", 1, 1)
                name_pdf = f"Receipt_{sel_c}.pdf"
                pdf.output(name_pdf)
                with open(name_pdf, "rb") as f:
                    st.download_button("Click to Download PDF", f, file_name=name_pdf)

# --- CATÁLOGOS Y OTROS MÓDULOS ---
elif "📅" in choice:
    st.title(t["m_citas"])
    with st.form("c"):
        f = st.date_input(t["fecha"]); hr = st.time_input("Time"); cl = st.text_input(t["cliente"])
        if st.form_submit_button(t["btn_save"]):
            pd.DataFrame([[str(f), str(hr), cl]], columns=["Fecha", "Hora", "Cliente"]).to_csv("citas.csv", mode='a', header=not os.path.exists("citas.csv"), index=False)
            st.success(t["exito"])
    if os.path.exists("citas.csv"): st.dataframe(pd.read_csv("citas.csv"), use_container_width=True)

elif "👥" in choice:
    st.title(t["m_nomina"])
    with st.form("p"):
        em = st.text_input("Employee"); hrs = st.number_input("Hours"); r = st.number_input("Rate")
        if st.form_submit_button(t["btn_save"]):
            tot = hrs * r
            pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), em, tot]], columns=["Fecha", "Empleado", "Total"]).to_csv("payroll.csv", mode='a', header=not os.path.exists("payroll.csv"), index=False)
            st.success(f"Registered: ${tot}")
    if os.path.exists("payroll.csv"): st.dataframe(pd.read_csv("payroll.csv"), use_container_width=True)

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
                    if os.path.exists(img): st.image(img, use_container_width=True)
                    st.subheader(n); st.link_button(t["ver_mas"], l)

st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
