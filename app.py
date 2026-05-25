import streamlit as st

import plotly.graph_objects as go

import numpy as np

import pandas as pd

import json

import os

import glob

import re

import easyocr

import cv2

from PIL import Image

from datetime import datetime

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
# ESTILO PREMIUM
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
# SIDEBAR
# ==================================================

st.sidebar.title("SIGNAL MAP AI")

page = st.sidebar.radio(
    "Navegación",
    [
        "Señal en Vivo",
        "Agregar Registro",
        "Diario de Señales",
        "Timeline",
        "Insights"
    ]
)

# ==================================================
# GUARDAR SEÑAL
# ==================================================

def save_signal(signal_data):

    os.makedirs("signals", exist_ok=True)

    filename = f"signals/{signal_data['date']}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(signal_data, f, indent=4)

# ==================================================
# CARGAR SEÑAL
# ==================================================

def load_signal(date):

    filename = f"signals/{date}.json"

    if os.path.exists(filename):

        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    return None

# ==================================================
# MOTOR DE ANÁLISIS
# ==================================================

def analyze_pattern(nodes):

    x_values = [n[0] for n in nodes]
    y_values = [n[1] for n in nodes]

    symmetry_score = round(
        1 - abs(np.mean(x_values)),
        2
    )

    vertical_alignment = np.std(x_values) < 0.25

    lower_density = np.mean(y_values) < 0

    reading = []

    if symmetry_score > 0.75:
        reading.append(
            "Alta alineación energética detectada."
        )

    if vertical_alignment:
        reading.append(
            "Se detectó una fuerte estructura de eje central."
        )

    if lower_density:
        reading.append(
            "La concentración inferior sugiere manifestación y estabilidad."
        )

    if len(reading) == 0:
        reading.append(
            "La estructura muestra exploración y expansión."
        )

    return {
        "pattern_type": "Estructura Humanoide",
        "energy_type": "Convergente",
        "symmetry_score": symmetry_score,
        "reading": " ".join(reading)
    }

# ==================================================
# NODOS BASE
# ==================================================

nodes = [

    (0.00, 0.60),
    (-0.15, 0.50),
    (0.15, 0.50),

    (-0.25, 0.30),
    (0.25, 0.30),

    (-0.10, 0.10),
    (0.10, 0.10),

    (0.00, -0.10),

    (-0.15, -0.30),
    (0.15, -0.30),

    (-0.05, -0.55),
    (0.05, -0.55)

]

# ==================================================
# SEÑAL EN VIVO
# ==================================================

if page == "Señal en Vivo":

    st.title("SIGNAL MAP AI")

    st.markdown("""
### Sistema Inteligente de Patrones

Analiza • Interpreta • Guarda • Visualiza
""")

    analysis = analyze_pattern(nodes)

    x = [n[0] for n in nodes]
    y = [n[1] for n in nodes]

    fig = go.Figure()

    for i in range(len(nodes)-1):

        fig.add_trace(
            go.Scatter(
                x=[nodes[i][0], nodes[i+1][0]],
                y=[nodes[i][1], nodes[i+1][1]],
                mode="lines",
                line=dict(
                    width=2,
                    color="#7B61FF"
                ),
                hoverinfo="none",
                showlegend=False
            )
        )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers+text",

            marker=dict(
                size=18,
                color="#B388FF",
                line=dict(
                    width=2,
                    color="white"
                )
            ),

            text=[
                str(i+1)
                for i in range(len(nodes))
            ],

            textposition="top center",

            hovertemplate=
            "<b>Nodo %{text}</b><extra></extra>"
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

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Simetría",
            f"{analysis['symmetry_score'] * 100:.0f}%"
        )

    with col2:

        st.metric(
            "Patrón",
            analysis["pattern_type"]
        )

    with col3:

        st.metric(
            "Energía",
            analysis["energy_type"]
        )

    st.subheader("Lectura de Patrón")

    st.info(
        analysis["reading"]
    )

    if st.button("Guardar Señal"):

        signal_entry = {

            "date": str(datetime.now().date()),

            "title": "Formación Central",

            "pattern_type": analysis["pattern_type"],

            "energy_type": analysis["energy_type"],

            "symmetry_score": analysis["symmetry_score"],

            "intensity": 92,

            "reading": analysis["reading"],

            "created_at": str(datetime.now())
        }

        save_signal(signal_entry)

        st.success(
            "Señal guardada correctamente."
        )

# ==================================================
# AGREGAR REGISTRO
# ==================================================

