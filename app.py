import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

div[data-testid="stPlotlyChart"] {
    background-color: rgba(255,255,255,0.03);
    padding: 10px;
    border-radius: 20px;
}

h1, h2, h3 {
    color: #8be9fd;
}

section[data-testid="stSidebar"] {
    background-color: #0b1023;
}

</style>
""", unsafe_allow_html=True)
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
