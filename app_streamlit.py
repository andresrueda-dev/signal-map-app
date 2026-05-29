import streamlit as st
import pandas as pd
import plotly.express as px
from motor_fractal import MetaPatternFractal

st.set_page_config(page_title="MetaPattern Engine - Fractal Module", layout="wide")

st.title("🧮 Módulo de Calibración Fractal (Mandelbrot Index)")
st.caption("Filtro geométrico espacial para secuencias numéricas vectorizadas.")

# Inicializar motor
motor = MetaPatternFractal()

# Sidebar: Ingreso de datos manuales para probar en caliente
st.sidebar.header("Calibrador Rápido")
entrada_usuario = st.sidebar.text_input("Introduce una secuencia separada por comas:", "7, 1, 2, 2, 11, 11")

if entrada_usuario:
    try:
        secuencia_test = [int(x.strip()) for x in entrada_usuario.split(",")]
        x_u, y_u = motor.transformar_secuencia(secuencia_test)
        iter_u = motor.calibrar_escape(x_u, y_u)
        clase_u, desc_u = motor.clasificar_metrica(iter_u)
        
        st.sidebar.success(f"**Coordenada:** ({x_u:.4f}, {y_u:.4f})")
        st.sidebar.metric(label="Iteraciones de Escape", value=iter_u)
        st.sidebar.info(f"**Clasificación:** {desc_u}")
    except ValueError:
        st.sidebar.error("Por favor, ingresa solo números válidos separados por comas.")

# --- SECCIÓN DE INVESTIGACIÓN DE CLUSTERS (LO QUE SUGIRIÓ CHATGPT) ---
st.subheader("📊 Análisis de Densidad y Agrupamientos (Clusters)")

# Base de datos simulada expandida para ver el mapa visual
@st.cache_data
def cargar_datos_ejemplo():
    # Simulamos 50 sorteos históricos ya procesados por el motor
    np.random.seed(42)
    datos_muchos = []
    for i in range(100):
        # Generar secuencias aleatorias imitando sorteos
        seq = list(np.random.randint(1, 56, size=6))
        x, y = motor.transformar_secuencia(seq)
        iters = motor.calibrar_escape(x, y)
        clase, _ = motor.clasificar_metrica(iters)
        datos_muchos.append({
            "Sorteo_ID": f"S-{i+1000}",
            "X": x,
            "Y": y,
            "Iteraciones": iters,
            "Zona": clase
        })
    return pd.DataFrame(datos_muchos)

df_mapa = cargar_datos_ejemplo()

# Añadir el punto del usuario al mapa si existe
if entrada_usuario:
    df_usuario = pd.DataFrame([{"Sorteo_ID": "INPUT_ACTUAL", "X": x_u, "Y": y_u, "Iteraciones": iter_u, "Zona": "INPUT_ACTUAL"}])
    df_mapa = pd.concat([df_mapa, df_usuario], ignore_index=True)

# Renderizar Gráfico con Plotly Express
fig = px.scatter(
    df_mapa, 
    x="X", 
    y="Y", 
    color="Zona",
    size="Iteraciones",
    hover_data=["Sorteo_ID", "Iteraciones"],
    color_discrete_map={
        "ESCAPE_RAPIDO": "#E74C3C",
        "TRANSICION_BAJA": "#F39C12",
        "TRANSICION_ALTA": "#3498DB",
        "INTERIOR_MANDELBROT": "#2C3E50",
        "INPUT_ACTUAL": "#2ECC71" # Verde brillante para resaltar tu jugada o secuencia actual
    },
    title="Espacio Geométrico del Histórico de Datos"
)

fig.update_layout(
    template="plotly_dark",
    xaxis=dict(range=[-2.1, 0.6]),
    yaxis=dict(range=[-1.3, 1.3]),
    width=900,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(df_mapa)
