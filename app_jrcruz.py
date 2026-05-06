import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. Configuración y Estilo de la Página
# ==========================================
st.set_page_config(page_title="JR CRUZ MASONRY LLC", page_icon="🏗️", layout="wide")

# Inicialización de Estados de Sesión (para guardar datos temporalmente)
if 'calculos_areas' not in st.session_state:
    st.session_state.calculos_areas = []
if 'registros_nomina' not in st.session_state:
    # Formato: {'Trabajador': {'Horas': 0, 'Pago_Hora': 0, 'Total': 0}}
    st.session_state.registros_nomina = {}

# Estilo CSS Personalizado (Azul Marino y Profesional)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1A4F8B; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .stButton>button { 
        background-color: #1A4F8B; color: white; border-radius: 10px; 
        font-weight: bold; width: 100%; border: 2px solid #000000;
        transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #0d3a6b; color: #f8f9fa; }
    .metric-box {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 8px solid #1A4F8B;
        margin-bottom: 20px;
    }
    .stTable { background-color: white; border-radius: 10px; overflow: hidden; }
    .catalogo-link {
        display: inline-block; padding: 15px 25px; background-color: white;
        color: #1A4F8B; text-decoration: none; border-radius: 10px;
        border: 2px solid #1A4F8B; font-weight: bold; margin: 10px;
        transition: all 0.3s;
    }
    .catalogo-link:hover { background-color: #1A4F8B; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Encabezado con Logo y Título
# ==========================================
header_col1, header_col2 = st.columns([1, 4])
with header_col1:
    try:
        # Asegúrate de que este nombre sea exacto
        st.image("5104.jpg", width=180, output_format="JPEG")
    except:
        st.write("🏗️ [Logo]")
with header_col2:
    st.markdown("<h1>JR CRUZ MASONRY LLC</h1>", unsafe_allow_html=True)
    st.markdown("### *Renovations and new construction: Floors and Bathrooms*")

st.markdown("---")

# ==========================================
# 3. Panel de Control / Menú Lateral
# ==========================================
st.sidebar.markdown("# Panel de Control")
# Solo español por ahora para simplificar y asegurar funcionalidad
menu_options = ["📊 Calculadora de Áreas", "👥 Nómina Interactiva", "🖼️ Catálogo de Materiales"]
choice = st.sidebar.radio("Seleccione una herramienta:", menu_options)

# ==========================================
# 4. Sección 1: Calculadora de Áreas
# ==========================================
if choice == "📊 Calculadora de Áreas":
    st.header("Suma de Áreas de Proyecto")
    
    with st.form("calc_form"):
        st.write("### Añadir nueva área")
        nombre_area = st.text_input("Nombre de la sección (ej. Baño Principal)", placeholder="Master Bathroom")
        c1, c2 = st.columns(2)
        largo = c1.number_input("Largo (ft)", min_value=0.0, step=0.5, format="%.2f")
        ancho = c2.number_input("Ancho (ft)", min_value=0.0, step=0.5, format="%.2f")
        submit_calc = st.form_submit_button("Añadir al Total")
        
        if submit_calc and largo > 0 and ancho > 0:
            area_sqft = largo * ancho
            # Guardar en estado de sesión
            st.session_state.calculos_areas.append({
                "Nombre": nombre_area if nombre_area else f"Área {len(st.session_state.calculos_areas)+1}",
                "SqFt": area_sqft
            })
            st.success(f"Área '{nombre_area}' añadida ({area_sqft:.2f} sqft).")

    # Mostrar Resumen y Total
    if st.session_state.calculos_areas:
        st.write("---")
        st.subheader("Resumen del Proyecto")
        
        # Crear DataFrame para visualización
        df_areas = pd.DataFrame(st.session_state.calculos_areas)
        st.table(df_areas)
        
        # Calcular y Mostrar Total
        total_sqft = df_areas['SqFt'].sum()
        
        st.markdown(f"""
            <div class="metric-box">
                <p style="margin: 0; font-size: 1.2em; color: #555;">Pies Cuadrados Totales:</p>
                <h1 style="margin: 0; color: #1A4F8B;">{total_sqft:.2f} SqFt</h1>
            </div>
            """, unsafe_allow_html=True)
        
        col_clear1, col_clear2 = st.columns([1, 3])
        if col_clear1.button("🗑️ Borrar Todo"):
            st.session_state.calculos_areas = []
            st.rerun()

# ==========================================
# 5. Sección 2: Nómina Interactiva (¡NUEVO!)
# ==========================================
elif choice == "👥 Nómina Interactiva":
    st.header("Control de Nómina Semanal")
    
    # 2.1 Gestión de Trabajadores
    with st.expander("➕ Gestionar Trabajadores", expanded=False):
        new_worker = st.text_input("Añadir nuevo trabajador:", placeholder="Nombre")
        if st.button("Crear Registro"):
            if new_worker and new_worker not in st.session_state.registros_nomina:
                # Inicializar registro
                st.session_state.registros_nomina[new_worker] = {
                    'Horas': 0.0,
                    'Pago_Hora': 0.0,
                    'Total_Debido': 0.0,
                    'Pagado': 0.0
                }
                st.success(f"Trabajador '{new_worker}' registrado.")
                st.rerun()
            elif new_worker in st.session_state.registros_nomina:
                st.warning("Este trabajador ya está registrado.")

    # 2.2 Panel de Nómina
    if st.session_state.registros_nomina:
        st.write("### Actualizar Horas y Pagos")
        
        # Seleccionar trabajador para editar
        selected_worker = st.selectbox("Seleccione un trabajador:", list(st.session_state.registros_nomina.keys()))
        
        if selected_worker:
            worker_data = st.session_state.registros_nomina[selected_worker]
            
            with st.form("nomina_update_form"):
                c1, c2, c3 = st.columns(3)
                horas = c1.number_input("Horas Trabajadas (Semana)", min_value=0.0, value=worker_data['Horas'], step=1.0)
                pago_hora = c2.number_input("Pago por Hora ($)", min_value=0.0, value=worker_data['Pago_Hora'], step=1.0)
                pagado = c3.number_input("Monto Pagado ($)", min_value=0.0, value=worker_data['Pagado'], step=10.0)
                
                submit_nomina = st.form_submit_button("Actualizar Nómina")
                
                if submit_nomina:
                    # Calcular nuevos totales
                    total_debido = horas * pago_hora
                    saldo = total_debido - pagado
                    
                    # Guardar actualizaciones
                    st.session_state.registros_nomina[selected_worker] = {
                        'Horas': horas,
                        'Pago_Hora': pago_hora,
                        'Total_Debido': total_debido,
                        'Pagado': pagado
                    }
                    st.success(f"Nómina de '{selected_worker}' actualizada.")
                    st.rerun()

        st.write("---")
        st.subheader("Estado de Nómina Semanal")
        
        # Crear DataFrame para visualización
        nomina_data = []
        total_pago_semana = 0
        total_pagado_semana = 0
        
        for worker, data in st.session_state.registros_nomina.items():
            total_debido = data['Horas'] * data['Pago_Hora']
            saldo = total_debido - data['Pagado']
            
            total_pago_semana += total_debido
            total_pagado_semana += data['Pagado']
            
            nomina_data.append({
                "Trabajador": worker,
                "Horas": data['Horas'],
                "$/Hora": f"${data['Pago_Hora']:.2f}",
                "Total Debido": f"${total_debido:.2f}",
                "Monto Pagado": f"${data['Pagado']:.2f}",
                "Saldo Restante": f"${saldo:.2f}"
            })
            
        df_nomina = pd.DataFrame(nomina_data)
        st.table(df_nomina)
        
        # Métricas Totales
        st.markdown(f"""
            <div class="metric-box">
                <p style="margin: 0; font-size: 1.2em; color: #555;">Total Debido Semana:</p>
                <h1 style="margin: 0; color: #1A4F8B;">${total_pago_semana:.2f}</h1>
                <p style="margin: 5px 0 0; color: #28a745;">Total Pagado: ${total_pagado_semana:.2f}</p>
                <p style="margin: 0; color: #dc3545; font-weight: bold;">Saldo Pendiente: ${total_pago_semana - total_pagado_semana:.2f}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Reiniciar Nómina"):
            st.session_state.registros_nomina = {}
            st.rerun()
    else:
        st.info("No hay trabajadores registrados. Use el botón superior para empezar.")

# ==========================================
# 6. Sección 3: Catálogo (¡NUEVO!)
# ==========================================
elif choice == "🖼️ Catálogo de Materiales":
    st.header("Catálogo de Materiales y Proveedores")
    
    st.write("### Enlaces Rápidos a Proveedores:")
    st.markdown("Acceda directamente a las páginas de cotización de material de los principales proveedores.")
    
    # 3.1 Botón Directo a Floor & Decor
    st.markdown("""
        <a href="https://www.flooranddecor.com/" target="_blank" class="catalogo-link">
            🛒 Cotizar en Floor & Decor (Directo)
        </a>
    """, unsafe_allow_html=True)
    
    # 3.2 Otros proveedores
    with st.expander("Ver otros proveedores"):
        st.markdown("""
            <a href="https://www.homedepot.com/b/Flooring/N-5yc1vZar4b" target="_blank" class="catalogo-link">
                Home Depot Flooring
            </a>
            <a href="https://www.lowes.com/c/Flooring" target="_blank" class="catalogo-link">
                Lowe's Flooring
            </a>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("Galería de Materiales Sugeridos")
    st.info("Aquí podrá subir fotos de materiales o trabajos terminados en el futuro.")
    # (En el futuro, podrías añadir st.image() para una galería real)

# ==========================================
# 7. Pie de Página
# ==========================================
st.markdown("---")
st.caption(f"©️ {datetime.now().year} JR CRUZ MASONRY LLC | Herramienta de Gestión Profesional V2.1")
