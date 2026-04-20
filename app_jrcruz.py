import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os
import base64

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

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
    .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE IDIOMAS ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "btn_save": "Guardar en Drive", "btn_edit": "Actualizar Pago", "ver_mas": "Ver detalles",
        "exito": "¡Guardado con éxito!", "error": "Error de conexión. Revisa el Excel."
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "btn_save": "Save to Drive", "btn_edit": "Update Payment", "ver_mas": "View details",
        "exito": "Successfully saved!", "error": "Connection error. Check Excel."
    }
}
t = texts[idioma]
choice = st.sidebar.selectbox("Seleccione / Select", t["menu"])

# --- 1. NUEVO ESTIMADO ---
if "📝" in choice:
    st.title(t["menu"][0])
    with st.form("f_est"):
        c1, c2 = st.columns(2)
        cliente = c1.text_input("Cliente / Client")
        fecha = c2.date_input("Fecha / Date")
        total = st.number_input("Total ($)", min_value=0.0)
        if st.form_submit_button(t["btn_save"]):
            try:
                df = conn.read(worksheet="Estimados", ttl=0).astype(str)
                # Columnas exactas de tu foto: Fecha, Cliente, Total, Depositos, Pagado, Balance
                nueva = pd.DataFrame([[str(fecha), cliente, str(total), "0", "0", str(total)]], 
                                    columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
                conn.update(worksheet="Estimados", data=pd.concat([df, nueva], ignore_index=True))
                st.success(t["exito"])
            except: st.error(t["error"])

# --- 2. HISTORIAL Y PAGOS ---
elif "📋" in choice:
    st.title(t["menu"][1])
    try:
        df_h = conn.read(worksheet="Estimados", ttl=0).astype(str)
        st.dataframe(df_h, use_container_width=True)
        
        sel = st.selectbox("Cliente / Client", [""] + list(df_h["Cliente"].unique()))
        if sel != "":
            idx = df_h[df_h["Cliente"] == sel].index[-1]
            tot_val = float(df_h.at[idx, "Total"])
            pag_val = float(df_h.at[idx, "Pagado"]) if df_h.at[idx, "Pagado"] != 'nan' else 0.0
            
            nuevo_p = st.number_input("Monto Pagado / Paid Amount ($)", value=pag_val)
            if st.button(t["btn_edit"]):
                df_h.at[idx, "Pagado"] = str(nuevo_p)
                df_h.at[idx, "Balance"] = str(tot_val - nuevo_p)
                conn.update(worksheet="Estimados", data=df_h)
                st.success(t["exito"]); st.rerun()
    except: st.error(t["error"])

# --- 3. CITAS ---
elif "📅" in choice:
    st.title(t["menu"][2])
    try:
        df_c = conn.read(worksheet="Citas", ttl=0).astype(str)
        st.table(df_c)
    except: st.info("Pestaña 'Citas' no encontrada.")

# --- 4. NÓMINA ---
elif "👥" in choice:
    st.title(t["menu"][3])
    try:
        df_n = conn.read(worksheet="Nomina", ttl=0).astype(str)
        st.dataframe(df_n)
    except: st.info("Pestaña 'Nomina' no encontrada.")

# --- 5. CATÁLOGO COMPLETO ---
elif "🛒" in choice:
    st.title(t["menu"][4])
    # Restauradas las 8 categorías del catálogo original
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
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(cat):
                n, l, img = cat[i+j]
                with cols[j]:
                    if os.path.exists(img): st.image(img)
                    st.subheader(n); st.link_button(t["ver_mas"], l)

st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
