import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG
st.set_page_config(
    page_title="Signal Map",
    layout="wide",
    page_icon="🔮"
)

# LOAD DATA
df = pd.read_csv("signals.csv")

# SIDEBAR
st.sidebar.title("⚡ Signal Map")
st.sidebar.markdown("Sistema de sincronías y patrones")

# TITLE
st.title("🔮 SIGNAL MAP")
st.markdown("### Visualizador de patrones numéricos")

# METRICS
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Señales", len(df))
col2.metric("Números Únicos", df["numero"].nunique())
col3.metric("Tipos", df["tipo"].nunique())
col4.metric("Hora Pico", "13:00")

# DIVIDER
st.divider()

# GRAPH 1
st.subheader("📈 Frecuencia de Tipos")

type_count = df["tipo"].value_counts().reset_index()
type_count.columns = ["tipo", "cantidad"]

fig1 = px.bar(
    type_count,
    x="tipo",
    y="cantidad",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)

# GRAPH 2
st.subheader("⏰ Mapa Temporal")

time_count = df["hora"].value_counts().reset_index()
time_count.columns = ["hora", "cantidad"]

fig2 = px.line(
    time_count,
    x="hora",
    y="cantidad",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# GRAPH 3
st.subheader("🧠 Números Dominantes")

number_count = df["numero"].value_counts().reset_index().head(10)
number_count.columns = ["numero", "cantidad"]

fig3 = px.pie(
    number_count,
    names="numero",
    values="cantidad",
    hole=0.5
)

st.plotly_chart(fig3, use_container_width=True)

# DATA TABLE
st.subheader("📂 Registro Completo")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)
