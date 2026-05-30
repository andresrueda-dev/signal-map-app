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
    """Inicializa el lector en caché de Streamlit para no ralentizar las recargas"""
    try:
        import easyocr
        # Configuramos lectura en español/inglés. GPU=False optimiza para contenedores cloud básicos.
        return easyocr.Reader(['es', 'en'], gpu=False)
    except Exception as e:
        st.error(f"Error crítico al inicializar la matriz OCR: {e}")
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
        st.markdown("<p style='text-align: center; color: #7928CA; font-size:14px;'>Framework de Calibración Fractal & Conectividad Termodinámica</p>", unsafe_allow_html=True)
        
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
                    st.success("🔒 Sincronización de matriz exitosa...")
                    st.rerun()
                else:
                    st.error("❌ Código incorrecto o usuario no registrado.")

if not st.session_state.autenticado:
    login()
    st.stop()

# =====================================================================
# 1. ARCHIVO LOCAL CSV Y CONTROL MAESTRO DE PERSISTENCIA ANTI-DUPLICADOS
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
            nodos_recuperados = []
            for comb in df['Combinacion'].tail(500).values:
                nodos_recuperados.append([int(x) for x in str(comb).split(',')])
            if len(nodos_recuperados) > 0: return nodos_recuperados
        except: pass
    
    return [[int((np.sin(i * 0.05 + j) * 7) + (np.cos(i * 0.13 + j) * 6) + 14) for j in range(5)] for i in range(500)]

# =====================================================================
# 2. PROCESAMIENTO ÓPTICO AVANZADO CON MOTOR EASYOCR
# =====================================================================
def escanear_lineas_easyocr(imagen_pil, tipo_sorteo):
    if reader is None:
        return [False, "El motor EasyOCR no se encuentra inicializado."]
    
    # Transformar la imagen cargada en un formato de array comprensible por el detector de mallas
    img_array = np.array(imagen_pil.convert('RGB'))
    
    # Ejecutar el escaneo de texto en un solo paso analítico
    resultados_ocr = reader.readtext(img_array, detail=0)
    lineas_encontradas = []
    
    for texto in resultados_ocr:
        # Extraemos secuencias numéricas ignorando basura del diseño del boleto
        numeros = [int(n) for n in re.findall(r'\b\d+\b', texto)]
        
        if tipo_sorteo == "CHISPAZO" and len(numeros) == 5:
            if all(1 <= n <= 28 for n in numeros):
                lineas_encontradas.append(sorted(numeros))
        elif tipo_sorteo == "TRIS" and len(numeros) == 5:
            if all(0 <= n <= 9 for n in numeros):
                lineas_encontradas.append(numeros)
                
    if len(lineas_encontradas) > 0:
        return [True, lineas_encontradas]
    return [False, "No se aislaron patrones numéricos correspondientes al sorteo. Asegúrate de encuadrar bien la zona de apuestas."]

# =====================================================================
# 3. MOTORES MATEMÁTICOS DE PROYECCIÓN GEOMÉTRICA (INVARIANTE)
# =====================================================================
def calcular_coordenadas_fractales(nodos_matriz):
    puntos_x, puntos_y, iteraciones_escape, raw_nodos = [], [], [], []
    for i, nodo in enumerate(nodos_matriz):
        if not nodo: nodo = [0]
        
        # Invarianza por Producto Punto para fijar la geometría
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
        
    df = pd.DataFrame({'Eje_X': puntos_x, 'Eje_Y': puntos_y, 'Iteraciones': iteraciones_escape, 'Vector_Boleto': raw_nodos, 'Tamaño': [7]*len(puntos_x)})
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
    except:
        return None

def verificar_actualizacion_por_horario():
    try:
        tz_cdmx = pytz.timezone('America/Mexico_City')
        hora_actual = datetime.datetime.now(tz_cdmx).time()
        horarios = [datetime.time(13,15), datetime.time(15,15), datetime.time(17,15), datetime.time(19,15), datetime.time(21,15)]
        for h in horarios:
            if abs(hora_actual.hour - h.hour) == 0 and abs(hora_actual.minute - h.minute) <= 5: return True
        return False
    except: return False

# Inicialización segura de memoria persistente
if "mapa_nodos" not in st.session_state:
    st.session_state.mapa_nodos = deque(maxlen=500)
    st.session_state.mapa_nodos.extend(cargar_nodos_desde_csv())

df_analisis = calcular_coordenadas_fractales(list(st.session_state.mapa_nodos))

# =====================================================================
# 4. ENTORNO VISUAL EN PESTAÑAS (UI/UX)
# =====================================================================
col_header, col_log = st.columns([6, 1])
with col_header:
    st.title("📡 SignalMap AI — Engine de Sincronización")
