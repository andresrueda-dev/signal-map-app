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
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
from PIL import Image
from datetime import datetime

# ==================================================
# FIREBASE INIT
# ==================================================

if not firebase_admin._apps:

    import json

firebase_secret = json.loads(
    st.secrets["firebase"]
)

cred = credentials.Certificate(
    firebase_secret
)

    firebase_admin.initialize_app(cred)

db = firestore.client()

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

input{

    border-radius:10px !important;
}

</style>

""", unsafe_allow_html=True)

# ==================================================
# CREAR CARPETA
# ==================================================

os.makedirs("signals", exist_ok=True)

# ==================================================
# SESSION STATE
# ==================================================

if "logged" not in st.session_state:

    st.session_state["logged"] = False

if "user" not in st.session_state:

    st.session_state["user"] = ""

# ==================================================
# LOGIN SCREEN
# ==================================================

if st.session_state["logged"] == False:

    st.title("🌌 SIGNAL MAP AI")

    st.subheader(
        "Cloud Signal Network"
    )

    st.markdown("---")

    login_tab, register_tab, recovery_tab = st.tabs(

        [

            "🔐 Login",

            "🛰️ Register",

            "🔑 Recover Password"
        ]
    )

    # ==================================================
    # LOGIN
    # ==================================================

    with login_tab:

        login_email = st.text_input(
            "Correo",
            key="login_email"
        )

        login_password = st.text_input(
            "Contraseña",
            type="password",
            key="login_password"
        )

        login_button = st.button(
            "Ingresar"
        )

        if login_button:

            if login_email != "":

                st.session_state["logged"] = True

                st.session_state["user"] = login_email

                st.success(
                    "Access Granted"
                )

                st.rerun()

    # ==================================================
    # REGISTER
    # ==================================================

    with register_tab:

        register_email = st.text_input(
            "Nuevo correo",
            key="register_email"
        )

        register_password = st.text_input(
            "Nueva contraseña",
            type="password",
            key="register_password"
        )

        register_button = st.button(
            "Crear Cuenta"
        )

        if register_button:

            if register_email != "":

                db.collection(
                    "users"
                ).add({

                    "email":
                    register_email,

                    "created":
                    str(datetime.now())
                })

                st.success(
                    "Cuenta creada."
                )

    # ==================================================
    # RECOVER PASSWORD
    # ==================================================

    with recovery_tab:

        recovery_email = st.text_input(
            "Correo de recuperación"
        )

        recovery_button = st.button(
            "Recuperar"
        )

        if recovery_button:

            st.success(
                f"Recovery link enviado a {recovery_email}"
            )

    st.stop()

# ==================================================
# ROLE SYSTEM
# ==================================================

MASTER_USERS = [

    "TU_CORREO@gmail.com",

    "admin@gmail.com"
]

if st.session_state["user"] in MASTER_USERS:

    role = "MASTER NODE"

else:

    role = "USER"

# ==================================================
# SIDEBAR VISUAL SYSTEM
# ==================================================

st.sidebar.success(

    f"👤 {st.session_state['user']}"
)

st.sidebar.info(

    f"🛰️ {role}"
)

logout = st.sidebar.button(
    "Cerrar Sesión"
)

if logout:

    st.session_state["logged"] = False

    st.rerun()

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

        "📡 Pattern Evolution",

        "🛰️ Master Console"
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
    "Signal Map AI v3.0"
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

# ==================================================
# REGISTRO COMPLETO DE SEÑAL
# ==================================================

if page == "⚡ Registro Rápido":

    st.title("🌌 Registro Completo de Señal")

    st.markdown("""

Sistema contextual de captura.

Puedes registrar:

• señales rápidas  
• sincronías  
• contexto emocional  
• entorno de aparición  
• resonancia  
• dispositivos  
• observaciones  

