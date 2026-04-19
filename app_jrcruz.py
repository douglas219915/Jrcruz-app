import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import os
import base64
from fpdf import FPDF

# 1. CONFIGURACIÓN E INICIO DE CONEXIÓN
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# Conexión a Google Sheets (usando los Secrets que ya configuraste)
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
    .stButton>button {{ width: 100%; background-color: #1A4F8B; color: white; border-radius: 8px; font-weight: bold; height: 45px; }}
    h1, h2, h3 {{ color: #1A4F8B; }}
    [data-testid="stImage"] img {{ width: 100% !important; height: 280px !important; object-fit: cover !important; border-radius: 12px; }}
    </style>
""", unsafe_allow_html=True)

# --- TRADUCCIONES CORREGIDAS (PARA EVITAR KEYERROR) ---
idioma = st.sidebar.radio("🌐 Language / Idioma", ["Español", "English"])
texts = {
    "Español": {
        "menu": ["📝 Nuevo Estimado", "📋 Historial y Pagos", "🛒 Catálogo"],
        "cliente": "Cliente", "fecha": "Fecha", "desc": "Descripción", "largo": "Largo (ft)", "ancho": "Ancho (ft)",
        "mano_obra": "Mano de Obra", "costo": "Costo ($)", "item": "Artículo", "dep": "Depósito",
        "total_c": "Total Contrato", "total_p": "Total Pagado", "balance": "Balance Pendiente",
        "btn_save": "Guardar en Google Drive", "btn_edit": "Actualizar en Google Drive", "btn_pdf": "Descargar Recibo PDF",
        "ver_mas": "Ver detalles", "exito": "¡Guardado con éxito!", "cambios": "¡Datos actualizados!"
    },
    "English": {
        "menu": ["📝 New Estimate", "📋 History & Payments", "🛒 Catalog"],
        "cliente": "Client", "fecha": "Date", "desc": "Description", "largo": "Length (ft)", "ancho": "Width (ft)",
        "mano_obra": "Labor Cost", "costo": "Cost ($)", "item": "Item", "dep": "Deposit",
        "total_c": "Total Contract", "total_p": "Total Paid", "balance": "Balance Due",
        "btn_save": "Save to Google Drive", "btn_edit": "Update to Google Drive", "btn_pdf": "Download Receipt PDF",
        "ver_mas": "View details", "exito": "Saved successfully!", "cambios": "Data updated!"
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
    
    st.subheader("1. " + ("Medidas" if idioma == "Español" else "Measurements"))
    if 'rows' not in st.session_state: st.session_state['rows'] = 1
    if st.button("+ Area"): st.session_state['rows'] += 1
    for i in range(st.session_state['rows']):
        ca1, ca2, ca3 = st.columns([2, 1, 1])
        ca1.text_input(f"{t['desc']} {i+1}", key=f"n_{i}")
        ca2.number_input(t["largo"], min_value=0.0, key=f"l_{i}")
        ca3.number_input(t["ancho"], min_value=0.0, key=f"a_{i}")
    
    st.subheader("2. " + ("Materiales y Mano de Obra" if idioma == "Español" else "Materials & Labor"))
    mano_obra = st.number_input(t["mano_obra"], min_value=0.0)
    if 'm_rows' not in st.session_state: st.session_state['m_rows'] = 1
    if st.button("+ Item"): st.session_state['m_rows'] += 1
    total_mat = 0.0
    for j in range(st.session_state['m_rows']):
        cm1, cm2 = st.columns([3, 1])
        cm1.text_input(f"{t['item']} {j+1}", key=f"md_{j}")
        v_mat = cm2.number_input(f"{t['costo']} {j+1}", min_value=0.0, key=f"mv_{j}")
        total_mat += v_mat

    st.subheader("3. " + t["dep"])
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
        # LEER DE GOOGLE DRIVE Y AGREGAR NUEVA FILA
        df_actual = conn.read(worksheet="Estimados")
        nueva_fila = pd.DataFrame([[str(fec), cliente, total_c, ";".join(map(str, lista_deps)), total_p, bal]], 
                                 columns=["Fecha", "Cliente", "Total", "Depositos", "Pagado", "Balance"])
        df_final = pd.concat([df_actual, nueva_fila], ignore_index=True)
        conn.update(worksheet="Estimados", data=df_final)
        st.success(t["exito"])

# --- MODULO 2: HISTORIAL Y PAGOS (SOLUCIÓN TYPEERROR) ---
elif "📋" in choice:
    st.title(t["menu"][1])
    try:
        df_h = conn.read(worksheet="Estimados")
        # Aseguramos que la columna 'Depositos' se lea como texto para evitar errores
        df_h["Depositos"] = df_h["Depositos"].astype(str)
        st.dataframe(df_h, use_container_width=True)
        
        st.markdown("---")
        sel_c = st.selectbox("Seleccione Cliente para actualizar", [""] + list(df_h["Cliente"].unique()))
        
        if sel_c != "":
            idx = df_h[df_h["Cliente"] == sel_c].index[-1]
            val_total = float(df_h.loc[idx, "Total"])
            
            # Limpieza de datos de depósitos
            raw_deps = str(df_h.loc[idx, "Depositos"])
            deps_list = [float(d) for d in raw_deps.split(";") if d and d != "nan"]
            
            if 'edit_count' not in st.session_state: st.session_state['edit_count'] = len(deps_list)
            if st.button("+ Agregar Celda de Pago"): st.session_state['edit_count'] += 1
            
            nuevos_val_deps = []
            for i in range(st.session_state['edit_count']):
                d_def = deps_list[i] if i < len(deps_list) else 0.0
                v = st.number_input(f"{t['dep']} {i+1}", value=float(d_def), key=f"ed_{i}")
                nuevos_val_deps.append(v)
            
            n_p = sum(nuevos_val_deps)
            n_b = val_total - n_p
            
            if st.button(t["btn_edit"]):
                # Actualización forzando tipos de datos correctos
                df_h["Depositos"] = df_h["Depositos"].astype(object)
                df_h.at[idx, "Depositos"] = ";".join(map(str, nuevos_val_deps))
                df_h.at[idx, "Pagado"] = float(n_p)
                df_h.at[idx, "Balance"] = float(n_b)
                
                conn.update(worksheet="Estimados", data=df_h)
                st.success(t["cambios"])
                st.rerun()

            if st.button(t["btn_pdf"]):
                pdf = FPDF()
                pdf.add_page()
                if os.path.exists("5104.jpg"): pdf.image("5104.jpg", 10, 8, 30)
                pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "JR CRUZ MASONRY LLC", 0, 1, "C"); pdf.ln(10)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"CLIENTE: {sel_c}", 0, 1)
                pdf.cell(0, 10, f"TOTAL CONTRATO: ${val_total}", 0, 1)
                for i, d in enumerate(nuevos_val_deps):
                    pdf.cell(0, 10, f"DEPOSITO {i+1}: ${d}", 0, 1)
                pdf.set_text_color(200, 0, 0)
                pdf.cell(0, 10, f"BALANCE PENDIENTE: ${n_b}", 0, 1)
                name_pdf = f"Recibo_{sel_c}.pdf"
                pdf.output(name_pdf)
                with open(name_pdf, "rb") as f: st.download_button(f"📩 {t['btn_pdf']}", f, file_name=name_pdf)
    except Exception as e:
        st.error(f"Error de conexión: Asegúrate de que la hoja 'Estimados' exista en tu Drive.")

# --- MODULO 3: CATÁLOGO (SOLUCIÓN KEYERROR) ---
elif "🛒" in choice:
    st.title(t["menu"][2])
    # Estructura simple sin diccionarios complejos para evitar errores de traducción
    items = [
        ("Tile", "https://www.flooranddecor.com/tile", "tile.jpg.png"), 
        ("Stone", "https://www.flooranddecor.com/stone", "stone.jpg.png"),
        ("Wood", "https://www.flooranddecor.com/hardwood", "wood.jpg.png"),
        ("Laminate", "https://www.flooranddecor.com/laminate", "laminate.jpg.JPG")
    ]
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(items):
                name, link, img = items[i+j]
                with cols[j]:
                    if os.path.exists(img): st.image(img)
                    st.subheader(name)
                    st.link_button(t["ver_mas"], link)

st.sidebar.markdown("---")
st.sidebar.caption("©️ 2026 JR CRUZ MASONRY LLC")
