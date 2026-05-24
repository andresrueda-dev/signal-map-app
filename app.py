import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
from PIL import Image
import pytesseract

st.subheader("🧠 AI Pattern Detection")

patterns = []

for num in df["numero"]:

    if "-" in str(num):
        parts = str(num).split("-")

        try:
            parts = [int(x) for x in parts]

            if sorted(parts) == list(range(min(parts), max(parts)+1)):
                patterns.append(f"Secuencia detectada: {num}")

        except:
            pass

    if str(num) == str(num)[::-1]:
        patterns.append(f"Espejo detectado: {num}")

for p in patterns:
    st.success(p)
st.subheader("⚡ Tesla Signal Network")

G = nx.Graph()

for _, row in df.iterrows():
    nums = str(row["numero"]).split("-")

    for i in range(len(nums)-1):
        G.add_edge(nums[i], nums[i+1])

pos = nx.spring_layout(G)

edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]

    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1),
    hoverinfo='none',
    mode='lines'
)

node_x = []
node_y = []
node_text = []

for node in G.nodes():
    x, y = pos[node]

    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers+text',
    text=node_text,
    textposition="top center",
    marker=dict(size=18)
)

fig_network = go.Figure(
    data=[edge_trace, node_trace]
)

fig_network.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(fig_network, use_container_width=True)
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