""")

    # ==================================================
    # SEÑAL PRINCIPAL
    # ==================================================

    signal_input = st.text_input(

        "⚡ Señal Detectada",

        placeholder="Ejemplo: 11:11"
    )

    # ==================================================
    # ENTORNO
    # ==================================================

    environment = st.selectbox(

        "🌎 Tipo de Entorno",

        [

            "📱 Digital",

            "🌆 Exterior",

            "👥 Social",

            "🌙 Personal",

            "🏫 Escuela",

            "🚗 Transporte",

            "🏠 Casa",

            "🧠 Mental",

            "🔮 Otro"
        ]
    )

    # ==================================================
    # ORIGEN
    # ==================================================

    origin = st.selectbox(

        "📡 Origen de la Señal",

        [

            "Celular",

            "Redes Sociales",

            "Computadora",

            "Televisión",

            "Videojuego",

            "Chat IA",

            "Mensaje",

            "Notificación",

            "Anuncio",

            "Placa de Auto",

            "Reloj",

            "TikTok",

            "YouTube",

            "Spotify",

            "Persona",

            "Conversación",

            "Sueño",

            "Pensamiento",

            "Escuela",

            "Calle",

            "Otro"
        ]
    )

    # ==================================================
    # INTENSIDAD
    # ==================================================

    intensity = st.slider(

        "⚡ Intensidad Percibida",

        1,

        10,

        5
    )

    # ==================================================
    # ESTADO EMOCIONAL
    # ==================================================

    emotional_state = st.selectbox(

        "🧠 Estado Emocional",

        [

            "Tranquilo",

            "Ansioso",

            "Motivado",

            "Inspirado",

            "Cansado",

            "Emocionado",

            "Confundido",

            "Curioso",

            "Neutral"
        ]
    )

    # ==================================================
    # UBICACIÓN
    # ==================================================

    location = st.selectbox(

        "📍 Ubicación",

        [

            "Casa",

            "Escuela",

            "Trabajo",

            "Calle",

            "Transporte",

            "Internet",

            "Habitación",

            "Otro"
        ]
    )

    # ==================================================
    # REPETICIÓN
    # ==================================================

    repeated_signal = st.selectbox(

        "🔁 ¿La viste varias veces?",

        [

            "Sí",

            "No"
        ]
    )

    # ==================================================
    # TESTIGOS
    # ==================================================

    witnesses = st.selectbox(

        "👁️ ¿Alguien más la vio?",

        [

            "Sí",

            "No",

            "No estoy seguro"
        ]
    )

    # ==================================================
    # CLIMA
    # ==================================================

    weather_context = st.selectbox(

        "🌦️ Contexto Ambiental",

        [

            "Día",

            "Noche",

            "Lluvia",

            "Silencio",

            "Música",

            "Tráfico",

            "Calma",

            "Ruido",

            "Otro"
        ]
    )

    # ==================================================
    # NOTAS
    # ==================================================

    personal_note = st.text_area(

        "📝 Nota Personal",

        placeholder="¿Qué ocurrió o qué sentiste?"
    )

    # ==================================================
    # GUARDAR
    # ==================================================

    if st.button("💾 Guardar Señal"):

        if signal_input != "":

            signal_type = classify_signal(
                signal_input
            )

            signal_data = {

                "user":
                st.session_state["user"],

                "signal":
                signal_input,

                "type":
                signal_type,

                "environment":
                environment,

                "origin":
                origin,

                "intensity":
                intensity,

                "emotion":
                emotional_state,

                "location":
                location,

                "repeated":
                repeated_signal,

                "witnesses":
                witnesses,

                "weather":
                weather_context,

                "note":
                personal_note,

                "timestamp":
                str(datetime.now())
            }

            # ==========================================
            # FIREBASE SAVE
            # ==========================================

            db.collection(
                "signals"
            ).add(signal_data)

            st.success(
                "🌌 Señal registrada correctamente."
            )

            st.info(f"""

⚡ Señal:
{signal_input}

📡 Origen:
{origin}

🌎 Entorno:
{environment}

⚡ Intensidad:
{intensity}/10

🧠 Estado:
{emotional_state}

📍 Ubicación:
{location}

""")

# ==================================================
# CONSTELACIÓN DEL DÍA
# ==================================================

if page == "🌌 Constelación del Día":

    st.title("Constelación del Día")

    docs = db.collection(
        "signals"
    ).where(

        "user",

        "==",

        st.session_state["user"]

    ).stream()

    signals = []

    for doc in docs:

        data = doc.to_dict()

        signals.append(
            data["signal"]
        )

    if len(signals) > 0:

        fig = go.Figure()

        angles = np.linspace(
            0,
            2*np.pi,
            len(signals),
            endpoint=False
        )

        radius = np.random.randint(
            1,
            10,
            len(signals)
        )

        x = radius * np.cos(angles)

        y = radius * np.sin(angles)

        fig.add_trace(

            go.Scatter(

                x=x,

                y=y,

                mode="markers+text",

                text=signals,

                marker=dict(

                    size=20,

                    color=radius,

                    colorscale="Purples"
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

    docs = db.collection(
        "signals"
    ).where(

        "user",

        "==",

        st.session_state["user"]

    ).stream()

    data_list = []

    for doc in docs:

        data_list.append(
            doc.to_dict()
        )

    if len(data_list) > 0:

        df = pd.DataFrame(data_list)

        st.dataframe(
            df,
            use_container_width=True
        )

# ==================================================
# TIMELINE
# ==================================================

if page == "📈 Timeline":

    st.title("Timeline de Señales")

    docs = db.collection(
        "signals"
    ).where(

        "user",

        "==",

        st.session_state["user"]

    ).stream()

    timeline = []

    for doc in docs:

        timeline.append(
            doc.to_dict()
        )

    if len(timeline) > 0:

        df = pd.DataFrame(
            timeline
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

    docs = db.collection(
        "signals"
    ).stream()

    frequency_map = {}

    for doc in docs:

        data = doc.to_dict()

        nums = re.findall(
            r'\d',
            data["signal"]
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

# ==================================================
# MASTER CONSOLE
# ==================================================

if page == "🛰️ Master Console":

    if role != "MASTER NODE":

        st.error(
            "Access Denied"
        )

    else:

        st.title(
            "🛰️ MASTER CONSOLE"
        )

        st.success(
            "Master Node Connected"
        )

        docs = db.collection(
            "signals"
        ).stream()

        all_data = []

        for doc in docs:

            all_data.append(
                doc.to_dict()
            )

        if len(all_data) > 0:

            df = pd.DataFrame(
                all_data
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            st.metric(
                "Global Signals",
                len(df)
            )
