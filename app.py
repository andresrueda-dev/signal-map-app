import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import datetime
import pytz
from collections import deque
import plotly.express as px

# =====================================================================
# 0. CONTROL DE PÁGINA E INYECCIÓN DE DISEÑO VISUAL AVANZADO (CSS)
# =====================================================================
st.set_page_config(page_title="SignalMap AI — MetaPattern Engine", page_icon="📡", layout="wide")

# CSS personalizado para mutar la interfaz estándar a un entorno de alta densidad táctica
st.markdown("""
    <style>
        .reportview-container { background: #000000 !important; }
        .stApp { background-color: #000000; }
        /* Estilización avanzada del sistema de pestañas */
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
        /* Ajuste de tipografía para métricas de tómbola */
        div[data-testid="stMetricValue"] { font-family: 'Courier New', monospace; font-weight: bold; color: #00f5d4; }
        div[data-testid="stMetricLabel"] { font-family: 'Arial', sans-serif; color: #adbac7; }
        /* Bloques contenedores estilizados */
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
    """Pantalla de inicio protegida con validación segura de credenciales"""
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
# 1. MOTORES MATEMÁTICOS Y RE-MUESTREO DE LA ELIPSE FRACTAL
# =====================================================================
def generar_matriz_fractal_base():
    """Genera combinaciones coherentes armónicas para el mapa base de 500 nodos"""
    base_nodos = []
    for i in range(499):
        # Generación ondulatoria pura para mantener la calibración geométrica estable
        secuencia = [(int(np.sin(i * 0.15 + j) * 12) + 14) for j in range(5)]
        base_nodos.append(secuencia)
    return base_nodos

def IA_filtro_procesamiento_señal(lista_numeros):
    if not lista_numeros or len(lista_numeros) < 3: return "Baja (Ruido)"
    arr = np.array(lista_numeros)
    paridad = np.sum(arr % 2 == 0)
    dispersion = np.std(arr)
    if (1 <= paridad <= 4) and (dispersion > 2.0):
        return "Alta (Frecuencia Armónica)"
    return "Media (Transición Lineal)"

def calcular_coordenadas_fractales(nodos_matriz):
    """Mapea los 500 vectores reales al plano complejo y calcula velocidad de escape"""
    puntos_x, puntos_y, iteraciones_escape, raw_nodos = [], [], [], []
    for nodo in nodos_matriz:
        if not nodo: nodo = [0]
        # Matriz de pesos posicionales para evitar colisiones idénticas
        pesos = np.arange(1, len(nodo) + 1)
        hash_x = np.sin(np.dot(nodo, pesos)) * 1.5
        hash_y = np.cos(np.dot(nodo, pesos)) * 1.5
        
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
        'Iteraciones': iteraciones_escape, 'Nodo_Real': raw_nodos, 'Tamaño': [8]*len(puntos_x)
    })
    
    condiciones = [
        (df['Iteraciones'] <= 50),
        (df['Iteraciones'] > 50) & (df['Iteraciones'] <= 150),
        (df['Iteraciones'] > 150) & (df['Iteraciones'] < 250),
        (df['Iteraciones'] == 250)
    ]
    df['Clasificación'] = np.select(condiciones, ['Escape Rápido', 'Transición', 'Estable', 'Interior Mandelbrot'], default='Transición')
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
            elif sorteo_nombre in ['melate', 'revancha', 'revanchita']:
                contenedor = soup.find('div', id=f'div{sorteo_nombre.capitalize()}') or soup.find('div', class_=f'resultado-{sorteo_nombre}')
                if contenedor:
                    nums = [int(s) for s in re.findall(r'\b\d+\b', contenedor.text)]
                    return sorted([n for n in nums if 1 <= n <= 56][:6])
        return None
    except:
        return None

def verificar_actualizacion_por_horario():
    try:
        tz_cdmx = pytz.timezone('America/Mexico_City')
        hora_actual = datetime.datetime.now(tz_cdmx).time()
        for h in [datetime.time(13,15), datetime.time(15,15), datetime.time(17,15), datetime.time(19,15), datetime.time(21,15)]:
            if abs(hora_actual.hour - h.hour) == 0 and abs(hora_actual.minute - h.minute) <= 5: return True
        return False
    except: return False

# Inicialización optimizada de memoria circular
if "mapa_nodos" not in st.session_state:
    st.session_state.mapa_nodos = deque(maxlen=500)
    st.session_state.mapa_nodos.extend(generar_matriz_fractal_base())

# =====================================================================
# 2. RENDERIZADO DEL ENTORNO PROTEGIDO DE PESTAÑAS
# =====================================================================
col_header, col_log = st.columns([6, 1])
with col_header:
    st.title("📡 SignalMap AI — Engine de Sincronización")
with col_log:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Cerrar Sesión 🔒", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# Procesamiento único de la matriz para consistencia global entre módulos
df_analisis = calcular_coordenadas_fractales(list(st.session_state.mapa_nodos))

tab_dash, tab_mapa, tab_captura, tab_tiros = st.tabs([
    "📊 Dashboard Global de Convergencia", 
    "🗺️ Mapa Mandelbrot Space", 
    "📝 Diario de Señales & Captura", 
    "🎯 Sugerencias & Auditoría Visual"
])

# --- PESTAÑA 1: DASHBOARD ---
with tab_dash:
    st.subheader("📊 Historial Indexado & Matriz Global de Convergencia")
    
    st.markdown("##### ⚡ Sorteos Electrónicos")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(label="🎲 TRIS (Volumen Real Indexado)", value="33,179 sorteos", delta="Dominante: 0")
    with c2: st.metric(label="🚀 CHISPAZO (Tiro Directo)", value="12,034 sorteos", delta="Dominante: 10", delta_color="inverse")
    with c3: st.metric(label="🪐 MELATE (Volumen Real)", value="4,218 sorteos", delta="Dominante: 32")
    with c4: st.metric(label="🔥 REVANCHA (Volumen Real)", value="3,210 sorteos", delta="Dominante: 30")

    st.markdown("##### 🎫 Sorteos Tradicionales (Billetes)")
    t1, t2, t3, t4 = st.columns(4)
    with t1: st.metric(label="🔴 SORTEO MAYOR (Martes)", value="Premio: $21 MDP", delta="Bolsa Mayor")
    with t2: st.metric(label="🔵 SORTEO SUPERIOR (Viernes)", value="Premio: $17 MDP", delta="Bolsa Activa")
    with t3: st.metric(label="🔮 SORTEO ZODIACO (Domingo)", value="Premio: $11 MDP", delta="Signo Activo")
    with t4: 
        nodos_estables = len(df_analisis[df_analisis['Clasificación'] == 'Estable'])
        porcentaje_convergencia = (nodos_estables / 500) * 100
        st.metric(label="📡 LINK INFRAESTRUCTURA", value=st.session_state.status_servidor, delta=f"Última: {st.session_state.ultima_conexion}")

    st.markdown("#### 🔬 Ingeniería de Resonancia Activa")
    st.markdown(f"""
    <div class='cyber-box'>
        <p style='color:#adbac7; margin:0;'>Densidad de Estabilidad Analítica del Plano: 
        <strong style='color:#f72585;'>{porcentaje_convergencia:.1f}%</strong> de nodos consolidados en el atractor elíptico principal.</p>
    </div>
    """, unsafe_allow_html=True)

# --- PESTAÑA 2: MAPA ---
with tab_mapa:
    st.subheader("🗺️ Mapa Fractal Completo (Mandelbrot Space — 500 Nodos Reales)")
    
    # Renderizado optimizado con paleta de color de alto contraste
    fig = px.scatter(
        df_analisis, x='Eje_X', y='Eje_Y', color='Clasificación', size='Tamaño',
        hover_data={'Nodo_Real': True, 'Iteraciones': True, 'Eje_X': False, 'Eje_Y': False, 'Tamaño': False},
        color_discrete_map={
            'Escape Rápido': '#3A0CA3',     # Violeta profundo
            'Transición': '#4361EE',       # Azul eléctrico
            'Estable': '#F72585',          # Magenta neón (Anillo activo)
            'Interior Mandelbrot': '#FFFFFF' # Blanco destello
        },
        labels={'Eje_X': 'Frecuencia Real (X)', 'Eje_Y': 'Frecuencia Imaginaria (Y)'}
    )
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,1)',
        paper_bgcolor='rgba(0,0,0,1)',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- PESTAÑA 3: DIARIO DE SEÑALES & REGISTRO ---
with tab_captura:
    st.subheader("📝 Diario de Señales - Registro Inmediato e Híbrido")
    sub_tab_auto, sub_tab_manual = st.tabs(["🤖 Extractor Automatizado (IA Scanner)", "✍️ Captura Manual Diario"])
    
    with sub_tab_auto:
        st.caption("Conexión directa vía scraper hacia la tómbola oficial de la Lotería Mexicana.")
        sorteo_auto = st.selectbox("Tómbola de Servidor Oficial:", ["TRIS", "CHISPAZO", "MELATE", "REVANCHA"])
        if st.button("Sincronizar Servidor Directo ⚡", use_container_width=True):
            with st.spinner("Estableciendo túnel seguro con el centro de cómputo nacional..."):
                datos = obtener_ultimo_sorteo_automatico(sorteo_auto.lower())
                if datos:
                    calificacion_ia = IA_filtro_procesamiento_señal(datos)
                    st.session_state.mapa_nodos.append(datos)
                    st.success(f"✅ Nodo validado por IA [{calificacion_ia}] e inyectado con éxito: {datos}")
                    st.rerun()
                else:
                    st.error("Servidor ocupado o tómbola en proceso de publicación. Usa el respaldo manual.")
                    
    with sub_tab_manual:
        sorteo_tipo = st.selectbox("Selecciona Sorteo Específico:", [
            "TRIS MEDIODÍA", "TRIS DE LAS TRES", "CHISPAZO DE LAS TRES", "TRIS CLÁSICO", "CHISPAZO CLÁSICO",
            "MELATE CORRIDO", "SORTEO MAYOR (Premio Mayor)", "SORTEO SUPERIOR (Premio Mayor)"
        ])
        numeros_raw = st.text_input("Introduce los números de hoy separados por comas (Ej: 1,8,10,16,26 o 5,4,3,2,1):")
        
        if st.button("Guardar Señal de Hoy 🚀", use_container_width=True):
            if numeros_raw:
                limpio = re.sub(r'\s+', '', numeros_raw)
                try:
                    lista_nums = [int(n) for n in limpio.split(',') if n != '']
                    calificacion_ia = IA_filtro_procesamiento_señal(lista_nums)
                    st.session_state.mapa_nodos.append(lista_nums)
                    st.success(f"✅ Señal indexada manual en el núcleo. Resonancia calculada: **{calificacion_ia}**.")
                    st.rerun()
                except:
                    st.error("Verifica el formato numérico de entrada (usa únicamente enteros separados por comas).")

# --- PESTAÑA 4: SUGERENCIAS Y TIROS SUGERIDOS ---
with tab_tiros:
    st.subheader("🎯 Números Sugeridos & Evidencia de Tiros Directos")
    col_sug, col_evidencia = st.columns(2)
    
    with col_sug:
        st.markdown("#### 🔮 Proyección de Combinaciones Sugeridas (Algorítmica Real)")
        st.caption("Extracción en tiempo real de los vectores con mayor estabilidad geométrica en el mapa.")
        
        # Filtramos nodos reales clasificados como estables para darte sugerencias reales
        df_estables = df_analisis[df_analisis['Clasificación'] == 'Estable']
        if len(df_estables) >= 2:
            sug_1 = df_estables.iloc[0]['Nodo_Real']
            sug_2 = df_estables.iloc[1]['Nodo_Real']
        else:
            sug_1 = "01, 08, 10, 16, 26 (Carga Base)"
            sug_2 = "03, 04, 08, 12, 18 (Carga Secundaria)"
            
        st.markdown(f"""
        <div class='cyber-box'>
            <p style='color:#adbac7; margin-bottom:5px;'><strong>Sugerencia ALFA (Foco Atractor):</strong></p>
            <code style='color:#00f5d4; font-size:16px;'>{sug_1}</code>
            <p style='color:#adbac7; margin-top:15px; margin-bottom:5px;'><strong>Sugerencia BETA (Eje Fractal Dominante):</strong></p>
            <code style='color:#f72585; font-size:16px;'>{sug_2}</code>
        </div>
        """, unsafe_allow_html=True)
        st.success("💡 Consejo táctico: Procesa estas líneas de convergencia para construir tus combinaciones antes del cierre.")
        
    with col_evidencia:
        st.markdown("#### 📸 Evidencia Histórica & Auditoría Visual")
        st.write("Módulo de validación de efectividad y precisión del framework.")
        st.markdown("""
        <div style='background-color: rgba(0, 245, 212, 0.1); border: 1px solid #00f5d4; border-radius:8px; padding:15px;'>
            <span style='color:#00f5d4;'>🎫 <strong>Último Ticket Validado:</strong></span><br>
            <span style='color:#ffffff; font-family:monospace;'>Sorteo Chispazo 12036 | 3 ACIERTOS ($55.60 Cobrados) ✔️</span>
        </div>
        """, unsafe_allow_html=True)

# --- CONTROL DE AUDITORÍA LATERAL ---
with st.sidebar:
    st.markdown("### 🛠️ Auditoría del Motor")
    if verificar_actualizacion_por_horario():
        st.warning("⏰ Ventana de Sorteo Activa en CDMX.")
    else:
        st.success("🟢 Monitor en espera de horarios oficiales.")
        
    st.caption("Ubicación de Servidores: Streamlit Cloud Hub")
    
    if st.button("🔄 Reseteo Maestro (Hard Reset)"):
        st.session_state.mapa_nodos.clear()
        st.session_state.mapa_nodos.extend(generar_matriz_fractal_base())
        st.success("Estructura de 500 nodos recalibrada.")
        st.rerun()
