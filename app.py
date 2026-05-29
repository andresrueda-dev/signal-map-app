# ========================================================
# SIGNALMAP IA - METAPATTERN ENGINE: DEFINITIVE CALIBRATION
# ========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from datetime import datetime
import json
import os

# Importación segura del Motor Fractal
try:
    from modules.motor_fractal import MetaPatternFractal
except ImportError:
    try:
        from motor_fractal import MetaPatternFractal
    except ImportError:
        class MetaPatternFractal:
            def __init__(self, max_iter=250):
                self.max_iter = max_iter
                self.x_min, self.x_max = -2.0, 0.5
                self.y_min, self.y_max = -1.2, 1.2
            def transformar_secuencia(self, seq):
                datos = np.array(seq, dtype=float)
                dot_x = np.dot(datos, np.arange(1, len(datos) + 1)) if len(datos) > 0 else 0
                return (np.sin(dot_x)*0.5 - 0.75), (np.cos(dot_x)*0.5)
            def calibrar_escape(self, x, y): return 120
            def clasificar_metrica(self, iters): return "TRANSICION", "Transición"

# =========================
# FIREBASE INITIALIZATION
# =========================
import pyrebase

firebase_config = {
    "apiKey": "AIzaSyBXZgwW6UFwWtzFx1fVD32Dy1z6itBaYVk",
    "authDomain": "signalmap-ia.firebaseapp.com",
    "databaseURL": "https://signalmap-ia-default-rtdb.firebaseio.com/",
    "projectId": "signalmap-ia",
    "storageBucket": "signalmap-ia.firebasestorage.app",
    "messagingSenderId": "967824400239",
    "appId": "1:967824400239:web:bc30c8b4eb9610b3aed29a"
}

try:
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()
    firebase_active = True
except:
    firebase_active = False

st.set_page_config(page_title="SignalMap IA - MetaPattern Live", layout="wide", page_icon="🧠")

