import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from datetime import datetime
import os

st.set_page_config(page_title="SignalMap IA - MetaPattern Live", layout="wide", page_icon="🧠")

GAME_CONFIG = {
    "Tris Medio Día": {"min": 0, "max": 9, "cantidad": 5, "archivo": "data/TrisMD.csv", "tipo": "lineal"},
    "Tris Tres": {"min": 0, "max": 9, "cantidad": 5, "archivo": "data/Tris3.csv", "tipo": "lineal"},
    "Chispazo Clásico": {"min": 1, "max": 28, "cantidad": 5, "archivo": "data/Chispazo.csv", "tipo": "matriz"},
    "Melate": {"min": 1, "max": 56, "cantidad": 6, "archivo": "data/Melate.csv", "tipo": "matriz"},
    "Revancha": {"min": 1, "max": 56, "cantidad": 6, "archivo": "data/Revancha.csv", "tipo": "matriz"},
    "Gana Gato": {"tipo": "matriz", "archivo": "data/GanaGato.csv"}
}

HORARIOS_SORTEOS = {
    "Tris Medio Día": "13:00", "Tris Tres": "15:00", "Tris Clásico": "21:00",
    "Chispazo Clásico": "21:00", "Melate": "21:00", "Revancha": "21:00"
}

st.markdown("""
<style>
.stApp { background-color: #020617; color: white; }
.stButton>button { background-color: #7c3aed; color: white; border-radius: 12px; }
.grid-cell-match { background-color: #15803d; color: white; padding: 10px; text-align: center; border-radius: 8px; }
.grid-cell-miss { background-color: #991b1b; color: white; padding: 10px; text-align: center; border-radius: 8px; }
.grid-cell-neutral { background-color: #1e293b; color: #94a3b8; padding: 10px; text-align: center; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

if "local_signals" not in st.session_state: st.session_state.local_signals = []
if "boletos_auditados" not in st.session_state: st.session_state.boletos_auditados = []

def render_radar():
    st.sidebar.subheader("🚨 Próximo Cierre")
    ahora = datetime.now()
    for nombre, hora in HORARIOS_SORTEOS.items():
        objetivo = datetime.strptime(hora, "%H:%M")
        minutos = (objetivo.hour * 60 + objetivo.minute) - (ahora.hour * 60 + ahora.minute)
        if 0 <= minutos <= 60:
            st.sidebar.error(f"⚠️ {nombre}: {minutos} min")

def main():
    st.title("SignalMap IA - Control Central")
    render_radar()
    
    menu = st.sidebar.radio("Navegación", ["📖 Diario", "🏠 Dashboard", "🎯 Sugeridos", "📸 Auditoría"])

    if menu == "📖 Diario":
        sorteo = st.selectbox("Sorteo", list(GAME_CONFIG.keys()))
        numeros = st.text_input("Números (coma separada)")
        if st.button("Guardar"):
            st.session_state.local_signals.append({"sorteo": sorteo, "numeros": numeros})
            st.success("Guardado")

    elif menu == "🏠 Dashboard":
        st.write("Visualizador de señales activo.")

    elif menu == "📸 Auditoría":
        st.write("Módulo de evidencias.")

if __name__ == "__main__":
    main()
