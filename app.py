

          
         # ==================================================
# IMPORTS
# ==================================================

import streamlit as st
import plotly.graph_objects as go
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
# MENÚ PRINCIPAL
# ==================================================

[
    "Registro Rápido",

    "Constelación del Día",

    "Cargar Imagen",

    "Diario de Señales",

    "Timeline",

    "Insights IA",

    "Predicción Numérica"
]

# ==================================================
# CLASIFICADOR IA
# ==================================================

def classify_signal(signal):

    clean_signal = signal.replace(":", "")

    # ==========================================
    # HORA ESPEJO
    # ==========================================

    if ":" in signal:

        parts = signal.split(":")

        if len(parts) == 2:

            if parts[0] == parts[1]:

                return "Hora Espejo"

            elif parts[0] == parts[1][::-1]:

                return "Hora Reflejo"

    # ==========================================
    # REPETITIVO
    # ==========================================

    if len(set(clean_signal)) == 1:

        return "Número Repetitivo"

    # ==========================================
    # ASCENDENTE
    # ==========================================

    ascending = ''.join(
        sorted(clean_signal)
    )

    if clean_signal == ascending:

        return "Secuencia Ascendente"

    # ==========================================
    # DESCENDENTE
    # ==========================================

    descending = ''.join(
        sorted(clean_signal, reverse=True)
    )

    if clean_signal == descending:

        return "Secuencia Descendente"

    return "Patrón General"

# ==================================================
# REGISTRO RÁPIDO
# ==================================================

if page == "Registro Rápido":

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

    # ==========================================
    # CARGAR DATOS
    # ==========================================

    if os.path.exists(signal_file):

        with open(signal_file, "r", encoding="utf-8") as f:

            daily_data = json.load(f)

    else:

        daily_data = {

            "date": today,

            "signals": []
        }

    # ==========================================
    # REGISTRAR SEÑAL
    # ==========================================

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

    # ==========================================
    # MOSTRAR SEÑALES
    # ==========================================

    st.subheader("Señales Registradas Hoy")

    if len(daily_data["signals"]) == 0:

        st.warning(
            "Aún no hay señales registradas."
        )

    else:

        freq_map = {}

        for item in daily_data["signals"]:

            signal = item["signal"]

            if signal in freq_map:

                freq_map[signal] += 1

            else:

                freq_map[signal] = 1

            st.markdown(f"""

### {signal}

• Tipo:
{item['type']}

• Hora:
{item['timestamp']}

""")

# ==================================================
# CONSTELACIÓN DEL DÍA
# ==================================================

if page == "Constelación del Día":

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

            # ======================================
            # LÍNEAS
            # ======================================

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

            # ======================================
            # NODOS
            # ======================================

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

            # ======================================
            # IA
            # ======================================

            dominant_signal = max(
                freq_map,
                key=freq_map.get
            )

            st.subheader(
                "Lectura IA"
            )

            st.info(f"""

La señal dominante del día es {dominant_signal}.

La constelación muestra concentración
sobre frecuencias repetitivas y patrones
de sincronía persistente.

El mapa energético presenta nodos
interconectados con expansión radial.

""")

        else:

            st.warning(
                "No hay señales suficientes."
            )

    else:

        st.warning(
            "Aún no existe registro para hoy."
        )

# ==================================================
# CARGAR IMAGEN
# ==================================================

if page == "Cargar Imagen":

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

        st.subheader(
            "Texto Detectado"
        )

        st.write(
            detected_text
        )

        numbers = re.findall(
            r'\d+',
            detected_text
        )

        if len(numbers) > 0:

            st.subheader(
                "Números Detectados"
            )

            for n in numbers:

                st.markdown(f"• {n}")

        else:

            st.warning(
                "No se detectaron números."
            )

# ==================================================
# DIARIO DE SEÑALES
# ==================================================

if page == "Diario de Señales":

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

            st.subheader(
                data["date"]
            )

            if "signals" in data:

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

if page == "Timeline":

    st.title("Timeline de Señales")

    files = sorted(
        glob.glob("signals/*.json")
    )

    if len(files) == 0:

        st.warning(
            "No hay señales guardadas."
        )

    else:

        timeline_data = []

        for file in files:

            with open(file, "r", encoding="utf-8") as f:

                data = json.load(f)

            total = len(data["signals"])

            timeline_data.append({

                "Fecha": data["date"],

                "Cantidad": total
            })

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

