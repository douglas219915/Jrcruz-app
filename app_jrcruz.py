import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import os
import base64

# CONFIGURACIÓN
st.set_page_config(page_title="JR CRUZ MASONRY LLC", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

def get_base64(file):
    try:
        with open(file, "rb") as f: return base64.b64encode(f.read()).decode()
    except: return None

# ESTILOS
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

# TRADUCCIONES
idioma = st.sidebar.radio("🌐 Language", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial", "📅 Citas", "👥 Nómina", "🛒 Catálogo"],
        "btn_save": "Guardar en Drive", "exito": "¡Guardado!", "cliente": "Cliente"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History", "📅 Appointments", "👥 Payroll", "🛒 Catalog"],
        "btn_save": "Save to Drive", "exito": "Saved!", "cliente": "Client"
    }
}
t = texts[idioma]
choice = st.sidebar.selectbox("Menu", t["menu"])

# --- MODULO 1: ESTIMADOS ---
if "📝" in choice:
    st.title(t["menu"][0])
    c1, c2 = st.columns(2)
    cli = c1.text_input(t["cliente"])
    fec = c2.date_input("Fecha")
    
    st.subheader("Medidas y Costos")
    largo = st.number_input("Largo (ft)", min_value=0.0)
    ancho = st.number_input("Ancho (ft)", min_value=0.0)
    m_obra = st.number_input("Mano de Obra ($)", min_value=0.0)
    
    total = float(m_obra + (largo * ancho * 2)) # Ejemplo de cálculo
    st.info(f"Total Estimado: ${total}")

    if st.button(t["btn_save"]):
        df_actual = conn.read(worksheet="Estimados").astype(str)
        nueva = pd.DataFrame([[str(fec), cli, str(total), "0", "0", str(total)]], 
                             columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
        df_f = pd.concat([df_actual, nueva], ignore_index=True)
        conn.update(worksheet="Estimados", data=df_f)
        st.success(t["exito"])

# --- MODULO 2: HISTORIAL (CON CORRECCIÓN DE ERROR) ---
elif "📋" in choice:
    st.title(t["menu"][1])
    try:
        df_h = conn.read(worksheet="Estimados").astype(str)
        st.dataframe(df_h, use_container_width=True)
        
        sel_c = st.selectbox("Seleccione Cliente", [""] + list(df_h["Cliente"].unique()))
        if sel_c != "":
            idx = df_h[df_h["Cliente"] == sel_c].index[-1]
            # Aquí forzamos la actualización para evitar el error de la foto
            st.warning(f"Editando pagos de: {sel_c}")
            nuevo_pago = st.number_input("Nuevo Depósito ($)", min_value=0.0)
            
            if st.button("Actualizar Pago"):
                df_h.at[idx, "Pagado"] = str(nuevo_pago)
                conn.update(worksheet="Estimados", data=df_h)
                st.success("¡Pago registrado!")
                st.rerun()
    except:
        st.error("Error al cargar la hoja 'Estimados'.")

# --- MODULO 3: CITAS ---
elif "📅" in choice:
    st.title(t["menu"][2])
    f_c = st.date_input("Fecha Cita")
    h_c = st.time_input("Hora")
    c_c = st.text_input("Nombre del Cliente")
    if st.button("Agendar Cita"):
        df_c = conn.read(worksheet="Citas").astype(str)
        n_c = pd.DataFrame([[str(f_c), str(h_c), c_c]], columns=["Fecha", "Hora", "Cliente"])
        conn.update(worksheet="Citas", data=pd.concat([df_c, n_c], ignore_index=True))
        st.success("Cita guardada")

# --- MODULO 4: NÓMINA ---
elif "👥" in choice:
    st.title(t["menu"][3])
    emp = st.text_input("Nombre del Empleado")
    hrs = st.number_input("Horas Trabajadas", min_value=0.0)
    pago = st.number_input("Pago Total", min_value=0.0)
    if st.button("Registrar en Nómina"):
        df_n = conn.read(worksheet="Nomina").astype(str)
        n_n = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), emp, str(pago)]], columns=["Fecha", "Empleado", "Total"])
        conn.update(worksheet="Nomina", data=pd.concat([df_n, n_n], ignore_index=True))
        st.success("Nómina actualizada")

# --- MODULO 5: CATÁLOGO ---
elif "🛒" in choice:
    st.title(t["menu"][4])
    st.subheader("Catálogo de Materiales")
    items = [("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"), 
             ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png")]
    for name, link, img in items:
        if os.path.exists(img): st.image(img, width=300)
        st.link_button(f"Ver {name}", link)

st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
