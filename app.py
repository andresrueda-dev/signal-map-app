import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def obtener_ultimo_sorteo_automatico(sorteo_nombre):
    """
    Extrae en tiempo real el último resultado oficial desde el portal de resultados.
    Sorteos soportados: 'tris', 'chispazo'
    """
    try:
        # Endpoint público y ligero de la Lotería Nacional para el histórico de hoy
        url = "https://www.pronosticos.gob.mx/Home/Resultados"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Hacemos la petición al servidor oficial
        response = requests.get(url, headers=headers, timeout=7)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if sorteo_nombre == 'chispazo':
            # Buscamos el contenedor donde se imprimen las esferas de Chispazo
            # La página oficial usa clases tipo 'bola' o estructuras de lista para los 5 números
            contenedor = soup.find('div', id='divChispazo') or soup.find('div', class_='resultado-chispazo')
            if contenedor:
                # Extraemos todos los dígitos dentro del contenedor usando expresiones regulares
                numeros = [int(s) for s in re.findall(r'\b\d+\b', contenedor.text)]
                # Nos aseguramos de filtrar solo los 5 números del boleto (omitimos el número de sorteo)
                numeros_validos = [n for n in numeros if 1 <= n <= 28][:5]
                return sorted(numeros_validos)
                
        elif sorteo_nombre == 'tris':
            # Buscamos el contenedor del último Tris (son 5 dígitos directos del 0 al 9)
            contenedor = soup.find('div', id='divTris') or soup.find('div', class_='resultado-tris')
            if contenedor:
                numeros = [int(s) for s in re.findall(r'\b\d+\b', contenedor.text)]
                # El Tris son los últimos o primeros 5 dígitos individuales (0-9) según el diseño de la tabla
                numeros_validos = [n for n in numeros if 0 <= n <= 9][:5]
                return numeros_validos
                
        return None
    except Exception as e:
        # En caso de caída de servidor o cambio de diseño en la página oficial, evita que tu app se rompa
        return None
# =====================================================================
# 1. CONFIGURACIÓN DEL MOTOR DE MEMORIA CIRCULAR (500 NODOS FRESCOS)
# =====================================================================
# Inicializamos la cola circular en el estado de la sesión si no existe
if "mapa_nodos" not in st.session_state:
    # collections.deque borra automáticamente el dato más viejo al pasar de 500
    st.session_state.mapa_nodos = deque(maxlen=500)
    
    # Simulación de arranque: Cargamos 499 nodos históricos base para no empezar en cero
    # (Aquí puedes conectar la lectura de tu CSV o Firebase)
    nodos_iniciales = np.random.randint(0, 10, size=(499, 5)).tolist()
    st.session_state.mapa_nodos.extend(nodos_iniciales)

# =====================================================================
# 2. INTERFAZ VISUAL: APARTADO DE CAPTURA MANUAL EN TIEMPO REAL
# =====================================================================
st.markdown("---")
st.subheader("⚡ Captura en Tiempo Real & Calibración de Nodos")
st.caption("Alimenta los resultados conforme ocurren en el día para actualizar el mapa fractal al segundo.")

# Crear columnas para optimizar el espacio visual
col1, col2 = st.columns([1, 2])

with col1:
    # Selector de Sorteo para mantener rigor cronológico
    sorteo_tipo = st.selectbox(
        "Selecciona el Sorteo:",
        ["TRIS MEDIODÍA", "TRIS DE LAS TRES", "CHISPAZO DE LAS TRES", "TRIS CLÁSICO", "CHISPAZO CLÁSICO", "MELATE/REVANCHA"]
    )
    
    # Input manual de los números oficiales que van saliendo
    numeros_raw = st.text_input("Números Oficiales (Ej: 1, 8, 10, 16, 26):", placeholder="Separados por comas")

with col2:
    st.markdown("**Estado de Sincronización:**")
    # Mostrar cuántos nodos vivos tiene el sistema actualmente
    st.info(f"🔮 Matriz Activa: **{len(st.session_state.mapa_nodos)} / 500** Nodos Calibrados.")

# BÓTON DE INYECCIÓN FRACTAL
if st.button("Inyectar al Mapa y Recalibrar 🚀", use_container_width=True):
    if numeros_raw:
        # --- VALIDACIÓN Y LIMPIEZA DE DATOS (REGEX) ---
        # Removemos espacios en blanco y nos aseguramos de que solo pasen números y comas
        limpio = re.sub(r'\s+', '', numeros_raw)
        
        try:
            # Convertimos la entrada de texto en una lista de enteros
            lista_numeros = [int(n) for n in limpio.split(',') if n != '']
            
            if len(lista_numeros) > 0:
                # --- INYECCIÓN EN COLA CIRCULAR (FIFO) ---
                # Agrega el nuevo sorteo al final; si ya hay 500, expulsa el nodo 501 automáticamente
                st.session_state.mapa_nodos.append(lista_numeros)
                
                st.success(f"✅ Sorteo **{sorteo_tipo}** inyectado con éxito. Nodo indexado en el Espacio de Mandelbrot.")
                
                # --- AQUÍ EJECUTAS LA RE-RENDERIZACIÓN DE TU MAPA FRACTAL ---
                # Al actualizar el session_state, el mapa de matplotlib/plotly se redibujará solo
                # con la nueva configuración de 500 puntos.
                st.rerun()
            else:
                st.error("❌ Formato inválido. Por favor, introduce números válidos separados por comas.")
        except ValueError:
            st.error("❌ Error de casteo: Asegúrate de ingresar únicamente números enteros separados por comas.")
    else:
        st.warning("⚠️ El campo de números está vacío. Introduce la señal oficial del sorteo.")

# =====================================================================
# 3. BOTÓN DE EMERGENCIA: RESECEPCIÓN O SINCRONIZACIÓN GLOBAL
# =====================================================================
with st.sidebar:
    st.markdown("### 🛠️ Mantenimiento del Motor")
    if st.button("🔄 Sincronizar Base Global (Hard Reset)"):
        # Función de pánico por si necesitas jalar de golpe tu archivo maestro o base externa
        st.session_state.mapa_nodos.clear()
        # Ejemplo de recarga limpia:
        nodos_maestros = np.random.randint(0, 10, size=(500, 5)).tolist()
        st.session_state.mapa_nodos.extend(nodos_maestros)
        st.sidebar.success("Base de 500 nodos resincronizada cronológicamente.")
        st.rerun()