if page == "Insights IA":

    st.title("Insights IA")

    files = sorted(
        glob.glob("signals/*.json")
    )

    total_signals = 0

    pattern_count = {}

    for file in files:

        with open(file, "r", encoding="utf-8") as f:

            data = json.load(f)

        total_signals += len(
            data["signals"]
        )

        for item in data["signals"]:

            signal_type = item["type"]

            if signal_type in pattern_count:

                pattern_count[signal_type] += 1

            else:

                pattern_count[signal_type] = 1

    st.metric(
        "Total de Señales",
        total_signals
    )

    if len(pattern_count) > 0:

        dominant_pattern = max(
            pattern_count,
            key=pattern_count.get
        )

        st.metric(
            "Patrón Dominante",
            dominant_pattern
        )

        st.subheader(
            "Lectura General IA"
        )

        st.info(f"""

El patrón dominante registrado es:

{dominant_pattern}

La IA detecta persistencia de sincronías
y repetición estructural dentro de los
registros diarios.

""")

# ==================================================
# PREDICCIÓN NUMÉRICA
# ==================================================

if page == "Predicción Numérica":

    st.title("Predicción Numérica")

    st.markdown("""

Este módulo genera líneas numéricas basadas en:

• Señales registradas hoy  
• Frecuencias repetidas  
• Patrones dominantes  
• Horas espejo  
• Secuencias recurrentes

""")

    today = str(datetime.now().date())

    signal_file = f"signals/{today}.json"

    if os.path.exists(signal_file):

        with open(signal_file, "r", encoding="utf-8") as f:

            daily_data = json.load(f)

        all_numbers = []

        # ==========================================
        # EXTRAER NÚMEROS
        # ==========================================

        for item in daily_data["signals"]:

            signal = item["signal"]

            nums = re.findall(r'\d+', signal)

            for n in nums:

                for digit in n:

                    number = int(digit)

                    if number > 0:

                        all_numbers.append(number)

        # ==========================================
        # VALIDAR
        # ==========================================

        if len(all_numbers) == 0:

            st.warning(
                "No hay suficientes señales numéricas."
            )

        else:

            # ======================================
            # FRECUENCIAS
            # ======================================

            freq_map = {}

            for num in all_numbers:

                if num in freq_map:

                    freq_map[num] += 1

                else:

                    freq_map[num] = 1

            # ======================================
            # TABLA
            # ======================================

            st.subheader(
                "Frecuencias Detectadas"
            )

            freq_df = pd.DataFrame({

                "Número":
                list(freq_map.keys()),

                "Frecuencia":
                list(freq_map.values())

            })

            st.dataframe(
                freq_df,
                use_container_width=True
            )

            # ======================================
            # ORDENAR
            # ======================================

            sorted_numbers = sorted(

                freq_map,

                key=freq_map.get,

                reverse=True
            )

            dominant_number = sorted_numbers[0]

            # ======================================
            # MELATE NORMAL
            # ======================================

            st.subheader(
                "Línea Tipo Melate"
            )

            melate_numbers = []

            while len(melate_numbers) < 6:

                n = np.random.choice(
                    sorted_numbers
                )

                generated = int(

                    (
                        n *
                        np.random.randint(5, 12)
                    ) % 56

                ) + 1

                if generated not in melate_numbers:

                    melate_numbers.append(
                        generated
                    )

            melate_numbers.sort()

            st.success(f"""

{melate_numbers}

""")

            # ======================================
            # MELATE RETRO
            # ======================================

            st.subheader(
                "Línea Tipo Melate Retro"
            )

            retro_numbers = []

            while len(retro_numbers) < 6:

                n = np.random.choice(
                    sorted_numbers
                )

                generated = int(

                    (
                        n *
                        np.random.randint(2, 9)
                    ) % 39

                ) + 1

                if generated not in retro_numbers:

                    retro_numbers.append(
                        generated
                    )

            retro_numbers.sort()

            st.success(f"""

{retro_numbers}

""")

            # ======================================
            # POWERBALL
            # ======================================

            st.subheader(
                "Línea Tipo PowerBall"
            )

            power_numbers = []

            while len(power_numbers) < 5:

                n = np.random.choice(
                    sorted_numbers
                )

                generated = int(

                    (
                        n *
                        np.random.randint(3, 8)
                    ) % 69

                ) + 1

                if generated not in power_numbers:

                    power_numbers.append(
                        generated
                    )

            power_numbers.sort()

            power_special = np.random.randint(
                1,
                27
            )

            st.success(f"""

Números:
{power_numbers}

Power:
{power_special}

""")

            # ======================================
            # IA
            # ======================================

            st.subheader(
                "Lectura IA"
            )

            st.info(f"""

La frecuencia dominante detectada hoy
fue el número {dominant_number}.

Las líneas generadas utilizan:

• repetición numérica  
• concentración energética  
• patrones recurrentes  
• distribución de frecuencias  

Las combinaciones fueron construidas
a partir de las señales registradas
durante el día.

""")

    else:

        st.warning(
            "Aún no existen señales registradas hoy."
        )
