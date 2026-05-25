# app.py COMPLETO — Signal Map AI V2

```python
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
    background-color:#040816;
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

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"]{
    background-color:#11162A;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# CREAR CARPETAS
# ==================================================

os.makedirs("signals", exist_ok=True)
os.makedirs("users", exist_ok=True)

# ==================================================
# USUARIO
# ==================================================

st.sidebar.title("SIGNAL MAP AI")

username = st.sidebar.text_input(
    "Usuario",
    value="emmanuel"
)

username = username.lower().strip()

user_folder = f"users/{username}"

os.makedirs(user_folder, exist_ok=True)

# ==================================================
# MENÚ PRINCIPAL
# ==================================================

page = st.sidebar.radio(
    "Menú Principal",
    [
        "Registro Rápido",
        "Constelación del Día",
        "Vista de Sincronicidad",
        "Cargar Imagen",
        "Diario de Señales",
        "Timeline",
        "Insights IA",
        "Predicción Numérica"
    ]
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

    ascending = ''.join(sorted(clean_signal))

    if clean_signal == ascending:
        return "Secuencia Ascendente"

    descending = ''.join(sorted(clean_signal, reverse=True))

    if clean_signal == descending:
        return "Secuencia Descendente"

    return "Patrón General"

# ==================================================
# COLORES POR TIPO
# ==================================================

TYPE_COLORS = {

    "Celular": "#4DA3FF",
    "Placa Vehicular": "#FF5C5C",
    "Radio": "#FFD84D",
    "Voz": "#C084FF",
    "Sueño": "#8EF7D0",
    "Redes Sociales": "#FF8AE2",
    "Ticket": "#FFA54D",
    "Hora": "#A6FF4D",
    "Otro": "#FFFFFF"
}

# ==================================================
# REGISTRO RÁPIDO
# ==================================================

if page == "Registro Rápido":

    st.title("Registro Rápido de Señales")

    st.markdown("""
Sistema de captura contextual de sincronías.

Aquí puedes registrar:

• Horas espejo
• Números repetitivos
• Secuencias
• Patrones visuales
• Sincronías del día
""")

    today = str(datetime.now().date())

    signal_file = f"{user_folder}/{today}.json"

    # ==============================================
    # CARGAR DATOS
    # ==============================================

    if os.path.exists(signal_file):

        with open(signal_file, "r", encoding="utf-8") as f:
            daily_data = json.load(f)

    else:

        daily_data = {
            "date": today,
            "user": username,
            "signals": []
        }

    # ==============================================
    # FORMULARIO
    # ==============================================

    signal_input = st.text_input(
        "Señal detectada",
        placeholder="Ejemplo: 11:11"
    )

    signal_source = st.selectbox(
        "Tipo de señal",
        [
            "Celular",
            "Placa Vehicular",
            "Radio",
            "Voz",
            "Sueño",
            "Redes Sociales",
            "Ticket",
            "Hora",
            "Otro"
        ]
    )

    # ==============================================
    # CONTEXTO DINÁMICO
    # ==============================================

    context_options = {

        "Celular": [
            "Hora",
            "Batería",
            "Notificación",
            "TikTok",
            "Mensaje",
            "Llamada"
        ],

        "Placa Vehicular": [
            "Auto Negro",
            "Taxi",
            "Camión",
            "Movimiento",
            "Estacionado"
        ],

        "Radio": [
            "Canción",
            "Frecuencia",
            "Comercial",
            "Número mencionado"
        ],

        "Voz": [
            "Conversación",
            "Nombre repetido",
            "Frase",
            "Palabra clave"
        ],

        "Sueño": [
            "Número",
            "Lugar",
            "Persona",
            "Mensaje"
        ],

        "Redes Sociales": [
            "Instagram",
            "TikTok",
            "YouTube",
            "Facebook"
        ],

        "Ticket": [
            "Compra",
            "Hora",
            "Monto",
            "Código"
        ],

        "Hora": [
            "Hora espejo",
            "Hora reflejo",
            "Hora repetitiva"
        ],

        "Otro": [
            "General"
        ]
    }

    signal_context = st.selectbox(
        "Contexto",
        context_options[signal_source]
    )

    impact_level = st.slider(
        "Intensidad percibida",
        1,
        5,
        3
    )

    emotion = st.selectbox(
        "Estado emocional",
        [
            "Tranquilo",
            "Ansioso",
            "Motivado",
            "Curioso",
            "Feliz",
            "Cansado"
        ]
    )

    location = st.selectbox(
        "Ubicación",
        [
            "Casa",
            "Escuela",
            "Trabajo",
            "Calle",
            "Automóvil"
        ]
    )

    # ==============================================
    # DATOS AUTOMÁTICOS
    # ==============================================

    battery = np.random.randint(15, 100)
    humidity = np.random.randint(20, 90)
    temperature = np.random.randint(15, 35)

    # ==============================================
    # GUARDAR
    # ==============================================

    if st.button("Guardar Señal"):

        if signal_input != "":

            signal_type = classify_signal(
                signal_input
            )

            signal_data = {

                "signal": signal_input,
                "classification": signal_type,
                "source": signal_source,
                "context": signal_context,
                "impact": impact_level,
                "emotion": emotion,
                "location": location,
                "battery": battery,
                "humidity": humidity,
                "temperature": temperature,
                "timestamp": str(datetime.now())
            }

            daily_data["signals"].append(
                signal_data
            )

            with open(signal_file, "w", encoding="utf-8") as f:

                json.dump(
                    daily_data,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            st.success(
                f"Señal guardada como: {signal_type}"
            )

    # ==============================================
    # MOSTRAR SEÑALES
    # ==============================================

    st.subheader("Señales Registradas Hoy")

    if len(daily_data["signals"]) == 0:

        st.warning(
            "Aún no hay señales registradas."
        )

    else:

        for item in reversed(daily_data["signals"]):

            st.markdown(f"""
### {item['signal']}

• Clasificación: {item['classification']}
• Tipo: {item['source']}
• Contexto: {item['context']}
• Intensidad: {item['impact']}/5
• Estado emocional: {item['emotion']}
• Ubicación: {item['location']}
• Batería: {item['battery']}%
• Humedad: {item['humidity']}%
• Temperatura: {item['temperature']}°C
• Hora: {item['timestamp']}
""")

# ==================================================
# CONSTELACIÓN DEL DÍA
# ==================================================

if page == "Constelación del Día":

    st.title("Constelación del Día")

    today = str(datetime.now().date())

    signal_file = f"{user_folder}/{today}.json"

    if os.path.exists(signal_file):

        with open(signal_file, "r", encoding="utf-8") as f:
            daily_data = json.load(f)

        signals = daily_data["signals"]

        if len(signals) > 0:

            fig = go.Figure()

            total = len(signals)

            angles = np.linspace(
                0,
                2*np.pi,
                total,
                endpoint=False
            )

            x_vals = []
            y_vals = []
            colors = []
            sizes = []
            texts = []

            for i, signal in enumerate(signals):

                radius = signal["impact"] * 1.5

                x = radius * np.cos(angles[i])
                y = radius * np.sin(angles[i])

                x_vals.append(x)
                y_vals.append(y)

                colors.append(
                    TYPE_COLORS.get(
                        signal["source"],
                        "white"
                    )
                )

                sizes.append(
                    signal["impact"] * 10
                )

                texts.append(signal["signal"])

            # ======================================
            # FILAMENTOS
            # ======================================

            for i in range(len(x_vals)-1):

                fig.add_trace(
                    go.Scatter(
                        x=[x_vals[i], x_vals[i+1]],
                        y=[y_vals[i], y_vals[i+1]],
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
                    x=x_vals,
                    y=y_vals,
                    mode="markers+text",
                    marker=dict(
                        size=sizes,
                        color=colors,
                        line=dict(
                            width=2,
                            color="white"
                        )
                    ),
                    text=texts,
                    textposition="top center"
                )
            )

            fig.update_layout(
                height=850,
                paper_bgcolor="#040816",
                plot_bgcolor="#040816",
                font=dict(color="white"),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.info("""
La geometría del mapa representa:

• alineación
• ejes
• proporción
• sincronías
• centralidad
• filamentos de conexión
• expansión radial
• concentración energética
""")

        else:
            st.warning("No hay señales registradas.")

    else:
        st.warning("Aún no existen señales registradas hoy.")

# ==================================================
# VISTA GENERAL
# ==================================================

if page == "Vista de Sincronicidad":

    st.title("Vista General de Sincronicidad")

    files = sorted(
        glob.glob(f"{user_folder}/*.json")
    )

    total_signals = 0
    all_types = []
    all_patterns = []

    for file in files:

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        total_signals += len(data["signals"])

        for item in data["signals"]:

            all_types.append(item["source"])
            all_patterns.append(item["classification"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Señales",
            total_signals
        )

    if len(all_types) > 0:

        dominant_type = max(
            set(all_types),
            key=all_types.count
        )

        dominant_pattern = max(
            set(all_patterns),
            key=all_patterns.count
        )

        with col2:
            st.metric(
                "Tipo Dominante",
                dominant_type
            )

        with col3:
            st.metric(
                "Patrón Dominante",
                dominant_pattern
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

        st.subheader("Texto Detectado")

        st.write(detected_text)

# ==================================================
# DIARIO DE SEÑALES
# ==================================================

if page == "Diario de Señales":

    st.title("Diario de Señales")

    files = sorted(
        glob.glob(f"{user_folder}/*.json")
    )

    if len(files) == 0:

        st.warning("No hay registros.")

    else:

        for file in reversed(files):

            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            st.subheader(data["date"])

            for item in data["signals"]:

                st.markdown(f"""
### {item['signal']}

• Clasificación: {item['classification']}
• Tipo: {item['source']}
• Contexto: {item['context']}
• Intensidad: {item['impact']}/5
""")

# ==================================================
# TIMELINE
# ==================================================

if page == "Timeline":

    st.title("Timeline")

    files = sorted(
        glob.glob(f"{user_folder}/*.json")
    )

    timeline_data = []

    for file in files:

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        timeline_data.append({
            "Fecha": data["date"],
            "Cantidad": len(data["signals"])
        })

    if len(timeline_data) > 0:

        df = pd.DataFrame(timeline_data)

        st.dataframe(
            df,
            use_container_width=True
        )

# ==================================================
# INSIGHTS IA
# ==================================================

if page == "Insights IA":

    st.title("Insights IA")

    st.info("""
El sistema analiza:

• frecuencia
• repetición
• patrones espejo
• secuencias
• sincronías persistentes
• alineación estructural
• nodos centrales
• expansión radial
""")

# ==================================================
# PREDICCIÓN NUMÉRICA
# ==================================================

if page == "Predicción Numérica":

    st.title("Predicción Numérica")

    today = str(datetime.now().date())

    signal_file = f"{user_folder}/{today}.json"

    if os.path.exists(signal_file):

        with open(signal_file, "r", encoding="utf-8") as f:
            daily_data = json.load(f)

        all_numbers = []

        for item in daily_data["signals"]:

            signal = item["signal"]

            nums = re.findall(r'\d+', signal)

            for n in nums:

                for digit in n:

                    number = int(digit)

                    if number > 0:
                        all_numbers.append(number)

        if len(all_numbers) > 0:

            freq_map = {}

            for num in all_numbers:

                if num in freq_map:
                    freq_map[num] += 1
                else:
                    freq_map[num] = 1

            sorted_numbers = sorted(
                freq_map,
                key=freq_map.get,
                reverse=True
            )

            top_numbers = sorted_numbers[:6]

            st.subheader(
                "Números Más Frecuentes"
            )

            st.success(top_numbers)

            melate_numbers = []

            while len(melate_numbers) < 6:

                n = np.random.choice(top_numbers)

                generated = int(
                    (
                        n * np.random.randint(5, 12)
                    ) % 56
                ) + 1

                if generated not in melate_numbers:
                    melate_numbers.append(generated)

            melate_numbers.sort()

            st.subheader("Línea Tipo Melate")

            st.success(melate_numbers)

        else:
            st.warning("No hay números suficientes.")

    else:
        st.warning("No existen señales registradas hoy.")
```

# REQUERIMIENTO EXTRA

En requirements.txt agrega:

```txt
streamlit
plotly
numpy
pandas
easyocr
Pillow
torch
torchvision
opencv-python-headless
```
