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
# INICIALIZACIÓN CONFIGURABLE Y SEGURA DEL MOTOR DE VISIÓN (EASYOCR)
# =====================================================================
@st.cache_resource
def inicializar_lector_ocr():
    try:
        import easyocr
        return easyocr.Reader(['es', 'en'], gpu=False)
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
# 1. ARCHIVO LOCAL CSV Y CONTROL MAESTRO DE PERSISTENCIA MULTI-SORTEO
# =====================================================================
DB_FILE = "historial_calibrado.csv"

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
    sorteos_pool = ["TRIS", "CHISPAZO", "MELATE", "MAYOR"]
    for i in range(500):
        secuencia = [int((np.sin(i * 0.05 + j) * 7) + (np.cos(i * 0.13 + j) * 6) + 14) for j in range(5)]
        base_nodos.append(secuencia)
        base_tipos.append(sorteos_pool[i % len(sorteos_pool)])
    return base_nodos, base_tipos

# =====================================================================
# 2. PROCESAMIENTO ÓPTICO AVANZADO CON MOTOR EASYOCR UNIVERSAL
# =====================================================================
def escanear_lineas_easyocr(imagen_pil, tipo_sorteo):
    if reader is None: return [False, "Lector EasyOCR no listo."]
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
            if all(0 <= n <= 9 for n in numeros): lineas_encontradas.append(numeros)
        elif tipo_sorteo in ["MAYOR", "SUPERIOR", "ZODIACO", "ESPECIAL"]:
            nums_largos = re.findall(r'\b\d{5,6}\b', texto)
            for n_l in nums_largos: lineas_encontradas.append([int(d) for d in str(n_l)])
    if len(lineas_encontradas) > 0: return [True, lineas_encontradas]
    return [False, "No se aislaron líneas. Ajusta el enfoque."]

# =====================================================================
# 3. MOTORES MATEMÁTICOS DE PROYECCIÓN GEOMÉTRICA (INVARIANTE)
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
        
    df = pd.DataFrame({'Eje_X': puntos_x, 'Eje_Y': puntos_y, 'Iteraciones': iteraciones_escape, 'Vector_Boleto': raw_nodos, 'Sorteo_Tipo': lista_tipos, 'Tamaño': [7]*len(puntos_x)})
    condiciones = [(df['Iteraciones'] <= 50), (df['Iteraciones'] > 50) & (df['Iteraciones'] <= 150), (df['Iteraciones'] > 150) & (df['Iteraciones'] < 250), (df['Iteraciones'] == 250)]
    df['Clasificación'] = np.select(condiciones, ['Escape Rápido', 'Transición', 'Estable', 'Interior Mandelbrot'], default='Transición')
    centro_x, centro_y = df['Eje_X'].mean(), df['Eje_Y'].mean()
    df['Distancia_Centro'] = np.sqrt((df['Eje_X'] - centro_x)**2 + (df['Eje_Y'] - centro_y)**2)
    df['Resonancia_Score'] = (df['Iteraciones'] / 250.0) - (df['Distancia_Centro'] * 0.2)
    return df

def obtener_ultimo_sorteo_automatico(sorteo_nombre):
    try:
        url = "https://www.pronosticos.gob.mx/Home/Resultados"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tz_cdmx = pytz.timezone('America/Mexico_City')
            st.session_state.ultima_conexion = datetime.datetime.now(tz_cdmx).strftime("%H:%M:%S MX")
            st.session_state.status_servidor = "EN VIVO (MANDELBROT SYNC)"
            if sorteo_nombre == 'chispazo':
                contenedor = soup.find('div', id='divChispazo') or soup.find('div', class_='resultado-chispazo')
                if contenedor:
                    nums = [int(s) for s in re.findall(r'\b\d+\b', contenedor.text)]
                    return sorted([n for n in nums if 1 <= n <= 28][:5])
            elif sorteo_nombre == 'tris':
                contenedor = soup.find('div', id='divTris') or soup.find('div', class_='resultado-tris')
                if contenedor:
                    nums = [int(s) for s in re.findall(r'\b\d+\b', contenedor.text)]
                    return [n for n in nums if 0 <= n <= 9][:5]
        return None
    except: return None

def verificar_actualizacion_por_horario():
    try:
        tz_cdmx = pytz.timezone('America/Mexico_City')
        hora_actual = datetime.datetime.now(tz_cdmx).time()
        horarios = [datetime.time(13,15), datetime.time(15,15), datetime.time(17,15), datetime.time(19,15), datetime.time(21,15)]
        for h in horarios:
            if abs(hora_actual.hour - h.hour) == 0 and abs(hora_actual.minute - h.minute) <= 5: return True
        return False
    except: return False

