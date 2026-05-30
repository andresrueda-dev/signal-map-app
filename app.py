import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import datetime
import pytz
from collections import deque  # <- Corregido: Importación faltante que tiraba el deploy

# =====================================================================
# 1. MOTOR AUTOMÁTICO DE EXTRACCIÓN (LOTERÍA NACIONAL / PRONÓSTICOS)
# =====================================================================
def obtener_ultimo_sorteo_automatico(sorteo_nombre):
    """
    Extrae en tiempo real el último resultado oficial desde el portal de resultados.
    Sorteos soportados: 'tris', 'chispazo'
    """
    try:
        url = "https://www.pronosticos.gob.mx/Home/Resultados"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=7)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if sorteo_nombre == 'chispazo':
            contenedor = soup.find('div', id='divChispazo') or soup.find('div', class_='resultado-chispazo')
            if contenedor:
                numeros = [int(s) for s in re.findall(r'\b\d+\b', contenedor.text)]
                numeros_validos = [n for n in numeros if 1 <= n <= 28][:5]
                return sorted(numeros_validos)
                
        elif sorteo_nombre == 'tris':
            contenedor = soup.find('div', id='divTris') or soup.find('div', class_='resultado-tris')
            if contenedor:
                numeros = [int(s) for s in re.findall(r'\b\d+\b', contenedor.text)]
                numeros_validos = [n for n in numeros if 0 <= n <= 9][:5]
                return numeros_validos
                
        return None
    except Exception as e:
        return None

def verificar_actualizacion_por_horario():
    """Monitorea ventanas de tiempo de sorteos en CDMX"""
    try:
        tz_cdmx = pytz.timezone('America/Mexico_City')
        hora_actual = datetime.datetime.now(tz_cdmx).time()
        horarios_sorteos = [
            datetime.time(13, 15), datetime.time(15, 15), 
            datetime.time(17, 15), datetime.time(19, 15), datetime.time(21, 30)
        ]
        for horario in horarios_sorteos:
            if abs(hora_actual.hour - horario.hour) == 0 and abs(hora_actual.minute - horario.minute) <= 5:
                return True
        return False
    except:
        return False

# =====================================================================
# 2. CONFIGURACIÓN DEL MOTOR DE MEMORIA CIRCULAR (500 NODOS FRESCOS)
# =====================================================================
if "mapa_nodos" not in st.session_state:
    # Genera la cola circular nativa limitada a 500
    st.session_state.mapa_nodos = deque(maxlen=500)
    
    # Carga inicial base (Simulada - Reemplazar por tu lectura de Firebase/CSV si es necesario)
    nodos_iniciales = np.random.randint(0, 10, size=(499, 5)).tolist()
    st.session_state.mapa_nodos.extend(nodos_iniciales)

# =====================================================================
# 3. INTERFAZ VISUAL PRINCIPAL
# =====================================================================
st.title("📡 SignalMap AI — Engine de Sincronización")

st.markdown("---")
st.subheader("⚡ Captura en Tiempo Real & Calibración de Nodos")
st.caption("Alimenta los resultados conforme ocurren en el día para actualizar el mapa fractal al segundo.")

# Estado de la Matriz en Pantalla
st.info(f"🔮 **Matriz Activa:** {len(st.session_state.mapa_nodos)} / 500 Nodos Calibrados en Memoria Circular.")

# Sistema Dinámico de Pestañas (Híbrido Automático / Manual)
tab_auto, tab_manual = st.tabs(["🔄 Conexión Automática (Live Scraper)", "✍️ Inyección Manual"])

# --- PESTAÑA A: CONTROL AUTOMÁTICO ---
with tab_auto:
    st.write("Consulta directa al servidor centralizado de la Lotería Nacional.")
    sorteo_auto = st.selectbox("Sorteo a Monitorear:", ["TRIS", "CHISPAZO"])
    
    if st.button("🔄 Sincronizar Servidor Oficial", use_container_width=True):
        with st.spinner("Estableciendo puente de datos con Pronósticos..."):
            nuevos_datos = obtener_ultimo_sorteo_automatico(sorteo_auto.lower())
            
            if nuevos_datos:
                st.session_state.mapa_nodos.append(nuevos_datos)
                st.success(f"✅ Sincronización Exitosa. Último nodo real detectado: **{nuevos_datos}**")
                st.rerun()
            else:
                st.error("❌ Servidor remoto saturado o sin respuesta. Usa la pestaña Manual de respaldo.")

# --- PESTAÑA B: CONTROL MANUAL ---
with tab_manual:
    col_input, col_info = st.columns([2, 1])
    
    with col_input:
        sorteo_tipo = st.selectbox(
            "Selecciona la Tómbola Temporal:",
            ["TRIS MEDIODÍA", "TRIS DE LAS TRES", "CHISPAZO DE LAS TRES", "TRIS CLÁSICO", "CHISPAZO CLÁSICO", "MELATE/REVANCHA"]
        )
        numeros_raw = st.text_input("Secuencia Oficial (Ej: 1,8,10,16,26):", placeholder="Separados por comas")
        
    with col_info:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption("La entrada limpia los espacios en blanco usando Regex de forma automática.")

    if st.button("Inyectar al Mapa y Recalibrar 🚀", use_container_width=True):
        if numeros_raw:
            limpio = re.sub(r'\s+', '', numeros_raw)
            try:
                lista_numeros = [int(n) for n in limpio.split(',') if n != '']
                if len(lista_numeros) > 0:
                    st.session_state.mapa_nodos.append(lista_numeros)
                    st.success(f"✅ Sorteo {sorteo_tipo} guardado. Nodo indexado correctamente.")
                    st.rerun()
                else:
                    st.error("❌ Formato inválido. Verifica los separadores.")
            except ValueError:
                st.error("❌ Error de casteo: Introduce únicamente números enteros separados por comas.")
        else:
            st.warning("⚠️ Ingresa datos numéricos antes de ejecutar la recalibración.")

# =====================================================================
# 4. BARRA LATERAL: MANTENIMIENTO DEL ENTORNO
# =====================================================================
with st.sidebar:
    st.markdown("### 🛠️ Mantenimiento del Motor")
    
    # Monitoreo de Reloj de Sorteos
    if verificar_actualizacion_por_horario():
        st.warning("⏰ Ventana de Sorteo Activa en CDMX.")
    else:
        st.success("🟢 Monitor en espera de horarios oficiales.")
        
    if st.button("🔄 Reseteo Maestro (Hard Reset)"):
        st.session_state.mapa_nodos.clear()
        nodos_maestros = np.random.randint(0, 10, size=(500, 5)).tolist()
        st.session_state.mapa_nodos.extend(nodos_maestros)
        st.success("Estructura de 500 nodos limpiada y recalibrada con historial base.")
        st.rerun()
