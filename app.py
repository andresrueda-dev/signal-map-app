# =========================
# SIGNALMAP IA - FIREBASE AI PLATFORM
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
# FIREBASE
# =========================

import pyrebase

firebase_config = {

    "apiKey": "TU_API_KEY",
    "authDomain": "TU_PROYECTO.firebaseapp.com",
    "databaseURL": "https://TU_PROYECTO-default-rtdb.firebaseio.com/",
    "projectId": "TU_PROYECTO",
    "storageBucket": "TU_PROYECTO.appspot.com",
    "messagingSenderId": "XXXX",
    "appId": "XXXX"
}

firebase = pyrebase.initialize_app(
    firebase_config
)

auth = firebase.auth()

db = firebase.database()

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="SignalMap IA",
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

.card-critical {
    border: 1px solid #ef4444;
    box-shadow: 0px 0px 12px #ef4444;
}

.card-hot {
    border: 1px solid #06b6d4;
    box-shadow: 0px 0px 10px #06b6d4;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.title("🧠 SignalMap IA")

    st.markdown("""
    ## 🔐 Login Firebase
    """)

    email = st.text_input("Correo")

    password = st.text_input(
        "Contraseña",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Iniciar Sesión"):

            try:

                user = auth.sign_in_with_email_and_password(
                    email,
                    password
                )

                st.session_state.user = user

                st.success(
                    "Sesión iniciada"
                )

                st.rerun()

            except:

                st.error(
                    "Error al iniciar sesión"
                )

    with col2:

        if st.button("Crear Cuenta"):

            try:

                auth.create_user_with_email_and_password(
                    email,
                    password
                )

                st.success(
                    "Cuenta creada"
                )

            except:

                st.error(
                    "No se pudo crear cuenta"
                )

    st.stop()

# =========================
# CONFIG
# =========================

GAME_CONFIG = {

    "TRIS": {
        "min": 0,
        "max": 9,
        "cantidad": 5
    },

    "Melate": {
        "min": 1,
        "max": 56,
        "cantidad": 6
    },

    "Chispazo": {
        "min": 1,
        "max": 28,
        "cantidad": 5
    },

    "Powerball": {
        "min": 1,
        "max": 69,
        "cantidad": 5
    },

    "Mega Millions": {
        "min": 1,
        "max": 70,
        "cantidad": 5
    },

    "Gana Gato": {
        "min": 1,
        "max": 5,
        "cantidad": 8
    }
}

# =========================
# FUNCTIONS
# =========================

def generar_datos(game):

    minimo = GAME_CONFIG[game]["min"]
    maximo = GAME_CONFIG[game]["max"]

    numeros = np.random.randint(
        minimo,
        maximo + 1,
        180
    )

    timestamps = pd.date_range(
        start=datetime.now(),
        periods=180,
        freq="min"
    )

    return pd.DataFrame({
        "numero": numeros,
        "timestamp": timestamps
    })

def espejo(numero):

    mapa = {
        "0":"5",
        "1":"6",
        "2":"7",
        "3":"8",
        "4":"9",
        "5":"0",
        "6":"1",
        "7":"2",
        "8":"3",
        "9":"4"
    }

    resultado = ""

    for d in str(numero):

        if d in mapa:
            resultado += mapa[d]

        else:
            resultado += d

    return resultado

def calcular_convergencia(
    persistencia,
    sincronias
):

    score = (
        persistencia * 10
    ) + (
        sincronias * 5
    )

    if score >= 120:
        return "⚡ Crítica", "🔥"

    elif score >= 80:
        return "Alta", "⚡"

    elif score >= 40:
        return "Media", "📡"

    else:
        return "Baja", "🌊"

def interpretacion_ia(
    dominante,
    persistencia,
    sincronias,
    convergencia
):

    mensajes = []

    if persistencia >= 10:

        mensajes.append(
            "Persistencia elevada detectada"
        )

    if sincronias >= 5:

        mensajes.append(
            "Sincronías múltiples activas"
        )

    if dominante % 2 == 0:

        mensajes.append(
            "Predominio estructural par"
        )

    else:

        mensajes.append(
            "Predominio estructural impar"
        )

    if convergencia == "Crítica":

        mensajes.append(
            "Ventana crítica activa"
        )

    elif convergencia == "Alta":

        mensajes.append(
            "Zona caliente detectada"
        )

    return mensajes

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🧭 SignalMap IA")

menu = st.sidebar.radio(
    "Navegación",
    [
        "🏠 Dashboard Global",
        "🎯 Sorteo Número Sugerido",
        "🧠 AI Interpretation",
        "🪞 Motor Espejo",
        "📖 Diario de Señales",
        "📊 Timeline",
        "🛰️ Master Console"
    ]
)

# =========================
# DASHBOARD GLOBAL
# =========================

if menu == "🏠 Dashboard Global":

    st.title("🧠 SignalMap IA")

    st.markdown("""
    ## 🌐 MATRIZ GLOBAL DE CONVERGENCIA
    """)

    resultados = []

    cols = st.columns(2)

    contador_col = 0

    for game in GAME_CONFIG.keys():

        df = generar_datos(game)

        freq = df["numero"].value_counts()

        dominante = int(freq.idxmax())

        persistencia = int(freq.max())

        sincronias = int(
            len(freq[freq > 5])
        )

        convergencia, icono = calcular_convergencia(
            persistencia,
            sincronias
        )

        resultados.append({

            "Sorteo": game,

            "Estado": icono,

            "Convergencia": convergencia,

            "Dominante": dominante
        })

        mensajes = interpretacion_ia(
            dominante,
            persistencia,
            sincronias,
            convergencia
        )

        with cols[contador_col]:

            st.markdown(f"""
            <div class="dashboard-card">
            <h3>{icono} {game}</h3>
            <p><b>Convergencia:</b> {convergencia}</p>
            <p><b>Dominante:</b> {dominante}</p>
            <p><b>Persistencia:</b> {persistencia}</p>
            <p><b>Sincronías:</b> {sincronias}</p>
            </div>
            """, unsafe_allow_html=True)

            for m in mensajes:

                st.write(f"• {m}")

            fig = px.bar(
                x=freq.index,
                y=freq.values,
                color=freq.values
            )

            fig.update_layout(
                template="plotly_dark",
                height=250
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        contador_col += 1

        if contador_col > 1:
            contador_col = 0

    st.divider()

    st.markdown("""
    ## 📊 MATRIZ GLOBAL
    """)

    tabla_df = pd.DataFrame(
        resultados
    )

    st.dataframe(
        tabla_df,
        use_container_width=True
    )

# =========================
# SORTEO SUGERIDO
# =========================

elif menu == "🎯 Sorteo Número Sugerido":

    st.title("🎯 Sorteo Número Sugerido")

    for game in GAME_CONFIG.keys():

        st.markdown(f"""
        ## 🎲 {game}
        """)

        registros = db.child(
            "signals"
        ).child(
            st.session_state.user["localId"]
        ).child(
            game
        ).get()

        todos = []

        if registros.each():

            for r in registros.each():

                data = r.val()

                if "numeros" in data:

                    todos.extend(
                        data["numeros"]
                    )

        if len(todos) == 0:

            minimo = GAME_CONFIG[game]["min"]

            maximo = GAME_CONFIG[game]["max"]

            todos = list(np.random.randint(
                minimo,
                maximo + 1,
                120
            ))

        contador = Counter(todos)

        top = contador.most_common(
            GAME_CONFIG[game]["cantidad"]
        )

        sugeridos = [x[0] for x in top]

        st.success(
            f"🎯 Sugerencia IA: {sugeridos}"
        )

        espejo_combo = []

        for n in sugeridos:

            espejo_combo.append(
                espejo(n)
            )

        st.info(
            f"🪞 Dualidad: {espejo_combo}"
        )

# =========================
# AI INTERPRETATION
# =========================

elif menu == "🧠 AI Interpretation":

    st.title("🧠 AI Interpretation")

    for game in GAME_CONFIG.keys():

        st.markdown(f"""
        ## 🔍 {game}
        """)

        df = generar_datos(game)

        freq = df["numero"].value_counts()

        dominante = int(freq.idxmax())

        persistencia = int(freq.max())

        sincronias = int(
            len(freq[freq > 5])
        )

        convergencia, icono = calcular_convergencia(
            persistencia,
            sincronias
        )

        mensajes = interpretacion_ia(
            dominante,
            persistencia,
            sincronias,
            convergencia
        )

        st.markdown(f"""
        ### {icono} {convergencia}
        """)

        for m in mensajes:

            st.write(f"• {m}")

# =========================
# MOTOR ESPEJO
# =========================

elif menu == "🪞 Motor Espejo":

    st.title("🪞 Motor Espejo")

    numero = st.text_input(
        "Introduce combinación"
    )

    if numero:

        resultado = espejo(numero)

        st.success(
            f"🪞 Espejo estructural: {resultado}"
        )

# =========================
# DIARIO
# =========================

elif menu == "📖 Diario de Señales":

    st.title("📖 Diario de Señales")

    sorteo = st.selectbox(
        "Sorteo",
        list(GAME_CONFIG.keys())
    )

    numeros = st.text_input(
        "Introduce números separados por coma"
    )

    nota = st.text_area(
        "Interpretación"
    )

    nivel = st.select_slider(
        "Nivel IA",
        options=[
            "🌊 Baja",
            "📡 Media",
            "⚡ Alta",
            "🔥 Crítica"
        ]
    )

    if st.button("Guardar señal"):

        lista_numeros = [

            int(x.strip())

            for x in numeros.split(",")

            if x.strip().isdigit()
        ]

        registro = {

            "timestamp": str(datetime.now()),

            "numeros": lista_numeros,

            "nota": nota,

            "nivel": nivel
        }

        db.child(
            "signals"
        ).child(
            st.session_state.user["localId"]
        ).child(
            sorteo
        ).push(
            registro
        )

        st.success(
            "⚡ Señal guardada en Firebase"
        )

# =========================
# TIMELINE
# =========================

elif menu == "📊 Timeline":

    st.title("📊 Timeline")

    timeline = []

    for game in GAME_CONFIG.keys():

        registros = db.child(
            "signals"
        ).child(
            st.session_state.user["localId"]
        ).child(
            game
        ).get()

        if registros.each():

            for r in registros.each():

                data = r.val()

                data["sorteo"] = game

                timeline.append(data)

    if len(timeline) > 0:

        timeline_df = pd.DataFrame(
            timeline
        )

        st.dataframe(
            timeline_df,
            use_container_width=True
        )

# =========================
# MASTER CONSOLE
# =========================

elif menu == "🛰️ Master Console":

    st.title("🛰️ Master Console")

    estados = {

        "Firebase": "Activo",
        "Convergencia": "Operativa",
        "AI Interpretation": "Online",
        "Motor Espejo": "Disponible",
        "Timeline": "Sincronizado"
    }

    for k,v in estados.items():

        st.success(
            f"{k}: {v}"
        )

    st.divider()

    st.code("""
>>> SIGNALMAP IA ACTIVE
>>> FIREBASE CONNECTED
>>> AI CONVERGENCE ONLINE
>>> MULTI-LOTTERY MODE ACTIVE
>>> GLOBAL MATRIX READY
>>> MIRROR ENGINE STANDBY
""")
