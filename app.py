# =========================
# SIGNALMAP IA - CORE ENGINE EVOLUTION X
# =========================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
from collections import Counter

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

h1,h2,h3,h4 {
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
    padding: 10px;
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "registro_senales" not in st.session_state:
    st.session_state.registro_senales = []

# =========================
# CONFIG SORTEOS
# =========================

GAME_CONFIG = {

    "TRIS": {
        "max": 9,
        "cantidad": 5,
        "min": 0
    },

    "Melate": {
        "max": 56,
        "cantidad": 6,
        "min": 1
    },

    "Chispazo": {
        "max": 28,
        "cantidad": 5,
        "min": 1
    },

    "Powerball": {
        "max": 69,
        "cantidad": 5,
        "min": 1
    },

    "Mega Millions": {
        "max": 70,
        "cantidad": 5,
        "min": 1
    },

    "Gana Gato": {
        "max": 5,
        "cantidad": 8,
        "min": 1
    }
}

# =========================
# FUNCIONES IA
# =========================

def generar_datos():

    minimo = GAME_CONFIG[sorteo]["min"]
    maximo = GAME_CONFIG[sorteo]["max"]

    numeros = np.random.randint(
        minimo,
        maximo + 1,
        150
    )

    timestamps = pd.date_range(
        start=datetime.now(),
        periods=150,
        freq="min"
    )

    df = pd.DataFrame({
        "numero": numeros,
        "timestamp": timestamps
    })

    return df

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

def calcular_convergencia(freq_max, sync):

    score = (freq_max * 10) + (sync * 5)

    if score >= 120:
        return "🔥 CRÍTICA"

    elif score >= 80:
        return "⚡ ALTA"

    elif score >= 40:
        return "📡 MEDIA"

    else:
        return "🌊 BAJA"

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🧭 SignalMap IA")

sorteo = st.sidebar.selectbox(
    "🎲 Sorteo",
    list(GAME_CONFIG.keys())
)

menu = st.sidebar.radio(
    "Navegación",
    [
        "🏠 Dashboard",
        "🎯 Sorteo Número Sugerido",
        "🧠 AI Interpretation",
        "🪞 Dualidad & Espejo",
        "🪐 Constellation Map",
        "📈 Pattern Evolution",
        "🎲 Predicción Numérica",
        "🗺️ Cartography Layer",
        "📖 Diario de Señales",
        "📊 Timeline",
        "⚡ Tesla Nodes",
        "🛰️ Master Console"
    ]
)

# =========================
# DATA
# =========================

df = generar_datos()

# =========================
# DASHBOARD
# =========================

if menu == "🏠 Dashboard":

    st.title("🧠 SignalMap IA")

    st.markdown(f"""
    ### Plataforma dinámica IA
    ### Sorteo activo: {sorteo}
    """)

    col1, col2, col3, col4 = st.columns(4)

    freq = df["numero"].value_counts()

    dominante = freq.idxmax()

    persistencia = freq.max()

    sincronias = len(
        freq[freq > 5]
    )

    convergencia = calcular_convergencia(
        persistencia,
        sincronias
    )

    col1.metric(
        "Nodo Dominante",
        dominante
    )

    col2.metric(
        "Persistencia",
        persistencia
    )

    col3.metric(
        "Sincronías",
        sincronias
    )

    col4.metric(
        "Convergencia",
        convergencia
    )

    st.divider()

    freq_sort = freq.sort_index()

    fig = px.bar(
        x=freq_sort.index,
        y=freq_sort.values,
        color=freq_sort.values,
        title="Frecuencia Dinámica"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# SORTEO NUMERO SUGERIDO
# =========================

elif menu == "🎯 Sorteo Número Sugerido":

    st.title("🎯 Sorteo Número Sugerido")

    st.markdown("""
    ## 🔥 Motor de convergencia IA
    """)

    todos = []

    # =====================================
    # DATOS REGISTRADOS
    # =====================================

    if st.session_state.registro_senales:

        for registro in st.session_state.registro_senales:

            if registro["sorteo"] == sorteo:

                todos.extend(
                    registro["numeros"]
                )

    # =====================================
    # FALLBACK
    # =====================================

    if len(todos) == 0:

        todos = df["numero"].tolist()

    contador = Counter(todos)

    top = contador.most_common(
        GAME_CONFIG[sorteo]["cantidad"]
    )

    sugeridos = [x[0] for x in top]

    # =====================================
    # HORA CALIENTE
    # =====================================

    hora_actual = datetime.now().hour

    if hora_actual < 15:
        ventana = "13:00 - 15:00"

    elif hora_actual < 19:
        ventana = "15:00 - 19:00"

    else:
        ventana = "19:00 - 21:15"

    # =====================================
    # CONVERGENCIA
    # =====================================

    convergencia = calcular_convergencia(
        max(contador.values()),
        len(contador)
    )

    # =====================================
    # DISPLAY
    # =====================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Ventana caliente",
        ventana
    )

    col2.metric(
        "Convergencia IA",
        convergencia
    )

    col3.metric(
        "Señales acumuladas",
        len(todos)
    )

    st.divider()

    st.success(
        f"🎯 Combinación sugerida: {sugeridos}"
    )

    # =====================================
    # ESPEJO
    # =====================================

    espejo_combo = []

    for n in sugeridos:

        espejo_combo.append(
            espejo(n)
        )

    st.info(
        f"🪞 Dualidad / espejo: {espejo_combo}"
    )

    # =====================================
    # ANALISIS IA
    # =====================================

    st.markdown("## 🧠 Lectura estructural")

    pares = len([
        x for x in sugeridos
        if int(x) % 2 == 0
    ])

    impares = len(sugeridos) - pares

    st.write(f"📡 Pares dominantes: {pares}")
    st.write(f"🌗 Impares dominantes: {impares}")

    if pares > impares:

        st.success(
            "⚡ Estructura par dominante"
        )

    else:

        st.warning(
            "🔥 Estructura impar dominante"
        )

# =========================
# AI INTERPRETATION
# =========================

elif menu == "🧠 AI Interpretation":

    st.title("🧠 AI Interpretation")

    frecuencia = df["numero"].value_counts()

    dominante = frecuencia.idxmax()

    persistencia = frecuencia.max()

    sincronias = len(
        frecuencia[frecuencia > 4]
    )

    st.markdown("## 🔍 Análisis IA")

    insights = []

    if persistencia > 8:

        insights.append(
            f"⚡ Alta persistencia detectada en nodo {dominante}"
        )

    if sincronias >= 4:

        insights.append(
            "🪐 Sincronías múltiples detectadas"
        )

    if dominante % 2 == 0:

        insights.append(
            "📡 Predominio estructural par"
        )

    else:

        insights.append(
            "🌗 Predominio estructural impar"
        )

    if dominante > (
        GAME_CONFIG[sorteo]["max"] / 2
    ):

        insights.append(
            "🔥 Zona alta dominante"
        )

    else:

        insights.append(
            "🌊 Zona baja dominante"
        )

    for i in insights:

        st.success(i)

# =========================
# DUALIDAD
# =========================

elif menu == "🪞 Dualidad & Espejo":

    st.title("🪞 Dualidad & Espejo")

    numero = st.text_input(
        "Introduce combinación"
    )

    if numero:

        resultado = espejo(numero)

        st.success(
            f"🪞 Espejo estructural: {resultado}"
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
                    GAME_CONFIG[sorteo]["max"],
                    40
                ),
                colorscale='Plasma'
            ),
            line=dict(width=1)
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
# EVOLUTION
# =========================

