# ========================================================
# SIGNALMAP IA - PRODUCTION CORE: GITHUB & STREAMLIT CLOUD
# ========================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter, deque
from datetime import datetime
import os

# --- MOTOR FRACTAL DE AYER (RESPETADO) ---
class MetaPatternFractal:
    def __init__(self, max_iter=250):
        self.max_iter = max_iter
    def transformar_secuencia(self, seq, i=0): # Se mantiene la 'i' para mantener la dinámica de ayer
        datos = np.array(seq, dtype=float)
        # Ecuación de ayer: suma de nodo * indice i
        dot_x = np.dot(datos, np.arange(1, len(datos) + 1)) if len(datos) > 0 else 0
        hash_x = np.sin(np.sum(datos) * (i * 0.001)) * 1.2 + np.cos(dot_x) * 0.4
        hash_y = np.cos(np.sum(datos) * (i * 0.001)) * 1.2 + np.sin(dot_x) * 0.4
        return hash_x, hash_y

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
if 'boletos_auditados' not in st.session_state: st.session_state.boletos_auditados = []
if "local_signals" not in st.session_state: st.session_state.local_signals = []

GAME_CONFIG = {
    "TRIS": {"min": 0, "max": 9, "cantidad": 5},
    "CHISPAZO": {"min": 1, "max": 28, "cantidad": 5},
    "MELATE": {"min": 1, "max": 56, "cantidad": 6}
}

st.set_page_config(page_title="SignalMap IA - MetaPattern Live", layout="wide", page_icon="🧠")

# Estilos CSS
st.markdown("""
<style>
    .grid-cell-match { background-color: #00f5d4; color: black; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; }
    .grid-cell-miss { background-color: #f72585; color: white; padding: 10px; border-radius: 5px; text-align: center; }
    .grid-cell-neutral { background-color: #1e1b4b; color: white; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #4338ca; }
    .dashboard-card { background-color: #111827; padding: 16px; border-radius: 16px; border: 1px solid #1f2937; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# Menú Principal
menu = st.sidebar.radio("Navegación", ["🏠 Dashboard Global", "📖 Diario de Señales", "📸 Evidencia & Diario de Aciertos", "🎯 Sorteo Número Sugerido"])

# --- FUNCIONES AUXILIARES ---
def espejo(numero):
    mapa = {"0":"5", "1":"6", "2":"7", "3":"8", "4":"9", "5":"0", "6":"1", "7":"2", "8":"3", "9":"4"}
    res = "".join([mapa.get(d, d) for d in str(numero)])
    return res

# 1. DASHBOARD GLOBAL
if menu == "🏠 Dashboard Global":
    st.title("🧠 Matriz Global de Convergencia")
    motor_f = MetaPatternFractal()
    puntos_mapeados = []
    
    # Simulación de datos (o carga tu CSV aquí)
    for game in GAME_CONFIG.keys():
        muestras = [list(np.random.randint(GAME_CONFIG[game]["min"], GAME_CONFIG[game]["max"]+1, GAME_CONFIG[game]["cantidad"])) for _ in range(50)]
        for idx, seq in enumerate(muestras):
            x, y = motor_f.transformar_secuencia(seq, i=idx)
            puntos_mapeados.append({"Eje X": x, "Eje Y": y, "Juego": game})

    fig_fractal = px.scatter(pd.DataFrame(puntos_mapeados), x="Eje X", y="Eje Y", color="Juego")
    fig_fractal.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig_fractal, use_container_width=True)

# 2. DIARIO DE SEÑALES
elif menu == "📖 Diario de Señales":
    st.title("📖 Registro de Señales")
    sorteo = st.selectbox("Sorteo", list(GAME_CONFIG.keys()))
    numeros = st.text_input("Números (Ej: 1,2,3,4,5)")
    if st.button("Guardar"):
        st.session_state.local_signals.append({"sorteo": sorteo, "numeros": [int(x) for x in numeros.split(",")]})
        st.success("Señal guardada")

# 3. EVIDENCIA Y DIARIO DE ACIERTOS (INTEGRACIÓN)
elif menu == "📸 Evidencia & Diario de Aciertos":
    st.title("📸 Evidencia de Tiros Directos & Auditoría Visual")
    col_izq, col_der = st.columns([1, 2])
    
    with col_izq:
        st.subheader("📁 Cargar Prueba")
        sorteo_sel = st.selectbox("Sorteo", list(GAME_CONFIG.keys()))
        numeros_boleto = st.text_input("Números Jugados")
        numeros_ganadores = st.text_input("Números Oficiales")
        
        if st.button("🔮 Auditar"):
            lista_jugados = [int(x.strip()) for x in numeros_boleto.split(",") if x.strip().isdigit()]
            lista_ganadores = [int(x.strip()) for x in numeros_ganadores.split(",") if x.strip().isdigit()]
            coincidentes = list(set(lista_jugados) & set(lista_ganadores))
            estado = "🎯 ACERTADO" if len(coincidentes) >= 2 else "❌ DESVIADO"
            st.session_state.boletos_auditados.append({"sorteo": sorteo_sel, "jugados": lista_jugados, "coincidentes": coincidentes, "estado": estado})
            st.success(f"Procesado: {estado}")

    with col_der:
        if st.session_state.boletos_auditados:
            ultimo = st.session_state.boletos_auditados[-1]
            config = GAME_CONFIG[ultimo['sorteo']]
            cols_grid = st.columns(8)
            for num in range(config["min"], config["max"]+1):
                with cols_grid[num % 8]:
                    if num in ultimo["coincidentes"]: st.markdown(f'<div class="grid-cell-match">{num}</div>', unsafe_allow_html=True)
                    elif num in ultimo["jugados"]: st.markdown(f'<div class="grid-cell-miss">{num}</div>', unsafe_allow_html=True)
                    else: st.markdown(f'<div class="grid-cell-neutral">{num}</div>', unsafe_allow_html=True)

# 4. SORTEO SUGERIDO
elif menu == "🎯 Sorteo Número Sugerido":
    st.title("🎯 Sugerencias IA")
    motor_f = MetaPatternFractal()
    for game in GAME_CONFIG.keys():
        sugeridos = list(np.random.randint(GAME_CONFIG[game]["min"], GAME_CONFIG[game]["max"]+1, GAME_CONFIG[game]["cantidad"]))
        st.info(f"{game}: {sugeridos} | Espejo: {[espejo(n) for n in sugeridos]}")
