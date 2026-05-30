import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import datetime
import pytz
import os
from collections import deque
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# =====================================================================
# INICIALIZACIÓN EN CACHÉ DEL MOTOR DE VISIÓN (EASYOCR COLD RAM)
# =====================================================================
@st.cache_resource
def inicializar_lector_ocr():
    try:
        import easyocr
        return easyocr.Reader(['es', 'en'], gpu=False, download_enabled=True)
    except Exception as e:
        return None

reader = inicializar_lector_ocr()

# =====================================================================
# 0. CONTROL DE PÁGINA E INYECCIÓN DE DISEÑO VISUAL AVANZADO (CSS)
# =====================================================================
st.set_page_config(page_title="SignalMap AI — MetaPattern Engine", page_icon="📡", layout="wide")

st.markdown("""
    <style>
        .reportview-container { background: #000000 !important; }
        .stApp { background-color: #000000; }
        .stTabs [data-baseweb="tab-list"] { gap: 14px; background-color: #000000; padding: 8px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #0a0e14;
            border: 1px solid #1f242c;
            border-radius: 6px;
            padding: 12px 24px;
            color: #8b949e;
            font-family: 'Courier New', monospace;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover { color: #f72585; border-color: #f72585; }
        .stTabs [aria-selected="true"] {
            background-color: #0d1117 !important;
            border: 1px solid #f72585 !important;
            box-shadow: 0px 0px 10px rgba(247, 37, 133, 0.3);
            color: #ffffff !important;
        }
        div[data-testid="stMetricValue"] { font-family: 'Courier New', monospace; font-weight: bold; color: #00f5d4; }
        div[data-testid="stMetricLabel"] { font-family: 'Arial', sans-serif; color: #adbac7; }
        .cyber-box {
            background-color: #0d1117;
            border: 1px solid #21262d;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "status_servidor" not in st.session_state:
    st.session_state.status_servidor = "SISTEMA PROTEGIDO"
if "ultima_conexion" not in st.session_state:
    st.session_state.ultima_conexion = "N/A"

def login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("<h2 style='text-align: center; color:#ffffff; font-family:monospace;'>🔮 MetaPattern Engine</h2>", unsafe_allow_html=True)
        with st.form("Formulario de Entrada Segura"):
            usuario = st.text_input("Identificador de Usuario", placeholder="Andrew...")
            password = st.text_input("Código de Validación", type="password", placeholder="••••")
            if st.form_submit_button("Desbloquear Matriz 🔓", use_container_width=True):
                try:
                    user_ok = st.secrets["credentials"]["username"]
                    pass_ok = st.secrets["credentials"]["password"]
                except:
                    user_ok = "andrew"
                    pass_ok = "7122"
                if usuario.lower() == user_ok and password == pass_ok:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("❌ Código incorrecto.")

if not st.session_state.autenticado:
    login()
    st.stop()

# =====================================================================
# 1. PERSISTENCIA EN CSV Y CATÁLOGO TOTAL DE JUEGOS DEL DÍA
# =====================================================================
DB_FILE = "historial_calibrado.csv"

sorteos_lista = [
    "TRIS", "CHISPAZO", "MELATE", "REVANCHA", 
    "REVANCHITA", "MELATE RETRO", "SORTEO MAYOR", 
    "SORTEO SUPERIOR", "SORTEO ZODIACO", "SORTEO ESPECIAL"
]

def guardar_nodo_en_csv(nodo, sorteo_nombre):
    nodo_str = ",".join(map(str, nodo))
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(DB_FILE):
        df_existente = pd.read_csv(DB_FILE)
        df_sorteo = df_existente[df_existente['Sorteo'] == sorteo_nombre]
        if nodo_str in df_sorteo['Combinacion'].values:
            return False 
    nuevo_registro = pd.DataFrame([[fecha_hoy, sorteo_nombre, nodo_str]], columns=['Fecha', 'Sorteo', 'Combinacion'])
    if os.path.exists(DB_FILE):
        nuevo_registro.to_csv(DB_FILE, mode='a', header=False, index=False)
    else:
        nuevo_registro.to_csv(DB_FILE, index=False)
    return True

def cargar_nodos_desde_csv():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            nodos_recuperados, tipos_sorteo = [], []
            for idx, row in df.tail(500).iterrows():
                nodos_recuperados.append([int(x) for x in str(row['Combinacion']).split(',')])
                tipos_sorteo.append(str(row['Sorteo']))
            if len(nodos_recuperados) > 0: return nodos_recuperados, tipos_sorteo
        except: pass
    
    base_nodos, base_tipos = [], []
    for i in range(500):
        secuencia = [int((np.sin(i * 0.05 + j) * 7) + (np.cos(i * 0.13 + j) * 6) + 14) for j in range(5)]
        base_nodos.append(secuencia)
        base_tipos.append(sorteos_lista[i % len(sorteos_lista)])
    return base_nodos, base_tipos

# =====================================================================
# 2. IA VISION SCANNER UNIVERSAL (EASYOCR MULTI-ESTRUCTURA)
# =====================================================================
def escanear_lineas_easyocr(imagen_pil, tipo_sorteo):
    if reader is None: return [False, "Lector EasyOCR no inicializado."]
    img_array = np.array(imagen_pil.convert('RGB'))
    resultados_ocr = reader.readtext(img_array, detail=0)
    lineas_encontradas = []
    
    for texto in resultados_ocr:
        numeros = [int(n) for n in re.findall(r'\b\d+\b', texto)]
        
        if tipo_sorteo in ["CHISPAZO", "MELATE", "REVANCHA", "REVANCHITA", "MELATE RETRO"]:
            longitud_esperada = 5 if tipo_sorteo == "CHISPAZO" else 6
            limite_superior = 28 if tipo_sorteo == "CHISPAZO" else 56
            if len(numeros) == longitud_esperada:
                if all(1 <= n <= limite_superior for n in numeros):
                    lineas_encontradas.append(sorted(numeros))
        elif tipo_sorteo == "TRIS" and len(numeros) == 5:
            if all(0 <= n <= 9 for n in numeros): 
                lineas_encontradas.append(numeros)
        elif "SORTEO" in tipo_sorteo or tipo_sorteo in ["MAYOR", "SUPERIOR", "ZODIACO", "ESPECIAL"]:
            nums_largos = re.findall(r'\b\d{5,6}\b', texto)
            for n_l in nums_largos: 
                lineas_encontradas.append([int(d) for d in str(n_l)])
                
    if len(lineas_encontradas) > 0: return [True, lineas_encontradas]
    return [False, "No se detectó el formato. Intenta otra toma."]

# =====================================================================
# 3. MOTORES MATEMÁTICOS FRACTALES (GEOMETRÍA INVARIANTE)
# =====================================================================
def calcular_coordenadas_fractales(nodos_matriz, lista_tipos):
    puntos_x, puntos_y, iteraciones_escape, raw_nodos = [], [], [], []
    for nodo in nodos_matriz:
        if not nodo: nodo = [0]
        pesos = np.arange(1, len(nodo) + 1)
        hash_base = np.dot(nodo, pesos)
        
        hash_x = np.sin(hash_base * 0.02) * 1.3
        hash_y = np.cos(hash_base * 0.02) * 1.3
        
        c = complex(hash_x, hash_y)
        z = 0j
        iteracion = 0
        while abs(z) <= 2.0 and iteracion < 250:
            z = z**2 + c
            iteracion += 1
        puntos_x.append(hash_x)
        puntos_y.append(hash_y)
        iteraciones_escape.append(iteracion)
        raw_nodos.append(", ".join(map(str, nodo)))
        
    df = pd.DataFrame({
        'Eje_X': puntos_x, 'Eje_Y': puntos_y, 
        'Iteraciones': iteraciones_escape, 'Vector_Boleto': raw_nodos, 
        'Sorteo_Tipo': lista_tipos, 'Tamaño': [7]*len(puntos_x)
    })
    condiciones = [(df['Iteraciones'] <= 50), (df['Iteraciones'] > 50) & (df['Iteraciones'] <= 150), (df['Iteraciones'] > 150) & (df['Iteraciones'] < 250), (df['Iteraciones'] == 250)]
    df['Clasificación'] = np.select(condiciones, ['Escape Rápido', 'Transición', 'Estable', 'Interior Mandelbrot'], default='Transición')
    
    centro_x, centro_y = df['Eje_X'].mean(), df['Eje_Y'].mean()
    df['Distancia_Centro'] = np.sqrt((df['Eje_X'] - centro_x)**2 + (df['Eje_Y'] - centro_y)**2)
    df['Resonancia_Score'] = (df['Iteraciones'] / 250.0) - (df['Distancia_Centro'] * 0.2)
    return df

if "mapa_nodos" not in st.session_state:
    st.session_state.mapa_nodos = deque(maxlen=500)
    st.session_state.mapa_tipos = deque(maxlen=500)
    nods, tps = cargar_nodos_desde_csv()
    st.session_state.mapa_nodos.extend(nods)
    st.session_state.mapa_tipos.extend(tps)

df_analisis = calcular_coordenadas_fractales(list(st.session_state.mapa_nodos), list(st.session_state.mapa_tipos))

# =====================================================================
# 4. ENTORNO VISUAL GENERAL EN PESTAÑAS (UI/UX)
# =====================================================================
tab_dash, tab_captura, tab_tiros = st.tabs(["📊 Dashboard Global & Constelación", "📸 IA Vision Scanner (EasyOCR)", "🎯 Focos Atractores & Sugerencias"])

# --- PESTAÑA 1: VENTANA DE CONVERGENCIA TOTAL CORREGIDA ---
with tab_dash:
    st.subheader("🎛️ Ventana General de Convergencia Espectral")
    st.caption("Estructura térmica calculada integrando entradas manuales, automáticas y escaneos ópticos (_OCR).")
    
    grid_cols = st.columns(4)
    for index, s_name in enumerate(sorteos_lista):
        with grid_cols[index % 4]:
            df_sorteo_actual = df_analisis[df_analisis['Sorteo_Tipo'].str.contains(s_name, case=False, na=False)]
            
            if len(df_sorteo_actual) > 0:
                estables_count = len(df_sorteo_actual[df_sorteo_actual['Clasificación'] == 'Estable'])
                ratio_conv = (estables_count / len(df_sorteo_actual)) * 100
                status_lbl = "🟢 ALTA CONVERGENCIA" if ratio_conv >= 20.0 else "🟡 CONVERGENCIA MEDIA" if ratio_conv >= 10.0 else "🔵 BAJA CONVERGENCIA"
            else:
                ratio_conv, status_lbl = 0.0, " Monitor listo"
                
            st.markdown(f"<div class='cyber-box'><strong>{s_name}</strong><br>Densidad: <strong style='color:#00f5d4;'>{ratio_conv:.1f}%</strong><br><span style='font-size:11px; font-weight:bold;'>{status_lbl}</span></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🗺️ Constelación General de Sorteos (Mandelbrot Space — 500 Nodos)")
    fig_points = px.scatter(df_analisis, x='Eje_X', y='Eje_Y', color='Clasificación', size='Tamaño', hover_data={'Vector_Boleto': True, 'Sorteo_Tipo': True, 'Iteraciones': True, 'Eje_X': False, 'Eje_Y': False, 'Tamaño': False}, color_discrete_map={'Escape Rápido': '#3A0CA3', 'Transición': '#4361EE', 'Estable': '#F72585', 'Interior Mandelbrot': '#FFFFFF'})
    fig_points.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,1)', paper_bgcolor='rgba(0,0,0,1)', height=400)
    st.plotly_chart(fig_points, use_container_width=True)

# --- PESTAÑA 2: IA VISION SCANNER ---
with tab_captura:
    st.subheader("📸 IA Vision Scanner")
    tipo_sorteo_scan = st.selectbox("1. Define el tipo de juego a escanear:", sorteos_lista)
    archivo_boleto = st.file_uploader("2. Cargar o tomar foto de la jugada:", type=["jpg", "jpeg", "png"])
    
    if archivo_boleto is not None:
        imagen = Image.open(archivo_boleto)
        st.image(imagen, caption="Señal óptica lista", width=250)
        if st.button("Lanzar Escaneo Óptico ⚡", use_container_width=True):
            with st.spinner("Procesando..."):
                exito, resultado = escanear_lineas_easyocr(imagen, tipo_sorteo_scan)
                if exito:
                    for linea in resultado:
                        tag_final = f"{tipo_sorteo_scan}_OCR"
                        if guardar_nodo_en_csv(linea, tag_final):
                            st.session_state.mapa_nodos.append(linea)
                            st.session_state.mapa_tipos.append(tag_final)
                    st.success("🎯 Escaneo e inyección completados con éxito.")
                    st.rerun()
                else:
                    st.error(f"❌ {resultado}")

# --- PESTAÑA 3: FOCOS ATRACTORES POR JUEGO ---
with tab_tiros:
    st.subheader("🎯 Focos Atractores por Coeficiente de Resonancia")
    st.caption("Sugerencias de alta densidad calculadas usando búsquedas mapeadas:")
    
    df_filtrado = df_analisis.sort_values(by='Resonancia_Score', ascending=False)
    
    for s_meta in ["CHISPAZO", "TRIS", "MELATE", "REVANCHA", "REVANCHITA", "MELATE RETRO"]:
        df_s_estables = df_filtrado[(df_filtrado['Sorteo_Tipo'].str.contains(s_meta, case=False, na=False)) & (df_filtrado['Clasificación'] == 'Estable')]
        
        if len(df_s_estables) > 0:
            sug_v = df_s_estables.iloc[0]['Vector_Boleto']
        else:
            sug_v = "Calibrando mallas... [Inyecta boletos en la pestaña anterior]"
            
        with st.status(f"🚀 Línea de Máxima Resonancia para {s_meta}", expanded=True):
            st.code(f"{sug_v}", language="text")

with st.sidebar:
    st.markdown("### 🛠️ Configuración e Infraestructura")
    if st.button("🔄 Reseteo Maestro (Hard Reset)"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.mapa_nodos.clear()
        st.session_state.mapa_tipos.clear()
        st.rerun()
