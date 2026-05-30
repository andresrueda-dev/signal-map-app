import streamlit as st
import pandas as pd
import numpy as np
import os
from collections import deque, Counter
from datetime import datetime
from PIL import Image

# --- MOTOR FRACTAL DE AYER (RESPETADO) ---
class MetaPatternFractal:
    def __init__(self, max_iter=250):
        self.max_iter = max_iter
    def transformar_secuencia(self, seq, i=0):
        datos = np.array(seq, dtype=float)
        dot_x = np.dot(datos, np.arange(1, len(datos) + 1)) if len(datos) > 0 else 0
        hash_x = np.sin(np.sum(datos) * (i * 0.001)) * 1.2 + np.cos(dot_x) * 0.4
        hash_y = np.cos(np.sum(datos) * (i * 0.001)) * 1.2 + np.sin(dot_x) * 0.4
        return hash_x, hash_y

# --- CONFIGURACIÓN TOTAL (INCLUYE LOTENAL) ---
GAME_CONFIG = {
    "TRIS": {"min": 0, "max": 9, "cantidad": 5},
    "CHISPAZO": {"min": 1, "max": 28, "cantidad": 5},
    "MELATE": {"min": 1, "max": 56, "cantidad": 6},
    "MAYOR": {"min": 0, "max": 9, "cantidad": 5},
    "SUPERIOR": {"min": 0, "max": 9, "cantidad": 5},
    "ZODIACO": {"min": 0, "max": 9, "cantidad": 5},
    "ESPECIAL": {"min": 0, "max": 9, "cantidad": 5}
}

# --- PERSISTENCIA (CSV ANTI-DUPLICADOS) ---
DB_FILE = "historial_calibrado.csv"
if 'boletos_auditados' not in st.session_state: st.session_state.boletos_auditados = []

def guardar_nodo_csv(nodo, sorteo):
    nodo_str = ",".join(map(str, nodo))
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        if nodo_str in df[df['sorteo']==sorteo]['numeros'].values: return False
    
    df_new = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), sorteo, nodo_str]], columns=['fecha', 'sorteo', 'numeros'])
    df_new.to_csv(DB_FILE, mode='a', header=not os.path.exists(DB_FILE), index=False)
    return True

# --- MOTOR DE VISIÓN (EASYOCR) ---
@st.cache_resource
def get_ocr():
    try:
        import easyocr
        return easyocr.Reader(['es', 'en'], gpu=False)
    except: return None

# --- UI Y LOGICA ---
st.set_page_config(page_title="SignalMap IA - Full", layout="wide")
menu = st.sidebar.radio("Navegación", ["🏠 Dashboard", "📸 IA Scanner & Diario", "🎯 Auditoría"])

# 1. DASHBOARD
if menu == "🏠 Dashboard":
    st.title("🧠 Constelación Fractal Dinámica")
    motor = MetaPatternFractal()
    puntos = []
    # Aquí puedes cargar tus datos del CSV
    st.info("Visualizando patrones en tiempo real sobre el motor de ayer.")
    
# 2. IA SCANNER (SOPORTE LOTENAL Y PERSISTENCIA)
elif menu == "📸 IA Vision Scanner":
    st.title("📸 Escáner Óptico de Boletos/Billetes")
    sorteo = st.selectbox("Sorteo", list(GAME_CONFIG.keys()))
    archivo = st.file_uploader("Subir foto", type=["jpg", "jpeg"])
    
    if archivo and st.button("Procesar"):
        reader = get_ocr()
        img = Image.open(archivo)
        resultados = reader.readtext(np.array(img), detail=0)
        st.write("Detectado:", resultados)
        # Lógica de extracción de números
        nums = [int(n) for n in re.findall(r'\d+', "".join(resultados))]
        if guardar_nodo_csv(nums, sorteo):
            st.success(f"Registrado en DB: {nums}")
        else:
            st.warning("Este boleto ya estaba registrado.")

# 3. AUDITORÍA VISUAL (TU CÓDIGO DE AYER)
elif menu == "🎯 Auditoría":
    st.title("🎯 Auditoría de Aciertos")
    col_izq, col_der = st.columns([1, 2])
    with col_izq:
        sorteo_sel = st.selectbox("Sorteo", list(GAME_CONFIG.keys()))
        numeros_boleto = st.text_input("Números Jugados")
        numeros_ganadores = st.text_input("Números Oficiales")
        if st.button("🔮 Auditar"):
            lista_j = [int(x.strip()) for x in numeros_boleto.split(",") if x.strip().isdigit()]
            lista_g = [int(x.strip()) for x in numeros_ganadores.split(",") if x.strip().isdigit()]
            coincidentes = list(set(lista_j) & set(lista_g))
            st.session_state.boletos_auditados.append({"sorteo": sorteo_sel, "jugados": lista_j, "coincidentes": coincidentes})
            
    with col_der:
        if st.session_state.boletos_auditados:
            ultimo = st.session_state.boletos_auditados[-1]
            cols_grid = st.columns(8)
            for num in range(0, 57):
                with cols_grid[num % 8]:
                    css = "grid-cell-match" if num in ultimo["coincidentes"] else "grid-cell-miss" if num in ultimo["jugados"] else "grid-cell-neutral"
                    st.markdown(f'<div class="{css}">{num}</div>', unsafe_allow_html=True)

# CSS de la planilla
st.markdown("""
<style>
    .grid-cell-match { background-color: #00f5d4; color: black; padding: 10px; border-radius: 5px; text-align: center; }
    .grid-cell-miss { background-color: #f72585; color: white; padding: 10px; border-radius: 5px; text-align: center; }
    .grid-cell-neutral { background-color: #1e1b4b; color: white; padding: 10px; border-radius: 5px; text-align: center; }
</style>
""", unsafe_allow_html=True)