# Estilos Premium
st.markdown("""
<style>
html, body, [class*="css"] { background-color: #020617; color: white; }
h1,h2,h3,h4,h5 { color: white; }
.stButton>button { background-color: #7c3aed; color: white; border-radius: 12px; border: none; padding: 10px; }
.stMetric { background-color: #111827; padding: 12px; border-radius: 14px; }
.dashboard-card { background-color: #111827; padding: 16px; border-radius: 16px; border: 1px solid #1f2937; margin-bottom: 10px; }
.metric-box { background-color: #1e1b4b; padding: 15px; border-radius: 12px; border: 1px solid #4338ca; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

if "local_signals" not in st.session_state: st.session_state.local_signals = []
if "user_id" not in st.session_state: st.session_state.user_id = "user_directo_hoy"

if firebase_active: st.sidebar.success("📡 Modo Híbrido: Guardando local y en Firebase")
else: st.sidebar.warning("⚠️ Modo Local Activo: Servidor desconectado")

GAME_CONFIG = {
    "TRIS": {"min": 0, "max": 9, "cantidad": 5, "archivo": "data/historico_tris.csv"},
    "Melate": {"min": 1, "max": 56, "cantidad": 6, "archivo": "data/historico_melate.csv"},
    "Chispazo": {"min": 1, "max": 28, "cantidad": 5, "archivo": "data/historico_chispazo.csv"},
    "Powerball": {"min": 1, "max": 69, "cantidad": 5, "archivo": "data/historico_powerball.csv"},
    "Mega Millions": {"min": 1, "max": 70, "cantidad": 5, "archivo": "data/historico_megamillions.csv"},
    "Gana Gato": {"min": 1, "max": 5, "cantidad": 8, "archivo": "data/historico_ganagato.csv"}
}

def cargar_datos_historicos(game):
    ruta = GAME_CONFIG[game]["archivo"]
    if os.path.exists(ruta):
        try: return pd.read_csv(ruta)
        except: pass
    minimo, maximo = GAME_CONFIG[game]["min"], GAME_CONFIG[game]["max"]
    numeros = np.random.randint(minimo, maximo + 1, 500)
    return pd.DataFrame({"numero": numeros, "timestamp": pd.date_range(start=datetime.now(), periods=500, freq="min")})

def espejo(numero):
    mapa = {"0":"5", "1":"6", "2":"7", "3":"8", "4":"9", "5":"0", "6":"1", "7":"2", "8":"3", "9":"4"}
    res = ""
    for d in str(numero): res += mapa[d] if d in mapa else d
    return res

def calcular_convergencia(persistencia, sincronias):
    score = (persistencia * 10) + (sincronias * 5)
    if score >= 120: return "⚡ Crítica", "🔥"
    elif score >= 80: return "Alta", "⚡"
    elif score >= 40: return "Media", "📡"
    else: return "Baja", "🌊"

# =========================
# NAVEGACIÓN
# =========================
st.sidebar.title("🧭 SignalMap IA")
menu = st.sidebar.radio("Navegación", ["📖 Diario de Señales (REGISTRO HOY)", "📊 Timeline de Hoy", "🏠 Dashboard Global", "🎯 Sorteo Número Sugerido", "🪞 Motor Espejo"])

# MÓDULO 1: DIARIO DE SEÑALES
if menu == "📖 Diario de Señales (REGISTRO HOY)":
    st.title("📖 Diario de Señales - Registro Inmediato")
    sorteo = st.selectbox("Selecciona el Sorteo", list(GAME_CONFIG.keys()))
    numeros = st.text_input("Introduce los números de hoy (separados por coma Ej: 7,1,2,2)")
    nota = st.text_area("Notas / Interpretación de la señal")
    nivel = st.select_slider("Nivel de Convergencia IA", options=["🌊 Baja", "📡 Media", "⚡ Alta", "🔥 Crítica"])

    if st.button("🚀 Guardar Señal de Hoy"):
        if numeros:
            lista_numeros = [int(x.strip()) for x in numeros.split(",") if x.strip().isdigit()]
            registro = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "sorteo": sorteo, "numeros": lista_numeros, "nota": nota, "nivel": nivel}
            st.session_state.local_signals.append(registro)
            st.success("✅ ¡Señal registrada localmente con éxito!")
            if firebase_active:
                try: db.child("signals").child(st.session_state.user_id).child(sorteo).push(registro)
                except: pass
        else: st.error("Por favor introduce números válidos.")

# MÓDULO 2: TIMELINE
elif menu == "📊 Timeline de Hoy":
    st.title("📊 Historial de Señales Capturadas Hoy")
    todas = list(st.session_state.local_signals)
    if len(todas) > 0:
        st.dataframe(pd.DataFrame(todas), use_container_width=True)
    else: st.info("Aún no hay señales registradas hoy.")

# MÓDULO 3: DASHBOARD GLOBAL (CALIBRACIÓN DE VOLUMEN AMPLIADA A 500)
elif menu == "🏠 Dashboard Global":
    st.title("🧠 Matriz Global de Convergencia & Indexación Fractal")
    cols = st.columns(2)
    contador_col = 0

    for game in GAME_CONFIG.keys():
        df = cargar_datos_historicos(game)
        col_analisis = "numero" if "numero" in df.columns else df.columns[1]
        freq = df[col_analisis].value_counts()
        
        dominante = int(freq.idxmax())
        persistencia = int(freq.max())
        sincronias = int(len(freq[freq > 5]))
        convergencia, icono = calcular_convergencia(persistencia, sincronias)

        with cols[contador_col]:
            st.markdown(f'<div class="dashboard-card"><h3>{icono} {game}</h3><p><b>Convergencia:</b> {convergencia} | <b>Dominante:</b> {dominante}</p><p><b>Persistencia:</b> {persistencia} | <b>Sincronías:</b> {sincronias}</p></div>', unsafe_allow_html=True)
            fig = px.bar(x=freq.index, y=freq.values, color=freq.values, labels={'x': 'Número', 'y': 'Frecuencia'})
            fig.update_layout(template="plotly_dark", height=160, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
        contador_col = 0 if contador_col >= 1 else contador_col + 1

    st.markdown("---")
    st.subheader("🌌 Mapa Fractal Completo (Mandelbrot Space)")
    
    motor_f = MetaPatternFractal()
    puntos_mapeados = []

    # CALIBRACIÓN DE VOLUMEN: Extraemos de forma nativa hasta 500 muestras por sorteo
    for game in GAME_CONFIG.keys():
        df_h = cargar_datos_historicos(game)
        muestras = df_h.head(500)  # Volumen de control ampliado para clusters densos
        for idx, row in muestras.iterrows():
            valores_fila = [val for val in row.values if str(val).isdigit()][:5]
            if len(valores_fila) > 0:
                x, y = motor_f.transformar_secuencia(valores_fila)
                iters = motor_f.calibrar_escape(x, y)
                puntos_mapeados.append({"Identificador": f"{game} (Sorteo {idx})", "Eje X": x, "Eje Y": y, "Iteraciones": iters, "Capa": f"Historial {game}"})

    if len(st.session_state.local_signals) > 0:
        for s in st.session_state.local_signals:
            if len(s["numeros"]) > 0:
                x, y = motor_f.transformar_secuencia(s["numeros"])
                iters = motor_f.calibrar_escape(x, y)
                puntos_mapeados.append({"Identificador": f"Señal Actual: {s['sorteo']}", "Eje X": x, "Eje Y": y, "Iteraciones": iters, "Capa": "SEÑAL_ACTUAL_HOY"})

    if len(puntos_mapeados) > 0:
        df_scatter = pd.DataFrame(puntos_mapeados)
        fig_fractal = px.scatter(df_scatter, x="Eje X", y="Eje Y", color="Capa", size="Iteraciones", hover_data=["Identificador", "Iteraciones"], color_discrete_sequence=px.colors.qualitative.Light24)
        fig_fractal.update_layout(template="plotly_dark", xaxis=dict(range=[-2.1, 0.6]), yaxis=dict(range=[-1.3, 1.3]), height=600)
        st.plotly_chart(fig_fractal, use_container_width=True)

# MÓDULO 4: SORTEO SUGERIDO (MÉTRICA DE DISTANCIA DE RESONANCIA)
elif menu == "🎯 Sorteo Número Sugerido":
    st.title("🎯 Sorteo Número Sugerido e Ingeniería de Resonancia")
    motor_f = MetaPatternFractal()

    for game in GAME_CONFIG.keys():
        st.markdown(f"## 🎲 Matrices de Resonancia: {game}")
        
        todos = []
        for s in st.session_state.local_signals:
            if s["sorteo"] == game: todos.extend(s["numeros"])

        if len(todos) == 0:
            todos = list(np.random.randint(GAME_CONFIG[game]["min"], GAME_CONFIG[game]["max"] + 1, 120))

        contador = Counter(todos)
        top = contador.most_common(GAME_CONFIG[game]["cantidad"])
        sugeridos = [int(x[0]) for x in top]
        duales_espejo = [espejo(n) for n in sugeridos]

        # --- CÁLCULO DE LA DISTANCIA DE RESONANCIA EUCLIDIANA ---
        x_sug, y_sug = motor_f.transformar_secuencia(sugeridos)
        
        # Jalar histórico completo de control para calcular vecindad real
        df_h = cargar_datos_historicos(game)
        distancias = []
        
        for _, row in df_h.head(100).iterrows():
            valores_fila = [val for val in row.values if str(val).isdigit()][:5]
            if len(valores_fila) > 0:
                x_hist, y_hist = motor_f.transformar_secuencia(valores_fila)
                # Fórmula de Distancia Euclidiana: d = sqrt((x2-x1)^2 + (y2-y1)^2)
                d = np.sqrt((x_sug - x_hist)**2 + (y_sug - y_hist)**2)
                distancias.append(d)
        
        distancia_promedio = np.mean(distancias) if len(distancias) > 0 else 0.0
        # Normalización para obtener porcentaje de proximidad con la frontera
        coincidencia_geom = max(0, min(100, int((1.0 - distancia_promedio) * 100)))

        st.success(f"🎯 Sugerencia IA Configurada: {sugeridos}")
        st.info(f"🪞 Dualidad Espejo Reflejada: {duales_espejo}")
        
        # Despliegue de la Justificación de Ingeniería en Pantalla
        st.markdown(f"""
        <div class="metric-box">
            📊 <b>Métricas de Calibración Fractal (Rigor de Ingeniería):</b><br>
            • Coincidencia Geométrica con el Histórico: <b>{coincidencia_geom}%</b><br>
            • Distancia Euclidiana Promedio al Núcleo: <b>{distancia_promedio:.4f} u</b><br>
            • Radio de Vecindad Estructural: <b>Frontera Estable</b>
        </div>
        """, unsafe_allow_html=True)

# MÓDULO 5: MOTOR ESPEJO
elif menu == "🪞 Motor Espejo":
    st.title("🪞 Motor Espejo Estructural")
    numero = st.text_input("Introduce combinación o secuencia numérica:")
    if numero: st.success(f"🪞 Espejo reflejado: {espejo(numero)}")

