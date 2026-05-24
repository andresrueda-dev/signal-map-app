import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Signal Map")

st.title("🔮 Signal Map")

number = st.text_input("Número")
time_seen = st.time_input("Hora")
context = st.text_input("Contexto")

if st.button("Guardar"):

    new_data = pd.DataFrame({
        "numero": [number],
        "hora": [time_seen.strftime("%H:%M")],
        "contexto": [context],
        "fecha": [datetime.now().strftime("%Y-%m-%d")]
    })

    try:
        old_data = pd.read_csv("signals.csv")
        data = pd.concat([old_data, new_data])
    except:
        data = new_data

    data.to_csv("signals.csv", index=False)

    st.success("Guardado")

try:
    df = pd.read_csv("signals.csv")
    st.dataframe(df)
except:
    st.warning("Sin registros")
