import math
from datetime import datetime

# --- CONFIGURACIÓN JR CRUZ MASONRY LLC ---
NOMBRE_EMPRESA = "JR CRUZ MASONRY LLC"
COLOR_PRIMARIO = "#1A4F8B" # Azul Marino del logo

def calcular_materiales(largo, ancho, sqft_caja):
    area = largo * ancho
    area_con_extra = area * 1.10
    cajas = math.ceil(area_con_extra / sqft_caja)
    return area, cajas

def login():
    print(f"🏛️ BIENVENIDO A LA APP DE {NOMBRE_EMPRESA}")
    user = input("Usuario: ")
    if user == "juancruz21":
        print("✅ Acceso concedido")
        return True
    return False

# --- CUERPO PRINCIPAL ---
if __name__ == "__main__":
    if login():
        # Aquí irá el menú que elijas (WhatsApp, Nómina o Inventario)
        print("Sistema listo. ¿Qué desea hacer hoy, Jefe?")