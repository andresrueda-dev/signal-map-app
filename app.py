
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import json
import os
import glob
import re
import easyocr

from PIL import Image
from datetime import datetime

# ==================================================
# CONFIGURACIÓN GENERAL
# ==================================================

st.set_page_config(

    page_title="Signal Map AI",

    layout="wide"
)

# ==================================================
# ESTILO VISUAL
# ==================================================

st.markdown("""

<style>

.stApp{

    background-color:#050816;
    color:white;
}

[data-testid="stSidebar"]{

    background-color:#0B1026;
}

h1,h2,h3,h4{

    color:#C8B6FF;
}

div.stButton > button{

    background:#7B61FF;
    color:white;
    border-radius:12px;
    border:none;
    padding:0.6rem 1rem;
    font-weight:bold;
}

div.stMetric{

    background-color:#11162A;
    padding:10px;
    border-radius:10px;
}

</style>

""", unsafe_allow_html=True)

# ==================================================
# CREAR CARPETA
# ==================================================

os.makedirs("signals", exist_ok=True)

# ==================================================
# SIDEBAR VISUAL SYSTEM
# ==================================================

st.sidebar.markdown("""

# 🌌 SIGNAL MAP AI

### Cartografía de Señales
Sistema Experimental de Patrones

---

""")

