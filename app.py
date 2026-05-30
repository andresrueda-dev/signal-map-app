import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE JUEGOS (Asegúrate de tener esto al inicio de tu app) ---
GAME_CONFIG = {
    "TRIS": {"min": 0, "max": 9},
    "CHISPAZO": {"min": 1, "max": 28},
    "MELATE": {"min": 1, "max": 56}
}

# Inicializar sesión si no existe
if 'boletos_auditados' not in st.session_state:
    st.session_state.boletos_auditados = []

# --- INSERCIÓN EN TU MENÚ (Donde tengas tu lógica de 'menu') ---
# Suponiendo que tienes un sidebar o selectbox para el menú
menu = st.sidebar.selectbox("Navegación", ["Dashboard", "📸 Evidencia & Diario de Aciertos"])

# --- CSS PARA LAS CELDAS DE LA PLANILLA ---
st.markdown("""
<style>
    .grid-cell-match { background-color: #00f5d4; color: black; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; }
    .grid-cell-miss { background-color: #f72585; color: white; padding: 10px; border-radius: 5px; text-align: center; }
    .grid-cell-neutral { background-color: #1a1a1a; color: white; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

if menu == "📸 Evidencia & Diario de Aciertos":
    st.title("📸 Evidencia de Tiros Directos & Auditoría Visual")
    
    col_izq, col_der = st.columns([1, 2])
    
    with col_izq:
        st.subheader("📁 Cargar Prueba de Éxito")
        sorteo_sel = st.selectbox("Sorteo Jugado", list(GAME_CONFIG.keys()))
        imagen_boleto = st.file_uploader("Subir Foto del Boleto Ganador", type=["png", "jpg", "jpeg"])
        numeros_boleto = st.text_input("Números Jugados (Ej: 1,3,11,14,22)")
        numeros_ganadores = st.text_input("Números Oficiales Ganadores")
        
        if st.button("🔮 Auditar y Archivar Boleto"):
            if numeros_boleto and numeros_ganadores:
                lista_jugados = [int(x.strip()) for x in numeros_boleto.split(",") if x.strip().isdigit()]
                lista_ganadores = [int(x.strip()) for x in numeros_ganadores.split(",") if x.strip().isdigit()]
                
                coincidentes = list(set(lista_jugados) & set(lista_ganadores))
                estado_tiro = "🎯 ACERTADO" if len(coincidentes) >= 2 else "❌ DESVIADO"
                
                registro_auditoria = {
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "sorteo": sorteo_sel,
                    "jugados": lista_jugados,
                    "ganadores": lista_ganadores,
                    "estado": estado_tiro,
                    "coincidentes": coincidentes
                }
                st.session_state.boletos_auditados.append(registro_auditoria)
                st.success(f"Boleto procesado como: {estado_tiro}")
                
    with col_der:
        st.subheader("📊 Planilla Digital Interactiva")
        if len(st.session_state.boletos_auditados) > 0:
            ultimo_b = st.session_state.boletos_auditados[-1]
            st.markdown(f"#### Analizando: **{ultimo_b['sorteo']}** ({ultimo_b['estado']})")
            
            config_juego = GAME_CONFIG[ultimo_b['sorteo']]
            st.markdown("##### 🏁 Mapa de Marcación")
            
            min_n, max_n = config_juego["min"], config_juego["max"]
            
            if min_n == 0 and max_n == 9: # Tris
                cols_grid = st.columns(10)
                for num in range(10):
                    with cols_grid[num]:
                        if num in ultimo_b["coincidentes"]: st.markdown(f'<div class="grid-cell-match">✔️<br>{num}</div>', unsafe_allow_html=True)
                        elif num in ultimo_b["jugados"]: st.markdown(f'<div class="grid-cell-miss">✖️<br>{num}</div>', unsafe_allow_html=True)
                        else: st.markdown(f'<div class="grid-cell-neutral"><br>{num}</div>', unsafe_allow_html=True)
            else: # Chispazo / Melate
                filas_num = 4 if max_n <= 28 else 7
                for f in range(filas_num):
                    cols_grid = st.columns(8)
                    for c in range(8):
                        num = f * 8 + c + min_n
                        if num <= max_n:
                            with cols_grid[c]:
                                if num in ultimo_b["coincidentes"]: st.markdown(f'<div class="grid-cell-match">✔️<br>{num}</div>', unsafe_allow_html=True)
                                elif num in ultimo_b["jugados"]: st.markdown(f'<div class="grid-cell-miss">✖️<br>{num}</div>', unsafe_allow_html=True)
                                else: st.markdown(f'<div class="grid-cell-neutral"><br>{num}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("📚 Historial de Evidencias")
            st.dataframe(pd.DataFrame(st.session_state.boletos_auditados), use_container_width=True)
        else:
            st.info("Sube tu jugada para activar la planilla interactiva.")
