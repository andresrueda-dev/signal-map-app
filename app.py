# ========================================================
# SIGNALMAP IA - METAPATTERN ENGINE & INTEGRATED FRACTAL
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

# Importación del Motor Fractal desde tu carpeta de módulos
try:
    from modules.motor_fractal import MetaPatternFractal
except ImportError:
    # Respaldo en caliente por si el archivo no se ha movido de la raíz
    try:
        from motor_fractal import MetaPatternFractal
    except ImportError:
        # Clase interna de emergencia si no se detecta el módulo para evitar caída de la app
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
    page_title="SignalMap IA - MetaPattern Live",
    layout="wide",
    page_icon="🧠"
)

# =========================
# CUSTOM STYLE CSS
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
# LOCAL STORAGE INITIALIZATION
# =========================
if "local_signals" not in st.session_state:
    st.session_state.local_signals = []

if "user_id" not in st.session_state:
    st.session_state.user_id = "user_directo_hoy"

# Alerta estática de modo de conexión en sidebar
if firebase_active:
    st.sidebar.success("📡 Modo Híbrido: Guardando local y en Firebase")
else:
    st.sidebar.warning("⚠️ Modo Local Activo: Datos guardados en el navegador")

# Configuración Maestra de Sorteos
GAME_CONFIG = {
    "TRIS": {"min": 0, "max": 9, "cantidad": 5, "archivo": "data/historico_tris.csv"},
    "Melate": {"min": 1, "max": 56, "cantidad": 6, "archivo": "data/historico_melate.csv"},
    "Chispazo": {"min": 1, "max": 28, "cantidad": 5, "archivo": "data/historico_chispazo.csv"},
    "Powerball": {"min": 1, "max": 69, "cantidad": 5, "archivo": "data/historico_powerball.csv"},
    "Mega Millions": {"min": 1, "max": 70, "cantidad": 5, "archivo": "data/historico_megamillions.csv"},
    "Gana Gato": {"min": 1, "max": 5, "cantidad": 8, "archivo": "data/historico_ganagato.csv"}
}

# =========================
# CORE APP FUNCTIONS
# =========================
def cargar_datos_historicos(game):
    """Carga los miles de sorteos reales del CSV si existen, de lo contrario genera simulación"""
    ruta = GAME_CONFIG[game]["archivo"]
    if os.path.exists(ruta):
        try:
            df_real = pd.read_csv(ruta)
            return df_real
        except:
            pass
    # Respaldo si no encuentra el archivo para mantener la visualización activa
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
# 1. DIARIO DE SEÑALES
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

            st.session_state.local_signals.append(registro)
            st.success("✅ ¡Señal registrada localmente con éxito en la sesión!")

            if firebase_active:
                try:
                    db.child("signals").child(st.session_state.user_id).child(sorteo).push(registro)
                    st.info("📡 Copia de seguridad sincronizada en la nube de Firebase.")
                except:
                    st.warning("⚠️ Error en Firebase. Tus datos se mantienen a salvo en la tabla local.")
        else:
            st.error("Por favor introduce números válidos antes de guardar.")

