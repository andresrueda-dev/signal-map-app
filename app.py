# =========================
# SIGNALMAP IA - AI CONVERGENCE PLATFORM
# =========================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from collections import Counter
import random

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

.sidebar .sidebar-content {
    background-color: #0f172a;
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

.slider-container {
    display: flex;
    overflow-x: auto;
    gap: 12px;
    padding: 10px 0px;
}

.slider-card {
    min-width: 220px;
    background-color: #111827;
    border-radius: 14px;
    padding: 14px;
    border: 1px solid #1f2937;
    text-align: center;
}

.slider-critical {
    border: 1px solid #ef4444;
    box-shadow: 0px 0px 14px #ef4444;
}

.slider-hot {
    border: 1px solid #06b6d4;
    box-shadow: 0px 0px 10px #06b6d4;
}

.interpret-box {
    background-color: #111827;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "registro_senales" not in st.session_state:
    st.session_state.registro_senales = []

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
        160
    )

    timestamps = pd.date_range(
        start=datetime.now(),
        periods=160,
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

    texto = str(numero)

    resultado = ""

    for d in texto:

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
        return "🔥 CRÍTICA", score

    elif score >= 80:
        return "⚡ ALTA", score

    elif score >= 40:
        return "📡 MEDIA", score

    else:
        return "🌊 BAJA", score

def generar_interpretacion(
    dominante,
    persistencia,
    sincronias,
    game,
    score
):

    mensajes = []

    if persistencia >= 10:

        mensajes.append(
            f"⚡ Persistencia fuerte detectada en {game}"
        )

    if sincronias >= 5:

        mensajes.append(
            f"🪐 Sincronías múltiples activas"
        )

    if dominante % 2 == 0:

        mensajes.append(
            "📡 Predominio estructural par"
        )

    else:

        mensajes.append(
            "🌗 Predominio estructural impar"
        )

    if score >= 120:

        mensajes.append(
            "🔥 Ventana crítica detectada"
        )

    elif score >= 80:

        mensajes.append(
            "⚡ Zona caliente activa"
        )

    else:

        mensajes.append(
            "🌊 Comportamiento estable"
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
        "⚡ Tesla Nodes",
        "🗺️ Cartography Layer",
        "🪐 Constellation Map",
        "🛰️ Master Console"
    ]
)

# =========================
# DASHBOARD GLOBAL
# =========================

if menu == "🏠 Dashboard Global":

    st.title("🧠 SignalMap IA")

    st.markdown("""
    ## 🌐 Centro de convergencia multi-sorteo
    """)

    cards_html = '<div class="slider-container">'

    resultados = []

    for game in GAME_CONFIG.keys():

        df = generar_datos(game)

        freq = df["numero"].value_counts()

        dominante = freq.idxmax()

        persistencia = freq.max()

        sincronias = len(
            freq[freq > 5]
        )

        convergencia, score = calcular_convergencia(
            persistencia,
            sincronias
        )

        if score >= 120:
            clase = "slider-critical"

        elif score >= 80:
            clase = "slider-hot"

        else:
            clase = ""

        cards_html += f"""
        <div class="slider-card {clase}">
            <h4>{game}</h4>
            <p>{convergencia}</p>
            <small>
            Nodo dominante: {dominante}
            </small>
        </div>
        """

        resultados.append({
            "Sorteo": game,
            "Dominante": dominante,
            "Persistencia": persistencia,
            "Sincronías": sincronias,
            "Convergencia": convergencia,
            "Score": score
        })

    cards_html += "</div>"

    st.markdown(
        cards_html,
        unsafe_allow_html=True
    )

    st.divider()

    dashboard_df = pd.DataFrame(
        resultados
    )

    st.dataframe(
        dashboard_df,
        use_container_width=True
    )

    st.markdown("""
    ## 🔥 Ranking IA
    """)

    fig_rank = px.bar(
        dashboard_df,
        x="Sorteo",
        y="Score",
        color="Score"
    )

    fig_rank.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_rank,
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

        todos = []

        if st.session_state.registro_senales:

            for registro in st.session_state.registro_senales:

                if registro["sorteo"] == game:

                    todos.extend(
                        registro["numeros"]
                    )

        if len(todos) == 0:

            minimo = GAME_CONFIG[game]["min"]
            maximo = GAME_CONFIG[game]["max"]

            todos = list(np.random.randint(
                minimo,
                maximo + 1,
                100
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

        heat_df = pd.DataFrame(
            contador.most_common(10),
            columns=[
                "Numero",
                "Frecuencia"
            ]
        )

        fig_heat = px.bar(
            heat_df,
            x="Numero",
            y="Frecuencia",
            color="Frecuencia"
        )

        fig_heat.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_heat,
            use_container_width=True
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

        dominante = freq.idxmax()

        persistencia = freq.max()

        sincronias = len(
            freq[freq > 5]
        )

        convergencia, score = calcular_convergencia(
            persistencia,
            sincronias
        )

        mensajes = generar_interpretacion(
            dominante,
            persistencia,
            sincronias,
            game,
            score
        )

        st.markdown(
            '<div class="interpret-box">',
            unsafe_allow_html=True
        )

        for m in mensajes:

            st.write(m)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

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
        "Interpretación / señal"
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

    categoria = st.selectbox(
        "Categoría",
        [
            "Persistencia",
            "Convergencia",
            "Nodo caliente",
            "Dualidad",
            "Patrón repetitivo"
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

            "sorteo": sorteo,

            "numeros": lista_numeros,

            "nota": nota,

            "nivel": nivel,

            "categoria": categoria
        }

        st.session_state.registro_senales.append(
            registro
        )

        st.success(
            "⚡ Señal registrada"
        )

    st.divider()

    if st.session_state.registro_senales:

        historial_df = pd.DataFrame(
            st.session_state.registro_senales
        )

        st.dataframe(
            historial_df,
            use_container_width=True
        )

# =========================
# TIMELINE
# =========================

elif menu == "📊 Timeline":

    st.title("📊 Timeline")

    if st.session_state.registro_senales:

        timeline_df = pd.DataFrame(
            st.session_state.registro_senales
        )

        st.dataframe(
            timeline_df,
            use_container_width=True
        )

        if "nivel" in timeline_df.columns:

            conteo = timeline_df[
                "nivel"
            ].value_counts()

            fig = px.pie(
                values=conteo.values,
                names=conteo.index
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# =========================
# TESLA NODES
# =========================

elif menu == "⚡ Tesla Nodes":

    st.title("⚡ Tesla Nodes")

    energia = np.random.randint(
        0,
        100,
        20
    )

    fig = px.scatter(
        x=np.arange(20),
        y=energia,
        size=energia,
        color=energia
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# CARTOGRAPHY
# =========================

elif menu == "🗺️ Cartography Layer":

    st.title("🗺️ Cartography Layer")

    mapa = pd.DataFrame({
        "x": np.random.randn(120),
        "y": np.random.randn(120),
        "intensidad": np.random.randint(
            1,
            500,
            120
        )
    })

    fig = px.density_heatmap(
        mapa,
        x="x",
        y="y",
        z="intensidad"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# CONSTELLATION
# =========================

elif menu == "🪐 Constellation Map":

    st.title("🪐 Constellation Map")

    x = np.random.randn(40)
    y = np.random.randn(40)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='markers+lines',
            marker=dict(
                size=14,
                color=np.random.randint(
                    0,
                    100,
                    40
                ),
                colorscale='Plasma'
            )
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# MASTER CONSOLE
# =========================

elif menu == "🛰️ Master Console":

    st.title("🛰️ Master Console")

    estados = {

        "Núcleo IA": "Activo",
        "Convergencia": "Operativa",
        "Timeline": "Activo",
        "Tesla Nodes": "Sincronizados",
        "Motor Espejo": "Disponible",
        "AI Interpretation": "Online"
    }

    for k,v in estados.items():

        st.success(
            f"{k}: {v}"
        )

    st.divider()

    st.code("""
>>> SIGNALMAP IA ACTIVE
>>> AI CONVERGENCE ONLINE
>>> MULTI-LOTTERY MODE ACTIVE
>>> STRUCTURAL ANALYSIS READY
>>> MIRROR ENGINE STANDBY
>>> TESLA NODE ONLINE
""")
