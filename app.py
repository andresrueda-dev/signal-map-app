import streamlit as st
import pandas as pd
import numpy as np
import re
from collections import deque

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
