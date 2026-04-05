import streamlit as st
import pandas as pd
import io
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

st.title("🌌 ROV Mission Intelligence Platform - Advanced")

uploaded_file = st.file_uploader("Upload ROV CSV", type=["csv"])

# =========================
# 📌 DISTÂNCIA REAL (HAVERSINE)
# =========================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)

    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

def total_distance(df):
    dist = 0
    for i in range(len(df)-1):
        dist += haversine(
            df.iloc[i]["latitude"], df.iloc[i]["longitude"],
            df.iloc[i+1]["latitude"], df.iloc[i+1]["longitude"]
        )
    return dist

# =========================
# 🚀 PROCESSAMENTO
# =========================
if uploaded_file is not None:
    with st.spinner("Processando missão..."):
        content = uploaded_file.getvalue().decode("utf-8")
        content = content.replace('"', '')

        df = pd.read_csv(io.StringIO(content))
        df.columns = df.columns.str.strip().str.lower()

        required = ['latitude', 'longitude', 'depth']
        missing = [c for c in required if c not in df.columns]

        if missing:
            st.error(f"Missing columns: {missing}")
        else:
            st.success("Missão carregada!")

            # =========================
            # ⏱️ TIMESTAMP
            # =========================
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
            else:
                df["timestamp"] = range(len(df))

            # =========================
            # 🧠 ANOMALIA AVANÇADA
            # =========================
            df["rolling_mean"] = df["depth"].rolling(5).mean()
            df["rolling_std"] = df["depth"].rolling(5).std()

            df["anomaly"] = abs(df["depth"] - df["rolling_mean"]) > 2 * df["rolling_std"]

            # =========================
            # 📊 KPIs
            # =========================
            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Avg Depth", f"{df['depth'].mean():.1f}")
            c2.metric("Max Depth", f"{df['depth'].max():.1f}")
            c3.metric("Distance (km)", f"{total_distance(df):.2f}")
            c4.metric("Anomalies", int(df["anomaly"].sum()))

            st.divider()

            # =========================
            # 🎛️ CONTROLE
            # =========================
            view = st.selectbox(
                "Mode",
                ["Replay Mission", "3D Terrain", "Heatmap", "Anomaly Detection", "Time Series"]
            )

            # =========================
            # 🎥 REPLAY AUTOMÁTICO
            # =========================
            if view == "Replay Mission":
                fig = px.line_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    animation_frame=df.index,
                    zoom=5,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🌐 3D TERRAIN
            # =========================
            elif view == "3D Terrain":
                fig = px.scatter_3d(
                    df,
                    x="longitude",
                    y="latitude",
                    z="depth",
                    color="depth"
                )
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🔥 HEATMAP
            # =========================
            elif view == "Heatmap":
                fig = px.density_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    z="depth",
                    radius=10,
                    zoom=5,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🔴 ANOMALIAS
            # =========================
            elif view == "Anomaly Detection":
                fig = px.scatter_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    color="anomaly",
                    zoom=5,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # ⏱️ TIME SERIES
            # =========================
            elif view == "Time Series":
                fig = px.line(
                    df,
                    x="timestamp",
                    y="depth",
                    title="Depth over Time"
                )
                st.plotly_chart(fig, use_container_width=True)

            with st.expander("Full dataset"):
                st.dataframe(df)
