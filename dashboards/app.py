import streamlit as st
import pandas as pd
import io
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

st.title("🌊 ROV Mission Intelligence Platform")

uploaded_file = st.file_uploader("Upload ROV CSV", type=["csv"])

# =========================
# 📌 DISTÂNCIA HAVERSINE
# =========================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)

    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return 2 * R * np.arctan2(np.sqrt(a), np.sqrt(1-a))

def total_distance(df):
    lat = df["latitude"].values
    lon = df["longitude"].values

    return np.sum(haversine(lat[:-1], lon[:-1], lat[1:], lon[1:]))

# =========================
# 🚀 PROCESSAMENTO
# =========================
if uploaded_file is not None:

    with st.spinner("Processing mission data..."):

        try:
            content = uploaded_file.getvalue().decode("utf-8")
            content = content.replace('"', '')

            df = pd.read_csv(io.StringIO(content))
            df.columns = df.columns.str.strip().str.lower()

            required = ['latitude', 'longitude', 'depth']
            missing = [c for c in required if c not in df.columns]

            if missing:
                st.error(f"Missing required columns: {missing}")
                st.stop()

            # =========================
            # ⏱️ TIMESTAMP (SAFE)
            # =========================
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                df = df.sort_values("timestamp")
            else:
                df["timestamp"] = range(len(df))

            # =========================
            # 🧠 ANOMALIA ROBUSTA
            # =========================
            rolling_mean = df["depth"].rolling(10, min_periods=1).mean()
            rolling_std = df["depth"].rolling(10, min_periods=1).std().fillna(0)

            df["anomaly"] = (abs(df["depth"] - rolling_mean) > 2 * rolling_std)

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
            # 🎛️ VISUALIZAÇÃO (DEFAULT OK)
            # =========================
            view = st.selectbox(
                "Visualization Mode",
                ["Map 2D", "Route", "3D View", "Anomalies", "Time Series"]
            )

            # =========================
            # 🗺️ MAPA 2D
            # =========================
            if view == "Map 2D":
                fig = px.scatter_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    color="depth",
                    zoom=6,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🧭 ROTA
            # =========================
            elif view == "Route":
                fig = px.line_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    zoom=6,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🌐 3D
            # =========================
            elif view == "3D View":
                fig = px.scatter_3d(
                    df,
                    x="longitude",
                    y="latitude",
                    z="depth",
                    color="depth"
                )
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🔴 ANOMALIAS
            # =========================
            elif view == "Anomalies":
                fig = px.scatter_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    color="anomaly",
                    zoom=6,
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

            # =========================
            # 📋 DADOS
            # =========================
            with st.expander("Show raw data"):
                st.dataframe(df)

        except Exception as e:
            st.error(f"Error processing file: {e}")