if page == "Agregar Registro":

    st.title("Agregar Registro")

    input_mode = st.radio(

        "Selecciona el tipo de entrada",

        [
            "Bloques Numéricos",
            "Detección con Cámara",
            "Imagen desde Galería"
        ]
    )

    # ==================================================
    # BLOQUES NUMÉRICOS
    # ==================================================

    if input_mode == "Bloques Numéricos":

        st.subheader("Registro de Señales del Día")

        signal_blocks = st.text_area(

            "Ingresa señales separadas por espacios o líneas",

            height=250,

            placeholder="""
111
222
777
11:11
444
888
333
"""
        )

        if st.button("Analizar Señales"):

            cleaned_text = signal_blocks.replace("\n", " ")

            signals = cleaned_text.split()

            detected_numbers = []

            for signal in signals:

                nums = re.findall(r'\d+', signal)

                for n in nums:
                    detected_numbers.append(n)

            frequency_map = {}

            for num in detected_numbers:

                if num in frequency_map:
                    frequency_map[num] += 1
                else:
                    frequency_map[num] = 1

            dominant_number = max(
                frequency_map,
                key=frequency_map.get
            )

            dominant_count = frequency_map[
                dominant_number
            ]

            digit_energy = 0

            for number in detected_numbers:

                digit_energy += sum(
                    map(int, number)
                )

            st.subheader("Resultados")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Señales Detectadas",
                    len(detected_numbers)
                )

            with col2:

                st.metric(
                    "Número Dominante",
                    dominant_number
                )

            with col3:

                st.metric(
                    "Frecuencia Total",
                    digit_energy
                )

            st.subheader("Frecuencias")

            freq_data = pd.DataFrame({

                "Número":
                list(frequency_map.keys()),

                "Repeticiones":
                list(frequency_map.values())

            })

            st.dataframe(
                freq_data,
                use_container_width=True
            )

            fig = go.Figure()

            fig.add_trace(

                go.Bar(

                    x=list(frequency_map.keys()),

                    y=list(frequency_map.values())
                )
            )

            fig.update_layout(

                title="Mapa de Frecuencias",

                paper_bgcolor="#050816",

                plot_bgcolor="#050816",

                font=dict(
                    color="white"
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            reading = f"""
La secuencia dominante del día fue {dominant_number},
repitiéndose {dominant_count} veces.

La frecuencia acumulativa total alcanzó
un valor de {digit_energy}.

El sistema detecta concentración energética
sobre patrones repetitivos y sincronías
numéricas persistentes.
"""

            st.subheader("Lectura Automática")

            st.info(reading)

            if st.button("Guardar Registro Diario"):

                signal_entry = {

                    "date": str(datetime.now().date()),

                    "title": "Registro Numérico Diario",

                    "pattern_type": "Frecuencia Numérica",

                    "energy_type": "Sincronía",

                    "symmetry_score": 0.90,

                    "intensity": digit_energy,

                    "dominant_number":
                    dominant_number,

                    "signals":
                    detected_numbers,

                    "reading":
                    reading,

                    "created_at":
                    str(datetime.now())
                }

                save_signal(signal_entry)

                st.success(
                    "Registro guardado correctamente."
                )

    # ==================================================
    # CÁMARA
    # ==================================================

    elif input_mode == "Detección con Cámara":

        st.subheader("Escaneo en Tiempo Real")

        camera_image = st.camera_input(
            "Captura una señal"
        )

        if camera_image is not None:

            image = Image.open(camera_image)

            st.image(
                image,
                caption="Imagen Capturada",
                use_container_width=True
            )

            reader = easyocr.Reader(['en'])

            results = reader.readtext(
                np.array(image)
            )

            detected_text = ""

            for result in results:

                detected_text += result[1] + " "

            st.subheader("Contenido Detectado")

            st.write(detected_text)

            numbers = re.findall(
                r'\d+',
                detected_text
            )

            digit_sum = sum(
                [sum(map(int, num)) for num in numbers]
            )

            st.metric(
                "Frecuencia Energética",
                digit_sum
            )

    # ==================================================
    # GALERÍA
    # ==================================================

    elif input_mode == "Imagen desde Galería":

        uploaded_file = st.file_uploader(

            "Sube una imagen",

            type=["png", "jpg", "jpeg"]
        )

        if uploaded_file is not None:

            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Imagen Analizada",
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

            numbers = re.findall(
                r'\d+',
                detected_text
            )

            digit_sum = sum(
                [sum(map(int, num)) for num in numbers]
            )

            st.metric(
                "Frecuencia Detectada",
                digit_sum
            )

# ==================================================
# DIARIO DE SEÑALES
# ==================================================

if page == "Diario de Señales":

    st.title("Diario de Señales")

    selected_date = st.date_input(
        "Selecciona una fecha"
    )

    signal = load_signal(
        str(selected_date)
    )

    if signal:

        st.subheader(
            signal["title"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Simetría",
                f"{signal['symmetry_score'] * 100:.0f}%"
            )

        with col2:

            st.metric(
                "Intensidad",
                signal["intensity"]
            )

        st.markdown(
            f"### Tipo de Patrón: {signal['pattern_type']}"
        )

        st.markdown(
            f"### Tipo de Energía: {signal['energy_type']}"
        )

        st.info(
            signal["reading"]
        )

    else:

        st.warning(
            "No existe una señal guardada para esta fecha."
        )

# ==================================================
# TIMELINE
# ==================================================

if page == "Timeline":

    st.title("Timeline de Señales")

    files = sorted(
        glob.glob("signals/*.json")
    )

    if len(files) == 0:

        st.warning(
            "Aún no hay señales guardadas."
        )

    for file in files:

        with open(file, "r", encoding="utf-8") as f:

            signal = json.load(f)

            st.markdown(f"""
---
## {signal['date']}

### {signal['pattern_type']}

**Energía**
{signal['energy_type']}

**Lectura**
{signal['reading']}
""")

# ==================================================
# INSIGHTS
# ==================================================

if page == "Insights":

    st.title("Insights")

    files = sorted(
        glob.glob("signals/*.json")
    )

    if len(files) == 0:

        st.warning(
            "No hay suficientes señales guardadas."
        )

    else:

        symmetry_scores = []

        for file in files:

            with open(file, "r", encoding="utf-8") as f:

                signal = json.load(f)

                symmetry_scores.append(
                    signal["symmetry_score"]
                )

        avg_symmetry = np.mean(
            symmetry_scores
        )

        st.metric(
            "Promedio de Simetría",
            f"{avg_symmetry * 100:.0f}%"
        )

        st.markdown("""
### Lectura General

Las señales recientes muestran incremento
en patrones repetitivos y sincronías.

El sistema detecta consolidación
de estructuras numéricas dominantes.
""")