page = st.sidebar.radio(

    "🧭 Navegación",

    [

        "⚡ Registro Rápido",

        "🌌 Constelación del Día",

        "🖼️ Cargar Imagen",

        "📖 Diario de Señales",

        "📈 Timeline",

        "🧠 Insights IA",

        "🎲 Predicción Numérica",

        "🧩 Constellation Map",

        "⚡ Tesla Nodes",

        "🗺️ Cartography Layer",

        "🔮 AI Interpretation",

        "📡 Pattern Evolution"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("""

### 🛰️ Estado del Sistema

🟢 Núcleo IA activo  
🟢 Cartografía cargada  
🟢 Registro sincronizado  
🟣 Nodo Tesla disponible  
🔵 Constelaciones dinámicas  

""")

st.sidebar.markdown("---")

st.sidebar.caption(
    "Signal Map AI v2.0"
)

# ==================================================
# CLASIFICADOR IA
# ==================================================

def classify_signal(signal):

    clean_signal = signal.replace(":", "")

    if ":" in signal:

        parts = signal.split(":")

        if len(parts) == 2:

            if parts[0] == parts[1]:

                return "Hora Espejo"

            elif parts[0] == parts[1][::-1]:

                return "Hora Reflejo"

    if len(set(clean_signal)) == 1:

        return "Número Repetitivo"

    ascending = ''.join(
        sorted(clean_signal)
    )

    if clean_signal == ascending:

        return "Secuencia Ascendente"

    descending = ''.join(
        sorted(clean_signal, reverse=True)
    )

    if clean_signal == descending:

        return "Secuencia Descendente"

    return "Patrón General"

# ==================================================
# REGISTRO RÁPIDO
# ==================================================

if page == "⚡ Registro Rápido":

    st.title("Registro Rápido de Señales")

    st.markdown("""

Aquí puedes registrar:

• Horas espejo  
• Números repetitivos  
• Secuencias  
• Sincronías  
• Señales del día

""")

    signal_input = st.text_input(

        "Escribe una señal",

        placeholder="Ejemplo: 11:11"
    )

    today = str(datetime.now().date())

    signal_file = f"signals/{today}.json"

    if os.path.exists(signal_file):

        with open(signal_file, "r", encoding="utf-8") as f:

            daily_data = json.load(f)

    else:

        daily_data = {

            "date": today,

            "signals": []
        }

    if st.button("Guardar Señal"):

        if signal_input != "":

            signal_type = classify_signal(
                signal_input
            )

            signal_data = {

                "signal": signal_input,

                "type": signal_type,

                "timestamp":
                str(datetime.now())
            }

            daily_data["signals"].append(
                signal_data
            )

            with open(

                signal_file,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(
                    daily_data,
                    f,
                    indent=4
                )

            st.success(
                f"Señal guardada como: {signal_type}"
            )

    st.subheader("Señales Registradas Hoy")

    if len(daily_data["signals"]) == 0:

        st.warning(
            "Aún no hay señales registradas."
        )

    else:

        for item in daily_data["signals"]:

            st.markdown(f"""

### {item['signal']}

• Tipo:
{item['type']}

• Hora:
{item['timestamp']}

""")

# ==================================================
# CONSTELACIÓN DEL DÍA
# ==================================================

if page == "🌌 Constelación del Día":

    st.title("Constelación del Día")

    today = str(datetime.now().date())

    signal_file = f"signals/{today}.json"

    if os.path.exists(signal_file):

        with open(signal_file, "r", encoding="utf-8") as f:

            daily_data = json.load(f)

        freq_map = {}

        for item in daily_data["signals"]:

            signal = item["signal"]

            if signal in freq_map:

                freq_map[signal] += 1

            else:

                freq_map[signal] = 1

        signals = list(freq_map.keys())

        repetitions = list(freq_map.values())

        if len(signals) > 0:

            fig = go.Figure()

            angles = np.linspace(
                0,
                2*np.pi,
                len(signals),
                endpoint=False
            )

            radius = repetitions

            x = radius * np.cos(angles)

            y = radius * np.sin(angles)

            for i in range(len(x)):

                next_i = (i + 1) % len(x)

                fig.add_trace(

                    go.Scatter(

                        x=[x[i], x[next_i]],

                        y=[y[i], y[next_i]],

                        mode="lines",

                        line=dict(
                            width=2,
                            color="#7B61FF"
                        ),

                        showlegend=False
                    )
                )

            fig.add_trace(

                go.Scatter(

                    x=x,

                    y=y,

                    mode="markers+text",

                    marker=dict(

                        size=[
                            r * 15
                            for r in repetitions
                        ],

                        color="#B388FF",

                        line=dict(
                            width=2,
                            color="white"
                        )
                    ),

                    text=signals,

                    textposition="top center"
                )
            )

            fig.update_layout(

                height=700,

                paper_bgcolor="#050816",

                plot_bgcolor="#050816",

                font=dict(
                    color="white"
                ),

                xaxis=dict(
                    visible=False
                ),

                yaxis=dict(
                    visible=False
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# ==================================================
# CARGAR IMAGEN
# ==================================================

if page == "🖼️ Cargar Imagen":

    st.title("Cargar Imagen de Señales")

    uploaded_file = st.file_uploader(

        "Selecciona una imagen",

        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Imagen Cargada",
            use_container_width=True
        )

        reader = easyocr.Reader(['en'])

        results = reader.readtext(
            np.array(image)
        )

        detected_text = ""

        for result in results:

            detected_text += result[1] + " "

        st.subheader("Texto Detectado")

        st.write(detected_text)

# ==================================================
# DIARIO DE SEÑALES
# ==================================================

if page == "📖 Diario de Señales":

    st.title("Diario de Señales")

    files = sorted(
        glob.glob("signals/*.json")
    )

    if len(files) == 0:

        st.warning(
            "Aún no hay registros."
        )

    else:

        for file in reversed(files):

            with open(file, "r", encoding="utf-8") as f:

                data = json.load(f)

            st.subheader(data["date"])

            for item in data["signals"]:

                st.markdown(f"""

### {item['signal']}

• Tipo:
{item['type']}

• Hora:
{item['timestamp']}

""")

# ==================================================
# TIMELINE
# ==================================================

if page == "📈 Timeline":

    st.title("Timeline de Señales")

    files = sorted(
        glob.glob("signals/*.json")
    )

    timeline_data = []

    for file in files:

        with open(file, "r", encoding="utf-8") as f:

            data = json.load(f)

        timeline_data.append({

            "Fecha": data["date"],

            "Cantidad":
            len(data["signals"])
        })

    if len(timeline_data) > 0:

        df = pd.DataFrame(
            timeline_data
        )

        st.dataframe(
            df,
            use_container_width=True
        )

# ==================================================
# INSIGHTS IA
# ==================================================

if page == "🧠 Insights IA":

    st.title("Insights IA")

    st.info("""

La IA analiza:

• persistencia  
• sincronías  
• repetición estructural  
• patrones dominantes  

""")

# ==================================================
# PREDICCIÓN NUMÉRICA
# ==================================================

if page == "🎲 Predicción Numérica":

    st.title("Predicción Numérica")

    st.info("""

Generador experimental basado en:

• frecuencias  
• patrones  
• resonancias  
• señales registradas  

""")

# ==================================================
# CONSTELLATION MAP
# ==================================================

if page == "🧩 Constellation Map":

    st.title("🧩 Constellation Map")

    st.info("""

Mapa avanzado de nodos y agrupaciones.

""")

# ==================================================
# TESLA NODES
# ==================================================

if page == "⚡ Tesla Nodes":

    st.title("⚡ Tesla Nodes")

    files = sorted(
        glob.glob("signals/*.json")
    )

    frequency_map = {}

    for file in files:

        with open(file, "r", encoding="utf-8") as f:

            data = json.load(f)

        for item in data["signals"]:

            nums = re.findall(
                r'\d',
                item["signal"]
            )

            for n in nums:

                n = int(n)

                if n in frequency_map:

                    frequency_map[n] += 1

                else:

                    frequency_map[n] = 1

    if len(frequency_map) > 0:

        df = pd.DataFrame({

            "Número":
            list(frequency_map.keys()),

            "Frecuencia":
            list(frequency_map.values())
        })

        fig = px.bar(

            df,

            x="Número",

            y="Frecuencia",

            color="Frecuencia",

            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==================================================
# CARTOGRAPHY LAYER
# ==================================================

if page == "🗺️ Cartography Layer":

    st.title("🗺️ Cartography Layer")

    st.info("""

Heatmaps y capas de densidad.

""")

# ==================================================
# AI INTERPRETATION
# ==================================================

if page == "🔮 AI Interpretation":

    st.title("🔮 AI Interpretation")

    st.info("""

Confidence score y lectura contextual IA.

""")

# ==================================================
# PATTERN EVOLUTION
# ==================================================

if page == "📡 Pattern Evolution":

    st.title("📡 Pattern Evolution")

    st.info("""

Seguimiento evolutivo de patrones.

""")
