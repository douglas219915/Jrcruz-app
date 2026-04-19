import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# 2. Estilos Personalizados
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; background-color: #1A4F8B; color: white; }
    h1 { color: #1A4F8B; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE BASE DE DATOS (CSV) ---
def guardar_datos(df, filename):
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

# 3. Encabezado
col_logo, col_txt = st.columns([1, 3])
with col_logo:
    if os.path.exists("5104.jpg"):
        st.image("5104.jpg", width=150)
with col_txt:
    st.title("JR CRUZ MASONRY LLC")
    st.write("**Gestión de Proyectos, Nómina y Materiales**")

st.markdown("---")

# 4. Menú Lateral
menu = ["📊 Calculadora", "👥 Nómina Semanal", "📋 Historial de Proyectos", "📸 Galería de Fotos"]
choice = st.sidebar.selectbox("Panel de Control", menu)

# --- MÓDULO 1: CALCULADORA ---
if choice == "📊 Calculadora":
    st.header("Estimado de Materiales")
    with st.form("calc_form"):
        cliente = st.text_input("Nombre del Proyecto/Cliente")
        largo = st.number_input("Largo (ft)", min_value=0.0)
        ancho = st.number_input("Ancho (ft)", min_value=0.0)
        submit = st.form_submit_button("Calcular y Guardar Proyecto")
    
    if submit and cliente:
        area = largo * ancho
        cajas = round((area * 1.10) / 15)
        st.success(f"Área: {area} sqft | Cajas estimadas: {cajas}")
        
        # Guardar en historial
        nuevo_p = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), cliente, area, "Construcción"]], 
                              columns=["Fecha", "Cliente", "Detalle", "Tipo"])
        guardar_datos(nuevo_p, "historial.csv")
        st.info("Proyecto guardado en el historial.")

# --- MÓDULO 2: NÓMINA ---
elif choice == "👥 Nómina Semanal":
    st.header("Registro de Pagos")
    with st.form("nomina_form"):
        emp = st.text_input("Nombre del Trabajador")
        hrs = st.number_input("Horas", min_value=0.0)
        rate = st.number_input("Pago por Hora", min_value=0.0)
        btn = st.form_submit_button("Registrar y Guardar")
    
    if btn and emp:
        total = hrs * rate
        st.write(f"Total a pagar a {emp}: **${total}**")
        # Guardar en nomina.csv
        nueva_n = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), emp, hrs, rate, total]], 
                              columns=["Fecha", "Empleado", "Horas", "Rate", "Total"])
        guardar_datos(nueva_n, "nomina.csv")
        st.success("Pago registrado permanentemente.")

# --- MÓDULO 3: HISTORIAL ---
elif choice == "📋 Historial de Proyectos":
    st.header("Registros Guardados")
    tab1, tab2 = st.tabs(["Proyectos", "Pagos de Nómina"])
    
    with tab1:
        if os.path.exists("historial.csv"):
            df_h = pd.read_csv("historial.csv")
            st.dataframe(df_h, use_container_width=True)
        else: st.write("No hay proyectos guardados.")
            
    with tab2:
        if os.path.exists("nomina.csv"):
            df_n = pd.read_csv("nomina.csv")
            st.dataframe(df_n, use_container_width=True)
            st.download_button("Descargar Nómina (Excel)", df_n.to_csv(), "nomina_jrcruz.csv")
        else: st.write("No hay pagos registrados.")

# --- MÓDULO 4: FOTOS ---
elif choice == "📸 Galería de Fotos":
    st.header("Antes y Después")
    foto = st.file_uploader("Sube una foto del trabajo", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, caption="Vista previa del trabajo", use_container_width=True)
        st.write("Foto cargada con éxito (esta versión muestra previsualización)")

st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC")
