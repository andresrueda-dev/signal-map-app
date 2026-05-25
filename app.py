import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.cluster import KMeans
from scipy.stats import gaussian_kde

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Signal Map AI",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# TITLE
# ==================================================

st.title("📊 Signal Map AI")
st.markdown(
    "Advanced Pattern Detection • Cluster Intelligence • Momentum Analysis"
)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("⚙️ Configuration")

user_input = st.sidebar.text_area(
    "Enter Numbers (comma separated)",
    "30,33,44,45,46,48,16"
)

advanced_mode = st.sidebar.checkbox(
    "Enable Advanced AI Analysis",
    value=True
)

# ==================================================
# DATA PARSING
# ==================================================

try:

    numbers = [
        int(x.strip())
        for x in user_input.split(",")
        if x.strip() != ""
    ]

except:

    st.error("Invalid input format.")
    st.stop()

# ==================================================
# BASIC DATAFRAME
# ==================================================

df = pd.DataFrame({
    "Index": range(len(numbers)),
    "Value": numbers
})

# ==================================================
# BASIC METRICS
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Numbers", len(numbers))

with col2:
    st.metric("Average", round(np.mean(numbers), 2))

with col3:
    st.metric("Max", max(numbers))

with col4:
    st.metric("Min", min(numbers))

# ==================================================
# MAIN CHART
# ==================================================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["Index"],
        y=df["Value"],
        mode="lines+markers",
        name="Signal"
    )
)

fig.update_layout(
    title="Signal Movement",
    xaxis_title="Sequence",
    yaxis_title="Value",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# ADVANCED AI ANALYSIS
# ==================================================

if advanced_mode:

    st.markdown("---")
    st.header("🔍 Advanced Pattern Detection")

    try:

        values = np.array(numbers).reshape(-1, 1)

        # ==========================================
        # AUTO CLUSTER DETECTION
        # ==========================================

        n_clusters = min(3, len(numbers))

        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10
        )

        kmeans.fit(values)

        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_

        df["Cluster"] = labels

        st.subheader("🧩 Automatic Cluster Detection")

        cluster_data = {}

        for i in range(n_clusters):

            cluster_values = [
                numbers[j]
                for j in range(len(numbers))
                if labels[j] == i
            ]

            cluster_data[i] = cluster_values

            st.write(
                f"Cluster {i+1}: {cluster_values}"
            )

        # ==========================================
        # CENTROID AVERAGE
        # ==========================================

        avg_centroid = np.mean(centroids)

        st.subheader("🎯 Average Centroid")

        st.metric(
            "Centroid Average",
            round(float(avg_centroid), 2)
        )

        # ==========================================
        # DOMINANT RANGE
        # ==========================================

        ranges = []

        for cluster_values in cluster_data.values():

            if len(cluster_values) > 0:

                cluster_range = (
                    min(cluster_values),
                    max(cluster_values)
                )

                ranges.append(cluster_range)

        dominant_range = max(
            ranges,
            key=lambda r: r[1] - r[0]
        )

        st.subheader("📈 Dominant Range")

        st.success(
            f"{dominant_range[0]} - {dominant_range[1]}"
        )

        # ==========================================
        # CLUSTER COLORING GRAPH
        # ==========================================

        st.subheader("🌈 Cluster Coloring Graph")

        cluster_fig = px.scatter(
            df,
            x="Index",
            y="Value",
            color="Cluster",
            size="Value",
            template="plotly_dark",
            title="Cluster Visualization"
        )

        st.plotly_chart(
            cluster_fig,
            use_container_width=True
        )

        # ==========================================
        # DENSITY HEATMAP
        # ==========================================

        st.subheader("🔥 Density Heatmap")

        density = gaussian_kde(numbers)

        xs = np.linspace(
            min(numbers),
            max(numbers),
            200
        )

        ys = density(xs)

        heatmap_fig = go.Figure()

        heatmap_fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                fill='tozeroy',
                mode='lines',
                name='Density'
            )
        )

        heatmap_fig.update_layout(
            template="plotly_dark",
            title="Density Distribution Heatmap",
            xaxis_title="Value",
            yaxis_title="Density",
            height=450
        )

        st.plotly_chart(
            heatmap_fig,
            use_container_width=True
        )

        # ==========================================
        # CONFIDENCE SCORE
        # ==========================================

        st.subheader("🛡️ Confidence Score")

        variance = np.var(numbers)

        confidence_score = max(
            0,
            100 - variance
        )

        confidence_score = round(
            confidence_score,
            2
        )

        st.metric(
            "Pattern Confidence",
            f"{confidence_score}%"
        )

        # ==========================================
        # MOMENTUM DETECTION
        # ==========================================

        st.subheader("⚡ Momentum Detection")

        momentum = np.diff(numbers)

        avg_momentum = np.mean(momentum)

        if avg_momentum > 0:

            momentum_text = "Bullish Momentum ↗️"

        elif avg_momentum < 0:

            momentum_text = "Bearish Momentum ↘️"

        else:

            momentum_text = "Neutral Momentum ➖"

        st.info(momentum_text)

        momentum_fig = go.Figure()

        momentum_fig.add_trace(
            go.Bar(
                x=list(range(len(momentum))),
                y=momentum,
                name="Momentum"
            )
        )

        momentum_fig.update_layout(
            template="plotly_dark",
            title="Momentum Flow",
            xaxis_title="Position",
            yaxis_title="Momentum",
            height=400
        )

        st.plotly_chart(
            momentum_fig,
            use_container_width=True
        )

        # ==========================================
        # AI INSIGHT SUMMARY
        # ==========================================

        st.subheader("🧠 AI Insight Summary")

        insight = f"""
        The AI system detected {n_clusters} major behavioral clusters.

        The average centroid concentration is near
        {round(float(avg_centroid),2)}.

        Dominant operational range detected between
        {dominant_range[0]} and {dominant_range[1]}.

        Estimated confidence score:
        {confidence_score}%.

        Current momentum state:
        {momentum_text}
        """

        st.success(insight)

    except Exception as e:

        st.error(
            f"Advanced analysis error: {e}"
        )

# ==================================================
# RAW DATA
# ==================================================

st.markdown("---")

st.subheader("📋 Raw Data")

st.dataframe(df)

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Signal Map AI • Advanced Cluster Intelligence System"
)           