elif menu == "📈 Pattern Evolution":

    st.title("📈 Evolución de Patrones")

    evolucion = np.cumsum(
        np.random.randn(100)
    )

    fig = px.line(
        x=np.arange(100),
        y=evolucion
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# PREDICCION NUMERICA
# =========================

elif menu == "🎲 Predicción Numérica":

    st.title("🎲 Predicción Numérica")

    cantidad = GAME_CONFIG[sorteo]["cantidad"]

    maximo = GAME_CONFIG[sorteo]["max"]

    minimo = GAME_CONFIG[sorteo]["min"]

    historial = pd.DataFrame()

    for i in range(cantidad):

        historial[f"P{i+1}"] = np.random.randint(
            minimo,
            maximo + 1,
            150
        )

    st.dataframe(
        historial,
        use_container_width=True
    )

    resumen = []

    for columna in historial.columns:

        numeros = historial[columna].tolist()

        contador = Counter(numeros)

        dominante = contador.most_common(1)[0][0]

        frecuencia = contador.most_common(1)[0][1]

        resumen.append({
            "Posición": columna,
            "Dominante": dominante,
            "Frecuencia": frecuencia
        })

    resumen_df = pd.DataFrame(
        resumen
    )

    st.markdown("## 🔥 Dominancia estructural")

    st.dataframe(
        resumen_df,
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
        template="plotly_dark",
        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# DIARIO
# =========================

elif menu == "📖 Diario de Señales":

    st.title("📖 Diario de Señales")

    numeros = st.text_input(
        "Introduce números separados por coma"
    )

    nota = st.text_area(
        "Interpretación / señal"
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
            "nota": nota
        }

        st.session_state.registro_senales.append(
            registro
        )

        st.success(
            "⚡ Señal registrada correctamente"
        )

    st.divider()

    st.markdown("## 📚 Historial")

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
# MASTER CONSOLE
# =========================

elif menu == "🛰️ Master Console":

    st.title("🛰️ Master Console")

    estados = {

        "Núcleo IA": "Activo",
        "Cartografía": "Sincronizada",
        "Clusters": "Detectados",
        "Timeline": "Operativo",
        "Predicción": "Estable",
        "Registro Universal": "Sincronizado",
        "Convergencia": "Activa",
        "Motor Multi-Sorteo": "Online"
    }

    for k,v in estados.items():

        st.success(f"{k}: {v}")

    st.divider()

    st.code(f"""
>>> SIGNALMAP IA CORE ACTIVE
>>> GAME MODE: {sorteo}
>>> CONVERGENCE ENGINE ONLINE
>>> TESLA NODE ACTIVE
>>> SIGNAL SCANNING
>>> MIRROR SYSTEM READY
>>> STRUCTURAL ANALYSIS ACTIVE
""")