if "mapa_nodos" not in st.session_state:
    st.session_state.mapa_nodos = deque(maxlen=500)
    st.session_state.mapa_tipos = deque(maxlen=500)
    nods, tps = cargar_nodos_desde_csv()
    st.session_state.mapa_nodos.extend(nods)
    st.session_state.mapa_tipos.extend(tps)

df_analisis = calcular_coordenadas_fractales(list(st.session_state.mapa_nodos), list(st.session_state.mapa_tipos))

# =====================================================================
# 4. ENTORNO VISUAL EN PESTAÑAS (UI/UX)
# =====================================================================
tab_dash, tab_captura, tab_tiros = st.tabs(["📊 Dashboard Global & Constelación", "📸 IA Vision Scanner (EasyOCR)", "🎯 Focos Atractores & Sugerencias"])

with tab_dash:
    st.subheader("🎛️ Ventana General de Convergencia Espectral")
    sorteos_lista = ["TRIS", "CHISPAZO", "MELATE", "REVANCHA", "REVANCHITA", "MAYOR", "SUPERIOR", "ZODIACO"]
    grid_cols = st.columns(4)
    for index, s_name in enumerate(sorteos_lista):
        with grid_cols[index % 4]:
            df_sorteo_actual = df_analisis[df_analisis['Sorteo_Tipo'].str.contains(s_name, case=False, na=False)]
            if len(df_sorteo_actual) > 0:
                estables_count = len(df_sorteo_actual[df_sorteo_actual['Clasificación'] == 'Estable'])
                ratio_conv = (estables_count / len(df_sorteo_actual)) * 100
                status_lbl = " ALTA CONVERGENCIA (POR SALIR)" if ratio_conv >= 30.0 else " CONVERGENCIA MEDIA" if ratio_conv >= 15.0 else " BAJA CONVERGENCIA"
            else:
                ratio_conv, status_lbl = 0.0, " MONITOR EN ESPERA"
            st.markdown(f"<div class='cyber-box'><strong>{s_name}</strong><br>Densidad: <strong style='color:#00f5d4;'>{ratio_conv:.1f}%</strong><br><span style='font-size:11px;'>{status_lbl}</span></div>", unsafe_allow_html=True)

    st.markdown("---")
    fig_points = px.scatter(df_analisis, x='Eje_X', y='Eje_Y', color='Clasificación', size='Tamaño', color_discrete_map={'Escape Rápido': '#3A0CA3', 'Transición': '#4361EE', 'Estable': '#F72585', 'Interior Mandelbrot': '#FFFFFF'})
    fig_points.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,1)', paper_bgcolor='rgba(0,0,0,1)', height=400)
    st.plotly_chart(fig_points, use_container_width=True)

with tab_captura:
    st.subheader("📸 IA Vision Scanner")
    tipo_sorteo_scan = st.selectbox("1. Define la estructura:", sorteos_lista)
    archivo_boleto = st.file_uploader("2. Cargar imagen:", type=["jpg", "jpeg", "png"])
    if archivo_boleto is not None:
        imagen = Image.open(archivo_boleto)
        if st.button("Lanzar Escaneo Óptico ⚡", use_container_width=True):
            exito, resultado = escanear_lineas_easyocr(imagen, tipo_sorteo_scan)
            if exito:
                for linea in resultado:
                    tag_final = f"{tipo_sorteo_scan}_OCR"
                    if guardar_nodo_en_csv(linea, tag_final):
                        st.session_state.mapa_nodos.append(linea)
                        st.session_state.mapa_tipos.append(tag_final)
                st.rerun()

with tab_tiros:
    st.subheader("🎯 Focos Atractores por Coeficiente de Resonancia")
    df_filtrado = df_analisis.sort_values(by='Resonancia_Score', ascending=False)
    df_estables = df_filtrado[df_filtrado['Clasificación'] == 'Estable']
    sug_1 = df_estables.iloc[0]['Vector_Boleto'] if len(df_estables) >= 1 else "01, 08, 10, 16, 26"
    with st.status("🚀 Sugerencia ALFA Activa", expanded=True): st.code(f"{sug_1}", language="text")

with st.sidebar:
    st.markdown("### 🛠️ Configuración")
    if st.button("🔄 Reseteo Maestro"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.mapa_nodos.clear()
        st.session_state.mapa_tipos.clear()
        st.rerun()