# =========================
# 2. TIMELINE DE HOY
# =========================
elif menu == "📊 Timeline de Hoy":
    st.title("📊 Historial de Señales Capturadas Hoy")
    todas_las_sevales = list(st.session_state.local_signals)

    if firebase_active:
        try:
            for game in GAME_CONFIG.keys():
                registros = db.child("signals").child(st.session_state.user_id).child(game).get()
                if registros.each():
                    for r in registros.each():
                        data = r.val()
                        data["sorteo"] = game
                        if data not in todas_las_sevales: tutte_le_segnalazioni.append(data)
        except:
            pass

    if len(todas_las_sevales) > 0:
        df_timeline = pd.DataFrame(todas_las_sevales)
        st.dataframe(df_timeline, use_container_width=True)
        
        json_string = json.dumps(todas_las_sevales, indent=4)
        st.download_button(
            label="📥 Descargar Respaldo de Señales (JSON)",
            data=json_string,
            file_name=f"signals_respaldo_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    else:
        st.info("Aún no has registrado señales. Ve al menú 'Diario de Señales' para empezar.")

# =========================
# 3. DASHBOARD GLOBAL (CON MOTOR FRACTAL INTEGRADO)
# =========================
elif menu == "🏠 Dashboard Global":
    st.title("🧠 Matriz Global de Convergencia & Indexación Fractal")
    
    # Render de tus tarjetas estadísticas e históricos tradicionales
    resultados = []
    cols = st.columns(2)
    contador_col = 0

    for game in GAME_CONFIG.keys():
        df = cargar_datos_historicos(game)
        
        # Procesamiento estadístico seguro para evitar errores si viene de un CSV real
        col_analisis = "numero" if "numero" in df.columns else df.columns[1]
        freq = df[col_analisis].value_counts()
        
        dominante = int(freq.idxmax())
        persistencia = int(freq.max())
        sincronias = int(len(freq[freq > 5]))
        convergencia, icono = calcular_convergencia(persistencia, sincronias)

        with cols[contador_col]:
            st.markdown(f"""
            <div class="dashboard-card">
            <h3>{icono} {game}</h3>
            <p><b>Convergencia:</b> {convergencia} | <b>Dominante:</b> {dominante}</p>
            <p><b>Persistencia:</b> {persistencia} | <b>Sincronías:</b> {sincronias}</p>
            </div>
            """, unsafe_allow_html=True)
            
            fig = px.bar(x=freq.index, y=freq.values, color=freq.values, labels={'x': 'Número', 'y': 'Frecuencia'})
            fig.update_layout(template="plotly_dark", height=180, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)

        contador_col = 0 if contador_col >= 1 else contador_col + 1

    # --- NUEVO SUBMÓDULO INTEGRADO: MAPA DE DENSIDAD DE MANDELBROT ---
    st.markdown("---")
    st.subheader("🌌 Mapa Geométrico del Histórico vs Señales (Mandelbrot Space)")
    st.caption("Validación y análisis espacial de la frontera del caos mediante producto punto posicional.")

    motor_f = MetaPatternFractal()
    puntos_mapeados = []

    # Procesar señales guardadas hoy en la sesión
    if len(st.session_state.local_signals) > 0:
        for s in st.session_state.local_signals:
            if len(s["numeros"]) > 0:
                x, y = motor_f.transformar_secuencia(s["numeros"])
                iters = motor_f.calibrar_escape(x, y)
                puntos_mapeados.append({
                    "Identificador": f"Señal: {s['sorteo']}",
                    "Eje X": x,
                    "Eje Y": y,
                    "Iteraciones": iters,
                    "Capa": "Señal Entorno Actual"
                })

    # Cargar y procesar una muestra de los históricos reales para crear los clusters
    for game in GAME_CONFIG.keys():
        df_h = cargar_datos_historicos(game)
        # Extraemos una sub-muestra para no sobrecargar el renderizador gráfico
        muestras = df_h.head(15)
        for idx, row in muestras.iterrows():
            valores_fila = [val for val in row.values if str(val).isdigit()][:5]
            if len(valores_fila) > 0:
                x, y = motor_f.transformar_secuencia(valores_fila)
                iters = motor_f.calibrar_escape(x, y)
                puntos_mapeados.append({
                    "Identificador": f"Histórico: {game} (Fila {idx})",
                    "Eje X": x,
                    "Eje Y": y,
                    "Iteraciones": iters,
                    "Capa": f"Muestra Histórica {game}"
                })

    if len(puntos_mapeados) > 0:
        df_scatter = pd.DataFrame(puntos_mapeados)
        
        fig_fractal = px.scatter(
            df_scatter,
            x="Eje X",
            y="Eje Y",
            color="Capa",
            size="Iteraciones",
            hover_data=["Identificador", "Iteraciones"],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_fractal.update_layout(
            template="plotly_dark",
            xaxis=dict(range=[-2.1, 0.6], title="Plano Real (X)"),
            yaxis=dict(range=[-1.3, 1.3], title="Plano Imaginario (Y)"),
            height=550
        )
        st.plotly_chart(fig_fractal, use_container_width=True)
    else:
        st.info("Introduce datos en el Diario de Señales o verifica tus archivos CSV para pintar el mapa fractal.")

# =========================
# 4. SORTEO SUGERIDO (CORREGIDO DE NP.INT64)
# =========================
elif menu == "🎯 Sorteo Número Sugerido":
    st.title("🎯 Sorteo Número Sugerido e Ingeniería de Dualidades")
    
    for game in GAME_CONFIG.keys():
        st.markdown(f"## 🎲 Matrices de Resonancia: {game}")
        
        todos = []
        for s in st.session_state.local_signals:
            if s["sorteo"] == game:
                todos.extend(s["numeros"])

        if len(todos) == 0:
            todos = list(np.random.randint(GAME_CONFIG[game]["min"], GAME_CONFIG[game]["max"] + 1, 120))

        contador = Counter(todos)
        top = contador.most_common(GAME_CONFIG[game]["cantidad"])
        
        # CORRECCIÓN EXPLICITA: Forzar casteo a enteros puros de Python para erradicar el bug de np.int64
        sugeridos = [int(x[0]) for x in top]
        duales_espejo = [espejo(n) for n in sugeridos]

        st.success(f"🎯 Sugerencia IA Configurada: {sugeridos}")
        st.info(f"🪞 Dualidad Espejo Reflejada: {duales_espejo}")

# =========================
# 5. MOTOR ESPEJO
# =========================
elif menu == "🪞 Motor Espejo":
    st.title("🪞 Motor Espejo Estructural")
    numero = st.text_input("Introduce combinación o secuencia numérica:")
    if numero:
        st.success(f"🪞 Espejo reflejado: {espejo(numero)}")
