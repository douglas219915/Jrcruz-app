import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os
import base64

# CONFIGURACIÓN DE LA PÁGINA
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

# --- MENÚ DE NAVEGACIÓN ---
menu = ["📝 Nuevo Estimado", "📋 Historial y Pagos", "📅 Citas", "👥 Nómina", "🛒 Catálogo"]
choice = st.sidebar.selectbox("Seleccione una opción", menu)

# --- 1. NUEVO ESTIMADO ---
if "Nuevo" in choice:
    st.title("Nuevo Estimado")
    with st.form("form_estimado"):
        col1, col2 = st.columns(2)
        cliente = col1.text_input("Nombre del Cliente")
        fecha = col2.date_input("Fecha")
        total = st.number_input("Total del Contrato ($)", min_value=0.0)
        
        if st.form_submit_button("Guardar en Drive"):
            try:
                df = conn.read(worksheet="Estimados", ttl=0).astype(str)
                # Columnas exactas: Fecha, Cliente, Total, Depositos, Pagado, Balance
                nueva_fila = pd.DataFrame([[str(fecha), cliente, str(total), "0", "0", str(total)]], 
                                         columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
                df_final = pd.concat([df, nueva_fila], ignore_index=True)
                conn.update(worksheet="Estimados", data=df_final)
                st.success("✅ Estimado guardado correctamente.")
            except Exception as e:
                st.error(f"Error al conectar: Revisa que la pestaña se llame 'Estimados'.")

# --- 2. HISTORIAL Y PAGOS ---
elif "Historial" in choice:
    st.title("Historial y Pagos")
    try:
        df_h = conn.read(worksheet="Estimados", ttl=0).astype(str)
        st.dataframe(df_h, use_container_width=True)
        
        cliente_sel = st.selectbox("Seleccione Cliente para actualizar pago", [""] + list(df_h["Cliente"].unique()))
        if cliente_sel != "":
            idx = df_h[df_h["Cliente"] == cliente_sel].index[-1]
            total_val = float(df_h.at[idx, "Total"])
            pagado_actual = float(df_h.at[idx, "Pagado"]) if df_h.at[idx, "Pagado"] != 'nan' else 0.0
            
            nuevo_pago = st.number_input("Monto Pagado Total ($)", value=pagado_actual)
            
            if st.button("Actualizar Pago"):
                df_h.at[idx, "Pagado"] = str(nuevo_pago)
                df_h.at[idx, "Balance"] = str(total_val - nuevo_pago)
                conn.update(worksheet="Estimados", data=df_h)
                st.success("✅ Pago actualizado.")
                st.rerun()
    except:
        st.error("❌ Error de conexión. Revisa que el Excel tenga las columnas: Fecha, Cliente, Total, Depositos, Pagado, Balance.")

# --- 3. CITAS ---
elif "Citas" in choice:
    st.title("Calendario de Citas")
    try:
        df_c = conn.read(worksheet="Citas", ttl=0).astype(str)
        st.table(df_c)
        with st.expander("Agendar Nueva Cita"):
            f = st.date_input("Fecha Cita")
            h = st.time_input("Hora")
            cl = st.text_input("Cliente")
            if st.button("Registrar Cita"):
                nueva_c = pd.DataFrame([[str(f), str(h), cl]], columns=["Fecha", "Hora", "Cliente"])
                conn.update(worksheet="Citas", data=pd.concat([df_c, nueva_c], ignore_index=True))
                st.success("Cita agendada.")
                st.rerun()
    except: st.error("Crea una pestaña llamada 'Citas' con columnas: Fecha, Hora, Cliente.")

# --- 4. NÓMINA ---
elif "Nómina" in choice:
    st.title("Registro de Nómina")
    try:
        df_n = conn.read(worksheet="Nomina", ttl=0).astype(str)
        st.dataframe(df_n, use_container_width=True)
        with st.form("nomina"):
            emp = st.text_input("Nombre del Empleado")
            pago = st.number_input("Total a Pagar ($)", min_value=0.0)
            if st.form_submit_button("Registrar Pago"):
                nueva_n = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), emp, str(pago)]], 
                                      columns=["Fecha", "Empleado", "Total"])
                conn.update(worksheet="Nomina", data=pd.concat([df_n, nueva_n], ignore_index=True))
                st.success("Nómina registrada.")
                st.rerun()
    except: st.error("Crea una pestaña llamada 'Nomina' con columnas: Fecha, Empleado, Total.")

# --- 5. CATÁLOGO COMPLETO ---
elif "Catálogo" in choice:
    st.title("Catálogo de Materiales")
    # Restauradas las 8 categorías que se perdieron
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
                nombre, link, img = cat[i+j]
                with cols[j]:
                    if os.path.exists(img): st.image(img)
                    st.subheader(nombre)
                    st.link_button("Ver detalles", link)

st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
