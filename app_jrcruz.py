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

# --- CSS: ESTILOS, LOGO Y UNIFORMIDAD DE IMÁGENES ---
logo_b64 = get_base64("5104.jpg")
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94))
        {f', url("data:image/jpg;base64,{logo_b64}")' if logo_b64 else ""};
        background-size: 400px; background-repeat: no-repeat; background-attachment: fixed; background-position: center;
    }}
    /* Estilo para que las imágenes del catálogo sean iguales */
    [data-testid="stImage"] img {{
        width: 100%;
        height: 250px; 
        object-fit: cover; 
        border-radius: 15px;
        border: 2px solid #1A4F8B;
    }}
    .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; }}
    h1, h2, h3 {{ color: #1A4F8B; }}
    </style>
""", unsafe_allow_html=True)

# --- TRADUCCIONES ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "cliente": "Cliente", "fecha": "Fecha", "total_c": "Total Contrato",
        "dep1": "Depósito 1", "dep2": "Depósito 2", "dep3": "Depósito 3",
        "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "edit_t": "Actualizar Pagos de Cliente", "edit_btn": "Guardar Cambios",
        "citas_t": "Programar Nueva Cita", "payroll_t": "Registro de Nómina",
        "emp": "Empleado", "hrs": "Horas Trabajadas", "p_h": "Pago por Hora",
        "cat_t": "Catálogo Floor & Decor", "ver_mas": "Ver detalles"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "cliente": "Client", "fecha": "Date", "total_c": "Total Contract",
        "dep1": "Deposit 1", "dep2": "Deposit 2", "dep3": "Deposit 3",
        "total_p": "Total Paid", "balance": "Balance Due",
        "edit_t": "Update Client Payments", "edit_btn": "Save Changes",
        "citas_t": "Schedule New Appointment", "payroll_t": "Payroll Registry",
        "emp": "Employee", "hrs": "Hours Worked", "p_h": "Pay per Hour",
        "cat_t": "Floor & Decor Catalog", "ver_mas": "View details"
    }
}
t = texts[idioma]

# --- FUNCIONES DE ARCHIVOS ---
def save_to_csv(df, file):
    if not os.path.isfile(file): df.to_csv(file, index=False)
    else: df.to_csv(file, mode='a', header=False, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel", t["menu"])

# --- MODULO 1: ESTIMADOS ---
if "📝" in choice:
    st.title(t["menu"][0])
    with st.form("form_est"):
        c1, c2 = st.columns(2)
        cli = c1.text_input(t["cliente"])
        fec = c2.date_input(t["fecha"])
        tot = st.number_input(t["total_c"], min_value=0.0)
        d1 = st.number_input(t["dep1"], min_value=0.0)
        if st.form_submit_button("Guardar"):
            df = pd.DataFrame([[str(fec), cli, tot, d1, 0, 0, d1, tot-d1]], 
                              columns=["Fecha", "Cliente", "TotalContract", "Dep1", "Dep2", "Dep3", "TotalPaid", "BalanceDue"])
            save_to_csv(df, "historial.csv")
            st.success("¡Guardado!")

# --- MODULO 2: HISTORIAL EDITABLE ---
elif "📋" in choice:
    st.title(t["menu"][1])
    if os.path.exists("historial.csv"):
        df = pd.read_csv("historial.csv")
        st.dataframe(df, use_container_width=True)
        st.subheader(t["edit_t"])
        sel_cli = st.selectbox("Seleccione Cliente", df["Cliente"].unique())
        if sel_cli:
            idx = df[df["Cliente"] == sel_cli].index[0]
            c_ed1, c_ed2 = st.columns(2)
            d2 = c_ed1.number_input(t["dep2"], value=float(df.at[idx, 'Dep2']))
            d3 = c_ed2.number_input(t["dep3"], value=float(df.at[idx, 'Dep3']))
            if st.button(t["edit_btn"]):
                df.at[idx, 'Dep2'], df.at[idx, 'Dep3'] = d2, d3
                total_p = df.at[idx, 'Dep1'] + d2 + d3
                df.at[idx, 'TotalPaid'], df.at[idx, 'BalanceDue'] = total_p, df.at[idx, 'TotalContract'] - total_p
                df.to_csv("historial.csv", index=False)
                st.rerun()

# --- MODULO 3: CITAS (OPERATIVO) ---
elif "📅" in choice:
    st.title(t["menu"][2])
    with st.form("form_citas"):
        st.subheader(t["citas_t"])
        col1, col2 = st.columns(2)
        f_cita = col1.date_input(t["fecha"])
        h_cita = col2.time_input("Hora / Time")
        c_cita = st.text_input(t["cliente"])
        obs = st.text_area("Notas / Notes")
        if st.form_submit_button("Agendar Cita"):
            df_cita = pd.DataFrame([[str(f_cita), str(h_cita), c_cita, obs]], columns=["Fecha", "Hora", "Cliente", "Notas"])
            save_to_csv(df_cita, "citas.csv")
            st.success("Cita agendada correctamente.")
    
    if os.path.exists("citas.csv"):
        st.markdown("---")
        st.dataframe(pd.read_csv("citas.csv"), use_container_width=True)

# --- MODULO 4: NÓMINA (OPERATIVO) ---
elif "👥" in choice:
    st.title(t["menu"][3])
    with st.form("form_nomina"):
        st.subheader(t["payroll_t"])
        emp = st.text_input(t["emp"])
        c1, c2 = st.columns(2)
        h = c1.number_input(t["hrs"], min_value=0.0)
        p = c2.number_input(t["p_h"], min_value=0.0)
        if st.form_submit_button("Registrar Pago"):
            total_w = h * p
            df_nom = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), emp, h, p, total_w]], 
                                  columns=["Fecha", "Empleado", "Horas", "PagoHora", "Total"])
            save_to_csv(df_nom, "payroll.csv")
            st.success(f"Registrado: ${total_w}")

    if os.path.exists("payroll.csv"):
        st.markdown("---")
        st.dataframe(pd.read_csv("payroll.csv"), use_container_width=True)

# --- MODULO 5: CATÁLOGO (IMÁGENES UNIFORMES) ---
elif "🛒" in choice:
    st.title(t["cat_t"])
    cat_items = [
        ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
        ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
        ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
        ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
        ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
        ("Fixtures", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png")
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

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