with col_log:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Cerrar Sesión 🔒", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

tab_dash, tab_captura, tab_tiros = st.tabs([
    "📊 Dashboard Global & Constelación", 
    "📸 IA Vision Scanner (EasyOCR)", 
    "🎯 Focos Atractores & Sugerencias"
])

# --- PESTAÑA 1: CORE GRÁFICO ---
with tab_dash:
    st.subheader("📊 Volumen Real Indexado & Matriz Global de Convergencia")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(label="🎲 TOTAL VECTORES RESPALDADOS", value=f"{len(st.session_state.mapa_nodos)} / 500")
    with c2: st.metric(label="🛰️ INFRAESTRUCTURA", value="EasyOCR Desplegado")
    with c3: st.metric(label="🪐 PERSISTENCIA CLOUD", value="Espejo CSV Sincronizado")
    with c4: st.metric(label="📡 LINK SERVIDOR REAL", value=st.session_state.status_servidor)

    st.markdown("---")
    st.subheader("🗺️ Constelación de Sorteos (Geometría Invariante Estable)")
    
    fig_points = px.scatter(
        df_analisis, x='Eje_X', y='Eje_Y', color='Clasificación', size='Tamaño',
        hover_data={'Vector_Boleto': True, 'Iteraciones': True, 'Eje_X': False, 'Eje_Y': False, 'Tamaño': False},
        color_discrete_map={'Escape Rápido': '#3A0CA3', 'Transición': '#4361EE', 'Estable': '#F72585', 'Interior Mandelbrot': '#FFFFFF'}
    )
    fig_points.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,1)', paper_bgcolor='rgba(0,0,0,1)', height=420)
    st.plotly_chart(fig_points, use_container_width=True)

    st.markdown("---")
    st.subheader("🎛️ Monitor de Onda-Frecuencia Termodinámica")
    tab_tris, tab_chisp, tab_mel = st.tabs(["🎲 Frecuencia TRIS", "🚀 Frecuencia CHISPAZO", "🪐 Frecuencia MELATE"])
    
    with tab_tris:
        datos_onda_tris = df_analisis['Iteraciones'].values[-80:] + (np.sin(np.arange(80)) * 15)
        fig_t = go.Figure(go.Scatter(y=datos_onda_tris, mode='lines', line=dict(color='#00f5d4', width=2)))
        fig_t.update_layout(template='plotly_dark', plot_bgcolor='rgba(10,14,20,0.4)', paper_bgcolor='rgba(0,0,0,1)', height=180, margin=dict(l=20,r=20,t=10,b=20))
        st.plotly_chart(fig_t, use_container_width=True)
        
    with tab_chisp:
        datos_onda_chisp = df_analisis['Iteraciones'].values[-80:] * (np.cos(np.arange(80)*0.2) * 0.4 + 1.1)
        fig_c = go.Figure(go.Scatter(y=datos_onda_chisp, mode='lines', line=dict(color='#f72585', width=2)))
        fig_c.update_layout(template='plotly_dark', plot_bgcolor='rgba(10,14,20,0.4)', paper_bgcolor='rgba(0,0,0,1)', height=180, margin=dict(l=20,r=20,t=10,b=20))
        st.plotly_chart(fig_c, use_container_width=True)
        
    with tab_mel:
        datos_onda_mel = np.abs(np.diff(df_analisis['Iteraciones'].values[-81:])) * 2.5
        fig_m = go.Figure(go.Scatter(y=datos_onda_mel, mode='lines', line=dict(color='#4361EE', width=2)))
        fig_m.update_layout(template='plotly_dark', plot_bgcolor='rgba(10,14,20,0.4)', paper_bgcolor='rgba(0,0,0,1)', height=180, margin=dict(l=20,r=20,t=10,b=20))
        st.plotly_chart(fig_m, use_container_width=True)

