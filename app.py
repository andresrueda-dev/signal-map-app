# =========================
# SIGNALMAP IA - INSTANT ACCESS PLATFORM
# =========================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from datetime import datetime
import random
import json

# =========================
# FIREBASE CONFIG & INITIALIZATION
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

# Inicialización segura de Firebase
try:
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()
    firebase_active = True
except:
    firebase_active = False

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="SignalMap IA - Live",
    layout="wide",
    page_icon="🧠"
)

# =========================
# STYLE
# =========================

st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #020617;
    color: white;
}
h1,h2,h3,h4,h5 {
    color: white;
}
.stButton>button {
    background-color: #7c3aed;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px;
}
.stMetric {
    background-color: #111827;
    padding: 12px;
    border-radius: 14px;
}
.dashboard-card {
    background-color: #111827;
    padding: 16px;
    border-radius: 16px;
    border: 1px solid #1f2937;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOCAL STORAGE INITIALIZATION (Bypass Login)
# =========================

if "local_signals" not in st.session_state:
    st.session_state.local_signals = []

if "user_id" not in st.session_state:
    st.session_state.user_id = "user_directo_hoy"

# Alerta de estado en la parte superior
if firebase_active:
    st.sidebar.success("📡 Modo Híbrido: Guardando local y en Firebase")
else:
    st.sidebar.warning("⚠️ Modo Local Activo: Datos guardados en el navegador")

# =========================
# CONFIG
# =========================

GAME_CONFIG = {
    "TRIS": {"min": 0, "max": 9, "cantidad": 5},
    "Melate": {"min": 1, "max": 56, "cantidad": 6},
    "Chispazo": {"min": 1, "max": 28, "cantidad": 5},
    "Powerball": {"min": 1, "max": 69, "cantidad": 5},
    "Mega Millions": {"min": 1, "max": 70, "cantidad": 5},
    "Gana Gato": {"min": 1, "max": 5, "cantidad": 8}
}

# =========================
# FUNCTIONS
# =========================

def generar_datos(game):
    minimo = GAME_CONFIG[game]["min"]
    maximo = GAME_CONFIG[game]["max"]
    numeros = np.random.randint(minimo, maximo + 1, 180)
    timestamps = pd.date_range(start=datetime.now(), periods=180, freq="min")
    return pd.DataFrame({"numero": numeros, "timestamp": timestamps})

def espejo(numero):
    mapa = {"0":"5", "1":"6", "2":"7", "3":"8", "4":"9", "5":"0", "6":"1", "7":"2", "8":"3", "9":"4"}
    resultado = ""
    for d in str(numero):
        if d in mapa: resultado += mapa[d]
        else: resultado += d
    return resultado

def calcular_convergencia(persistencia, sincronias):
    score = (persistencia * 10) + (sincronias * 5)
    if score >= 120: return "⚡ Crítica", "🔥"
    elif score >= 80: return "Alta", "⚡"
    elif score >= 40: return "Media", "📡"
    else: return "Baja", "🌊"

def interpretacion_ia(dominante, persistencia, sincronias, convergencia):
    mensajes = []
    if persistencia >= 10: mensajes.append("Persistencia elevada detectada")
    if sincronias >= 5: mensajes.append("Sincronías múltiples activas")
    if dominante % 2 == 0: mensajes.append("Predominio estructural par")
    else: mensajes.append("Predominio estructural impar")
    if convergencia == "Crítica": mensajes.append("Ventana crítica activa")
    elif convergencia == "Alta": mensajes.append("Zona caliente detectada")
    return mensajes

# =========================
# SIDEBAR NAVEGACIÓN
# =========================

st.sidebar.title("🧭 SignalMap IA")
menu = st.sidebar.radio(
    "Navegación",
    [
        "📖 Diario de Señales (REGISTRO HOY)",
        "📊 Timeline de Hoy",
        "🏠 Dashboard Global",
        "🎯 Sorteo Número Sugerido",
        "🪞 Motor Espejo"
    ]
)

# =========================
# DIARIO DE SEÑALES (MÓDULO PRIORITARIO)
# =========================

if menu == "📖 Diario de Señales (REGISTRO HOY)":
    st.title("📖 Diario de Señales - Registro Inmediato")
    st.markdown("### Captura las configuraciones y secuencias detectadas hoy sin restricciones.")

    sorteo = st.selectbox("Selecciona el Sorteo", list(GAME_CONFIG.keys()))
    numeros = st.text_input("Introduce los números de hoy (separados por coma Ej: 7,1,2,2)")
    nota = st.text_area("Notas / Interpretación de la señal")
    nivel = st.select_slider("Nivel de Convergencia IA", options=["🌊 Baja", "📡 Media", "⚡ Alta", "🔥 Crítica"])

    if st.button("🚀 Guardar Señal de Hoy"):
        if numeros:
            lista_numeros = [int(x.strip()) for x in numeros.split(",") if x.strip().isdigit()]
            
            registro = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sorteo": sorteo,
                "numeros": lista_numeros,
                "nota": nota,
                "nivel": nivel
            }

            # 1. Guardado Instantáneo en la Memoria Local
            st.session_state.local_signals.append(registro)
            st.success("✅ ¡Señal registrada localmente con éxito en la sesión!")

            # 2. Intento de respaldo en Firebase en segundo plano
            if firebase_active:
                try:
                    db.child("signals").child(st.session_state.user_id).child(sorteo).push(registro)
                    st.info("📡 Copia de seguridad sincronizada en la nube de Firebase.")
                except:
                    st.warning("⚠️ No se pudo enviar a Firebase, pero tu señal está segura en la tabla local abajo.")
        else:
            st.error("Por favor introduce números válidos antes de guardar.")

