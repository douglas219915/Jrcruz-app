import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
from fpdf import FPDF

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción)
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# --- FUNCIÓN PARA OPTIMIZAR EL LOGO ---
@st.cache_data
def get_base64(file):
    try:
        if os.path.exists(file):
            with open(file, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except: return None
    return None

logo_b64 = get_base64("5104.jpg")

# --- CSS: ESTILOS LIGEROS ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.95)) 
        {f', url("data:image/jpg;base64,{logo_b64}")' if logo_b64 else ""};
        background-size: 400px; background-repeat: no-repeat; background-position: center;
    }}
    .stButton>button {{ width: 100%; border-radius: 8px; font-weight: bold; height: 40px; }}
    .stMetric {{ background: rgba(26, 79, 139, 0.05); padding: 10px; border-radius: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- TRADUCCIONES ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "cliente": "Cliente", "fecha": "Fecha", "total_c": "Total Contrato",
        "dep1": "Depósito 1", "dep2": "Depósito 2", "dep3": "Depósito 3",
        "total_p": "Total Pagado", "balance": "Balance Pendiente", "edit_btn": "Actualizar Pagos",
        "ver_mas": "Ver detalles",
        "items": [
            ("Loseta (Tile)", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Piedra (Stone)", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Madera", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminado", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinilo", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decorativos", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
            ("Baños", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materiales", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "cliente": "Client", "fecha": "Date", "total_c": "Total Contract",
        "dep1": "Deposit 1", "dep2": "Deposit 2", "dep3": "Deposit 3",
        "total_p": "Total Paid", "balance": "Balance Due", "edit_btn": "Update Payments",
        "ver_mas": "View details",
        "items": [
            ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"),
            ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
            ("Hardwood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
            ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG"),
            ("Vinyl", "https://www.flooranddecor.com/vinyl", "vinyl.jpg.JPG"),
            ("Decoratives", "https://www.flooranddecor.com/decoratives", "decoratives.jpg.jpeg"),
            ("Fixtures", "https://www.flooranddecor.com/bathroom-fixtures", "fixtures.jpg.png"),
            ("Materials", "https://www.flooranddecor.com/installation-materials", "materials.jpg.jpeg")
        ]
    }
}
t = texts[idioma]

# --- LÓGICA DE DATOS ---
FILE = "historial.csv"
COLS = ["Fecha", "Cliente", "TotalContract", "Dep1", "Dep2", "Dep3", "TotalPaid", "BalanceDue"]

def save_data(df):
    df.to_csv(FILE, index=False)

# --- NAVEGACIÓN ---
choice = st.sidebar.selectbox("Panel", t["menu"])

if "📝" in choice:
    st.title(t["menu"][0])
    with st.form("new_est"):
        c1, c2 = st.columns(2)
        cli = c1.text_input(t["cliente"])
        fec = c2.date_input(t["fecha"])
        total = st.number_input(t["total_c"], min_value=0.0)
        d1 = st.number_input(t["dep1"], min_value=0.0)
        if st.form_submit_button("Guardar Estimado"):
            df = pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(columns=COLS)
            new_row = pd.DataFrame([[str(fec), cli, total, d1, 0, 0, d1, total-d1]], columns=COLS)
            save_data(pd.concat([df, new_row], ignore_index=True))
            st.success("Guardado!")

elif "📋" in choice:
    st.title(t["menu"][1])
    if os.path.exists(FILE):
        try:
            df = pd.read_csv(FILE)
            st.dataframe(df, use_container_width=True)
            
            cli_edit = st.selectbox("Seleccionar Cliente para Pago", df["Cliente"].unique())
            idx = df[df["Cliente"] == cli_edit].index[0]
            
            c_ed1, c_ed2 = st.columns(2)
            d2 = c_ed1.number_input(t["dep2"], value=float(df.at[idx, 'Dep2']))
            d3 = c_ed2.number_input(t["dep3"], value=float(df.at[idx, 'Dep3']))
            
            if st.button(t["edit_btn"]):
                df.at[idx, 'Dep2'] = d2
                df.at[idx, 'Dep3'] = d3
                total_p = df.at[idx, 'Dep1'] + d2 + d3
                df.at[idx, 'TotalPaid'] = total_p
                df.at[idx, 'BalanceDue'] = df.at[idx, 'TotalContract'] - total_p
                save_data(df)
                st.rerun()
        except: st.error("Error en archivo. Borra el historial para reiniciar.")
        if st.button("Borrar Todo el Historial"): os.remove(FILE); st.rerun()

elif "🛒" in choice:
    st.title(t["menu"][4])
    # Seccion optimizada: muestra los 8 items del catálogo
    it = t["items"]
    for i in range(0, len(it), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(it):
                name, link, img = it[i+j]
                with cols[j]:
                    if os.path.exists(img): st.image(img, use_container_width=True)
                    st.subheader(name)
                    st.link_button(t["ver_mas"], link)

# --- OTROS MÓDULOS (Lógica Simple) ---
elif "📅" in choice:
    st.title(t["menu"][2])
    st.info("Módulo de Citas")
elif "👥" in choice:
    st.title(t["menu"][3])
    st.info("Módulo de Nómina")

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