# ---------------------------------------------------------------------
# PESTAÑA 2: IA VISION SCANNER CON INFRAESTRUCTURA EASYOCR
# ---------------------------------------------------------------------
with tab_captura:
    st.subheader("📸 IA Vision Scanner — Análisis Espectral de Mallas de Juego")
    st.caption("Captura de forma óptica el boleto impreso para inyectar de forma directa todas las jugadas activas.")
    
    col_v1, col_v2 = st.columns([1.5, 1])
    
    with col_v1:
        tipo_sorteo_scan = st.selectbox("1. Define la estructura analítica del boleto:", ["CHISPAZO", "TRIS"])
        archivo_boleto = st.file_uploader("2. Cargar imagen de la jugada (Sube archivo o toma foto):", type=["jpg", "jpeg", "png"])
        
        if archivo_boleto is not None:
            imagen = Image.open(archivo_boleto)
            st.image(imagen, caption="Señal óptica estructurada para EasyOCR", width=280)
            
            if st.button("Lanzar Escaneo Óptico Automatizado ⚡", use_container_width=True):
                with st.spinner("Decodificando mallas y localizando renglones numéricos..."):
                    exito, resultado = escanear_lineas_easyocr(imagen, tipo_sorteo_scan)
                    
                    if exito:
                        st.success(f"🎯 Escáner Ejecutado. Se localizaron {len(resultado)} líneas de juego activas.")
                        duplicados, nuevos = 0, 0
                        
                        for linea in resultado:
                            fue_guardado = guardar_nodo_en_csv(linea, f"{tipo_sorteo_scan}_OCR")
                            if fue_guardado:
                                st.session_state.mapa_nodos.append(linea)
                                nuevos += 1
                            else:
                                duplicados += 1
                                
                        if nuevos > 0: 
                            st.write(f"📥 **Se inyectaron {nuevos} vectores limpios a la Constelación.**")
                        if duplicados > 0: 
                            st.info(f"📋 Se omitieron {duplicados} líneas que ya formaban parte de la persistencia local.")
                        st.rerun()
                    else:
                        st.error(f"❌ Falla en la lectura: {resultado}")
                        
    with col_v2:
        st.markdown("""
        <div style='background-color: #0d1117; border: 1px solid #21262d; border-radius: 8px; padding: 20px;'>
            <h4 style='color: #00f5d4; margin-top:0;'>📋 Protocolo de Captura Óptica</h4>
            <p style='color: #adbac7; font-size: 13px;'>El motor calcula de forma nativa la cantidad de líneas jugadas basándose en mallas puras de 5 números.</p>
            <ul style='color: #adbac7; font-size: 13px; padding-left:20px;'>
                <li>Busca un encuadre vertical y recto del boleto.</li>
                <li>Los datos duplicados en el mismo boleto o sorteos previos se filtran en automático para mantener la pureza geométrica del fractal.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🤖 Escáner Automatizado por Servidor (Web Scraper)")
    sorteo_auto = st.selectbox("Canal Remoto de Pronósticos Oficiales:", ["TRIS", "CHISPAZO"])
    if st.button("Lanzar Escáner de Red ⚡", use_container_width=True):
        with st.spinner("Conectando con servidores centrales..."):
            datos = obtener_ultimo_sorteo_automatico(sorteo_auto.lower())
            if datos:
                es_nuevo = guardar_nodo_en_csv(datos, sorteo_auto.upper())
                if es_nuevo:
                    st.session_state.mapa_nodos.append(datos)
                    st.success(f"✅ Sincronización Exitosa: Nodo remoto indexado: {datos}")
                    st.rerun()
                else: st.info(f"📋 Sorteo al día: El resultado [{datos}] ya existía en el historial.")
            else: st.error("Servidor remoto sin respuesta momentánea.")

# ---------------------------------------------------------------------
# PESTAÑA 3: PROYECCIÓN AVANZADA DE FOCOS ATRACTORES
# ---------------------------------------------------------------------
with tab_tiros:
    st.subheader("🎯 Focos Atractores Filtrados por Coeficiente de Resonancia")
    df_filtrado = df_analisis.sort_values(by='Resonancia_Score', ascending=False)
    df_estables = df_filtrado[df_filtrado['Clasificación'] == 'Estable']
    sug_1 = df_estables.iloc[0]['Vector_Boleto'] if len(df_estables) >= 1 else "01, 08, 10, 16, 26"
    sug_2 = df_estables.iloc[1]['Vector_Boleto'] if len(df_estables) >= 2 else "03, 04, 08, 12, 18"
    
    with st.status("🚀 Ver Sugerencia ALFA para CHISPAZO (Foco Atractor Central)", expanded=True):
        st.code(f"{sug_1}", language="text")
    with st.status("🎲 Ver Sugerencia BETA para TRIS (Eje Fractal de Resonancia)", expanded=True):
        st.code(f"{sug_2}", language="text")

# --- BARRA LATERAL TÉCNICA ---
with st.sidebar:
    st.markdown("### 🛠️ Configuración e Infraestructura")
    if verificar_actualizacion_por_horario(): st.warning("Ventana de Sorteo Activa en CDMX.")
    else: st.success("Monitor en espera de horarios.")
    if st.button("🔄 Reseteo Maestro (Hard Reset)"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.mapa_nodos.clear()
        st.rerun()