# =========================
# TIMELINE DE HOY
# =========================

elif menu == "📊 Timeline de Hoy":
    st.title("📊 Historial de Señales Capturadas Hoy")
    
    # Combinar datos locales y de Firebase si están disponibles
    todas_las_sevales = list(st.session_state.local_signals)

    if firebase_active:
        try:
            for game in GAME_CONFIG.keys():
                registros = db.child("signals").child(st.session_state.user_id).child(game).get()
                if registros.each():
                    for r in registros.each():
                        data = r.val()
                        data["sorteo"] = game
                        if data not in todas_las_sevales:
                            todas_las_sevales.append(data)
        except:
            pass

    if len(todas_las_sevales) > 0:
        df_timeline = pd.DataFrame(todas_las_sevales)
        st.dataframe(df_timeline, use_container_width=True)
        
        # Opción para descargar tus datos de hoy en JSON por si cierras la app
        json_string = json.dumps(todas_las_sevales, indent=4)
        st.download_button(
            label="📥 Descargar Respaldo de Señales (JSON)",
            data=json_string,
            file_name=f"signals_respaldo_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    else:
        st.info("Aún no has registrado señales en esta sesión. Ve al menú 'Diario de Señales' para empezar.")

# =========================
# DASHBOARD GLOBAL
# =========================

elif menu == "🏠 Dashboard Global":
    st.title("🧠 Matriz Global de Convergencia")
    resultados = []
    cols = st.columns(2)
    contador_col = 0

    for game in GAME_CONFIG.keys():
        df = generar_datos(game)
        freq = df["numero"].value_counts()
        dominante = int(freq.idxmax())
        persistencia = int(freq.max())
        sincronias = int(len(freq[freq > 5]))
        convergencia, icono = calcular_convergencia(persistencia, sincronias)

        resultados.append({"Sorteo": game, "Estado": icono, "Convergencia": convergencia, "Dominante": dominante})
        mensajes = interpretacion_ia(dominante, persistencia, sincronias, convergencia)

        with cols[contador_col]:
            st.markdown(f"""
            <div class="dashboard-card">
            <h3>{icono} {game}</h3>
            <p><b>Convergencia:</b> {convergencia} | <b>Dominante:</b> {dominante}</p>
            <p><b>Persistencia:</b> {persistencia} | <b>Sincronías:</b> {sincronias}</p>
            </div>
            """, unsafe_allow_html=True)
            
            fig = px.bar(x=freq.index, y=freq.values, color=freq.values)
            fig.update_layout(template="plotly_dark", height=200, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

        contador_col = 0 if contador_col >= 1 else contador_col + 1

# =========================
# SORTEO SUGERIDO
# =========================

elif menu == "🎯 Sorteo Número Sugerido":
    st.title("🎯 Sorteo Número Sugerido")
    for game in GAME_CONFIG.keys():
        st.markdown(f"## 🎲 {game}")
        
        # Extraer de la sesión actual
        todos = []
        for s in st.session_state.local_signals:
            if s["sorteo"] == game:
                todos.extend(s["numeros"])

        if len(todos) == 0:
            todos = list(np.random.randint(GAME_CONFIG[game]["min"], GAME_CONFIG[game]["max"] + 1, 120))

        contador = Counter(todos)
        top = contador.most_common(GAME_CONFIG[game]["cantidad"])
        sugeridos = [x[0] for x in top]

        st.success(f"🎯 Sugerencia IA: {sugeridos}")
        st.info(f"🪞 Dualidad Espejo: {[espejo(n) for n in sugeridos]}")

# =========================
# MOTOR ESPEJO
# =========================

elif menu == "🪞 Motor Espejo":
    st.title("🪞 Motor Espejo Estructural")
    numero = st.text_input("Introduce combinación o secuencia numérica")
    if numero:
        st.success(f"🪞 Espejo reflejado: {espejo(numero)}")
